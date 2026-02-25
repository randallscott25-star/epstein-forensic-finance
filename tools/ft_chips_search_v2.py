#!/usr/bin/env python3
"""
FT CHIPS SEARCH v2 — Schema-aware
First discovers actual column names, then runs corrected queries.
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

def run(cur, label, sql, params=None):
    t0 = time.time()
    try:
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        elapsed = time.time() - t0
        if not rows:
            print(f"  [{label}] (no results) [{elapsed:.1f}s]")
            return rows
        print(f"  [{label}] {len(rows)} rows [{elapsed:.1f}s]")
        # Print header
        hdr = " | ".join(f"{c:<40}" for c in cols[:6])
        print(f"  {hdr}")
        print(f"  {'-' * min(250, 42 * min(len(cols), 6))}")
        for row in rows[:50]:
            vals = []
            for v in list(row)[:6]:
                s = str(v) if v is not None else "NULL"
                if len(s) > 40:
                    s = s[:37] + "..."
                vals.append(f"{s:<40}")
            print(f"  {' | '.join(vals)}")
        if len(rows) > 50:
            print(f"  ... ({len(rows) - 50} more rows)")
        return rows
    except Exception as e:
        print(f"  [{label}] ERROR: {e}")
        return []

conn = sqlite3.connect(DB)
cur = conn.cursor()

banner("SCHEMA DISCOVERY — Tables that had errors")

for tbl in ['extracted_text', 'financial_hits', 'fund_flows', 'fund_flows_audited',
            'verified_wires', 'files', 'poi_rankings', 'redaction_summary',
            'financial_redactions', 'dates_found']:
    cur.execute(f"PRAGMA table_info({tbl})")
    cols = cur.fetchall()
    if cols:
        col_names = [c[1] for c in cols]
        print(f"\n  {tbl}: {', '.join(col_names)}")
    else:
        print(f"\n  {tbl}: TABLE NOT FOUND")

banner("PART 1: EXTRACTED TEXT — MANDELSON (using correct columns)")

# Figure out extracted_text columns
cur.execute("PRAGMA table_info(extracted_text)")
et_cols = [c[1] for c in cur.fetchall()]
print(f"  extracted_text columns: {et_cols}")

# Find the text content column
text_col = None
for candidate in ['content', 'extracted_text', 'text_content', 'raw_text', 'ocr_text', 'page_text']:
    if candidate in et_cols:
        text_col = candidate
        break
if not text_col:
    # Try the longest-name column that isn't file_id or page
    for c in et_cols:
        if c not in ('file_id', 'page', 'page_number', 'id', 'rowid'):
            text_col = c
            break

print(f"  Using text column: '{text_col}'")

if text_col:
    section("1A: Mandelson in extracted_text")
    run(cur, "1A", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), 'mandelson') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE LOWER(e.{text_col}) LIKE '%mandelson%'
        ORDER BY f.dataset, f.id
        LIMIT 50
    """)

    section("1B: 'Reinaldo' or 'Avila da Silva' in extracted_text")
    run(cur, "1B", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, MAX(1, 
                   CASE WHEN INSTR(LOWER(e.{text_col}), 'reinaldo') > 0 
                        THEN INSTR(LOWER(e.{text_col}), 'reinaldo')
                        ELSE INSTR(LOWER(e.{text_col}), 'avila da silva')
                   END - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE LOWER(e.{text_col}) LIKE '%reinaldo%'
           OR LOWER(e.{text_col}) LIKE '%avila da silva%'
        ORDER BY f.dataset, f.id
        LIMIT 50
    """)

    section("1C: CHIPS in extracted_text (financial context)")
    run(cur, "1C", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, MAX(1, INSTR(UPPER(e.{text_col}), 'CHIPS') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE (UPPER(e.{text_col}) LIKE '% CHIPS %'
               OR UPPER(e.{text_col}) LIKE '%CHIPS/%'
               OR UPPER(e.{text_col}) LIKE '%CHIPS PAYMENT%'
               OR UPPER(e.{text_col}) LIKE '%CHIPS NUMBER%'
               OR UPPER(e.{text_col}) LIKE '%CHIPS TRANSFER%'
               OR UPPER(e.{text_col}) LIKE '%CHIPS ID%'
               OR UPPER(e.{text_col}) LIKE '%CHIPS SEQUENCE%')
        ORDER BY f.dataset, f.id
        LIMIT 50
    """)

    section("1D: 'Loans and Exchanges' in extracted_text")
    run(cur, "1D", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), 'loans and exchanges') - 60), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE LOWER(e.{text_col}) LIKE '%loans and exchanges%'
        ORDER BY f.dataset, f.id
        LIMIT 30
    """)

    section("1E: Barclays in extracted_text (count + samples)")
    run(cur, "1E-count", f"""
        SELECT COUNT(*) AS pages_with_barclays
        FROM extracted_text WHERE LOWER({text_col}) LIKE '%barclays%'
    """)
    run(cur, "1E-sample", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), 'barclays') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE LOWER(e.{text_col}) LIKE '%barclays%'
        ORDER BY f.dataset, f.id
        LIMIT 25
    """)

    section("1F: HSBC in extracted_text (count + samples)")
    run(cur, "1F-count", f"""
        SELECT COUNT(*) AS pages_with_hsbc
        FROM extracted_text WHERE LOWER({text_col}) LIKE '%hsbc%'
    """)
    run(cur, "1F-sample", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), 'hsbc') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE LOWER(e.{text_col}) LIKE '%hsbc%'
        ORDER BY f.dataset, f.id
        LIMIT 25
    """)

    section("1G: $25,000 + (Barclays OR HSBC OR Mandelson OR JPMorgan) in same page")
    run(cur, "1G", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), '25,000') - 100), 300) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE (e.{text_col} LIKE '%25,000%' OR e.{text_col} LIKE '%25000%')
          AND (LOWER(e.{text_col}) LIKE '%barclays%'
               OR LOWER(e.{text_col}) LIKE '%hsbc%'
               OR LOWER(e.{text_col}) LIKE '%mandelson%'
               OR LOWER(e.{text_col}) LIKE '%avila%'
               OR LOWER(e.{text_col}) LIKE '%chips%')
        LIMIT 30
    """)

    section("1H: 'best pal' or 'chief life adviser' in extracted_text")
    run(cur, "1H", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, 1, 400) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE LOWER(e.{text_col}) LIKE '%best pal%'
           OR LOWER(e.{text_col}) LIKE '%chief life adviser%'
           OR LOWER(e.{text_col}) LIKE '%chief life advisor%'
        ORDER BY f.dataset, f.id
        LIMIT 20
    """)

    section("1I: 'Related Entities' + 2003 or 2004 in extracted_text")
    run(cur, "1I", f"""
        SELECT e.file_id, f.title, f.doc_type, f.dataset,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), 'related entities') - 60), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE LOWER(e.{text_col}) LIKE '%related entities%'
          AND (e.{text_col} LIKE '%2003%' OR e.{text_col} LIKE '%2004%')
        LIMIT 30
    """)

banner("PART 2: FINANCIAL_HITS — CORRECTED")

cur.execute("PRAGMA table_info(financial_hits)")
fh_cols = [c[1] for c in cur.fetchall()]
print(f"  financial_hits columns: {fh_cols}")

# Find the snippet/context column
snippet_col = None
for candidate in ['context_snippet', 'snippet', 'context', 'raw_context', 'surrounding_text']:
    if candidate in fh_cols:
        snippet_col = candidate
        break
if not snippet_col:
    for c in fh_cols:
        if 'context' in c.lower() or 'snippet' in c.lower() or 'text' in c.lower():
            snippet_col = c
            break

print(f"  Using snippet column: '{snippet_col}'")

if snippet_col:
    section("2A: $25,000 hits with Mandelson/Barclays/HSBC context")
    run(cur, "2A", f"""
        SELECT fh.file_id, f.title, fh.amount, fh.category,
               SUBSTR(fh.{snippet_col}, 1, 150) AS ctx, f.dataset
        FROM financial_hits fh
        JOIN files f ON fh.file_id = f.id
        WHERE fh.amount BETWEEN 24000 AND 26000
          AND (LOWER(fh.{snippet_col}) LIKE '%mandelson%'
               OR LOWER(fh.{snippet_col}) LIKE '%barclays%'
               OR LOWER(fh.{snippet_col}) LIKE '%hsbc%'
               OR LOWER(fh.{snippet_col}) LIKE '%avila%'
               OR LOWER(fh.{snippet_col}) LIKE '%chips%')
        LIMIT 30
    """)

    section("2B: Any financial_hits mentioning Barclays or HSBC")
    run(cur, "2B", f"""
        SELECT fh.file_id, f.title, fh.amount, fh.category,
               SUBSTR(fh.{snippet_col}, 1, 150) AS ctx, f.dataset
        FROM financial_hits fh
        JOIN files f ON fh.file_id = f.id
        WHERE LOWER(fh.{snippet_col}) LIKE '%barclays%'
           OR LOWER(fh.{snippet_col}) LIKE '%hsbc%'
        ORDER BY fh.amount DESC
        LIMIT 30
    """)

    section("2C: Any financial_hits mentioning Mandelson")
    run(cur, "2C", f"""
        SELECT fh.file_id, f.title, fh.amount, fh.category,
               SUBSTR(fh.{snippet_col}, 1, 200) AS ctx, f.dataset
        FROM financial_hits fh
        JOIN files f ON fh.file_id = f.id
        WHERE LOWER(fh.{snippet_col}) LIKE '%mandelson%'
           OR LOWER(fh.{snippet_col}) LIKE '%avila%'
        ORDER BY fh.amount DESC
        LIMIT 30
    """)

banner("PART 3: FUND FLOWS + VERIFIED WIRES — CORRECTED")

cur.execute("PRAGMA table_info(fund_flows)")
ff_cols = [c[1] for c in cur.fetchall()]
print(f"  fund_flows columns: {ff_cols}")

cur.execute("PRAGMA table_info(fund_flows_audited)")
ffa_cols = [c[1] for c in cur.fetchall()]
print(f"  fund_flows_audited columns: {ffa_cols}")

cur.execute("PRAGMA table_info(verified_wires)")
vw_cols = [c[1] for c in cur.fetchall()]
print(f"  verified_wires columns: {vw_cols}")

section("3A: fund_flows — Barclays/HSBC/Mandelson (using actual cols)")
ff_from = 'entity_from' if 'entity_from' in ff_cols else 'source' if 'source' in ff_cols else ff_cols[1] if len(ff_cols) > 1 else None
ff_to = 'entity_to' if 'entity_to' in ff_cols else 'target' if 'target' in ff_cols else ff_cols[2] if len(ff_cols) > 2 else None
if ff_from and ff_to:
    run(cur, "3A", f"""
        SELECT * FROM fund_flows
        WHERE LOWER({ff_from}) LIKE '%barclays%'
           OR LOWER({ff_to}) LIKE '%barclays%'
           OR LOWER({ff_from}) LIKE '%hsbc%'
           OR LOWER({ff_to}) LIKE '%hsbc%'
           OR LOWER({ff_from}) LIKE '%mandelson%'
           OR LOWER({ff_to}) LIKE '%mandelson%'
        LIMIT 30
    """)

section("3B: fund_flows_audited — Barclays/HSBC/Mandelson")
ffa_from = 'entity_from' if 'entity_from' in ffa_cols else ffa_cols[1] if len(ffa_cols) > 1 else None
ffa_to = 'entity_to' if 'entity_to' in ffa_cols else ffa_cols[2] if len(ffa_cols) > 2 else None
if ffa_from and ffa_to:
    run(cur, "3B", f"""
        SELECT * FROM fund_flows_audited
        WHERE LOWER({ffa_from}) LIKE '%barclays%'
           OR LOWER({ffa_to}) LIKE '%barclays%'
           OR LOWER({ffa_from}) LIKE '%hsbc%'
           OR LOWER({ffa_to}) LIKE '%hsbc%'
           OR LOWER({ffa_from}) LIKE '%mandelson%'
           OR LOWER({ffa_to}) LIKE '%mandelson%'
        LIMIT 30
    """)

section("3C: verified_wires — Barclays/HSBC/Mandelson")
run(cur, "3C", f"""
    SELECT * FROM verified_wires
    WHERE LOWER(entity_from) LIKE '%barclays%'
       OR LOWER(entity_to) LIKE '%barclays%'
       OR LOWER(entity_from) LIKE '%hsbc%'
       OR LOWER(entity_to) LIKE '%hsbc%'
       OR LOWER(entity_from) LIKE '%mandelson%'
       OR LOWER(entity_to) LIKE '%mandelson%'
    LIMIT 20
