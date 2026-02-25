#!/usr/bin/env python3
"""
INFLATION FIX — LAYER 4: SURGICAL CLEANUP
Examines remaining $323M / 6,040 TRANSACTION records.
Shows top records per bank with full descriptions for manual review.
Applies final targeted fixes.

Author: Randall Scott Taylor
"""

import sqlite3, re, os
from collections import Counter, defaultdict

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")


def get_source_text(c, bates, max_chars=500):
    """Pull source OCR for context."""
    c.execute("""
        SELECT et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE REPLACE(f.title, '.pdf', '') = ?
        ORDER BY et.page_num LIMIT 1
    """, (bates,))
    row = c.fetchone()
    if row and row[0]:
        return row[0][:max_chars].replace('\n', ' | ')
    return ''


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("LAYER 4 — SURGICAL DIAGNOSTIC")
    print("=" * 70)

    # ── TOP 10 PER BANK ──
    banks_to_check = [
        'Citibank', 'First Bank PR', 'Deutsche Bank', 'UBS',
        'Barclays', 'Bear Stearns', 'BNY Mellon', 'HSBC'
    ]

    for bank in banks_to_check:
        c.execute("""
            SELECT id, bates, tx_amount, tx_date, description, source_doc_type
            FROM bank_statement_transactions
            WHERE record_type = 'TRANSACTION' AND bank = ?
            ORDER BY tx_amount DESC LIMIT 10
        """, (bank,))
        rows = c.fetchall()
        if not rows:
            continue

        total_bank = sum(r[2] or 0 for r in rows)
        c.execute("SELECT SUM(tx_amount) FROM bank_statement_transactions WHERE record_type='TRANSACTION' AND bank=?", (bank,))
        bank_total = c.fetchone()[0] or 0

        print(f"\n{'─' * 70}")
        print(f"  {bank} — Top 10 of ${bank_total:,.2f} total")
        print(f"  (Top 10 = ${total_bank:,.2f} = {total_bank/bank_total*100:.0f}% of bank volume)")
        print(f"{'─' * 70}")

        for rec_id, bates, amount, date, desc, stype in rows:
            desc_clean = (desc or '').replace('\n', ' ')[:80]
            print(f"  #{rec_id:<6} ${amount or 0:>14,.2f}  {date or 'no-date':<12} [{stype or '?'}]")
            print(f"         {bates or '':<16} {desc_clean}")

            # Pull source for suspicious ones
            if amount and amount > 500_000:
                src = get_source_text(c, bates, 200)
                print(f"         SRC: {src[:150]}")

    # ── PATTERN ANALYSIS ──
    print(f"\n{'=' * 70}")
    print("PATTERN ANALYSIS — REMAINING ISSUES")
    print(f"{'=' * 70}")

    # Check: how many records have NO date?
    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NULL
        GROUP BY bank ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  Records with NO DATE (suspicious — real transactions have dates):")
    no_date_vol = 0
    for bank, cnt, vol in c.fetchall():
        vol = vol or 0
        no_date_vol += vol
        print(f"    {bank:<22} {cnt:>6} records  ${vol:>14,.2f}")
    print(f"    TOTAL no-date volume: ${no_date_vol:,.2f}")

    # Check: SDNY exhibit amounts — are these individual transactions or summaries?
    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount), AVG(tx_amount), MAX(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND source_doc_type = 'SDNY_EXHIBIT'
        GROUP BY bank ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  SDNY Exhibit records (may contain summary amounts):")
    for bank, cnt, vol, avg, mx in c.fetchall():
        print(f"    {bank:<22} {cnt:>6} records  ${vol or 0:>14,.2f}  avg=${avg or 0:>10,.2f}  max=${mx or 0:>10,.2f}")

    # Check: single-bates concentration
    c.execute("""
        SELECT bates, bank, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        GROUP BY bates, bank
        HAVING SUM(tx_amount) > 5000000
        ORDER BY SUM(tx_amount) DESC
        LIMIT 15
    """)
    print(f"\n  High-concentration bates pages (>$5M from single page):")
    for bates, bank, cnt, vol in c.fetchall():
        print(f"    {bates:<16} {bank:<18} {cnt:>4} recs  ${vol or 0:>14,.2f}")

    # Check: amounts that appear in BOTH bank_statement_transactions AND extracted_payments
    # (double-counting across tables)
    print(f"\n  Cross-table overlap check (bank_stmt_txns vs extracted_payments):")
    c.execute("""
        SELECT COUNT(*) FROM (
            SELECT DISTINCT bates FROM bank_statement_transactions 
            WHERE record_type = 'TRANSACTION' AND bates IS NOT NULL
            INTERSECT
            SELECT DISTINCT bates FROM extracted_payments WHERE bates IS NOT NULL
        )
    """)
    overlap = c.fetchone()[0]
    print(f"    Shared bates pages: {overlap}")

    # ── APPLY TARGETED FIXES ──
    print(f"\n{'=' * 70}")
    print("APPLYING TARGETED FIXES")
    print(f"{'=' * 70}")

    fixed = 0

    # FIX A: No-date records over $100K → likely summary/balance lines
    # Real transactions virtually always have dates
    print(f"\n[FIX A] No-date records over $100K → NODATE_SUSPECT...")
    c.execute("""
        SELECT id, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NULL AND tx_amount > 100000
    """)
    fix_a = 0
    fix_a_vol = 0
    for rec_id, amount in c.fetchall():
        c.execute("UPDATE bank_statement_transactions SET record_type = 'NODATE_SUSPECT' WHERE id = ?", (rec_id,))
        fix_a += 1
        fix_a_vol += (amount or 0)
        fixed += 1
    print(f"  Demoted {fix_a} records (${fix_a_vol:,.2f})")

    # FIX B: SDNY exhibit records > $1M without clear transaction language
    # Exhibits have summaries mixed with individual transactions
    print(f"\n[FIX B] SDNY exhibit high-value without transaction verbs...")
    TX_VERBS = r'(?i)(wire|transfer|deposit|withdrawal|payment|check|ach|fee|interest|dividend|bought|sold)'
    c.execute("""
        SELECT id, description, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND source_doc_type = 'SDNY_EXHIBIT' AND tx_amount > 1000000
    """)
    fix_b = 0
    fix_b_vol = 0
    for rec_id, desc, amount in c.fetchall():
        if not desc or not re.search(TX_VERBS, desc):
            c.execute("UPDATE bank_statement_transactions SET record_type = 'EXHIBIT_SUMMARY' WHERE id = ?", (rec_id,))
            fix_b += 1
            fix_b_vol += (amount or 0)
            fixed += 1
    print(f"  Demoted {fix_b} records (${fix_b_vol:,.2f})")

    # FIX C: Same amount from same bates appearing multiple times 
    # (different "transactions" extracted from same line of same page)
    print(f"\n[FIX C] Same-page duplicate amounts...")
    c.execute("""
        SELECT id, bank, bates, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' ORDER BY bates, tx_amount DESC
    """)
    seen_page_amounts = {}
    fix_c = 0
    fix_c_vol = 0
    for rec_id, bank, bates, amount in c.fetchall():
        if not amount or not bates:
            continue
        key = f"{bates}|{round(amount, 2)}"
        if key in seen_page_amounts:
            c.execute("UPDATE bank_statement_transactions SET record_type = 'SAME_PAGE_DUP' WHERE id = ?", (rec_id,))
            fix_c += 1
            fix_c_vol += amount
            fixed += 1
        else:
            seen_page_amounts[key] = rec_id
    print(f"  Demoted {fix_c} records (${fix_c_vol:,.2f})")

    # FIX D: Description contains "balance" anywhere (final catch-all)
    print(f"\n[FIX D] Remaining 'balance' language in descriptions...")
    BALANCE_FINAL = r'(?i)\b(balance|total\s+value|total\s+assets|net\s+worth|account\s+value|market\s+value)\b'
    c.execute("""
        SELECT id, description, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND description IS NOT NULL AND tx_amount > 50000
    """)
    fix_d = 0
    fix_d_vol = 0
    for rec_id, desc, amount in c.fetchall():
        if re.search(BALANCE_FINAL, desc):
            c.execute("UPDATE bank_statement_transactions SET record_type = 'BALANCE_LANGUAGE' WHERE id = ?", (rec_id,))
            fix_d += 1
            fix_d_vol += (amount or 0)
            fixed += 1
    print(f"  Demoted {fix_d} records (${fix_d_vol:,.2f})")

    conn.commit()

    # ═══════════════════════════════════════════════════════
    # FINAL FINAL RESULTS
    # ═══════════════════════════════════════════════════════

    print(f"\n{'=' * 70}")
    print("FINAL RECORD TYPES")
    print(f"{'=' * 70}")
    c.execute("""
        SELECT record_type, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        GROUP BY record_type ORDER BY SUM(tx_amount) DESC
    """)
    final_vol = 0
    final_cnt = 0
    print(f"\n  {'Type':<25} {'Recs':>8} {'Volume':>20}")
    print("  " + "─" * 55)
    for rtype, cnt, vol in c.fetchall():
        vol = vol or 0
        m = " ← CLEAN" if rtype == 'TRANSACTION' else ""
        print(f"  {rtype:<25} {cnt:>8,} ${vol:>18,.2f}{m}")
        if rtype == 'TRANSACTION':
            final_vol = vol
            final_cnt = cnt

    print(f"\n{'=' * 70}")
    print("FINAL PER-BANK")
    print(f"{'=' * 70}")
    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount), MIN(tx_amount), MAX(tx_amount), AVG(tx_amount)
        FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'
        GROUP BY bank ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Bank':<22} {'Recs':>6} {'Volume':>16} {'Max':>12} {'Avg':>10}")
    print("  " + "─" * 70)
    gt = 0
    for bank, cnt, vol, mn, mx, avg in c.fetchall():
        vol = vol or 0
        gt += vol
        print(f"  {bank:<22} {cnt:>6,} ${vol:>14,.2f} ${mx or 0:>10,.2f} ${avg or 0:>8,.2f}")
    print("  " + "─" * 70)
    print(f"  {'TOTAL':<22} {final_cnt:>6,} ${gt:>14,.2f}")

    # Entity matches
    print(f"\n{'=' * 70}")
    print("ENTITY MATCHES (final clean)")
    print(f"{'=' * 70}")
    c.execute("""
        SELECT entity_match, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE entity_match IS NOT NULL AND record_type = 'TRANSACTION'
        GROUP BY entity_match ORDER BY SUM(tx_amount) DESC LIMIT 20
    """)
    for entity, cnt, vol in c.fetchall():
        print(f"  {entity:<30} {cnt:>6} txns  ${vol or 0:>14,.2f}")

    # Full progression
    print(f"\n{'=' * 70}")
    print("COMPLETE INFLATION FIX PROGRESSION")
    print(f"{'=' * 70}")
    print(f"  Layer 0 (raw parser):            $68,745,222,404.77  (24,563 records)")
    print(f"  Layer 1 (record classifier):     $23,695,632,641.86  (10,513 records)")
    print(f"  Layer 2 (source doc type):        $14,612,679,834.57  ( 8,123 records)")
    print(f"  Layer 3 (outlier+dedup caps):     $ 4,113,970,148.71  ( 7,374 records)")
    print(f"  Layer 4 (WM+stats+IQR):           $   323,079,163.74  ( 6,040 records)")
    print(f"  Layer 5 (surgical cleanup):       ${final_vol:>18,.2f}  ({final_cnt:,} records)")
    if final_vol > 0:
        reduction = (1 - final_vol / 68_745_222_404.77) * 100
        print(f"  Total inflation removed:          {reduction:.2f}%")

    conn.close()
    print(f"\n  Surgical cleanup complete.")


if __name__ == "__main__":
    main()
