#!/usr/bin/env python3
"""
FT CHIPS PAYMENT SEARCH — Full corpus scan for Mandelson/Avila da Silva payments
Target: 3 payments of $25,000 each from Epstein JPMorgan accounts
  1. May 2003 → Barclays (Reinaldo Avila da Silva), Mandelson as BEN
  2. June 2004 → HSBC (Mandelson)
  3. June 2004 → HSBC (Mandelson), days after #2

Run: python3 ft_chips_search.py /path/to/epstein_files.db
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
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}")

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
            print(f"  (no results) [{elapsed:.1f}s]")
            return rows
            
        # Print header
        print("  " + " | ".join(f"{c:<35}" for c in cols))
        print("  " + "-" * (37 * len(cols)))
        for row in rows:
            vals = []
            for v in row:
                s = str(v) if v is not None else "NULL"
                if len(s) > 35:
                    s = s[:32] + "..."
                vals.append(f"{s:<35}")
            print("  " + " | ".join(vals))
        print(f"  [{elapsed:.1f}s, {len(rows)} rows]")
        return rows
    except Exception as e:
        print(f"  ERROR: {e}")
        return []

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Verify database
cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
tcount = cur.fetchone()[0]
print(f"\nConnected to: {DB}")
print(f"Tables: {tcount}")

banner("PART 1: TEXT SEARCH — 'MANDELSON' ACROSS ALL TEXT")

section("1A: extracted_text — full-text search for 'Mandelson'")
run(cur, "1A", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'mandelson') - 60), 150) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%mandelson%'
    ORDER BY f.dataset, f.id
    LIMIT 50
""")

section("1B: extracted_text — search for 'Avila' or 'Reinaldo'")
run(cur, "1B", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'avila') - 60), 150) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%avila%'
       OR LOWER(e.text) LIKE '%reinaldo%'
    ORDER BY f.dataset, f.id
    LIMIT 50
""")

section("1C: extracted_text — search for 'CHIPS' (payment system)")
run(cur, "1C", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(UPPER(e.text), 'CHIPS') - 60), 150) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE UPPER(e.text) LIKE '%CHIPS%'
       AND (LOWER(e.text) LIKE '%payment%' 
            OR LOWER(e.text) LIKE '%transfer%'
            OR LOWER(e.text) LIKE '%clearing%'
            OR LOWER(e.text) LIKE '%interbank%'
            OR LOWER(e.text) LIKE '%25000%'
            OR LOWER(e.text) LIKE '%25,000%')
    ORDER BY f.dataset, f.id
    LIMIT 40
""")

section("1D: extracted_text — search for 'CHIPS' (broad, any context)")
run(cur, "1D", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(UPPER(e.text), 'CHIPS') - 60), 150) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE UPPER(e.text) LIKE '% CHIPS %'
       OR UPPER(e.text) LIKE '%CHIPS PAYMENT%'
       OR UPPER(e.text) LIKE '%CHIPS TRANSFER%'
       OR UPPER(e.text) LIKE '%CHIPS NUMBER%'
       OR UPPER(e.text) LIKE '%CHIPS ID%'
       OR UPPER(e.text) LIKE '%CHIPS/%'
    ORDER BY f.dataset, f.id
    LIMIT 40
""")

banner("PART 2: ENTITY SEARCH — MANDELSON IN NLP ENTITIES")

section("2A: entities table — 'Mandelson'")
run(cur, "2A", """
    SELECT e.file_id, f.title, e.entity_text, e.entity_type, f.doc_type, f.dataset
    FROM entities e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.entity_text) LIKE '%mandelson%'
    ORDER BY f.dataset, f.id
    LIMIT 50
""")

section("2B: entities table — 'Avila' or 'Reinaldo'")
run(cur, "2B", """
    SELECT e.file_id, f.title, e.entity_text, e.entity_type, f.doc_type, f.dataset
    FROM entities e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.entity_text) LIKE '%avila%'
       OR LOWER(e.entity_text) LIKE '%reinaldo%'
    ORDER BY f.dataset, f.id
    LIMIT 50
""")

section("2C: poi_rankings — Mandelson in persons of interest")
run(cur, "2C", """
    SELECT * FROM poi_rankings
    WHERE LOWER(name) LIKE '%mandelson%'
       OR LOWER(name) LIKE '%avila%'
    LIMIT 20
