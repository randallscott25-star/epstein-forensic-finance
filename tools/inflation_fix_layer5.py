#!/usr/bin/env python3
"""
INFLATION FIX — LAYER 5: FINAL SCRUB
Three remaining issues:

1. BALANCE-AS-TRANSACTION: Parser grabbed largest $ on line, but it's
   the balance. Real transaction amount is smaller number in description.
   Fix: when description contains a dollar amount significantly smaller
   than tx_amount, tx_amount is likely the balance.

2. BANK MISATTRIBUTION: Pages tagged as Barclays but source is UBS,
   HSBC but source is Deutsche Bank, Citi/First Bank PR but source is JPM.
   Fix: check source text for actual bank identity, correct or flag.

3. BALANCE-LINE PATTERNS: "Dividends/Interest", "Funds Deposited",
   "Net cash flow" followed by a smaller amount — the tx_amount is the
   running balance, not the transaction.

Author: Randall Scott Taylor
"""

import sqlite3, re, os
from collections import Counter, defaultdict

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")

DOLLAR_IN_DESC = re.compile(r'\$?\s*([\d]{1,3}(?:,\d{3})*(?:\.\d{2}))')

# Pattern: description has a clear smaller amount that IS the transaction
# while tx_amount is the running balance
BALANCE_LINE_PATTERNS = [
    # "Dividends/Interest 12,362.64" — the number after is the real amount
    r'(?i)(dividend|interest|coupon)\s*[/&]?\s*(interest|dividend)?\s+[\$]?([\d,]+\.?\d*)',
    # "Funds Deposited 150,000.00"
    r'(?i)(funds?\s+deposited|deposits?)\s+[\$]?([\d,]+\.?\d*)',
    # "Funds Withdrawn 5,000.00"  
    r'(?i)(funds?\s+withdrawn|withdrawals?)\s+[\$]?([\d,]+\.?\d*)',
    # "Check Paid 50.00" or "Checks Paid 50.00"
    r'(?i)(checks?\s+paid)\s+[\$]?([\d,]+\.?\d*)',
    # "Interest Paid this Period" (no amount after — it's a summary line)
    r'(?i)interest\s+paid\s+(this\s+period|year\s+to\s+da[lt]e)',
    # "Average Balance"
    r'(?i)average\s+balance',
    # "Total Debits" / "Total Credits"  
    r'(?i)total\s+(debits?|credits?)\s',
    # "Total Cash"
    r'(?i)total\s+cash\b',
    # "Transactions by Type of Activity"
    r'(?i)transactions\s+by\s+type',
    # "100.00% Value of your account"
    r'(?i)100\.?00%\s+(value|total)',
    # "Value of your account"
    r'(?i)value\s+of\s+your\s+account',
    # "Net cash flow"
    r'(?i)net\s+cash\s+flow',
    # "Number of days in interest period"
    r'(?i)number\s+of\s+days\s+in',
    # "Deposit Sweep Interest"
    r'(?i)deposit\s+sweep\s+interest',
    # OCR garbage: just numbers, no words
    r'^[\d\s,\.\$\-]+$',
    # Description is just a bates number
    r'^EFTA\d{8,}$',
    # "Date Description" or "Date Dacription" (OCR header)
    r'(?i)^date\s+d[ae][sc][cr]',
    # "Deposits and Other Credits" (summary header)
    r'(?i)deposits?\s+and\s+other\s+credits?',
    # Single word descriptions that are headers
    r'(?i)^(distributions?|disbursements?)$',
]

# Source text patterns for bank misattribution detection
REAL_BANK_PATTERNS = {
    'JPMorgan': [
        r'(?i)JPMorgan\s+Private\s+Bank',
        r'(?i)Premier\s+Check',
        r'(?i)Account\s+Number:?\s*739-',
    ],
    'UBS': [
        r'(?i)UBS\s+Financial\s+Services',
        r'(?i)Account\s+name:\s*GHISL',
    ],
    'Deutsche Bank': [
        r'(?i)Deutsche\s+Asset\s+&?\s*Wealth',
        r'(?i)Deutsche\s+Bank\s+Private\s+Wealth',
    ],
}


def get_source_text(c, bates):
    """Pull first page source OCR."""
    c.execute("""
        SELECT et.text_content
        FROM extracted_text et JOIN files f ON f.id = et.file_id
        WHERE REPLACE(f.title, '.pdf', '') = ?
        ORDER BY et.page_num LIMIT 1
    """, (bates,))
    row = c.fetchone()
    return row[0][:1000] if row and row[0] else ''


