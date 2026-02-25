#!/usr/bin/env python3
"""
BANK STATEMENT RECORD CLASSIFIER
Classifies bank_statement_transactions records into:
  TRANSACTION  — actual money movement (wire, check, deposit, withdrawal)
  BALANCE      — account balance snapshot (opening/closing/ending balance)
  HOLDING      — portfolio/securities holding value
  SUMMARY      — account summary line (total assets, net worth)
  UNKNOWN      — can't determine

Then recalculates volumes using only TRANSACTION records.

Run after multi_bank_parser.py --live

Author: Randall Scott Taylor
"""

import sqlite3, re, os, sys
from collections import Counter

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")

# ── Classification patterns ──

# BALANCE indicators: these amounts are snapshots, not movements
BALANCE_PATTERNS = [
    r'(?i)(opening|closing|ending|beginning|previous|available|current|account)\s+balance',
    r'(?i)balance\s+(forward|brought|carried)',
    r'(?i)total\s+(balance|value|equity|assets)',
    r'(?i)net\s+(asset|worth|balance|equity)',
    r'(?i)market\s+value',
    r'(?i)as\s+of\s+\d',
    r'(?i)balance\s+as\s+of',
    r'(?i)estimated\s+(value|total|balance)',
]

# HOLDING indicators: portfolio line items
HOLDING_PATTERNS = [
    r'(?i)portfolio\s+holdings?',
    r'(?i)(shares?|units?)\s+held',
    r'(?i)(cusip|isin|sedol)',
    r'(?i)dreyfus|vanguard|fidelity|schwab\s+fund',
    r'(?i)(mutual\s+fund|money\s+market|bond\s+fund|equity\s+fund)',
    r'(?i)cash\s+&?\s*cash\s+equivalents',
    r'(?i)(maturity|coupon|yield|par\s+value)',
    r'(?i)security\s+(description|name|type)',
    r'(?i)quantity\s+.*\s+price',
    r'(?i)(stock|bond|note|treasury)\s+(position|holding)',
    r'(?i)unrealized\s+(gain|loss)',
]

# SUMMARY indicators: account-level totals
SUMMARY_PATTERNS = [
    r'(?i)account\s+summary',
    r'(?i)total\s+(debit|credit|deposit|withdrawal)s?\s*:',
    r'(?i)total\s+(?:for\s+)?(?:this\s+)?(?:period|month|quarter|statement)',
    r'(?i)what.?s\s+in\s+this\s+statement',
    r'(?i)your\s+(account|portfolio)\s+(summary|overview|at\s+a\s+glance)',
    r'(?i)summary\s+of\s+.*\s+accounts?',
    r'(?i)financial\s+instutition',  # typo in source data
]

# TRANSACTION indicators: actual money movement
TRANSACTION_PATTERNS = [
    r'(?i)(wire|wir)\s*(transfer|in|out|received|sent)',
    r'(?i)(deposit|deposited)\s',
    r'(?i)(withdrawal|withdrawn|disbursement)',
    r'(?i)check\s*(#|number|paid|cleared)',
    r'(?i)(payment|paid)\s+(to|from|received)',
    r'(?i)(ach|eft)\s*(debit|credit|transfer)',
    r'(?i)(book\s+transfer|journal\s+entry)',
    r'(?i)(interest|dividend)\s*(paid|earned|credited|received)',
    r'(?i)(fee|charge)\s*(assessed|deducted|charged)',
    r'(?i)(bought|sold|purchase|sale)\s+\d',
    r'(?i)(incoming|outgoing)\s+(wire|transfer|payment)',
    r'(?i)transfer\s+(to|from)\s+',
]

# Banks that are primarily brokerage (most records will be holdings)
BROKERAGE_BANKS = ['Bear Stearns', 'Morgan Stanley', 'Charles Schwab']

# Banks with primarily banking activity (most records should be transactions)
BANKING_BANKS = ['Deutsche Bank', 'Citibank', 'First Bank PR', 'Navy Federal', 'Merchants Commercial']