""")

banner("PART 3: FINANCIAL SEARCH — $25,000 PAYMENTS + JPMORGAN→BARCLAYS/HSBC")

section("3A: financial_hits — amounts near $25,000")
run(cur, "3A", """
    SELECT fh.file_id, f.title, fh.amount, fh.category, fh.verify_tier,
           SUBSTR(fh.context_snippet, 1, 100) AS ctx,
           f.doc_type, f.dataset
    FROM financial_hits fh
    JOIN files f ON fh.file_id = f.id
    WHERE fh.amount BETWEEN 24000 AND 26000
      AND (LOWER(fh.context_snippet) LIKE '%mandelson%'
           OR LOWER(fh.context_snippet) LIKE '%avila%'
           OR LOWER(fh.context_snippet) LIKE '%barclays%'
           OR LOWER(fh.context_snippet) LIKE '%hsbc%'
           OR LOWER(fh.context_snippet) LIKE '%chips%'
           OR LOWER(fh.context_snippet) LIKE '%ben %')
    LIMIT 40
""")

section("3B: financial_hits — any $25,000 from JPMorgan context")
run(cur, "3B", """
    SELECT fh.file_id, f.title, fh.amount, fh.category, fh.verify_tier,
           SUBSTR(fh.context_snippet, 1, 120) AS ctx,
           f.doc_type, f.dataset
    FROM financial_hits fh
    JOIN files f ON fh.file_id = f.id
    WHERE fh.amount BETWEEN 24500 AND 25500
      AND (LOWER(fh.context_snippet) LIKE '%jpmorgan%'
           OR LOWER(fh.context_snippet) LIKE '%jp morgan%'
           OR LOWER(fh.context_snippet) LIKE '%chase%')
    LIMIT 40
""")

section("3C: fund_flows — any flows mentioning Mandelson, Barclays, or HSBC")
run(cur, "3C", """
    SELECT ff.entity_from, ff.entity_to, ff.amount, ff.date, ff.confidence,
           SUBSTR(ff.context, 1, 100) AS ctx
    FROM fund_flows ff
    WHERE LOWER(ff.entity_from) LIKE '%mandelson%'
       OR LOWER(ff.entity_to) LIKE '%mandelson%'
       OR LOWER(ff.entity_from) LIKE '%avila%'
       OR LOWER(ff.entity_to) LIKE '%avila%'
       OR LOWER(ff.entity_from) LIKE '%barclays%'
       OR LOWER(ff.entity_to) LIKE '%barclays%'
       OR LOWER(ff.entity_from) LIKE '%hsbc%'
       OR LOWER(ff.entity_to) LIKE '%hsbc%'
    LIMIT 40
""")

section("3D: fund_flows_audited — Barclays or HSBC flows")
run(cur, "3D", """
    SELECT entity_from, entity_to, amount, tier, ent_cat, composite_score,
           SUBSTR(context_snippet, 1, 100) AS ctx
    FROM fund_flows_audited
    WHERE LOWER(entity_from) LIKE '%barclays%'
       OR LOWER(entity_to) LIKE '%barclays%'
       OR LOWER(entity_from) LIKE '%hsbc%'
       OR LOWER(entity_to) LIKE '%hsbc%'
       OR LOWER(entity_from) LIKE '%mandelson%'
       OR LOWER(entity_to) LIKE '%mandelson%'
    LIMIT 40
""")

section("3E: verified_wires — any Barclays or HSBC")
run(cur, "3E", """
    SELECT date, entity_from, entity_to, amount, exhibit, bates_number
    FROM verified_wires
    WHERE LOWER(entity_from) LIKE '%barclays%'
       OR LOWER(entity_to) LIKE '%barclays%'
       OR LOWER(entity_from) LIKE '%hsbc%'
       OR LOWER(entity_to) LIKE '%hsbc%'
       OR LOWER(entity_from) LIKE '%mandelson%'
       OR LOWER(entity_to) LIKE '%mandelson%'
    LIMIT 20