""")

banner("PART 4: DEEP DIVE — KEY DOCUMENTS")

section("4A: Full file list with Mandelson entity hits")
run(cur, "4A", f"""
    SELECT DISTINCT f.id, f.title, f.doc_type, f.dataset
    FROM files f
    WHERE f.id IN (
        SELECT file_id FROM entities WHERE LOWER(entity_text) LIKE '%mandelson%'
    )
    ORDER BY f.dataset, f.id
""")

section("4B: EFTA00086575.pdf — ALL entities in the Mandelson+Avila letter")
run(cur, "4B", """
    SELECT entity_text, entity_type
    FROM entities
    WHERE file_id = 18528
    ORDER BY entity_type, entity_text
""")

section("4C: EFTA00086575.pdf — Full extracted text")
if text_col:
    run(cur, "4C", f"""
        SELECT SUBSTR(e.{text_col}, 1, 2000) AS full_text
        FROM extracted_text e
        WHERE e.file_id = 18528
        LIMIT 5
    """)

section("4D: EFTA00037176.pdf (DS8 document) — ALL entities")
run(cur, "4D", """
    SELECT entity_text, entity_type
    FROM entities
    WHERE file_id = 13959
    ORDER BY entity_type, entity_text
""")

section("4E: EFTA00037176.pdf — Full extracted text")
if text_col:
    run(cur, "4E", f"""
        SELECT SUBSTR(e.{text_col}, 1, 2000) AS full_text
        FROM extracted_text e
        WHERE e.file_id = 13959
        LIMIT 5
    """)

section("4F: EFTA00103831.pdf (email) — ALL entities + text")
run(cur, "4F-entities", """
    SELECT entity_text, entity_type
    FROM entities
    WHERE file_id = 21239
    ORDER BY entity_type, entity_text
