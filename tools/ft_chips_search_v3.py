#!/usr/bin/env python3
"""
FT CHIPS SEARCH v3 — Targeted deep-dive on key hits
"""

import sqlite3
import sys
import time

DB = sys.argv[1] if len(sys.argv) > 1 else "/Users/randall/Desktop/epstein_files.db"

def banner(text):
    print("\n" + "█" * 80)
    print(f"  {text}")
    print("█" * 80)

def section(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

conn = sqlite3.connect(DB)
cur = conn.cursor()

banner("1: EFTA01552348 — $25K CHIPS DEBIT VIA DEUTSCHE BANK")

section("1A: Full extracted text (all pages)")
cur.execute("""
    SELECT page_num, text_content
    FROM extracted_text
    WHERE file_id = 763924
    ORDER BY page_num
""")
for row in cur.fetchall():
    print(f"\n--- Page {row[0]} ---")
    print(row[1][:3000] if row[1] else "(empty)")

section("1B: File metadata")
cur.execute("SELECT * FROM files WHERE id = 763924")
row = cur.fetchone()
cols = [d[0] for d in cur.description]
for c, v in zip(cols, row):
    if v: print(f"  {c}: {v}")

section("1C: All financial_hits from this file")
cur.execute("""
    SELECT amount, category, context FROM financial_hits
    WHERE file_id = 763924
    ORDER BY amount DESC
""")
for row in cur.fetchall():
    print(f"  ${row[0]:,.2f} [{row[1]}] {str(row[2])[:200]}")

banner("2: EFTA00796197 — CHIPS CREDIT VIA BANK")

section("2A: Full extracted text (all pages)")
cur.execute("""
    SELECT page_num, text_content
    FROM extracted_text
    WHERE file_id = 403634
    ORDER BY page_num
""")
for row in cur.fetchall():
    print(f"\n--- Page {row[0]} ---")
    print(row[1][:3000] if row[1] else "(empty)")

section("2B: All financial_hits from this file")
cur.execute("""
    SELECT amount, category, context FROM financial_hits
    WHERE file_id = 403634
    ORDER BY amount DESC
""")
for row in cur.fetchall():
    print(f"  ${row[0]:,.2f} [{row[1]}] {str(row[2])[:200]}")

banner("3: EFTA02415526 — MANDELSON + HSBC EMAIL (DS11)")

section("3A: Full extracted text (all pages)")
cur.execute("""
    SELECT page_num, text_content
    FROM extracted_text
    WHERE file_id = 1158077
    ORDER BY page_num
""")
for row in cur.fetchall():
    print(f"\n--- Page {row[0]} ---")
    print(row[1][:4000] if row[1] else "(empty)")

section("3B: All entities")
cur.execute("""
    SELECT entity_text, entity_type FROM entities
    WHERE file_id = 1158077
    ORDER BY entity_type, entity_text
""")
for row in cur.fetchall():
    print(f"  [{row[1]}] {row[0]}")

banner("4: EFTA00086575 — MANDELSON + AVILA DA SILVA LETTER")

section("4A: Full extracted text (all pages)")
cur.execute("""
    SELECT page_num, text_content
    FROM extracted_text
    WHERE file_id = 18528
    ORDER BY page_num
""")
for row in cur.fetchall():
    print(f"\n--- Page {row[0]} ---")
    print(row[1][:4000] if row[1] else "(empty)")

banner("5: JPMORGAN BANK STATEMENTS 2003-2004")

section("5A: Search for 'Jeffrey E. Epstein and Related Entities' exact phrase")
cur.execute("""
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text_content, MAX(1, INSTR(LOWER(e.text_content), 'jeffrey e. epstein and related') - 40), 300) AS ctx
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text_content) LIKE '%jeffrey e. epstein and related%'
    LIMIT 30
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  [{r[3]}] {r[1]} ({r[2]})")
        print(f"  {r[4]}")
        print()
else:
    print("  (no results)")

section("5B: Search for 'Jeffrey E Epstein' + 'Related' (looser)")
cur.execute("""
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text_content, MAX(1, INSTR(LOWER(e.text_content), 'related') - 60), 200) AS ctx
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text_content) LIKE '%jeffrey e%epstein%'
      AND LOWER(e.text_content) LIKE '%related entit%'
    LIMIT 20
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  [{r[3]}] {r[1]} ({r[2]})")
        print(f"  {r[4]}")
        print()
else:
    print("  (no results)")