""")

section("3F: fincen_transactions — Barclays or HSBC bank connections")
run(cur, "3F", """
    SELECT filer_org_name, originator_bank, beneficiary_bank,
           begin_date, end_date, number_transactions, amount_transactions
    FROM fincen_transactions
    WHERE LOWER(originator_bank) LIKE '%barclays%'
       OR LOWER(beneficiary_bank) LIKE '%barclays%'
       OR LOWER(originator_bank) LIKE '%hsbc%'
       OR LOWER(beneficiary_bank) LIKE '%hsbc%'
    LIMIT 30
""")

banner("PART 4: DOCUMENT-LEVEL SEARCH — ACCOUNTANT DOCS & LOANS/EXCHANGES")

section("4A: Files classified as 'financial' mentioning Mandelson")
run(cur, "4A", """
    SELECT f.id, f.title, f.doc_type, f.dataset, f.date_extracted
    FROM files f
    WHERE f.id IN (
        SELECT file_id FROM extracted_text 
        WHERE LOWER(text) LIKE '%mandelson%'
    )
    AND f.doc_type IN ('financial', 'spreadsheet', 'bank_statement')
    ORDER BY f.dataset, f.id
    LIMIT 30
""")

section("4B: Files mentioning 'loans and exchanges' (the header FT found)")
run(cur, "4B", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'loans and exchanges') - 40), 150) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%loans and exchanges%'
    ORDER BY f.dataset, f.id
    LIMIT 30
""")

section("4C: Files mentioning 'related entities' near 2003 or 2004")
run(cur, "4C", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'related entities') - 40), 150) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%related entities%'
      AND (e.text LIKE '%2003%' OR e.text LIKE '%2004%')
    ORDER BY f.dataset, f.id
    LIMIT 30
""")

section("4D: Documents with 'Epstein' + 'accountant' or 'accounting'")
run(cur, "4D", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'account') - 40), 120) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%loans and exchanges%'
      AND LOWER(e.text) LIKE '%25,000%'
    ORDER BY f.dataset, f.id
    LIMIT 20
""")

banner("PART 5: TEMPORAL SEARCH — 2003-2004 DOCUMENTS")

section("5A: Files dated 2003 mentioning JPMorgan + $25,000")
run(cur, "5A", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), '25,000') - 80), 200) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE (e.text LIKE '%2003%')
      AND (e.text LIKE '%25,000%' OR e.text LIKE '%25000%')
      AND (LOWER(e.text) LIKE '%jpmorgan%' 
           OR LOWER(e.text) LIKE '%jp morgan%'
           OR LOWER(e.text) LIKE '%chase%')
    LIMIT 30
""")

section("5B: Files dated 2004 mentioning $25,000 + HSBC")
run(cur, "5B", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), '25,000') - 80), 200) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE (e.text LIKE '%2004%')
      AND (e.text LIKE '%25,000%' OR e.text LIKE '%25000%')
      AND (LOWER(e.text) LIKE '%hsbc%')
    LIMIT 30
""")

section("5C: dates_found — May 2003 and June 2004 in financial docs")
run(cur, "5C", """
    SELECT df.file_id, f.title, df.date_text, f.doc_type, f.dataset,
           SUBSTR(df.context, 1, 100) AS ctx
    FROM dates_found df
    JOIN files f ON df.file_id = f.id
    WHERE (df.date_text LIKE '%May 2003%' OR df.date_text LIKE '%June 2004%'
           OR df.date_text LIKE '%2003-05%' OR df.date_text LIKE '%2004-06%')
      AND f.doc_type IN ('financial', 'spreadsheet', 'bank_statement', 'email')
      AND (LOWER(df.context) LIKE '%25%' OR LOWER(df.context) LIKE '%payment%'
           OR LOWER(df.context) LIKE '%wire%' OR LOWER(df.context) LIKE '%transfer%')
    LIMIT 30
""")

banner("PART 6: BROADER NET — BARCLAYS + HSBC ANYWHERE IN CORPUS")

section("6A: All Barclays mentions in extracted_text (count + samples)")
run(cur, "6A", """
    SELECT COUNT(*) AS total_pages_with_barclays
    FROM extracted_text
    WHERE LOWER(text) LIKE '%barclays%'
""")

run(cur, "6A-sample", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'barclays') - 60), 150) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%barclays%'
    ORDER BY f.dataset, f.id
    LIMIT 20
