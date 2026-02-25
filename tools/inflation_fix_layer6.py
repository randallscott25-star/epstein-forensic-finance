#!/usr/bin/env python3
"""
INFLATION FIX — LAYER 6: DEEP AUDIT
Examines every remaining TRANSACTION record over $10K with source context.
Identifies remaining balance/summary contamination.

Author: Randall Scott Taylor
"""

import sqlite3, re, os
from collections import Counter, defaultdict

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")


def get_page_text(c, bates, max_chars=800):
    c.execute("""
        SELECT et.text_content FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE REPLACE(f.title, '.pdf', '') = ?
        ORDER BY et.page_num LIMIT 1
    """, (bates,))
    row = c.fetchone()
    return row[0][:max_chars] if row and row[0] else ''


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("LAYER 6 — DEEP AUDIT OF $10K+ RECORDS")
    print("=" * 70)

    # Get all TRANSACTION records over $10K
    c.execute("""
        SELECT id, bank, bates, tx_amount, tx_date, description, source_doc_type
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_amount >= 10000
        ORDER BY tx_amount DESC
    """)
    big_rows = c.fetchall()
    print(f"[IN] {len(big_rows)} records >= $10K (${sum(r[3] or 0 for r in big_rows):,.2f})")

    # Show ALL of them grouped by bank, top 20 per bank
    by_bank = defaultdict(list)
    for row in big_rows:
        by_bank[row[1]].append(row)

    for bank in sorted(by_bank.keys(), key=lambda b: -sum(r[3] or 0 for r in by_bank[b])):
        recs = by_bank[bank]
        vol = sum(r[3] or 0 for r in recs)
        print(f"\n{'─' * 70}")
        print(f"  {bank} — {len(recs)} records >= $10K, ${vol:,.2f}")
        print(f"{'─' * 70}")

        for rec_id, bk, bates, amount, date, desc, stype in recs[:25]:
            desc_clean = (desc or '').replace('\n', ' ')[:90]
            print(f"  #{rec_id:<6} ${amount:>12,.2f}  {date or 'no-date':<12} {desc_clean}")

    # ── PATTERN DETECTION ──
    print(f"\n{'=' * 70}")
    print("PATTERN DETECTION ON ALL 4,394 RECORDS")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT id, bank, bates, tx_amount, description, source_doc_type
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
    """)
    all_txns = c.fetchall()

    # Patterns that indicate NOT a real transaction
    SUSPECT_PATTERNS = {
        'OPENING_BALANCE': r'(?i)opening\s+balance',
        'CLOSING_BALANCE': r'(?i)closing\s+balance',
        'ENDING_BALANCE': r'(?i)ending\s+balance',
        'BEGINNING_BAL': r'(?i)beginning\s+balance',
        'PREV_BALANCE': r'(?i)previous\s+balance',
        'AVAIL_BALANCE': r'(?i)available\s+balance',
        'CURRENT_BALANCE': r'(?i)current\s+balance',
        'ACCOUNT_VALUE': r'(?i)account\s+value',
        'TOTAL_LINE': r'(?i)^total\s',
        'FDIC_INSURED': r'(?i)FDIC\s+insured',
        'MARKET_VALVE': r'(?i)market\s+val[uv]e',  # OCR "value"
        'STATEMENT_PERIOD': r'(?i)statement\s+period',
        'PERCENT_LINE': r'\d+\.?\d*%',  # "100.00%" or "45.2%"
        'PAGE_HEADER': r'(?i)page\s+\d+\s+of\s+\d+',
        'REPORT_DATE': r'(?i)(as\s+of|report\s+date|valued\s+as)',
        'GAIN_LOSS': r'(?i)(unrealized|realized)\s+(gain|loss)',
        'COST_BASIS': r'(?i)(cost|tax)\s+basis',
        'ACCRUED_INT': r'(?i)accrued\s+(interest|income)',
        'YIELD_RATE': r'(?i)(yield|rate|apy|apr)\s*[:\d]',
        'ANNUALIZED': r'(?i)annual(ized)?\s+(return|rate|yield|income)',
        'YTD_LINE': r'(?i)(year|ytd|year.to.date)',
        'MATURITY': r'(?i)maturity\s+(date|value)',
        'PAR_VALUE': r'(?i)par\s+value',
        'FACE_AMOUNT': r'(?i)face\s+(amount|value)',
        'SHARES_UNITS': r'(?i)\d+[\.,]\d+\s+(shares?|units?)',
        'PRICE_PER': r'(?i)price\s+(per|each)',
        'NAV': r'(?i)\bNAV\b',
        'CUSIP': r'(?i)\bCUSIP\b',
        'SEDOL': r'(?i)\bSEDOL\b',
        'ISIN': r'(?i)\bISIN\b',
    }

    pattern_hits = Counter()
    pattern_vol = defaultdict(float)
    flagged_ids = {}

    for rec_id, bank, bates, amount, desc, stype in all_txns:
        if not desc:
            continue
        for label, pat in SUSPECT_PATTERNS.items():
            if re.search(pat, desc):
                pattern_hits[label] += 1
                pattern_vol[label] += (amount or 0)
                if rec_id not in flagged_ids:
                    flagged_ids[rec_id] = (label, amount or 0)

    print(f"\n  {'Pattern':<25} {'Hits':>6} {'Volume':>16}")
    print("  " + "─" * 50)
    for label, cnt in pattern_hits.most_common():
        vol = pattern_vol[label]
        print(f"  {label:<25} {cnt:>6} ${vol:>14,.2f}")

    print(f"\n  Total flagged: {len(flagged_ids)} records, ${sum(v[1] for v in flagged_ids.values()):,.2f}")

    # ── APPLY FIXES ──
    print(f"\n{'=' * 70}")
    print("APPLYING FIXES")
    print(f"{'=' * 70}")

    fixed = 0
    fix_vol = 0

    # FIX 1: All pattern-matched records
    print(f"\n[FIX 1] Demoting pattern-matched records...")
    for rec_id, (label, amount) in flagged_ids.items():
        c.execute("UPDATE bank_statement_transactions SET record_type = ? WHERE id = ?",
                 (f'PATTERN:{label}', rec_id))
        fixed += 1
        fix_vol += amount
    print(f"  Demoted {fixed} records (${fix_vol:,.2f})")

    # FIX 2: No-date records $10K-$50K
    print(f"\n[FIX 2] No-date records $10K-$50K...")
    c.execute("""
        SELECT id, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NULL AND tx_amount BETWEEN 10000 AND 50000
    """)
    fix2 = 0
    fix2_vol = 0
    for rec_id, amount in c.fetchall():
        c.execute("UPDATE bank_statement_transactions SET record_type = 'NODATE_10K' WHERE id = ?", (rec_id,))
        fix2 += 1
        fix2_vol += (amount or 0)
    print(f"  Demoted {fix2} records (${fix2_vol:,.2f})")

    # FIX 3: JPMorgan records — these are already in extracted_payments
    # They got misattributed from Citibank/First Bank PR but JPM is already parsed
    print(f"\n[FIX 3] JPMorgan records (already in extracted_payments, double-counted)...")
    c.execute("""
        SELECT id, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND bank = 'JPMorgan'
    """)
    fix3 = 0
    fix3_vol = 0
    for rec_id, amount in c.fetchall():
        c.execute("UPDATE bank_statement_transactions SET record_type = 'JPM_DUPLICATE' WHERE id = ?", (rec_id,))
        fix3 += 1
        fix3_vol += (amount or 0)
    print(f"  Demoted {fix3} records (${fix3_vol:,.2f})")

    # FIX 4: Records where description is ONLY a date or date fragment
    print(f"\n[FIX 4] Description is only date/number fragments...")
    c.execute("""
        SELECT id, tx_amount, description FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_amount > 5000
    """)
    fix4 = 0
    fix4_vol = 0
    DATE_ONLY = re.compile(r'^[\d/\-\s\.,:]+$')
    for rec_id, amount, desc in c.fetchall():
        desc_clean = (desc or '').strip()
        if desc_clean and DATE_ONLY.match(desc_clean):
            c.execute("UPDATE bank_statement_transactions SET record_type = 'DATE_FRAGMENT' WHERE id = ?", (rec_id,))
            fix4 += 1
            fix4_vol += (amount or 0)
    print(f"  Demoted {fix4} records (${fix4_vol:,.2f})")

    # FIX 5: Remaining no-date records $5K-$10K
    print(f"\n[FIX 5] No-date records $5K-$10K...")
    c.execute("""
        SELECT id, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NULL AND tx_amount BETWEEN 5000 AND 10000
    """)
    fix5 = 0
    fix5_vol = 0
    for rec_id, amount in c.fetchall():
        c.execute("UPDATE bank_statement_transactions SET record_type = 'NODATE_5K' WHERE id = ?", (rec_id,))
        fix5 += 1
        fix5_vol += (amount or 0)
    print(f"  Demoted {fix5} records (${fix5_vol:,.2f})")

    conn.commit()

    # ═══════════════════════════════════════════════════════
    # FINAL RESULTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("RESULTS AFTER LAYER 6")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT record_type, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
    """)
    row = c.fetchone()
    final_cnt = row[1] or 0
    final_vol = row[2] or 0

    print(f"\n  TRANSACTION: {final_cnt:,} records, ${final_vol:,.2f}")

    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount), MAX(tx_amount), AVG(tx_amount)
        FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'
        GROUP BY bank ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Bank':<22} {'Recs':>6} {'Volume':>14} {'Max':>10} {'Avg':>10}")
    print("  " + "─" * 66)
    for bank, cnt, vol, mx, avg in c.fetchall():
        vol = vol or 0
        print(f"  {bank:<22} {cnt:>6,} ${vol:>12,.2f} ${mx or 0:>8,.2f} ${avg or 0:>8,.2f}")

    # Show remaining $10K+ records
    c.execute("""
        SELECT id, bank, tx_amount, description
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_amount >= 10000
        ORDER BY tx_amount DESC
    """)
    remaining_big = c.fetchall()
    print(f"\n  Remaining records >= $10K: {len(remaining_big)}")
    for rec_id, bank, amount, desc in remaining_big[:30]:
        desc_clean = (desc or '').replace('\n', ' ')[:70]
        print(f"    #{rec_id:<6} {bank:<16} ${amount:>10,.2f}  {desc_clean}")

    # Entity matches
    print(f"\n  Entity Matches:")
    c.execute("""
        SELECT entity_match, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE entity_match IS NOT NULL AND record_type = 'TRANSACTION'
        GROUP BY entity_match ORDER BY SUM(tx_amount) DESC
    """)
    for entity, cnt, vol in c.fetchall():
        print(f"    {entity:<30} {cnt:>4} txns  ${vol or 0:>12,.2f}")

    # Amount distribution
    print(f"\n  Amount Distribution:")
    c.execute("SELECT tx_amount FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'")
    amounts = [r[0] or 0 for r in c.fetchall()]
    for label, lo, hi in [('$10K+', 10000, 999999999), ('$1K-10K', 1000, 10000),
                           ('$100-1K', 100, 1000), ('$10-100', 10, 100), ('<$10', 0, 10)]:
        bucket = [a for a in amounts if lo <= a < hi]
        print(f"    {label:<12} {len(bucket):>6} recs  ${sum(bucket):>12,.2f}")

    # Progression
    print(f"\n{'=' * 70}")
    print("COMPLETE PROGRESSION")
    print(f"{'=' * 70}")
    print(f"  Layer 0 (raw):         $68,745,222,404.77  (24,563)")
    print(f"  Layer 1 (rec type):    $23,695,632,641.86  (10,513)")
    print(f"  Layer 2 (source doc):  $14,612,679,834.57  ( 8,123)")
    print(f"  Layer 3 (caps):        $ 4,113,970,148.71  ( 7,374)")
    print(f"  Layer 4 (WM+IQR):     $   323,079,163.74  ( 6,040)")
    print(f"  Layer 5 (surgical):    $    49,438,314.99  ( 5,429)")
    print(f"  Layer 6 (scrub):       $    19,018,048.23  ( 4,394)")
    print(f"  Layer 7 (deep audit):  ${final_vol:>18,.2f}  ({final_cnt:,})")
    reduction = (1 - final_vol / 68_745_222_404.77) * 100 if final_vol > 0 else 100
    print(f"  Inflation removed:     {reduction:.4f}%")

    conn.close()
    print(f"\n  Deep audit complete.")


if __name__ == "__main__":
    main()