""")
if text_col:
    run(cur, "4F-text", f"""
        SELECT SUBSTR(e.{text_col}, 1, 2000) AS full_text
        FROM extracted_text e
        WHERE e.file_id = 21239
        LIMIT 5
    """)

section("4G: EFTA00143627.pdf (flight_log with Mandelson) — text")
if text_col:
    run(cur, "4G", f"""
        SELECT SUBSTR(e.{text_col}, 1, 2000) AS full_text
        FROM extracted_text e
        WHERE e.file_id = 24929
        LIMIT 5
    """)

banner("PART 5: POI_RANKINGS — CORRECTED")

cur.execute("PRAGMA table_info(poi_rankings)")
poi_cols = [c[1] for c in cur.fetchall()]
print(f"  poi_rankings columns: {poi_cols}")

# Find the name column
poi_name = None
for candidate in ['name', 'person_name', 'entity_name', 'poi_name', 'canonical_name']:
    if candidate in poi_cols:
        poi_name = candidate
        break
if not poi_name and poi_cols:
    poi_name = poi_cols[1] if len(poi_cols) > 1 else poi_cols[0]

if poi_name:
    section("5A: Mandelson in POI rankings")
    run(cur, "5A", f"""
        SELECT * FROM poi_rankings
        WHERE LOWER({poi_name}) LIKE '%mandelson%'
        LIMIT 10
    """)

banner("PART 6: FILES TABLE — CORRECTED")

cur.execute("PRAGMA table_info(files)")
f_cols = [c[1] for c in cur.fetchall()]
print(f"  files columns: {f_cols}")

# Full file list for Mandelson
section("6A: All files mentioning Mandelson (via entities)")
run(cur, "6A", f"""
    SELECT DISTINCT f.id, f.title, f.doc_type, f.dataset,
           (SELECT COUNT(*) FROM entities e2 WHERE e2.file_id = f.id 
            AND LOWER(e2.entity_text) LIKE '%mandelson%') AS entity_hits
    FROM files f
    WHERE f.id IN (SELECT file_id FROM entities WHERE LOWER(entity_text) LIKE '%mandelson%')
    ORDER BY f.dataset, f.id
