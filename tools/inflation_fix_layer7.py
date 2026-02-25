#!/usr/bin/env python3
"""
INFLATION FIX — LAYER 7: FINAL TRIAGE
Manual review of 8 remaining $10K+ records.
Pattern sweep of sub-$10K records for remaining noise.

Author: Randall Scott Taylor
"""

import sqlite3, re, os
from collections import Counter

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("LAYER 7 — FINAL TRIAGE")
    print("=" * 70)

    c.execute("""
        SELECT COUNT(*), SUM(tx_amount) FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
    """)
    cnt, vol = c.fetchone()
    print(f"[IN] {cnt:,} TRANSACTION records, ${vol:,.2f}")

    fixed = 0
    fix_vol = 0

    # ── MANUAL TRIAGE: 8 records over $10K ──
    print(f"\n[FIX 1] Manual triage of $10K+ records...")

    # IDs to demote with reason
    MANUAL_KILLS = {
        18024: 'TRADE_SETTLEMENT',     # Barclays $152,720 "TRADE DATE: VALUE DATE:" — securities settlement
        22477: 'MORTGAGE_RECORD',       # Citibank $150,000 "Loan Amount: Lender Name: ASTORIA FSLA"
        22974: 'STMT_HEADER',           # Citibank $23,222 "Primary Account: For the Period to"
        24196: 'EXHIBIT_HEADER',        # Citibank $10,000 "EXHIBIT N: TIMELINE OF PAYMENTS TO..."
    }

    for rec_id, reason in MANUAL_KILLS.items():
        c.execute("SELECT tx_amount FROM bank_statement_transactions WHERE id = ? AND record_type = 'TRANSACTION'", (rec_id,))
        row = c.fetchone()
        if row:
            c.execute("UPDATE bank_statement_transactions SET record_type = ? WHERE id = ?", (reason, rec_id))
            fixed += 1
            fix_vol += (row[0] or 0)
            print(f"    #{rec_id} ${row[0]:,.2f} → {reason}")

    # ── PATTERN SWEEP: sub-$10K remaining noise ──
    print(f"\n[FIX 2] Sub-$10K pattern sweep...")

    # Patterns that indicate noise in smaller records
    NOISE_PATTERNS = [
        # Statement/bank marketing language
        (r'(?i)citibank\s+global\s+transfers', 'BANK_MARKETING'),
        (r'(?i)give\s+yourself\s+the\s+gift', 'BANK_MARKETING'),
        (r'(?i)when\s+planning\s+your\s+big\s+trip', 'BANK_MARKETING'),
        (r'(?i)help\s+protect\s+yourself\s+from\s+fraud', 'BANK_MARKETING'),
        (r'(?i)tax\s+statements?\s+are\s+now\s+available', 'BANK_MARKETING'),
        (r'(?i)suggestions?\s+and\s+recommendations?', 'BANK_MARKETING'),
        (r'(?i)discontinued\s+as\s+of', 'BANK_NOTICE'),
        (r'(?i)basic\s+banking\s+package', 'FEE_SCHEDULE'),
        (r'(?i)streamlined\s+checking\s+fees', 'FEE_SCHEDULE'),
        (r'(?i)type\s+of\s+charge', 'FEE_SCHEDULE'),
        (r'(?i)service\s+charges?\s+and\s+other\s+fees', 'FEE_HEADER'),
        (r'(?i)NSF\s+.*item\s+fees\s+for\s+this\s+statement', 'FEE_HEADER'),

        # OCR garbage / garbled text
        (r'(?i)MACR\s+WPM\s+.*SAMMAST', 'OCR_GARBAGE'),
        (r'(?i)IIIMMall\s+igiaM', 'OCR_GARBAGE'),
        (r'(?i)MRVACRVAME', 'OCR_GARBAGE'),
        (r'(?i)atement\s+eriod', 'OCR_GARBAGE'),  # garbled "statement period"

        # Account structure / header lines
        (r'(?i)savings\s+checking\s+plus', 'ACCOUNT_TYPE'),
        (r'(?i)citibusiness\s+streamlined', 'ACCOUNT_TYPE'),
        (r'(?i)bank\s+number:\s+\d', 'ACCOUNT_HEADER'),
        (r'(?i)account\s+number\s+at\s+', 'ACCOUNT_HEADER'),
        (r'(?i)deposit\s+services\s+checks', 'SERVICE_HEADER'),

        # Securities/investment language (not transactions)
        (r'(?i)unrealized\s+gain', 'UNREALIZED'),
        (r'(?i)noncovered\s+under\s+the\s+cost\s+basis', 'COST_BASIS'),
        (r'(?i)total\s+fixed\s+income', 'PORTFOLIO_LINE'),
        (r'(?i)unrested\s+giddies', 'OCR_GARBAGE'),  # garbled "unrealized"
        (r'(?i)awned\s+intend', 'OCR_GARBAGE'),       # garbled "accrued interest"
        (r'(?i)selected\s+untealzed', 'OCR_GARBAGE'),  # garbled "unrealized"

        # Closing balance language variants
        (r'(?i)closing\s+.*deposit\s+balance', 'CLOSING_BALANCE'),
        (r'(?i)closing\s+balance', 'CLOSING_BALANCE'),
        (r'(?i)dosing\s+balance', 'CLOSING_BALANCE'),  # OCR "closing"

        # Items already credited / legal boilerplate
        (r'(?i)all\s+items\s+are\s+credited\s+subject\s+to\s+final', 'LEGAL_BOILERPLATE'),
        (r'(?i)receipt\s+of\s+proceed', 'LEGAL_BOILERPLATE'),

        # SDNY document references
        (r'(?i)SDNY\s*GM\s*\d{8}', 'SDNY_REF'),
        (r'(?i)confidential\s+treatment\s+requested', 'LEGAL_STAMP'),

        # Page structure
        (r'(?i)page\s+\d+\s+of\s+\d+', 'PAGE_HEADER'),
        (r'(?i)totals?\s+\d[\d,]+\.\d{2}', 'TOTAL_LINE'),

        # "For the Period" headers
        (r'(?i)for\s+the\s+period\s+(to|from|ending)', 'PERIOD_HEADER'),

        # "Additions/Subtractions" summary headers  
        (r'(?i)(additions|subtractions)\s+(deposits|checks|withdrawals)', 'SUMMARY_HEADER'),

        # "Account activity this month"
        (r'(?i)account\s+activity\s+this\s+month', 'ACTIVITY_HEADER'),

        # Annual percentage
        (r'(?i)annual\s+percentage\s+.*earned', 'APY_LINE'),

        # "The total deposits activity for the statement period"
        (r'(?i)total\s+(deposits?|withdrawals?)\s+activity\s+for', 'PERIOD_SUMMARY'),

        # Interest earned (without specific amount context = balance line)
        (r'(?i)^interest\s+earned$', 'INTEREST_SUMMARY'),
        (r'(?i)^interest\s+earned\s+[\$\d]', 'INTEREST_LINE'),

        # Exhibit headers
        (r'(?i)EXHIBIT\s+[A-Z]:\s+(TIMELINE|SUMMARY|LIST)', 'EXHIBIT_HEADER'),

        # Loan/mortgage records
        (r'(?i)loan\s+amount:', 'LOAN_RECORD'),
        (r'(?i)lender\s+name:', 'LOAN_RECORD'),
        (r'(?i)recording\s+date:', 'LOAN_RECORD'),
    ]

    c.execute("""
        SELECT id, tx_amount, description FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND description IS NOT NULL
    """)
    pattern_fixes = Counter()
    for rec_id, amount, desc in c.fetchall():
        for pat, label in NOISE_PATTERNS:
            if re.search(pat, desc):
                c.execute("UPDATE bank_statement_transactions SET record_type = ? WHERE id = ?",
                         (f'NOISE:{label}', rec_id))
                pattern_fixes[label] += 1
                fixed += 1
                fix_vol += (amount or 0)
                break

    print(f"  Pattern hits:")
    for label, cnt in pattern_fixes.most_common():
        print(f"    {label:<25} {cnt:>4}")
    print(f"  Total: {sum(pattern_fixes.values())} records")

    # ── FIX 3: Empty description records over $1K ──
    print(f"\n[FIX 3] Empty description records over $1K...")
    c.execute("""
        SELECT id, tx_amount, description FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_amount > 1000
    """)
    fix3 = 0
    fix3_vol = 0
    for rec_id, amount, desc in c.fetchall():
        desc_clean = (desc or '').strip()
        if len(desc_clean) < 3:
            c.execute("UPDATE bank_statement_transactions SET record_type = 'NO_DESC_1K' WHERE id = ?", (rec_id,))
            fix3 += 1
            fix3_vol += (amount or 0)
    print(f"  Demoted {fix3} records (${fix3_vol:,.2f})")

    # ── FIX 4: No-date records $1K-$5K ──
    print(f"\n[FIX 4] No-date records $1K-$5K...")
    c.execute("""
        SELECT id, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NULL AND tx_amount BETWEEN 1000 AND 5000
    """)
    fix4 = 0
    fix4_vol = 0
    for rec_id, amount in c.fetchall():
        c.execute("UPDATE bank_statement_transactions SET record_type = 'NODATE_1K' WHERE id = ?", (rec_id,))
        fix4 += 1
        fix4_vol += (amount or 0)
    print(f"  Demoted {fix4} records (${fix4_vol:,.2f})")

    conn.commit()

    # ═══════════════════════════════════════════════════════
    # FINAL RESULTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("RESULTS AFTER LAYER 7")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT COUNT(*), SUM(tx_amount) FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
    """)
    final_cnt, final_vol = c.fetchone()
    final_vol = final_vol or 0
    print(f"\n  TRANSACTION: {final_cnt:,} records, ${final_vol:,.2f}")

    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount), MAX(tx_amount), AVG(tx_amount)
        FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'
        GROUP BY bank ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Bank':<22} {'Recs':>6} {'Volume':>14} {'Max':>10} {'Avg':>8}")
    print("  " + "─" * 64)
    gt = 0
    for bank, cnt, vol, mx, avg in c.fetchall():
        vol = vol or 0
        gt += vol
        print(f"  {bank:<22} {cnt:>6,} ${vol:>12,.2f} ${mx or 0:>8,.2f} ${avg or 0:>6,.2f}")
    print("  " + "─" * 64)
    print(f"  {'TOTAL':<22} {final_cnt:>6,} ${gt:>12,.2f}")

    # Remaining $10K+
    c.execute("""
        SELECT id, bank, tx_amount, tx_date, description
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_amount >= 10000
        ORDER BY tx_amount DESC
    """)
    big = c.fetchall()
    print(f"\n  Remaining >= $10K: {len(big)}")
    for rec_id, bank, amount, date, desc in big:
        print(f"    #{rec_id} {bank:<14} ${amount:>10,.2f} {date or 'no-date':<12} {(desc or '')[:60]}")

    # Remaining $1K+
    c.execute("""
        SELECT COUNT(*), SUM(tx_amount) FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_amount >= 1000
    """)
    k_cnt, k_vol = c.fetchone()
    print(f"\n  Remaining >= $1K: {k_cnt} records, ${k_vol or 0:,.2f}")

    # Amount distribution
    print(f"\n  Amount Distribution:")
    c.execute("SELECT tx_amount FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'")
    amounts = [r[0] or 0 for r in c.fetchall()]
    for label, lo, hi in [('$10K+', 10000, 999999999), ('$1K-10K', 1000, 10000),
                           ('$100-1K', 100, 1000), ('$10-100', 10, 100), ('<$10', 0, 10)]:
        bucket = [a for a in amounts if lo <= a < hi]
        print(f"    {label:<12} {len(bucket):>6} recs  ${sum(bucket):>12,.2f}")

    # Entity matches
    print(f"\n  Entity Matches:")
    c.execute("""
        SELECT entity_match, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE entity_match IS NOT NULL AND record_type = 'TRANSACTION'
        GROUP BY entity_match ORDER BY SUM(tx_amount) DESC
    """)
    for entity, cnt, vol in c.fetchall():
        print(f"    {entity:<30} {cnt:>4} txns  ${vol or 0:>10,.2f}")

    # Has-date vs no-date
    c.execute("""
        SELECT 
            SUM(CASE WHEN tx_date IS NOT NULL THEN 1 ELSE 0 END) as with_date,
            SUM(CASE WHEN tx_date IS NULL THEN 1 ELSE 0 END) as no_date,
            SUM(CASE WHEN tx_date IS NOT NULL THEN tx_amount ELSE 0 END) as date_vol,
            SUM(CASE WHEN tx_date IS NULL THEN tx_amount ELSE 0 END) as nodate_vol
        FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'
    """)
    wd, nd, dv, nv = c.fetchone()
    print(f"\n  Date coverage: {wd or 0} with date (${dv or 0:,.2f}), {nd or 0} no date (${nv or 0:,.2f})")

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
    print(f"  Layer 7 (deep audit):  $     2,138,920.65  ( 3,027)")
    print(f"  Layer 8 (final):       ${final_vol:>18,.2f}  ({final_cnt:,})")
    reduction = (1 - final_vol / 68_745_222_404.77) * 100 if final_vol > 0 else 100
    print(f"  Inflation removed:     {reduction:.5f}%")

    conn.close()
    print(f"\n  Final triage complete.")


if __name__ == "__main__":
    main()