def detect_real_bank(source_text):
    """Check if source text reveals a different bank than attributed."""
    for real_bank, patterns in REAL_BANK_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, source_text):
                return real_bank
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("LAYER 5 — FINAL SCRUB")
    print("=" * 70)

    c.execute("""
        SELECT id, bank, bates, tx_amount, tx_date, description, source_doc_type
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        ORDER BY tx_amount DESC
    """)
    txn_rows = c.fetchall()
    current_vol = sum(r[3] or 0 for r in txn_rows)
    print(f"[IN] {len(txn_rows):,} TRANSACTION records, ${current_vol:,.2f}")

    fixes = Counter()
    fix_vol = Counter()

    # ── FIX 1: Balance-line pattern detection ──
    print(f"\n[FIX 1] Balance-line and summary-header detection...")

    for rec_id, bank, bates, amount, date, desc, stype in txn_rows:
        if not amount:
            continue
        desc_str = desc or ''

        for pat in BALANCE_LINE_PATTERNS:
            if re.search(pat, desc_str):
                c.execute("UPDATE bank_statement_transactions SET record_type = 'BALANCE_LINE' WHERE id = ?",
                         (rec_id,))
                fixes['BALANCE_LINE'] += 1
                fix_vol['BALANCE_LINE'] += amount
                break

    print(f"  Demoted {fixes['BALANCE_LINE']:,} records (${fix_vol['BALANCE_LINE']:,.2f})")

    # ── FIX 2: Empty/minimal description with high amount ──
    # Real transactions have descriptions. No description + high amount = balance snapshot.
    print(f"\n[FIX 2] Empty/minimal description over $10K...")

    c.execute("""
        SELECT id, tx_amount, description FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_amount > 10000
    """)
    for rec_id, amount, desc in c.fetchall():
        desc_clean = (desc or '').strip()
        # Empty, single word, or just numbers
        if len(desc_clean) < 3 or (len(desc_clean.split()) <= 1 and not re.search(r'[a-zA-Z]{3,}', desc_clean)):
            c.execute("UPDATE bank_statement_transactions SET record_type = 'NO_CONTEXT' WHERE id = ?",
                     (rec_id,))
            fixes['NO_CONTEXT'] += 1
            fix_vol['NO_CONTEXT'] += (amount or 0)

    print(f"  Demoted {fixes['NO_CONTEXT']:,} records (${fix_vol['NO_CONTEXT']:,.2f})")

    # ── FIX 3: Bank misattribution flagging ──
    print(f"\n[FIX 3] Checking for bank misattribution...")

    # Check Citibank, First Bank PR, Barclays, HSBC records
    SUSPECT_BANKS = ['Citibank', 'First Bank PR', 'Barclays', 'HSBC']
    c.execute("""
        SELECT DISTINCT bates, bank FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND bank IN ({})
        AND bates IS NOT NULL
    """.format(','.join('?' * len(SUSPECT_BANKS))), SUSPECT_BANKS)

    misattributed = 0
    misattr_vol = 0
    bates_corrections = {}

    for bates, attributed_bank in c.fetchall():
        src = get_source_text(c, bates)
        if not src:
            continue
        real_bank = detect_real_bank(src)
        if real_bank and real_bank != attributed_bank:
            bates_corrections[bates] = (attributed_bank, real_bank)

    # Apply corrections — update bank name, add note
    for bates, (old_bank, new_bank) in bates_corrections.items():
        c.execute("""
            UPDATE bank_statement_transactions 
            SET bank = ?, description = description || ' [CORRECTED: was ' || ? || ']'
            WHERE bates = ? AND record_type = 'TRANSACTION'
        """, (new_bank, old_bank, bates))
        c.execute("SELECT COUNT(*), SUM(tx_amount) FROM bank_statement_transactions WHERE bates = ?", (bates,))
        cnt, vol = c.fetchone()
        misattributed += cnt
        misattr_vol += (vol or 0)
        print(f"    {bates}: {old_bank} → {new_bank} ({cnt} records)")

    print(f"  Corrected {misattributed:,} records across {len(bates_corrections)} bates pages")

    # ── FIX 4: Remaining records over $50K with no date ──
    # We already did >$100K. Now catch $50K-$100K no-date.
    print(f"\n[FIX 4] No-date records $50K-$100K...")
    c.execute("""
        SELECT id, tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NULL
        AND tx_amount BETWEEN 50000 AND 100000
    """)
    for rec_id, amount in c.fetchall():
        c.execute("UPDATE bank_statement_transactions SET record_type = 'NODATE_SUSPECT' WHERE id = ?",
                 (rec_id,))
        fixes['NODATE_50K'] += 1
        fix_vol['NODATE_50K'] += (amount or 0)
    print(f"  Demoted {fixes['NODATE_50K']:,} records (${fix_vol['NODATE_50K']:,.2f})")

    # ── FIX 5: Starbucks and obvious personal spend noise (UBS) ──
    print(f"\n[FIX 5] Card purchase / personal spend noise over $50K...")
    c.execute("""
        SELECT id, tx_amount, description FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_amount > 50000
        AND description LIKE '%card purchase%'
    """)
    for rec_id, amount, desc in c.fetchall():
        c.execute("UPDATE bank_statement_transactions SET record_type = 'CARD_SUMMARY' WHERE id = ?",
                 (rec_id,))
        fixes['CARD_SUMMARY'] += 1
        fix_vol['CARD_SUMMARY'] += (amount or 0)
    print(f"  Demoted {fixes['CARD_SUMMARY']:,} records (${fix_vol['CARD_SUMMARY']:,.2f})")

    conn.commit()

    # ═══════════════════════════════════════════════════════
    # FINAL RESULTS
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
    print("FINAL PER-BANK (corrected attributions)")
    print(f"{'=' * 70}")
    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount), MAX(tx_amount), AVG(tx_amount)
        FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'
        GROUP BY bank ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Bank':<22} {'Recs':>6} {'Volume':>16} {'Max':>12} {'Avg':>10}")
    print("  " + "─" * 70)
    gt = 0
    for bank, cnt, vol, mx, avg in c.fetchall():
        vol = vol or 0
        gt += vol
        print(f"  {bank:<22} {cnt:>6,} ${vol:>14,.2f} ${mx or 0:>10,.2f} ${avg or 0:>8,.2f}")
    print("  " + "─" * 70)
    print(f"  {'TOTAL':<22} {final_cnt:>6,} ${gt:>14,.2f}")

    # Entity matches
    print(f"\n  Entity Matches:")
    c.execute("""
        SELECT entity_match, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE entity_match IS NOT NULL AND record_type = 'TRANSACTION'
        GROUP BY entity_match ORDER BY SUM(tx_amount) DESC LIMIT 15
    """)
    for entity, cnt, vol in c.fetchall():
        print(f"    {entity:<30} {cnt:>4} txns  ${vol or 0:>12,.2f}")

    # Amount distribution
    print(f"\n  Amount Distribution:")
    ranges = [
        ('$10K+', 10000), ('$1K-10K', 1000), ('$100-1K', 100),
        ('$10-100', 10), ('Under $10', 0)
    ]
    c.execute("""
        SELECT tx_amount FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
    """)
    amounts = [r[0] or 0 for r in c.fetchall()]
    for label, floor in ranges:
        if floor == 0:
            bucket = [a for a in amounts if a < 10]
        else:
            ceiling = floor * 10
            bucket = [a for a in amounts if floor <= a < ceiling]
        bvol = sum(bucket)
        print(f"    {label:<15} {len(bucket):>6} records  ${bvol:>14,.2f}")

    # Progression
    print(f"\n{'=' * 70}")
    print("COMPLETE PROGRESSION")
    print(f"{'=' * 70}")
    print(f"  Layer 0 (raw):              $68,745,222,404.77  (24,563 records)")
    print(f"  Layer 1 (record type):      $23,695,632,641.86  (10,513)")
    print(f"  Layer 2 (source doc):       $14,612,679,834.57  ( 8,123)")
    print(f"  Layer 3 (outlier caps):     $ 4,113,970,148.71  ( 7,374)")
    print(f"  Layer 4 (WM+IQR):          $   323,079,163.74  ( 6,040)")
    print(f"  Layer 5 (surgical):         $    49,438,314.99  ( 5,429)")
    print(f"  Layer 6 (final scrub):      ${final_vol:>18,.2f}  ({final_cnt:,})")
    if final_vol > 0:
        reduction = (1 - final_vol / 68_745_222_404.77) * 100
        print(f"  Inflation removed:          {reduction:.3f}%")

    conn.close()
    print(f"\n  Final scrub complete.")


if __name__ == "__main__":
    main()
