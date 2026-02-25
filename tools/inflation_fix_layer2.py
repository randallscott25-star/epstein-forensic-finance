#!/usr/bin/env python3
"""
INFLATION FIX — LAYER 2
Attacks remaining volume inflation in bank_statement_transactions.

Three fixes:
1. AMOUNT DISTRIBUTION — identify where the dollars concentrate
2. CROSS-PAGE DEDUP — same amount on multiple pages of same document
3. REASONABLENESS — cap per-record amounts based on known account sizes

Then: reclassify inflated records as BALANCE_REPEAT, SUBTOTAL, or OUTLIER.

Author: Randall Scott Taylor
"""

import sqlite3, re, os
from collections import Counter, defaultdict

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("INFLATION FIX — LAYER 2: AMOUNT ANALYSIS")
    print("=" * 70)

    # ── DIAGNOSTIC 1: Amount distribution ──
    c.execute("""
        SELECT id, bank, bates, tx_amount, tx_date, description,
               record_type, source_doc_type
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        ORDER BY tx_amount DESC
    """)
    txn_rows = c.fetchall()
    print(f"\n[DIAG] Current TRANSACTION records: {len(txn_rows):,}")

    # Bucket by amount range
    buckets = {
        '$1B+': [],
        '$100M-1B': [],
        '$10M-100M': [],
        '$1M-10M': [],
        '$100K-1M': [],
        '$10K-100K': [],
        '$1K-10K': [],
        'Under $1K': [],
    }

    for row in txn_rows:
        rec_id, bank, bates, amount, date, desc, rtype, stype = row
        amount = amount or 0
        if amount >= 1_000_000_000:
            buckets['$1B+'].append(row)
        elif amount >= 100_000_000:
            buckets['$100M-1B'].append(row)
        elif amount >= 10_000_000:
            buckets['$10M-100M'].append(row)
        elif amount >= 1_000_000:
            buckets['$1M-10M'].append(row)
        elif amount >= 100_000:
            buckets['$100K-1M'].append(row)
        elif amount >= 10_000:
            buckets['$10K-100K'].append(row)
        elif amount >= 1_000:
            buckets['$1K-10K'].append(row)
        else:
            buckets['Under $1K'].append(row)

    print(f"\n  {'Amount Range':<20} {'Records':>8} {'Total Volume':>22} {'% of Total':>10}")
    print("  " + "─" * 62)
    total_vol = sum(r[3] or 0 for r in txn_rows)
    for bucket_name, rows in buckets.items():
        vol = sum(r[3] or 0 for r in rows)
        pct = vol / total_vol * 100 if total_vol > 0 else 0
        print(f"  {bucket_name:<20} {len(rows):>8,} ${vol:>20,.2f} {pct:>9.1f}%")

    # ── DIAGNOSTIC 2: Top 30 by amount — what are these? ──
    print(f"\n{'=' * 70}")
    print("TOP 30 TRANSACTION RECORDS BY AMOUNT")
    print(f"{'=' * 70}")
    print(f"  {'$Amount':>18} {'Bank':<18} {'Source':.<14} {'Bates':<16} {'Description (first 60)'}")
    print("  " + "─" * 100)
    for row in txn_rows[:30]:
        rec_id, bank, bates, amount, date, desc, rtype, stype = row
        desc_short = (desc or '')[:60].replace('\n', ' ')
        print(f"  ${amount or 0:>17,.2f} {bank:<18} {stype or '':<14} {bates or '':<16} {desc_short}")

    # ── DIAGNOSTIC 3: Per-bank amount profiles ──
    print(f"\n{'=' * 70}")
    print("PER-BANK AMOUNT PROFILES")
    print(f"{'=' * 70}")

    bank_amounts = defaultdict(list)
    for row in txn_rows:
        bank_amounts[row[1]].append(row[3] or 0)

    for bank in sorted(bank_amounts.keys(), key=lambda b: -sum(bank_amounts[b])):
        amounts = sorted(bank_amounts[bank], reverse=True)
        total = sum(amounts)
        median = amounts[len(amounts)//2] if amounts else 0
        top10_vol = sum(amounts[:10])
        top10_pct = top10_vol / total * 100 if total > 0 else 0
        print(f"\n  {bank} ({len(amounts):,} records, ${total:,.0f} total)")
        print(f"    Median: ${median:,.2f} | Top 10 = {top10_pct:.0f}% of volume")
        print(f"    Top 5: {['${:,.0f}'.format(a) for a in amounts[:5]]}")
        if len(amounts) > 5:
            print(f"    p95: ${amounts[int(len(amounts)*0.05)]:,.2f} | p50: ${median:,.2f} | p5: ${amounts[int(len(amounts)*0.95)]:,.2f}")

    # ── DIAGNOSTIC 4: Cross-page repeats ──
    print(f"\n{'=' * 70}")
    print("CROSS-PAGE AMOUNT REPEATS (same bank + amount + date)")
    print(f"{'=' * 70}")

    # Group by bank + amount + date
    sig_groups = defaultdict(list)
    for row in txn_rows:
        rec_id, bank, bates, amount, date, desc, rtype, stype = row
        if amount and amount > 100:
            sig = f"{bank}|{amount:.2f}|{date or 'nodate'}"
            sig_groups[sig].append(row)

    repeats = {sig: rows for sig, rows in sig_groups.items() if len(rows) > 1}
    repeat_records = sum(len(rows) - 1 for rows in repeats.values())  # excess copies
    repeat_volume = sum((len(rows) - 1) * (rows[0][3] or 0) for rows in repeats.values())

    print(f"  Unique amount+date combos with repeats: {len(repeats):,}")
    print(f"  Excess duplicate records: {repeat_records:,}")
    print(f"  Excess duplicate volume: ${repeat_volume:,.2f}")

    # Show top repeats
    top_repeats = sorted(repeats.items(), key=lambda x: -(len(x[1]) - 1) * (x[1][0][3] or 0))[:15]
    print(f"\n  Top repeated amounts:")
    for sig, rows in top_repeats:
        bank, amt_str, date = sig.split('|')
        n_copies = len(rows)
        excess_vol = (n_copies - 1) * (rows[0][3] or 0)
        bates_list = list(set(r[2] for r in rows))[:3]
        print(f"    {bank:<18} ${float(amt_str):>14,.2f} x{n_copies} ({date}) excess=${excess_vol:,.0f}")
        print(f"      bates: {bates_list}")

    # ═══════════════════════════════════════════════════════
    # NOW APPLY FIXES
    # ═══════════════════════════════════════════════════════

    print(f"\n{'=' * 70}")
    print("APPLYING FIXES")
    print(f"{'=' * 70}")

    fixed = 0

    # FIX 1: Amounts > $50M on a single record → almost certainly not a transaction
    # Known Epstein max single wire: ~$30M (to Leon Black entities)
    # Allow SDNY exhibits slightly higher since they may aggregate
    print(f"\n[FIX 1] Capping outlier amounts (>$50M per record)...")
    outlier_count = 0
    outlier_vol = 0
    for row in txn_rows:
        rec_id, bank, bates, amount, date, desc, rtype, stype = row
        if not amount:
            continue

        # $50M cap for bank statements, $100M for SDNY exhibits
        cap = 100_000_000 if stype == 'SDNY_EXHIBIT' else 50_000_000
        if amount > cap:
            c.execute("UPDATE bank_statement_transactions SET record_type = 'OUTLIER' WHERE id = ?",
                     (rec_id,))
            outlier_count += 1
            outlier_vol += amount
            fixed += 1

    print(f"  Demoted {outlier_count:,} records (${outlier_vol:,.2f}) as OUTLIER")

    # FIX 2: Cross-page dedup — keep first occurrence, demote rest
    print(f"\n[FIX 2] Deduping cross-page repeats...")
    dedup_count = 0
    dedup_vol = 0

    # Re-fetch current TRANSACTION records (after fix 1)
    c.execute("""
        SELECT id, bank, bates, tx_amount, tx_date
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        ORDER BY id
    """)
    current_txns = c.fetchall()

    sig_seen = {}
    for rec_id, bank, bates, amount, date in current_txns:
        if not amount or amount < 100:
            continue
        sig = f"{bank}|{amount:.2f}|{date or 'nodate'}"
        if sig in sig_seen:
            # This is a repeat — demote it
            c.execute("UPDATE bank_statement_transactions SET record_type = 'PAGE_REPEAT' WHERE id = ?",
                     (rec_id,))
            dedup_count += 1
            dedup_vol += amount
            fixed += 1
        else:
            sig_seen[sig] = rec_id

    print(f"  Demoted {dedup_count:,} records (${dedup_vol:,.2f}) as PAGE_REPEAT")

    # FIX 3: Description-based balance detection
    # Records that slipped through the first classifier
    print(f"\n[FIX 3] Catching remaining balance/subtotal language...")
    balance_catch = 0
    balance_vol = 0

    BALANCE_CATCHALL = [
        r'(?i)(total|net)\s+(asset|worth|value|equity|portfolio)',
        r'(?i)(market|account|portfolio)\s+(value|total)',
        r'(?i)total\s+(?:for\s+)?(?:all|this)',
        r'(?i)grand\s+total',
        r'(?i)combined\s+(total|value|balance)',
        r'(?i)aggregate\s+(value|balance|total)',
        r'(?i)sum\s+of\s+all',
    ]

    c.execute("""
        SELECT id, description, tx_amount
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        AND description IS NOT NULL
    """)
    for rec_id, desc, amount in c.fetchall():
        if not desc:
            continue
        for pat in BALANCE_CATCHALL:
            if re.search(pat, desc):
                c.execute("UPDATE bank_statement_transactions SET record_type = 'SUBTOTAL' WHERE id = ?",
                         (rec_id,))
                balance_catch += 1
                balance_vol += (amount or 0)
                fixed += 1
                break

    print(f"  Demoted {balance_catch:,} records (${balance_vol:,.2f}) as SUBTOTAL")

    # FIX 4: Per-bank reasonableness based on known account sizes
    print(f"\n[FIX 4] Per-bank reasonableness caps...")
    # Known approximate max single transaction sizes per bank
    BANK_CAPS = {
        'Deutsche Bank': 30_000_000,      # Largest known DB-Epstein wire ~$30M
        'Bear Stearns': 20_000_000,       # Brokerage, max individual tx
        'UBS': 10_000_000,                # Maxwell accounts, smaller
        'Citibank': 10_000_000,           # Gratitude America, capped
        'Morgan Stanley': 10_000_000,
        'Barclays': 10_000_000,           # Maxwell foreign accounts
        'BNY Mellon': 10_000_000,
        'First Bank PR': 5_000_000,       # Smaller institution
        'Credit Suisse': 10_000_000,
        'HSBC': 10_000_000,
        'Navy Federal': 100_000,          # Personal credit union
        'Charles Schwab': 5_000_000,      # Personal brokerage
        'Merchants Commercial': 1_000_000,
    }

    bank_cap_count = 0
    bank_cap_vol = 0

    c.execute("""
        SELECT id, bank, tx_amount
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
    """)
    for rec_id, bank, amount in c.fetchall():
        if not amount:
            continue
        cap = BANK_CAPS.get(bank, 50_000_000)
        if amount > cap:
            c.execute("UPDATE bank_statement_transactions SET record_type = 'OVER_CAP' WHERE id = ?",
                     (rec_id,))
            bank_cap_count += 1
            bank_cap_vol += amount
            fixed += 1

    print(f"  Demoted {bank_cap_count:,} records (${bank_cap_vol:,.2f}) as OVER_CAP")

    conn.commit()

    # ═══════════════════════════════════════════════════════
    # FINAL RESULTS
    # ═══════════════════════════════════════════════════════

    print(f"\n{'=' * 70}")
    print("FINAL RECORD TYPE DISTRIBUTION")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT record_type, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        GROUP BY record_type
        ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Record Type':<25} {'Records':>8} {'Volume':>20}")
    print("  " + "─" * 55)
    final_txn_vol = 0
    final_txn_count = 0
    for rtype, cnt, vol in c.fetchall():
        vol = vol or 0
        marker = " ← REAL" if rtype == 'TRANSACTION' else ""
        print(f"  {rtype:<25} {cnt:>8,} ${vol:>18,.2f}{marker}")
        if rtype == 'TRANSACTION':
            final_txn_vol = vol
            final_txn_count = cnt

    # Per-bank final
    print(f"\n{'=' * 70}")
    print("FINAL TRANSACTION RECORDS BY BANK")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount),
               MIN(tx_amount), MAX(tx_amount),
               AVG(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        GROUP BY bank
        ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Bank':<22} {'Recs':>6} {'Volume':>18} {'Min':>12} {'Max':>14} {'Avg':>14}")
    print("  " + "─" * 90)
    grand_total = 0
    for bank, cnt, vol, mn, mx, avg in c.fetchall():
        vol = vol or 0
        grand_total += vol
        print(f"  {bank:<22} {cnt:>6,} ${vol:>16,.2f} ${mn or 0:>10,.2f} ${mx or 0:>12,.2f} ${avg or 0:>12,.2f}")
    print("  " + "─" * 90)
    print(f"  {'TOTAL':<22} {final_txn_count:>6,} ${grand_total:>16,.2f}")

    # Entity matches
    print(f"\n{'=' * 70}")
    print("ENTITY MATCHES (clean TRANSACTION only)")
    print(f"{'=' * 70}")
    c.execute("""
        SELECT entity_match, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE entity_match IS NOT NULL
        AND record_type = 'TRANSACTION'
        GROUP BY entity_match
        ORDER BY SUM(tx_amount) DESC
        LIMIT 20
    """)
    for entity, cnt, vol in c.fetchall():
        vol = vol or 0
        print(f"  {entity:<30} {cnt:>6} txns  ${vol:>14,.2f}")

    # Progression
    print(f"\n{'=' * 70}")
    print("INFLATION FIX PROGRESSION")
    print(f"{'=' * 70}")
    print(f"  Layer 0 (raw parser):          $68,745,222,404.77  (24,563 records)")
    print(f"  Layer 1 (record classifier):   $23,695,632,641.86  (10,513 records)")
    print(f"  Layer 2 (source doc type):     $14,612,679,834.57  ( 8,123 records)")
    print(f"  Layer 3 (amount fixes):        ${final_txn_vol:>18,.2f}  ({final_txn_count:,} records)")
    if final_txn_vol > 0:
        reduction = (1 - final_txn_vol / 68_745_222_404.77) * 100
        print(f"  Total inflation removed:       {reduction:.1f}%")

    conn.close()
    print(f"\n  Layer 2 fixes complete. Total fixes applied: {fixed:,}")


if __name__ == "__main__":
    main()