""")

banner("PART 7: DS11 SEARCH — THE BIG ONE")
print("  DS11 has 331,659 files. FT says 'most recent release of ~3M documents'")
print("  These CHIPS payments are most likely in DS11.")

section("7A: DS11 files with Mandelson in entities")
run(cur, "7A", """
    SELECT DISTINCT f.id, f.title, f.doc_type
    FROM files f
    JOIN entities e ON e.file_id = f.id
    WHERE f.dataset = '11'
      AND LOWER(e.entity_text) LIKE '%mandelson%'
    LIMIT 30
""")

section("7B: DS11 files with Mandelson in extracted_text")
if text_col:
    run(cur, "7B", f"""
        SELECT e.file_id, f.title, f.doc_type,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), 'mandelson') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE f.dataset = '11'
          AND LOWER(e.{text_col}) LIKE '%mandelson%'
        LIMIT 30
    """)

section("7C: DS11 files with Barclays in extracted_text")
if text_col:
    run(cur, "7C", f"""
        SELECT e.file_id, f.title, f.doc_type,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), 'barclays') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE f.dataset = '11'
          AND LOWER(e.{text_col}) LIKE '%barclays%'
        LIMIT 30
    """)

section("7D: DS11 files with HSBC in extracted_text")
if text_col:
    run(cur, "7D", f"""
        SELECT e.file_id, f.title, f.doc_type,
               SUBSTR(e.{text_col}, MAX(1, INSTR(LOWER(e.{text_col}), 'hsbc') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE f.dataset = '11'
          AND LOWER(e.{text_col}) LIKE '%hsbc%'
        LIMIT 30
    """)

section("7E: DS11 — 'CHIPS' anywhere")
if text_col:
    run(cur, "7E", f"""
        SELECT e.file_id, f.title, f.doc_type,
               SUBSTR(e.{text_col}, MAX(1, INSTR(UPPER(e.{text_col}), 'CHIPS') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE f.dataset = '11'
          AND (UPPER(e.{text_col}) LIKE '% CHIPS %'
               OR UPPER(e.{text_col}) LIKE '%CHIPS/%'
               OR UPPER(e.{text_col}) LIKE '%CHIPS PAYMENT%'
               OR UPPER(e.{text_col}) LIKE '%CHIPS NUMBER%')
        LIMIT 30
    """)

section("7F: DS11 — $25,000 in any financial context")
if text_col:
    run(cur, "7F", f"""
        SELECT e.file_id, f.title, f.doc_type,
               SUBSTR(e.{text_col}, MAX(1, INSTR(e.{text_col}, '25,000') - 80), 250) AS context
        FROM extracted_text e
        JOIN files f ON e.file_id = f.id
        WHERE f.dataset = '11'
          AND (e.{text_col} LIKE '%25,000%')
          AND (LOWER(e.{text_col}) LIKE '%mandelson%'
               OR LOWER(e.{text_col}) LIKE '%barclays%'
               OR LOWER(e.{text_col}) LIKE '%hsbc%'
               OR LOWER(e.{text_col}) LIKE '%loan%')
        LIMIT 30
    """)

banner("PART 8: REDACTION + FINANCIAL REDACTIONS — CORRECTED")

cur.execute("PRAGMA table_info(redaction_summary)")
rs_cols = [c[1] for c in cur.fetchall()]
print(f"  redaction_summary columns: {rs_cols}")

cur.execute("PRAGMA table_info(financial_redactions)")
fr_cols = [c[1] for c in cur.fetchall()]
print(f"  financial_redactions columns: {fr_cols}")

# Redactions in Mandelson files
mandelson_file_ids = [13959, 18528, 21239, 24929, 24931, 24936, 24939, 24943, 24946, 24947, 24977, 24982]
id_list = ','.join(str(x) for x in mandelson_file_ids)

section("8A: Redaction summary for known Mandelson files")
run(cur, "8A", f"""
    SELECT * FROM redaction_summary
    WHERE file_id IN ({id_list})
    ORDER BY file_id
""")

section("8B: Financial redactions in known Mandelson files")
run(cur, "8B", f"""
    SELECT * FROM financial_redactions
    WHERE file_id IN ({id_list})
    ORDER BY file_id
""")

print("\n")
banner("DONE — v2 COMPLETE")
print("Key files to investigate:")
print("  EFTA00086575.pdf — letter with BOTH Mandelson AND Reinaldo Avila da Silva")
print("  EFTA00037176.pdf — DS8 document with Peter Mandelson")
print("  EFTA00103831.pdf — email chain re: Mandelson")
print("  EFTA00143627.pdf — flight log with Mandelson")
print("=" * 80)

conn.close()