""")

section("6B: All HSBC mentions in extracted_text (count + samples)")
run(cur, "6B", """
    SELECT COUNT(*) AS total_pages_with_hsbc
    FROM extracted_text
    WHERE LOWER(text) LIKE '%hsbc%'
""")

run(cur, "6B-sample", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'hsbc') - 60), 150) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%hsbc%'
    ORDER BY f.dataset, f.id
    LIMIT 20
""")

section("6C: Barclays + HSBC in financial_hits")
run(cur, "6C", """
    SELECT fh.file_id, f.title, fh.amount, fh.category,
           SUBSTR(fh.context_snippet, 1, 100) AS ctx, f.dataset
    FROM financial_hits fh
    JOIN files f ON fh.file_id = f.id
    WHERE LOWER(fh.context_snippet) LIKE '%barclays%'
       OR LOWER(fh.context_snippet) LIKE '%hsbc%'
    ORDER BY fh.amount DESC
    LIMIT 30
""")

banner("PART 7: EMAIL SEARCH — CORRESPONDENCE MENTIONING MANDELSON")

section("7A: Emails mentioning Mandelson")
run(cur, "7A", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'mandelson') - 80), 200) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%mandelson%'
      AND f.doc_type = 'email'
    ORDER BY f.dataset, f.id
    LIMIT 30
""")

section("7B: Emails mentioning 'Avila' or 'Reinaldo'")
run(cur, "7B", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'avila') - 80), 200) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE (LOWER(e.text) LIKE '%avila%' OR LOWER(e.text) LIKE '%reinaldo%')
      AND f.doc_type = 'email'
    ORDER BY f.dataset, f.id
    LIMIT 30
""")

section("7C: Emails mentioning 'best pal' or 'chief life adviser'")
run(cur, "7C", """
    SELECT e.file_id, f.title, f.doc_type, f.dataset,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'best pal') - 60), 180) AS context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%best pal%'
       OR LOWER(e.text) LIKE '%chief life adviser%'
       OR LOWER(e.text) LIKE '%chief life advisor%'
    ORDER BY f.dataset, f.id
    LIMIT 20
""")

banner("PART 8: REDACTION ANALYSIS — WHAT'S HIDDEN NEAR MANDELSON")

section("8A: Redactions in files that mention Mandelson")
run(cur, "8A", """
    SELECT rm.file_id, f.title, rm.redaction_count, rm.has_financial, 
           rm.has_names, rm.has_dates, f.doc_type, f.dataset
    FROM redaction_summary rm
    JOIN files f ON rm.file_id = f.id
    WHERE rm.file_id IN (
        SELECT file_id FROM extracted_text 
        WHERE LOWER(text) LIKE '%mandelson%'
    )
    ORDER BY rm.redaction_count DESC
    LIMIT 20
""")

section("8B: Financial redactions near Mandelson files")
run(cur, "8B", """
    SELECT fr.file_id, f.title, fr.amount, fr.confidence,
           SUBSTR(fr.context, 1, 100) AS ctx, f.dataset
    FROM financial_redactions fr
    JOIN files f ON fr.file_id = f.id
    WHERE fr.file_id IN (
        SELECT file_id FROM extracted_text 
        WHERE LOWER(text) LIKE '%mandelson%'
    )
    ORDER BY fr.amount DESC
    LIMIT 20
""")

banner("PART 9: ICIJ CROSS-REFERENCE — MANDELSON OFFSHORE")

section("9A: ICIJ officers — Mandelson")
run(cur, "9A", """
    SELECT name, countries, sourceID
    FROM icij_officers
    WHERE LOWER(name) LIKE '%mandelson%'
    LIMIT 10
""")

section("9B: ICIJ entities — Mandelson")
run(cur, "9B", """
    SELECT name, jurisdiction_description, company_type, status, sourceID
    FROM icij_entities
    WHERE LOWER(name) LIKE '%mandelson%'
    LIMIT 10
""")

banner("PART 10: FULL DOCUMENT LIST — EVERY FILE MENTIONING MANDELSON")

