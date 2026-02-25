#!/usr/bin/env python3
"""
Pull everything from the actual bank statements containing the three CHIPS payments.
Full text, every page, plus adjacent EFTA pages (consecutive statement pages).
Who else is on these statements? What's redacted? What's around the Mandelson lines?
"""

import sqlite3, sys

DB = sys.argv[1] if len(sys.argv) > 1 else "/Users/randall/Desktop/epstein_files.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

# The three payment documents + their duplicates
targets = {
    "PAYMENT 1 — $25K BARCLAYS MAY 2003": {
        "primary": [1487808, 1487811],  # duplicate statements
        "context_range": range(1487805, 1487815),  # surrounding pages
    },
    "PAYMENT 2 — $25K HSBC JUN 24 2004": {
        "primary": [1482503],
        "context_range": range(1482498, 1482510),
    },
    "PAYMENT 3 — $25K HSBC JUN 30 2004": {
        "primary": [1482505],
        "context_range": range(1482498, 1482510),  # overlaps with payment 2 — same statement period
    },
}

divider = "█" * 80

for label, info in targets.items():
    print(f"\n{divider}")
    print(f"  {label}")
    print(f"{divider}")

    # Full text from primary documents — every page
    for serial in info["primary"]:
        bates = f"EFTA{serial:08d}.pdf"
        cur.execute("SELECT id, page_count, doc_type, doc_date_earliest, doc_date_latest FROM files WHERE title = ?", (bates,))
        row = cur.fetchone()
        if not row:
            print(f"\n  {bates}: NOT FOUND")
            continue

        fid, pages, dtype, d1, d2 = row
        print(f"\n{'='*70}")
        print(f"  {bates}  |  {dtype}  |  {d1} to {d2}  |  {pages} pages")
        print(f"{'='*70}")

        cur.execute("SELECT page_num, text_content FROM extracted_text WHERE file_id = ? ORDER BY page_num", (fid,))
        for pnum, txt in cur.fetchall():
            print(f"\n--- Page {pnum} ---")
            print(txt)

        # All entities
        cur.execute("SELECT entity_text, entity_type, COUNT(*) FROM entities WHERE file_id = ? GROUP BY entity_text, entity_type ORDER BY COUNT(*) DESC", (fid,))
        ents = cur.fetchall()
        if ents:
            print(f"\n  ENTITIES ({len(ents)}):")
            for e, t, c in ents:
                print(f"    {e} [{t}] x{c}")

        # All financial hits
        cur.execute("SELECT amount, category, context FROM financial_hits WHERE file_id = ? ORDER BY amount DESC", (fid,))
        hits = cur.fetchall()
        if hits:
            print(f"\n  FINANCIAL HITS ({len(hits)}):")
            for amt, cat, ctx in hits:
                print(f"    ${amt:,.2f} [{cat}] {ctx[:150]}")

    # Now pull the surrounding EFTA pages for context
    print(f"\n{'='*70}")
    print(f"  SURROUNDING PAGES — EFTA{min(info['context_range']):08d} to EFTA{max(info['context_range']):08d}")
    print(f"{'='*70}")

    serials = list(info["context_range"])
    placeholders = ",".join([f"'EFTA{s:08d}.pdf'" for s in serials])

    cur.execute(f"""
        SELECT f.title, f.id, f.page_count, f.doc_type
        FROM files f
        WHERE f.title IN ({placeholders})
        ORDER BY f.title
    """)
    neighbors = cur.fetchall()

    for title, fid, pages, dtype in neighbors:
        is_primary = any(f"EFTA{s:08d}.pdf" == title for s in info["primary"])
        marker = " ◄◄◄ PRIMARY" if is_primary else ""
        print(f"\n  {title} [{dtype}, {pages}p]{marker}")

        # Just first page text for context pages (full text already shown for primaries)
        if not is_primary:
            cur.execute("SELECT page_num, text_content FROM extracted_text WHERE file_id = ? ORDER BY page_num", (fid,))
            for pnum, txt in cur.fetchall():
                print(f"    --- Page {pnum} ---")
                # Show full text but cap at 2000 chars per page for context pages
                print(f"    {txt[:2000]}")

            cur.execute("SELECT entity_text, entity_type FROM entities WHERE file_id = ? AND entity_type = 'PERSON' GROUP BY entity_text", (fid,))
            persons = cur.fetchall()
            if persons:
                print(f"    PERSONS: {', '.join(p[0] for p in persons)}")

            cur.execute("SELECT amount, category, context FROM financial_hits WHERE file_id = ? ORDER BY amount DESC LIMIT 5", (fid,))
            fhits = cur.fetchall()
            if fhits:
                for amt, cat, ctx in fhits:
                    print(f"    ${amt:,.2f} [{cat}] {ctx[:120]}")

# Also check: are there OTHER CHIPS debits to HSBC on these same statements?
print(f"\n\n{divider}")
print(f"  BONUS: ALL CHIPS DEBITS TO HSBC ACROSS ENTIRE CORPUS")
print(f"{divider}")

cur.execute("""
    SELECT f.title, fh.amount, fh.context, f.dataset, f.doc_date_earliest
    FROM financial_hits fh
    JOIN files f ON fh.file_id = f.id
    WHERE LOWER(fh.context) LIKE '%chips%'
      AND LOWER(fh.context) LIKE '%hsbc%'
    ORDER BY f.doc_date_earliest, f.title
""")
for title, amt, ctx, ds, dt in cur.fetchall():
    print(f"  [{ds}] {title} | ${amt:,.2f} | {dt} | {ctx[:200]}")

# And all CHIPS debits where beneficiary is a PERSON (not FX or corporate)
print(f"\n\n{divider}")
print(f"  BONUS: CHIPS DEBITS TO NAMED INDIVIDUALS (not corporate/FX)")
print(f"{divider}")

cur.execute("""
    SELECT f.title, fh.amount, fh.context, f.dataset, f.doc_date_earliest
    FROM financial_hits fh
    JOIN files f ON fh.file_id = f.id
    WHERE LOWER(fh.context) LIKE '%chips debit%'
      AND (LOWER(fh.context) LIKE '%ben:%' OR LOWER(fh.context) LIKE '%nc: %')
      AND LOWER(fh.context) NOT LIKE '%fx usd%'
      AND LOWER(fh.context) NOT LIKE '%fx operations%'
      AND LOWER(fh.context) NOT LIKE '%incoming%'
    ORDER BY fh.amount DESC
    LIMIT 50
""")
for title, amt, ctx, ds, dt in cur.fetchall():
    # try to extract the name
    ctx_lower = ctx.lower()
    name = ""
    for prefix in ["ben: ", "nc: "]:
        idx = ctx_lower.find(prefix)
        if idx >= 0:
            chunk = ctx[idx+len(prefix):idx+len(prefix)+60].split("\n")[0].split("SSN")[0].split("REF")[0].strip()
            if chunk and name == "":
                name = chunk
    print(f"  ${amt:>12,.2f} | {name[:40]:<40} | {title} | DS{ds} | {dt}")

conn.close()
print(f"\n{'='*70}")
print("  DONE")
print(f"{'='*70}")