def classify_record(description, bank, tx_type, amount):
    """Classify a single record based on description context."""
    if not description:
        # No description — use bank type as heuristic
        if bank in BROKERAGE_BANKS:
            return 'HOLDING'
        return 'UNKNOWN'

    desc = description

    # Score each category
    scores = {
        'TRANSACTION': 0,
        'BALANCE': 0,
        'HOLDING': 0,
        'SUMMARY': 0,
    }

    for pat in TRANSACTION_PATTERNS:
        if re.search(pat, desc):
            scores['TRANSACTION'] += 2

    for pat in BALANCE_PATTERNS:
        if re.search(pat, desc):
            scores['BALANCE'] += 2

    for pat in HOLDING_PATTERNS:
        if re.search(pat, desc):
            scores['HOLDING'] += 2

    for pat in SUMMARY_PATTERNS:
        if re.search(pat, desc):
            scores['SUMMARY'] += 2

    # tx_type from parser gives bonus points
    if tx_type in ('wire_transfer', 'check', 'deposit', 'withdrawal',
                    'book_transfer', 'fee', 'interest', 'dividend'):
        scores['TRANSACTION'] += 3

    if tx_type == 'securities':
        scores['HOLDING'] += 1
        scores['TRANSACTION'] += 1  # could be a trade

    # Bank-type heuristic for ties
    if bank in BROKERAGE_BANKS:
        scores['HOLDING'] += 1
    elif bank in BANKING_BANKS:
        scores['TRANSACTION'] += 1

    # Very large amounts are more likely balances/holdings than transactions
    if amount and amount > 10_000_000:
        scores['BALANCE'] += 1
        scores['HOLDING'] += 1

    # Pick winner
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return 'UNKNOWN'
    
    # If it's a tie including TRANSACTION, prefer TRANSACTION
    if scores['TRANSACTION'] == scores[best] and best != 'TRANSACTION':
        return 'TRANSACTION'

    return best


def reclassify_from_source(conn):
    """Go back to source OCR text for records that need context.
    For records with empty/short descriptions, pull the source page
    and re-examine the surrounding text."""
    c = conn.cursor()
    
    # Get records with empty/short descriptions
    c.execute("""
        SELECT bst.id, bst.bates, bst.bank, bst.tx_amount, bst.description
        FROM bank_statement_transactions bst
        WHERE bst.record_type = 'UNKNOWN'
        AND bst.bates IS NOT NULL
        LIMIT 5000
    """)
    unknown_recs = c.fetchall()
    
    if not unknown_recs:
        return 0
    
    reclassified = 0
    # Group by bates for efficiency
    by_bates = {}
    for rec_id, bates, bank, amount, desc in unknown_recs:
        if bates not in by_bates:
            by_bates[bates] = []
        by_bates[bates].append((rec_id, bank, amount, desc))
    
    for bates, recs in by_bates.items():
        # Get source text
        c.execute("""
            SELECT et.text_content 
            FROM extracted_text et
            JOIN files f ON f.id = et.file_id
            WHERE REPLACE(f.title, '.pdf', '') = ?
            LIMIT 1
        """, (bates,))
        row = c.fetchone()
        if not row or not row[0]:
            continue
        
        page_text = row[0][:3000]
        
        for rec_id, bank, amount, desc in recs:
            # Use full page context for classification
            new_type = classify_record(page_text, bank, 'unknown', amount)
            if new_type != 'UNKNOWN':
                c.execute("UPDATE bank_statement_transactions SET record_type = ? WHERE id = ?",
                         (new_type, rec_id))
                reclassified += 1
    
    conn.commit()
    return reclassified


