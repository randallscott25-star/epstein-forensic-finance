#!/usr/bin/env python3
"""
FINAL AUDIT — 1,558 REMAINING TRANSACTION RECORDS
Shows everything. Finds any last noise.

Author: Randall Scott Taylor
"""

import sqlite3, re, os
from collections import Counter, defaultdict

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")

# Noise patterns that might still be hiding
NOISE_CHECK = [
    ('balance_word', r'(?i)\bbalance\b'),
    ('total_word', r'(?i)\btotal\b'),
    ('summary_word', r'(?i)\bsummary\b'),
    ('page_of', r'(?i)page\s*\d+\s*of\s*\d+'),
    ('percent', r'\d+\.\d+%'),
    ('account_number', r'(?i)account\s*number'),
    ('statement_period', r'(?i)statement\s*period'),
    ('net_cash', r'(?i)net\s+cash'),
    ('value_of', r'(?i)value\s+of\s+(your|the)'),
    ('fdic', r'(?i)fdic'),
    ('yield_apy', r'(?i)(yield|apy|apr)\b'),
    ('unrealized', r'(?i)unrealized'),
    ('cost_basis', r'(?i)cost\s+basis'),
    ('portfolio', r'(?i)portfolio'),
    ('closing_opening', r'(?i)(closing|opening|ending|beginning)\b'),
    ('accrued', r'(?i)accrued'),
    ('annualized', r'(?i)annual(ized)?\b'),
    ('maturity', r'(?i)maturity'),
    ('estimated', r'(?i)estimated'),
    ('market_value', r'(?i)market\s+val'),
    ('par_face', r'(?i)(par|face)\s+(value|amount)'),
    ('cusip_isin', r'(?i)(cusip|isin|sedol)\b'),
    ('confidential', r'(?i)confidential'),
    ('exhibit', r'(?i)exhibit\s+[a-z]'),
    ('corrected_tag', r'\[CORRECTED'),
    ('dividend_interest_bare', r'(?i)^dividend.*interest\s*$'),
    ('interest_earned_bare', r'(?i)^interest\s+earned\s*$'),
    ('funds_deposited_bare', r'(?i)^funds?\s+deposited\s*$'),
    ('deposits_withdrawals', r'(?i)deposits?\s+and\s+(other\s+)?(credits?|withdrawals?)'),
    ('checks_paid_bare', r'(?i)^checks?\s+paid\s*$'),
    ('empty_after_trim', r'^\s*$'),
]


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("FINAL AUDIT — ALL 1,558 TRANSACTION RECORDS")
    print("=" * 70)

    c.execute("""
        SELECT id, bank, bates, tx_amount, tx_date, description, source_doc_type
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        ORDER BY bank, tx_amount DESC
    """)
    all_txns = c.fetchall()
    print(f"[IN] {len(all_txns):,} records, ${sum(r[3] or 0 for r in all_txns):,.2f}")

    # ── NOISE SCAN ──
    print(f"\n{'=' * 70}")
    print("NOISE PATTERN SCAN")
    print(f"{'=' * 70}")

    flagged = {}  # id -> (label, amount)
    pattern_hits = Counter()
    pattern_vol = defaultdict(float)

    for rec_id, bank, bates, amount, date, desc, stype in all_txns:
        if not desc:
            # No description at all
            if rec_id not in flagged:
                flagged[rec_id] = ('NO_DESC', amount or 0)
                pattern_hits['NO_DESC'] += 1
                pattern_vol['NO_DESC'] += (amount or 0)
            continue

        desc_clean = desc.strip()

        for label, pat in NOISE_CHECK:
            if re.search(pat, desc_clean):
                if rec_id not in flagged:
                    flagged[rec_id] = (label, amount or 0)
                pattern_hits[label] += 1
                pattern_vol[label] += (amount or 0)

    print(f"\n  {'Pattern':<30} {'Hits':>6} {'Volume':>12}")
    print("  " + "─" * 50)
    for label, cnt in pattern_hits.most_common():
        print(f"  {label:<30} {cnt:>6} ${pattern_vol[label]:>10,.2f}")
    print(f"\n  Total uniquely flagged: {len(flagged)} records, ${sum(v[1] for v in flagged.values()):,.2f}")

    # ── SHOW FLAGGED RECORDS ──
    print(f"\n{'=' * 70}")
    print("FLAGGED RECORDS (potential remaining noise)")
    print(f"{'=' * 70}")

    for rec_id, (label, amount) in sorted(flagged.items(), key=lambda x: -x[1][1])[:50]:
        c.execute("SELECT bank, tx_date, description FROM bank_statement_transactions WHERE id = ?", (rec_id,))
        row = c.fetchone()
        if row:
            bank, date, desc = row
            desc_clean = (desc or '').replace('\n', ' ')[:70]
            print(f"  #{rec_id:<6} {label:<25} {bank:<14} ${amount:>8,.2f} {date or 'no-date':<12} {desc_clean}")

    # ── PER-BANK TOP RECORDS ──
    print(f"\n{'=' * 70}")
    print("PER-BANK TOP 10 RECORDS")
    print(f"{'=' * 70}")

    by_bank = defaultdict(list)
    for r in all_txns:
        by_bank[r[1]].append(r)

    for bank in sorted(by_bank.keys(), key=lambda b: -sum(r[3] or 0 for r in by_bank[b])):
        recs = by_bank[bank]
        vol = sum(r[3] or 0 for r in recs)
        if len(recs) == 0:
            continue
        print(f"\n  {bank} — {len(recs)} records, ${vol:,.2f}")
        for rec_id, bk, bates, amount, date, desc, stype in recs[:10]:
            desc_clean = (desc or '').replace('\n', ' ')[:65]
            flag = " ⚠" if rec_id in flagged else ""
            print(f"    #{rec_id:<6} ${amount:>8,.2f} {date or 'no-date':<12} {desc_clean}{flag}")

    # ── DATE QUALITY ──
    print(f"\n{'=' * 70}")
    print("DATE QUALITY")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT tx_date, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NOT NULL
        GROUP BY tx_date
        ORDER BY COUNT(*) DESC
        LIMIT 20
    """)
    print(f"\n  Top 20 dates by record count (suspicious if too concentrated):")
    for date, cnt, vol in c.fetchall():
        flag = " ⚠ CONCENTRATED" if cnt > 20 else ""
        print(f"    {date}  {cnt:>4} records  ${vol or 0:>10,.2f}{flag}")

    # Year-only dates (Jan 1)
    c.execute("""
        SELECT COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date LIKE '%-01-01'
    """)
    jan1_cnt, jan1_vol = c.fetchone()
    print(f"\n  Jan-1 dates (year-only recoveries): {jan1_cnt or 0} records, ${jan1_vol or 0:,.2f}")

    # Year distribution
    c.execute("""
        SELECT SUBSTR(tx_date, 1, 4) as yr, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NOT NULL
        GROUP BY yr ORDER BY yr
    """)
    print(f"\n  Year distribution:")
    for yr, cnt, vol in c.fetchall():
        print(f"    {yr}  {cnt:>5} records  ${vol or 0:>10,.2f}")

    # ── AMOUNT DISTRIBUTION ──
    print(f"\n{'=' * 70}")
    print("AMOUNT DISTRIBUTION")
    print(f"{'=' * 70}")

    amounts = [r[3] or 0 for r in all_txns]
    for label, lo, hi in [
        ('$100K+', 100000, 999999999),
        ('$10K-100K', 10000, 100000),
        ('$1K-10K', 1000, 10000),
        ('$500-1K', 500, 1000),
        ('$100-500', 100, 500),
        ('$50-100', 50, 100),
        ('$10-50', 10, 50),
        ('$1-10', 1, 10),
        ('<$1', 0, 1),
    ]:
        bucket = [a for a in amounts if lo <= a < hi]
        bvol = sum(bucket)
        pct = bvol / sum(amounts) * 100 if sum(amounts) > 0 else 0
        print(f"    {label:<12} {len(bucket):>6} recs  ${bvol:>10,.2f}  ({pct:.1f}%)")

    # ── CLEAN vs FLAGGED SUMMARY ──
    clean_ids = set(r[0] for r in all_txns) - set(flagged.keys())
    clean_vol = sum(r[3] or 0 for r in all_txns if r[0] in clean_ids)
    flagged_vol = sum(v[1] for v in flagged.values())

    print(f"\n{'=' * 70}")
    print("CLEAN vs FLAGGED")
    print(f"{'=' * 70}")
    print(f"  Clean records:   {len(clean_ids):>6}  ${clean_vol:>12,.2f}")
    print(f"  Flagged records: {len(flagged):>6}  ${flagged_vol:>12,.2f}")
    print(f"  Total:           {len(all_txns):>6}  ${sum(amounts):>12,.2f}")

    conn.close()
    print(f"\n  Audit complete. Review flagged records above.")


if __name__ == "__main__":
    main()