section("10A: Complete file inventory with Mandelson reference")
run(cur, "10A", """
    SELECT DISTINCT f.id, f.title, f.doc_type, f.dataset, f.date_extracted,
           (SELECT COUNT(*) FROM extracted_text e2 
            WHERE e2.file_id = f.id AND LOWER(e2.text) LIKE '%mandelson%') AS pages_with_hit
    FROM files f
    WHERE f.id IN (
        SELECT file_id FROM extracted_text 
        WHERE LOWER(text) LIKE '%mandelson%'
    )
    ORDER BY f.dataset, f.id
    LIMIT 50
""")

section("10B: Complete file inventory with Avila/Reinaldo reference")
run(cur, "10B", """
    SELECT DISTINCT f.id, f.title, f.doc_type, f.dataset, f.date_extracted
    FROM files f
    WHERE f.id IN (
        SELECT file_id FROM extracted_text 
        WHERE LOWER(text) LIKE '%avila%' OR LOWER(text) LIKE '%reinaldo%'
    )
    ORDER BY f.dataset, f.id
    LIMIT 50
""")

banner("PART 11: DEEP TEXT EXTRACTION — FULL CONTEXT FROM MANDELSON DOCS")

section("11A: Full text snippets from top Mandelson files (financial docs)")
run(cur, "11A", """
    SELECT e.file_id, f.title, e.page_number,
           SUBSTR(e.text, MAX(1, INSTR(LOWER(e.text), 'mandelson') - 200), 500) AS full_context
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE LOWER(e.text) LIKE '%mandelson%'
      AND (f.doc_type IN ('financial', 'spreadsheet', 'bank_statement')
           OR LOWER(e.text) LIKE '%25,000%'
           OR LOWER(e.text) LIKE '%25000%'
           OR LOWER(e.text) LIKE '%barclays%'
           OR LOWER(e.text) LIKE '%hsbc%'
           OR LOWER(e.text) LIKE '%chips%'
           OR LOWER(e.text) LIKE '%loans%')
    ORDER BY f.dataset, f.id
    LIMIT 30
""")

section("11B: Full text from files with BOTH Mandelson AND ($25,000 OR Barclays OR HSBC)")
run(cur, "11B", """
    SELECT e.file_id, f.title, e.page_number,
           SUBSTR(e.text, 1, 800) AS full_text_start
    FROM extracted_text e
    JOIN files f ON e.file_id = f.id
    WHERE e.file_id IN (
        SELECT file_id FROM extracted_text WHERE LOWER(text) LIKE '%mandelson%'
    )
    AND (LOWER(e.text) LIKE '%25,000%'
         OR LOWER(e.text) LIKE '%25000%'
         OR LOWER(e.text) LIKE '%barclays%'
         OR LOWER(e.text) LIKE '%hsbc%'
         OR LOWER(e.text) LIKE '%chips%'
         OR LOWER(e.text) LIKE '%loans and exchanges%')
    ORDER BY f.id, e.page_number
    LIMIT 30
""")

banner("PART 12: DATASET COVERAGE CHECK")

section("12A: Which datasets contain docs from 2003-2004?")
run(cur, "12A", """
    SELECT f.dataset, COUNT(*) AS files_2003_2004
    FROM files f
    WHERE f.date_extracted LIKE '%2003%' OR f.date_extracted LIKE '%2004%'
    GROUP BY f.dataset
    ORDER BY files_2003_2004 DESC
    LIMIT 20
""")

section("12B: Total files per dataset (coverage check)")
run(cur, "12B", """
    SELECT dataset, COUNT(*) AS file_count
    FROM files
    GROUP BY dataset
    ORDER BY CAST(dataset AS INTEGER)
""")

section("12C: Are DS11/DS12 (recent DOJ releases) in the corpus?")
run(cur, "12C", """
    SELECT dataset, COUNT(*) AS files, 
           MIN(title) AS first_file, MAX(title) AS last_file
    FROM files
    WHERE dataset IN ('11', '12', '98', '99', '100', '101', '102', '103', '104')
    GROUP BY dataset
    ORDER BY CAST(dataset AS INTEGER)
""")

print("\n")
banner("DONE. Paste full output back to Claude.")
print("This searches every table for Mandelson, Avila da Silva, CHIPS payments,")
print("Barclays, HSBC, $25K amounts, 2003-2004 dates, and related redactions.")
print("=" * 80)

conn.close()