def main():
    print("=" * 70)
    print("BANK STATEMENT RECORD CLASSIFIER")
    print("=" * 70)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Add record_type column if not exists
    try:
        c.execute("ALTER TABLE bank_statement_transactions ADD COLUMN record_type TEXT DEFAULT 'UNKNOWN'")
        conn.commit()
        print("[DB] Added record_type column")
    except:
        print("[DB] record_type column exists")

    # Get all records
    c.execute("""
        SELECT id, bank, description, tx_type, tx_amount
        FROM bank_statement_transactions
    """)
    rows = c.fetchall()
    print(f"[DB] Classifying {len(rows):,} records...")

    type_counts = Counter()
    bank_types = {}

    for rec_id, bank, desc, tx_type, amount in rows:
        record_type = classify_record(desc, bank, tx_type, amount)
        type_counts[record_type] += 1

        if bank not in bank_types:
            bank_types[bank] = Counter()
        bank_types[bank][record_type] += 1

        c.execute("UPDATE bank_statement_transactions SET record_type = ? WHERE id = ?",
                  (record_type, rec_id))

    conn.commit()

    # Phase 2: re-examine UNKNOWNs using source text
    print(f"\n[PHASE 2] Re-examining UNKNOWN records using source OCR text...")
    reclassified = reclassify_from_source(conn)
    print(f"  Reclassified {reclassified:,} records from source text")

    # Refresh counts
    c.execute("""
        SELECT record_type, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        GROUP BY record_type
    """)
    
    print(f"\n{'=' * 70}")
    print("CLASSIFICATION RESULTS")
    print(f"{'=' * 70}")
    print(f"\n  {'Type':<20} {'Records':>10} {'Volume':>20}")
    print("  " + "─" * 52)
    
    total_tx_vol = 0
    for rtype, cnt, vol in c.fetchall():
        vol = vol or 0
        marker = " ← real money" if rtype == 'TRANSACTION' else ""
        print(f"  {rtype:<20} {cnt:>10,} ${vol:>18,.2f}{marker}")
        if rtype == 'TRANSACTION':
            total_tx_vol = vol

    # Per-bank breakdown
    print(f"\n  {'Bank':<25} {'TXN':>6} {'BAL':>6} {'HOLD':>6} {'SUM':>6} {'UNK':>6} {'TXN Volume':>18}")
    print("  " + "─" * 80)
    
    c.execute("""
        SELECT bank, record_type, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        GROUP BY bank, record_type
        ORDER BY bank
    """)
    
    bank_data = {}
    for bank, rtype, cnt, vol in c.fetchall():
        if bank not in bank_data:
            bank_data[bank] = {}
        bank_data[bank][rtype] = {'count': cnt, 'volume': vol or 0}
    
    for bank in sorted(bank_data.keys(), key=lambda b: -sum(v['count'] for v in bank_data[b].values())):
        data = bank_data[bank]
        txn = data.get('TRANSACTION', {}).get('count', 0)
        bal = data.get('BALANCE', {}).get('count', 0)
        hold = data.get('HOLDING', {}).get('count', 0)
        summ = data.get('SUMMARY', {}).get('count', 0)
        unk = data.get('UNKNOWN', {}).get('count', 0)
        txn_vol = data.get('TRANSACTION', {}).get('volume', 0)
        print(f"  {bank:<25} {txn:>6} {bal:>6} {hold:>6} {summ:>6} {unk:>6} ${txn_vol:>16,.2f}")

    # Show what the workbook should report
    c.execute("""
        SELECT COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
    """)
    txn_count, txn_vol = c.fetchone()
    txn_vol = txn_vol or 0

    c.execute("""
        SELECT COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type IN ('TRANSACTION', 'BALANCE', 'HOLDING', 'SUMMARY')
    """)
    all_count, all_vol = c.fetchone()

    print(f"\n{'=' * 70}")
    print("WORKBOOK NUMBERS")
    print(f"{'=' * 70}")
    print(f"  Transaction records only: {txn_count:,} records, ${txn_vol:,.2f}")
    print(f"  All classified records:   {all_count:,} records")
    print(f"  Volume correction:        ${68_745_222_404.77:,.2f} → ${txn_vol:,.2f}")
    if txn_vol > 0:
        reduction = (1 - txn_vol / 68_745_222_404.77) * 100
        print(f"  Inflation removed:        {reduction:.1f}%")

    # Entity matches by record type
    print(f"\n  Entity Matches (TRANSACTION only):")
    c.execute("""
        SELECT entity_match, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE entity_match IS NOT NULL
        AND record_type = 'TRANSACTION'
        GROUP BY entity_match
        ORDER BY SUM(tx_amount) DESC
        LIMIT 15
    """)
    for entity, cnt, vol in c.fetchall():
        vol = vol or 0
        print(f"    {entity:<30} {cnt:>6} txns  ${vol:>14,.2f}")

    conn.close()
    print(f"\n  Classification complete.")


if __name__ == "__main__":
    main()