section("5C: JPMorgan statements from 2003 era")
cur.execute("""
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text_content, 1, 400) AS start_text
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE f.doc_type = 'financial'
      AND (LOWER(e.text_content) LIKE '%jpmorgan%' OR LOWER(e.text_content) LIKE '%jp morgan%')
      AND e.text_content LIKE '%2003%'
      AND (e.text_content LIKE '%25,000%' OR e.text_content LIKE '%25000%')
    LIMIT 20
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  [{r[3]}] {r[1]} ({r[2]})")
        print(f"  {r[4][:300]}")
        print()
else:
    print("  (no results)")

banner("6: ALL CHIPS TRANSACTIONS IN FINANCIAL_HITS")

section("6A: Every financial_hit with 'chips' in context")
cur.execute("""
    SELECT fh.file_id, f.title, fh.amount, fh.category, fh.context, f.dataset
    FROM financial_hits fh
    JOIN files f ON fh.file_id = f.id
    WHERE LOWER(fh.context) LIKE '%chips%'
    ORDER BY fh.amount DESC
    LIMIT 50
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  [{r[5]}] {r[1]} | ${r[2]:,.2f} [{r[3]}]")
        print(f"  {str(r[4])[:250]}")
        print()
else:
    print("  (no results)")

banner("7: EPSTEIN→REINALDO AVILA EMAIL DEEP DIVE")

section("7A: Key Epstein-Avila emails — full text samples")
avila_emails = [372195, 372199, 372216, 372341, 372393, 372466, 372469, 372472,
                372563, 372565, 372567, 372726, 369148, 369460, 369786, 370020,
                370021, 370469, 181091, 278705]

for fid in avila_emails[:8]:
    cur.execute("""
        SELECT page_num, SUBSTR(text_content, 1, 1500) 
        FROM extracted_text WHERE file_id = ? ORDER BY page_num LIMIT 2
    """, (fid,))
    rows = cur.fetchall()
    if rows:
        cur.execute("SELECT title FROM files WHERE id = ?", (fid,))
        title = cur.fetchone()[0]
        print(f"\n  === {title} (file_id={fid}) ===")
        for r in rows:
            print(f"  Page {r[0]}:")
            print(f"  {r[1]}")

banner("8: MANDELSON FINANCIAL DOCUMENTS — BROADER SEARCH")

section("8A: Files with Mandelson entity AND doc_type = 'financial'")
cur.execute("""
    SELECT DISTINCT f.id, f.title, f.dataset
    FROM files f
    JOIN entities e ON e.file_id = f.id
    WHERE LOWER(e.entity_text) LIKE '%mandelson%'
      AND f.doc_type = 'financial'
    ORDER BY f.dataset, f.id
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  [{r[2]}] {r[1]} (file_id={r[0]})")
else:
    print("  (no results — Mandelson not in any 'financial' doc type)")

section("8B: Mandelson in DS10 JPMorgan statements")
cur.execute("""
    SELECT DISTINCT e.file_id, f.title, f.doc_type
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE f.dataset = '10'
      AND f.doc_type = 'financial'
      AND LOWER(e.text_content) LIKE '%mandelson%'
    LIMIT 20
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  {r[1]} ({r[2]}) file_id={r[0]}")
else:
    print("  (no results)")

section("8C: Any DS10 financial doc with $25,000 CHIPS")
cur.execute("""
    SELECT e.file_id, f.title, 
           SUBSTR(e.text_content, MAX(1, INSTR(LOWER(e.text_content), 'chips') - 100), 300) AS ctx
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE f.dataset = '10'
      AND f.doc_type = 'financial'
      AND LOWER(e.text_content) LIKE '%chips%'
      AND (e.text_content LIKE '%25,000%' OR e.text_content LIKE '%25000%')
    LIMIT 20
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  {r[1]} (file_id={r[0]})")
        print(f"  {r[2]}")
        print()
else:
    print("  (no results)")

section("8D: Any financial doc with $25,000 CHIPS anywhere in corpus")
cur.execute("""
    SELECT e.file_id, f.title, f.dataset, f.doc_type,
           SUBSTR(e.text_content, MAX(1, INSTR(LOWER(e.text_content), 'chips') - 100), 400) AS ctx
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text_content) LIKE '%chips%'
      AND (e.text_content LIKE '%25,000%' OR e.text_content LIKE '%25000%')
      AND f.doc_type IN ('financial', 'bank_statement')
    LIMIT 20
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  [{r[2]}] {r[1]} ({r[3]}) file_id={r[0]}")
        print(f"  {r[4]}")
        print()
else:
    print("  (no results)")

banner("9: DS10 JPMORGAN STATEMENTS — THE MOTHER LODE")
print("  DS10 has 503,271 files. JPMorgan statements from 2003-2004")
print("  are where the FT CHIPS payments would appear.")

section("9A: How many DS10 financial docs exist?")
cur.execute("""
    SELECT doc_type, COUNT(*) as cnt 
    FROM files WHERE dataset = '10' 
    GROUP BY doc_type ORDER BY cnt DESC LIMIT 10
""")
for r in cur.fetchall():
    print(f"  {r[0]}: {r[1]:,}")

section("9B: DS10 financial docs with 'Epstein Interests' (JPM account name)")
cur.execute("""
    SELECT e.file_id, f.title,
           SUBSTR(e.text_content, MAX(1, INSTR(LOWER(e.text_content), 'epstein interests') - 60), 250) AS ctx
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE f.dataset = '10'
      AND LOWER(e.text_content) LIKE '%epstein interests%'
      AND (e.text_content LIKE '%2003%' OR e.text_content LIKE '%2004%')
    LIMIT 20
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  {r[1]} (file_id={r[0]})")
        print(f"  {r[2]}")
        print()
else:
    print("  (no results)")

section("9C: DS10 with 'Epstein Interests' + $25,000")
cur.execute("""
    SELECT e.file_id, f.title,
           SUBSTR(e.text_content, MAX(1, INSTR(e.text_content, '25,000') - 100), 300) AS ctx
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE f.dataset = '10'
      AND LOWER(e.text_content) LIKE '%epstein interests%'
      AND (e.text_content LIKE '%25,000%' OR e.text_content LIKE '%25000%')
    LIMIT 20
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  {r[1]} (file_id={r[0]})")
        print(f"  {r[2]}")
        print()
else:
    print("  (no results)")

print("\n")
banner("DONE — v3 TARGETED DEEP DIVE COMPLETE")
conn.close()
