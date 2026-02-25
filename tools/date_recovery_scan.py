#!/usr/bin/env python3
"""
DATE RECOVERY SCAN
Before killing undated records, scan for dates in:
1. Description field (may have "Oct 08 Fedwire" or "03/15/2005")
2. Source OCR text (surrounding context on the page)

If a date is found, update tx_date and keep as TRANSACTION.
If no date found anywhere, it's not a real transaction.

Author: Randall Scott Taylor
"""

import sqlite3, re, os
from collections import Counter, defaultdict

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")

# Date patterns — ordered from most specific to least
DATE_PATTERNS = [
    # MM/DD/YYYY or MM/DD/YY
    (r'(\d{1,2})/(\d{1,2})/(\d{4})', 'MDY4'),
    (r'(\d{1,2})/(\d{1,2})/(\d{2})\b', 'MDY2'),

    # MM-DD-YYYY or MM-DD-YY
    (r'(\d{1,2})-(\d{1,2})-(\d{4})', 'MDY4_DASH'),
    (r'(\d{1,2})-(\d{1,2})-(\d{2})\b', 'MDY2_DASH'),

    # YYYY-MM-DD (ISO)
    (r'(\d{4})-(\d{2})-(\d{2})', 'ISO'),

    # Month name patterns: "Oct 08", "October 08", "Oct 8, 2005"
    (r'(?i)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})(?:,?\s+(\d{4}))?', 'MONTH_NAME'),

    # "08-Oct" or "08 Oct 2005"
    (r'(?i)(\d{1,2})[\s\-](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?(?:[\s\-,]+(\d{4}))?', 'DAY_MONTH'),
]

MONTH_MAP = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}


def parse_date_match(match, pattern_type, context_year=None):
    """Convert a regex match into YYYY-MM-DD string."""
    try:
        if pattern_type == 'MDY4':
            m, d, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
        elif pattern_type == 'MDY2':
            m, d, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
            y = 2000 + y if y < 50 else 1900 + y
        elif pattern_type == 'MDY4_DASH':
            m, d, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
        elif pattern_type == 'MDY2_DASH':
            m, d, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
            y = 2000 + y if y < 50 else 1900 + y
        elif pattern_type == 'ISO':
            y, m, d = int(match.group(1)), int(match.group(2)), int(match.group(3))
        elif pattern_type == 'MONTH_NAME':
            month_str = match.group(1).lower()[:3]
            m = MONTH_MAP.get(month_str, 0)
            d = int(match.group(2))
            y_str = match.group(3)
            y = int(y_str) if y_str else context_year
        elif pattern_type == 'DAY_MONTH':
            d = int(match.group(1))
            month_str = match.group(2).lower()[:3]
            m = MONTH_MAP.get(month_str, 0)
            y_str = match.group(3)
            y = int(y_str) if y_str else context_year
        else:
            return None

        if not y or not m:
            return None

        # Validate
        if not (1990 <= y <= 2025 and 1 <= m <= 12 and 1 <= d <= 31):
            return None

        return f"{y:04d}-{m:02d}-{d:02d}"
    except:
        return None


def extract_year_from_page(text):
    """Get year from statement period on the page."""
    patterns = [
        r'(?i)(?:statement\s+period|for\s+the\s+period|period\s+ending)[:\s]*.*?(\d{4})',
        r'(?i)(\d{4})\s*[-\xe2\x80\x93]\s*\d{4}',
    ]
    for pat in patterns:
        m = re.search(pat, text[:500])
        if m:
            yr = int(m.group(1))
            if 1990 <= yr <= 2025:
                return yr

    # Fall back: find any 4-digit year in first 500 chars
    years = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', text[:500])
    if years:
        return int(years[0])
    return None


