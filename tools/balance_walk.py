#!/usr/bin/env python3
"""
balance_walk.py
Pull the full June 2004 statement text to settle the bounced payment question.
Peter's theory: Payment 3 (Jun 30) might be the retry of the bounced Payment 2 (Jun 24),
not a separate payment. Balance math settles it.

If $50K net outflow to HSBC/Mandelson across Jun 24-30 → two payments.
If $25K net outflow → one payment attempted twice.

Usage:
    python3 balance_walk.py /path/to/epstein_files.db 2>&1 | tee balance_walk_results.txt
"""

import sqlite3, sys, os, re

DB = sys.argv[1] if len(sys.argv) > 1 else "/Users/randall/Desktop/epstein_files.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=" * 80)
print("  BALANCE WALK — June 2004 Statement")
print("  Question: Two $25K payments or one retried?")
print("=" * 80)

# The June 2004 statement spans multiple EFTA pages.
# Payment 2 is on EFTA01482503 (page 7 of 10)
# Payment 3 is on EFTA01482505 (page 9 of 10)
# We need the full statement — all pages.

# First, find the file_ids
target_bates = [
    "EFTA01482503",  # Payment 2
    "EFTA01482505",  # Payment 3
]

print("\n── RESOLVING TARGET FILES ──")
file_ids = {}
for bates in target_bates:
    row = cur.execute(
        "SELECT id, title, dataset, page_count FROM files WHERE title LIKE ?",
        (f"%{bates}%",)
    ).fetchone()
    if row:
        file_ids[bates] = row[0]
        print(f"  {bates} → file_id {row[0]}, DS{row[2]}, {row[3]} pages")
    else:
        print(f"  {bates} → NOT FOUND")

# Now get ALL pages of these documents
print("\n── FULL TEXT EXTRACTION ──")
for bates in target_bates:
    fid = file_ids.get(bates)
    if not fid:
        continue

    print(f"\n{'█' * 80}")
    print(f"  {bates} (file_id: {fid})")
    print(f"{'█' * 80}")

    pages = cur.execute(
        "SELECT page_num, text_content FROM extracted_text WHERE file_id = ? ORDER BY page_num",
        (fid,)
    ).fetchall()

    for page_num, text in pages:
        print(f"\n{'─' * 60}")
        print(f"  PAGE {page_num}")
        print(f"{'─' * 60}")
        print(text[:5000] if text else "[EMPTY]")

# Now look at adjacent EFTA numbers to get the full statement
# The statement is "May 29 - June 30, 2004" spanning ~10 pages
# EFTA01482497 through EFTA01482510 ish

print(f"\n\n{'█' * 80}")
print(f"  ADJACENT PAGES — Full Statement Context")
print(f"  Looking for pages around EFTA01482497-EFTA01482510")
print(f"{'█' * 80}")

# Find files in the Bates range
adj_rows = cur.execute("""
    SELECT f.id, f.title, f.dataset,
           (SELECT COUNT(*) FROM extracted_text WHERE file_id = f.id) as pages
    FROM files f
    WHERE f.title >= 'EFTA01482497'
      AND f.title <= 'EFTA01482515'
    ORDER BY f.title
""").fetchall()

print(f"\n  Found {len(adj_rows)} files in Bates range:")
for fid, title, ds, pages in adj_rows:
    print(f"    {title} (file_id {fid}, DS{ds}, {pages} pages)")

# Pull text for all adjacent pages
for fid, title, ds, page_ct in adj_rows:
    bates = title.replace(".pdf", "")

    pages = cur.execute(
        "SELECT page_num, text_content FROM extracted_text WHERE file_id = ? ORDER BY page_num",
        (fid,)
    ).fetchall()

    for page_num, text in pages:
        if not text:
            continue

        # only print pages that have financial content
        has_money = bool(re.search(r'\$[\d,]+', text))
        has_balance = bool(re.search(r'(?i)balance|ending|opening|total', text))
        has_mandelson = bool(re.search(r'(?i)mandelson', text))
        has_chips = bool(re.search(r'(?i)chips', text))
        has_hsbc = bool(re.search(r'(?i)hsbc', text))
        has_reversal = bool(re.search(r'(?i)reversal|reverse|returned|bounced', text))

        if any([has_money, has_balance, has_mandelson, has_chips, has_hsbc, has_reversal]):
            print(f"\n{'─' * 60}")
            print(f"  {bates} PAGE {page_num}", end="")
            flags = []
            if has_mandelson: flags.append("MANDELSON")
            if has_chips: flags.append("CHIPS")
            if has_hsbc: flags.append("HSBC")
            if has_reversal: flags.append("REVERSAL")
            if has_balance: flags.append("BALANCE")
            if flags:
                print(f"  *** {' | '.join(flags)} ***")
            else:
                print()
            print(f"{'─' * 60}")
            print(text[:5000])

# ── Now specifically extract all dollar amounts and balance lines ──

print(f"\n\n{'█' * 80}")
print(f"  BALANCE PROGRESSION EXTRACTION")
print(f"  Every dollar amount on the June 24-30 pages")
print(f"{'█' * 80}")

for fid, title, ds, page_ct in adj_rows:
    bates = title.replace(".pdf", "")
    pages = cur.execute(
        "SELECT page_num, text_content FROM extracted_text WHERE file_id = ? ORDER BY page_num",
        (fid,)
    ).fetchall()

    for page_num, text in pages:
        if not text:
            continue

        # look for June 24-30 content specifically
        has_jun24 = bool(re.search(r'Jun\w*\s*24|6/24|06/24', text, re.IGNORECASE))
        has_jun30 = bool(re.search(r'Jun\w*\s*30|6/30|06/30', text, re.IGNORECASE))

        if has_jun24 or has_jun30:
            print(f"\n  {bates} p{page_num}:")
            # extract all lines with dollar amounts
            for line in text.split('\n'):
                if re.search(r'\$[\d,]+\.?\d*', line):
                    line_clean = line.strip()
                    if line_clean:
                        # flag key items
                        tag = ""
                        if re.search(r'(?i)mandelson', line): tag = " ← MANDELSON"
                        elif re.search(r'(?i)chips', line): tag = " ← CHIPS"
                        elif re.search(r'(?i)hsbc', line): tag = " ← HSBC"
                        elif re.search(r'(?i)reversal|reverse', line): tag = " ← REVERSAL"
                        elif re.search(r'(?i)balance|ending|opening', line): tag = " ← BALANCE"
                        elif re.search(r'(?i)book\s*transfer', line): tag = " ← BOOK TRANSFER"
                        print(f"    {line_clean}{tag}")

conn.close()

print(f"\n\n{'=' * 80}")
print("  WHAT TO LOOK FOR:")
print("  1. Opening balance for the June 24 page")
print("  2. Every debit and credit between Jun 24-30")
print("  3. Running balance after each transaction")
print("  4. Specifically: does the balance drop $50K or $25K")
print("     for HSBC/Mandelson transactions?")
print("  5. The reversal credit — does it NET against a")
print("     debit on the same page, or is it standalone?")
print("=" * 80)