def find_date_in_text(text, context_year=None):
    """Search text for any date pattern. Return first valid date found."""
    if not text:
        return None

    for pat_str, pat_type in DATE_PATTERNS:
        for match in re.finditer(pat_str, text):
            date = parse_date_match(match, pat_type, context_year)
            if date:
                return date
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("DATE RECOVERY SCAN")
    print("=" * 70)

    # Get all undated TRANSACTION records
    c.execute("""
        SELECT id, bank, bates, tx_amount, description, source_doc_type
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NULL
        ORDER BY tx_amount DESC
    """)
    undated = c.fetchall()

    # Get dated records for comparison
    c.execute("""
        SELECT COUNT(*), SUM(tx_amount) FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND tx_date IS NOT NULL
    """)
    dated_cnt, dated_vol = c.fetchone()

    print(f"[IN] {len(undated):,} undated TRANSACTION records (${sum(r[3] or 0 for r in undated):,.2f})")
    print(f"[IN] {dated_cnt:,} already-dated TRANSACTION records (${dated_vol or 0:,.2f})")

    # Cache source text by bates
    bates_text_cache = {}
    bates_year_cache = {}

    results = {
        'desc_date': [],      # Date found in description
        'source_date': [],    # Date found in source OCR
        'year_only': [],      # Only year found (from statement period)
        'no_date': [],        # No date found anywhere
    }

    for i, (rec_id, bank, bates, amount, desc, stype) in enumerate(undated):
        # Phase 1: Check description for date
        desc_date = find_date_in_text(desc) if desc else None
        if desc_date:
            results['desc_date'].append((rec_id, bank, bates, amount, desc, desc_date))
            continue

        # Phase 2: Check source OCR text
        if bates and bates not in bates_text_cache:
            c.execute("""
                SELECT et.text_content FROM extracted_text et
                JOIN files f ON f.id = et.file_id
                WHERE REPLACE(f.title, '.pdf', '') = ?
                ORDER BY et.page_num LIMIT 1
            """, (bates,))
            row = c.fetchone()
            bates_text_cache[bates] = row[0] if row and row[0] else ''
            bates_year_cache[bates] = extract_year_from_page(bates_text_cache[bates])

        source_text = bates_text_cache.get(bates, '')
        context_year = bates_year_cache.get(bates)

        # Search source for date near the dollar amount
        source_date = None
        if source_text and amount:
            # Try to find dollar amount in source and look nearby for dates
            amt_patterns = [
                f"{amount:,.2f}",
                f"{amount:,.0f}",
                f"{amount:.2f}",
            ]
            for amt_str in amt_patterns:
                amt_pos = source_text.find(amt_str[:min(len(amt_str), 10)])
                if amt_pos >= 0:
                    window_start = max(0, amt_pos - 300)
                    window_end = min(len(source_text), amt_pos + 300)
                    window = source_text[window_start:window_end]
                    source_date = find_date_in_text(window, context_year)
                    if source_date:
                        break

            # Broader search if amount-proximity failed
            if not source_date:
                source_date = find_date_in_text(source_text[:3000], context_year)

        if source_date:
            results['source_date'].append((rec_id, bank, bates, amount, desc, source_date))
        elif context_year:
            results['year_only'].append((rec_id, bank, bates, amount, desc, context_year))
        else:
            results['no_date'].append((rec_id, bank, bates, amount, desc))

        if (i + 1) % 500 == 0:
            print(f"  Scanned {i+1:,}/{len(undated):,}...")

    # ── REPORT ──
    print(f"\n{'=' * 70}")
    print("DATE RECOVERY RESULTS")
    print(f"{'=' * 70}")

    desc_vol = sum(r[3] or 0 for r in results['desc_date'])
    src_vol = sum(r[3] or 0 for r in results['source_date'])
    year_vol = sum(r[3] or 0 for r in results['year_only'])
    nodate_vol = sum(r[3] or 0 for r in results['no_date'])

    print(f"\n  {'Recovery Source':<35} {'Records':>8} {'Volume':>14}")
    print("  " + "─" * 60)
    print(f"  Date found in description          {len(results['desc_date']):>8,} ${desc_vol:>12,.2f}")
    print(f"  Date found in source OCR           {len(results['source_date']):>8,} ${src_vol:>12,.2f}")
    print(f"  Year only (statement period)       {len(results['year_only']):>8,} ${year_vol:>12,.2f}")
    print(f"  NO DATE FOUND ANYWHERE             {len(results['no_date']):>8,} ${nodate_vol:>12,.2f}")
    print(f"  " + "─" * 60)
    total_recovered = len(results['desc_date']) + len(results['source_date'])
    total_rec_vol = desc_vol + src_vol
    print(f"  Total with specific dates          {total_recovered:>8,} ${total_rec_vol:>12,.2f}")

    # Show samples
    for label, recs in [('DESCRIPTION DATE', results['desc_date']),
                         ('SOURCE OCR DATE', results['source_date'])]:
        if not recs:
            continue
        print(f"\n  Sample {label} recoveries (top 15 by amount):")
        for item in sorted(recs, key=lambda r: -(r[3] or 0))[:15]:
            rec_id, bank, bates, amount, desc, date = item
            desc_clean = (desc or '').replace('\n', ' ')[:55]
            print(f"    #{rec_id:<6} {bank:<14} ${amount:>8,.2f} -> {date}  {desc_clean}")

    print(f"\n  Sample YEAR ONLY (top 10 by amount):")
    for item in sorted(results['year_only'], key=lambda r: -(r[3] or 0))[:10]:
        rec_id, bank, bates, amount, desc, year = item
        desc_clean = (desc or '').replace('\n', ' ')[:55]
        print(f"    #{rec_id:<6} {bank:<14} ${amount:>8,.2f} -> year={year}  {desc_clean}")

    print(f"\n  Sample TRULY DATELESS (top 15 by amount):")
    for item in sorted(results['no_date'], key=lambda r: -(r[3] or 0))[:15]:
        rec_id, bank, bates, amount, desc = item
        desc_clean = (desc or '').replace('\n', ' ')[:60]
        print(f"    #{rec_id:<6} {bank:<14} ${amount:>8,.2f}  {desc_clean}")

    # Per-bank breakdown
    print(f"\n  Recovery by bank:")
    bank_stats = defaultdict(lambda: {'desc': 0, 'source': 0, 'year': 0, 'none': 0})
    for r in results['desc_date']:
        bank_stats[r[1]]['desc'] += 1
    for r in results['source_date']:
        bank_stats[r[1]]['source'] += 1
    for r in results['year_only']:
        bank_stats[r[1]]['year'] += 1
    for r in results['no_date']:
        bank_stats[r[1]]['none'] += 1

    print(f"    {'Bank':<22} {'Desc':>6} {'Source':>6} {'Year':>6} {'None':>6}")
    print("    " + "─" * 50)
    for bank in sorted(bank_stats.keys()):
        s = bank_stats[bank]
        print(f"    {bank:<22} {s['desc']:>6} {s['source']:>6} {s['year']:>6} {s['none']:>6}")

    # ── APPLY ──
    print(f"\n{'=' * 70}")
    print("APPLYING RECOVERIES")
    print(f"{'=' * 70}")

    # Update specific dates
    recovered = 0
    for rec_id, bank, bates, amount, desc, date in results['desc_date']:
        c.execute("UPDATE bank_statement_transactions SET tx_date = ? WHERE id = ?", (date, rec_id))
        recovered += 1
    for rec_id, bank, bates, amount, desc, date in results['source_date']:
        c.execute("UPDATE bank_statement_transactions SET tx_date = ? WHERE id = ?", (date, rec_id))
        recovered += 1
    print(f"  Specific dates recovered: {recovered:,} records (${total_rec_vol:,.2f})")

    # Year-only: set to Jan 1 of that year
    year_set = 0
    for rec_id, bank, bates, amount, desc, year in results['year_only']:
        c.execute("UPDATE bank_statement_transactions SET tx_date = ? WHERE id = ?",
                 (f"{year}-01-01", rec_id))
        year_set += 1
    print(f"  Year-only dates set: {year_set:,} records (${year_vol:,.2f})")

    # Kill truly dateless
    killed = 0
    killed_vol = 0
    for rec_id, bank, bates, amount, desc in results['no_date']:
        c.execute("UPDATE bank_statement_transactions SET record_type = 'NO_DATE_ANYWHERE' WHERE id = ?", (rec_id,))
        killed += 1
        killed_vol += (amount or 0)
    print(f"  Truly dateless killed: {killed:,} records (${killed_vol:,.2f})")

    conn.commit()

    # ── FINAL STATE ──
    print(f"\n{'=' * 70}")
    print("FINAL STATE")
    print(f"{'=' * 70}")

    c.execute("SELECT COUNT(*), SUM(tx_amount) FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'")
    final_cnt, final_vol = c.fetchone()
    final_vol = final_vol or 0

    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions WHERE record_type = 'TRANSACTION'
        GROUP BY bank ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  TRANSACTION: {final_cnt:,} records, ${final_vol:,.2f}")
    print(f"\n  {'Bank':<22} {'Recs':>6} {'Volume':>14}")
    print("  " + "─" * 44)
    for bank, cnt, vol in c.fetchall():
        print(f"  {bank:<22} {cnt:>6,} ${vol or 0:>12,.2f}")

    # Progression
    print(f"\n  Inflation progression:")
    print(f"  Raw:            $68,745,222,404.77  (24,563)")
    print(f"  After cleanup:  ${final_vol:>18,.2f}  ({final_cnt:,})")
    reduction = (1 - final_vol / 68_745_222_404.77) * 100
    print(f"  Removed:        {reduction:.6f}%")

    conn.close()
    print(f"\n  Date recovery complete.")


if __name__ == "__main__":
    main()
