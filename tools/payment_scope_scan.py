#!/usr/bin/env python3
"""
payment_scope_scan.py
Phase 1: Scope the full payment universe across 2.87M extracted text pages.
Quantifies every payment clearing type before we build extractors.

This is the "how big is the gap" script.

Usage:
    python3 payment_scope_scan.py /path/to/epstein_files.db 2>&1 | tee payment_scope_results.txt

Author: Randall Scott Taylor
"""

import sqlite3, sys, os, re, json
from collections import defaultdict, Counter
from datetime import datetime

DB = sys.argv[1] if len(sys.argv) > 1 else "/Users/randall/Desktop/epstein_files.db"

if not os.path.exists(DB):
    print(f"ERROR: {DB} not found")
    sys.exit(1)

conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=" * 80)
print("  PAYMENT UNIVERSE SCOPE SCAN")
print(f"  Database: {DB} ({os.path.getsize(DB)/1e9:.2f} GB)")
print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# ── Current pipeline state ───────────────────────────────

print("\n── CURRENT PIPELINE STATE ──")
for table in ["fund_flows_audited", "verified_wires", "financial_hits"]:
    try:
        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count:,} rows")
    except:
        print(f"  {table}: NOT FOUND")

et_count = cur.execute("SELECT COUNT(*) FROM extracted_text").fetchone()[0]
files_count = cur.execute("SELECT COUNT(*) FROM files").fetchone()[0]
print(f"  extracted_text: {et_count:,} pages")
print(f"  files: {files_count:,} documents")

# ── Payment type signatures ──────────────────────────────
# Each tuple: (category, sql_where_clause, description)
# We use SQL LIKE for the initial filter (fast, uses indexes if available)
# then regex for precision counting on the matches

PAYMENT_TYPES = [
    # ── Clearing systems ──
    {
        "cat": "CHIPS",
        "sql": "text_content LIKE '%CHIPS%'",
        "patterns": [
            (r'CHIPS\s*DEBIT', "CHIPS Debit"),
            (r'CHIPS\s*CREDIT', "CHIPS Credit"),
            (r'VIA:?\s*.*CHIPS', "VIA CHIPS routing"),
        ],
        "desc": "Clearing House Interbank Payment System — missed by Fedwire pipeline",
    },
    {
        "cat": "FEDWIRE",
        "sql": "text_content LIKE '%Fedwire%' OR text_content LIKE '%FEDWIRE%' OR text_content LIKE '%Fed Wire%'",
        "patterns": [
            (r'(?i)fedwire\s*debit', "Fedwire Debit"),
            (r'(?i)fedwire\s*credit', "Fedwire Credit"),
            (r'(?i)fed\s*wire', "Fed Wire"),
        ],
        "desc": "Federal Reserve wire — current pipeline target, baseline count",
    },
    {
        "cat": "SWIFT",
        "sql": "text_content LIKE '%SWIFT%' OR text_content LIKE '%MT103%' OR text_content LIKE '%MT202%'",
        "patterns": [
            (r'SWIFT:\s*[A-Z]{6}[A-Z0-9]{2,5}', "SWIFT BIC code"),
            (r'MT103', "MT103 (single customer credit transfer)"),
            (r'MT202', "MT202 (bank-to-bank transfer)"),
            (r'MT940', "MT940 (statement message)"),
            (r'MT950', "MT950 (statement message)"),
        ],
        "desc": "SWIFT international wire messages and BIC codes",
    },
    {
        "cat": "ACH",
        "sql": "text_content LIKE '%ACH %' OR text_content LIKE '%ACH/%'",
        "patterns": [
            (r'ACH\s*DEBIT', "ACH Debit"),
            (r'ACH\s*CREDIT', "ACH Credit"),
            (r'ACH\s*(?:PAYMENT|PMT)', "ACH Payment"),
            (r'NACHA', "NACHA reference"),
        ],
        "desc": "Automated Clearing House — recurring/smaller payments",
    },
    # ── Internal bank movements ──
    {
        "cat": "BOOK_TRANSFER",
        "sql": "text_content LIKE '%Book Transfer%' OR text_content LIKE '%BOOK TRANSFER%' OR text_content LIKE '%BK XFER%'",
        "patterns": [
            (r'(?i)book\s*transfer\s*(?:credit|debit)', "Book Transfer Credit/Debit"),
            (r'(?i)book\s*transfer', "Book Transfer (general)"),
            (r'(?i)bk\s*xfer', "BK XFER abbreviation"),
            (r'(?i)reversal\s*of\s*entry', "Reversal of Entry"),
        ],
        "desc": "Internal bank book transfers — inter-account movements, reversals",
    },
    {
        "cat": "INTERNAL_TRANSFER",
        "sql": "text_content LIKE '%Internal Funds%' OR text_content LIKE '%INTERNAL FUNDS%' OR text_content LIKE '%INT FUNDS%'",
        "patterns": [
            (r'(?i)internal\s*funds?\s*transfer', "Internal Funds Transfer"),
            (r'(?i)int\s*funds?\s*(?:xfer|transfer)', "INT FUNDS XFER"),
            (r'(?i)funds?\s*transferred\s*from', "Funds Transferred From"),
        ],
        "desc": "Internal funds transfers between Epstein accounts at same bank",
    },
    # ── Paper instruments ──
    {
        "cat": "CHECKS",
        "sql": "text_content LIKE '%Check #%' OR text_content LIKE '%CHECK #%' OR text_content LIKE '%CHK #%' OR text_content LIKE '%Check No%'",
        "patterns": [
            (r'(?i)check\s*#\s*\d+', "Check # with number"),
            (r'(?i)chk\s*#\s*\d+', "CHK # with number"),
            (r'(?i)check\s*(?:no|number)\s*\.?\s*\d+', "Check No/Number"),
            (r'(?i)cashier.?s?\s*check', "Cashier's Check"),
        ],
        "desc": "Check disbursements — numbered checks on statements",
    },
    # ── FX and international ──
    {
        "cat": "FX",
        "sql": "text_content LIKE '%FX %' OR text_content LIKE '%Foreign Exchange%' OR text_content LIKE '%FOREIGN EXCHANGE%'",
        "patterns": [
            (r'(?i)fx\s*(?:debit|credit|operations?|usd)', "FX operation"),
            (r'(?i)foreign\s*exchange', "Foreign Exchange"),
            (r'(?i)fx\s*(?:incoming|outgoing)', "FX directional"),
        ],
        "desc": "Foreign exchange transactions — international money movement",
    },
    {
        "cat": "CORRESPONDENT_BANK",
        "sql": """text_content LIKE '%VIA:%' OR text_content LIKE '%VIA.%'""",
        "patterns": [
            (r'VIA:?\s*(?:HSBC|BARCLAYS|DEUTSCHE|CITIBANK|NATWEST|CREDIT SUISSE|UBS|BNP)', "VIA named bank"),
            (r'VIA:?\s*[A-Z][A-Z ]{3,30}BANK', "VIA [BANK] pattern"),
            (r'/\d{4}\s', "Correspondent bank routing code (/NNNN)"),
        ],
        "desc": "Correspondent bank routing — identifies the intermediary bank network",
    },
    # ── Trust and entity distributions ──
    {
        "cat": "TRUST_DISTRIBUTION",
        "sql": "text_content LIKE '%trust%distribut%' OR text_content LIKE '%Trust%Distribut%' OR text_content LIKE '%Butterfly%Trust%'",
        "patterns": [
            (r'(?i)trust\s*distribution', "Trust Distribution"),
            (r'(?i)butterfly\s*trust', "Butterfly Trust"),
            (r'(?i)(?:grantor|beneficiary)\s*trust', "Grantor/Beneficiary Trust"),
        ],
        "desc": "Trust distributions — Butterfly Trust and other Epstein trust structures",
    },
    # ── Brokerage ──
    {
        "cat": "BROKERAGE",
        "sql": "text_content LIKE '%margin%' OR text_content LIKE '%securities%transfer%' OR text_content LIKE '%brokerage%'",
        "patterns": [
            (r'(?i)margin\s*(?:call|transfer|payment)', "Margin activity"),
            (r'(?i)securities?\s*transfer', "Securities Transfer"),
            (r'(?i)brokerage\s*(?:transfer|account|debit|credit)', "Brokerage Transfer"),
            (r'(?i)liquidat', "Liquidation"),
        ],
        "desc": "Brokerage/securities movements that become wire funding sources",
    },
    # ── Catch-all wire patterns ──
    {
        "cat": "WIRE_GENERIC",
        "sql": "text_content LIKE '%Wire Transfer%' OR text_content LIKE '%WIRE TRANSFER%' OR text_content LIKE '%wire debit%' OR text_content LIKE '%wire credit%'",
        "patterns": [
            (r'(?i)wire\s*transfer\s*(?:debit|credit)?', "Wire Transfer"),
            (r'(?i)wire\s*(?:debit|credit)', "Wire Debit/Credit"),
            (r'(?i)outgoing\s*wire', "Outgoing Wire"),
            (r'(?i)incoming\s*wire', "Incoming Wire"),
        ],
        "desc": "Generic wire transfer language not captured by CHIPS/Fedwire",
    },
]

# ── Named beneficiary pattern (for any payment type) ─────

BEN_PATTERN = re.compile(
    r'(?:BEN|NC|BENEFICIARY|PAYEE|TO|CREDIT)\s*[:.]?\s*([A-Z][A-Z\s\.,]{3,50})',
    re.IGNORECASE
)
AMOUNT_PATTERN = re.compile(r'\$\s*([\d,]+\.?\d{0,2})')
DATE_PATTERN = re.compile(
    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}|'
    r'\d{1,2}/\d{1,2}/\d{2,4}|'
    r'\d{4}-\d{2}-\d{2}'
)

# ── Scan ─────────────────────────────────────────────────

results = {}
all_samples = {}

for ptype in PAYMENT_TYPES:
    cat = ptype["cat"]
    print(f"\n{'█' * 80}")
    print(f"  {cat}: {ptype['desc']}")
    print(f"{'█' * 80}")

    # Phase 1: SQL count (fast)
    sql = f"SELECT COUNT(*) FROM extracted_text WHERE {ptype['sql']}"
    try:
        doc_count = cur.execute(sql).fetchone()[0]
    except Exception as e:
        print(f"  SQL error: {e}")
        doc_count = 0

    print(f"  Documents matching SQL filter: {doc_count:,}")

    if doc_count == 0:
        results[cat] = {"docs": 0, "patterns": {}, "samples": []}
        continue

    # Phase 2: Pull samples for regex precision counting
    # Limit to 5000 for speed, but count all
    sample_sql = f"""
        SELECT et.file_id, f.title, f.dataset, SUBSTR(et.text_content, 1, 3000)
        FROM extracted_text et
        JOIN files f ON et.file_id = f.id
        WHERE {ptype['sql']}
        LIMIT 5000
    """
    try:
        rows = cur.execute(sample_sql).fetchall()
    except Exception as e:
        print(f"  Sample query error: {e}")
        rows = []

    pattern_counts = Counter()
    beneficiaries = Counter()
    amounts = []
    samples = []
    seen_files = set()

    for file_id, title, ds, text in rows:
        if file_id in seen_files:
            continue
        seen_files.add(file_id)

        if not text:
            continue

        # count pattern subtypes
        for pat, label in ptype["patterns"]:
            matches = re.findall(pat, text)
            if matches:
                pattern_counts[label] += 1

        # extract beneficiaries
        for m in BEN_PATTERN.finditer(text):
            name = m.group(1).strip().rstrip(',.')
            if len(name) > 3 and name.upper() not in ('THE', 'FOR', 'AND', 'FROM', 'BANK'):
                beneficiaries[name[:50]] += 1

        # extract amounts
        for m in AMOUNT_PATTERN.finditer(text):
            try:
                amt = float(m.group(1).replace(',', ''))
                if 100 <= amt <= 50_000_000:  # reasonable range
                    amounts.append(amt)
            except:
                pass

        # keep first 5 samples per category
        if len(samples) < 5:
            bates = re.search(r'EFTA\d+', title or "")
            bates_str = bates.group(0) if bates else str(file_id)
            # extract the relevant line
            for pat, label in ptype["patterns"]:
                m = re.search(pat, text)
                if m:
                    start = max(0, m.start() - 80)
                    end = min(len(text), m.end() + 120)
                    context = text[start:end].replace('\n', ' ').strip()
                    samples.append({
                        "bates": bates_str,
                        "ds": ds,
                        "match": label,
                        "context": context[:200],
                    })
                    break

    # report
    print(f"\n  Pattern breakdown (from {len(seen_files):,} unique files sampled):")
    for label, count in pattern_counts.most_common(10):
        print(f"    {label:45s} {count:,}")

    if beneficiaries:
        print(f"\n  Top beneficiaries/named parties:")
        for name, count in beneficiaries.most_common(20):
            print(f"    {name:45s} {count:,}")

    if amounts:
        amounts.sort(reverse=True)
        total = sum(amounts)
        print(f"\n  Financial scope (from sampled docs):")
        print(f"    Transactions with amounts: {len(amounts):,}")
        print(f"    Total: ${total:,.2f}")
        print(f"    Largest: ${amounts[0]:,.2f}")
        print(f"    Median: ${amounts[len(amounts)//2]:,.2f}")
        if len(amounts) >= 5:
            print(f"    Top 5: {', '.join(f'${a:,.0f}' for a in amounts[:5])}")

    if samples:
        print(f"\n  Sample extractions:")
        for s in samples[:5]:
            print(f"    [{s['bates']}] DS{s['ds']} | {s['match']}")
            print(f"      {s['context']}")

    results[cat] = {
        "docs": doc_count,
        "unique_files_sampled": len(seen_files),
        "patterns": dict(pattern_counts),
        "top_beneficiaries": dict(beneficiaries.most_common(20)),
        "amount_count": len(amounts),
        "amount_total": sum(amounts) if amounts else 0,
        "samples": samples,
    }

# ── Summary ──────────────────────────────────────────────

print(f"\n\n{'=' * 80}")
print(f"  SCOPE SUMMARY")
print(f"{'=' * 80}")
print(f"\n  {'Category':<25s} {'Docs':>10s} {'Has Amounts':>12s} {'Est. Total':>18s}")
print(f"  {'─'*25} {'─'*10} {'─'*12} {'─'*18}")

total_docs = 0
total_amounts = 0
for cat, data in sorted(results.items(), key=lambda x: x[1]['docs'], reverse=True):
    docs = data['docs']
    amts = data['amount_count']
    total = data['amount_total']
    total_docs += docs
    total_amounts += total
    print(f"  {cat:<25s} {docs:>10,} {amts:>12,} ${total:>16,.0f}")

print(f"  {'─'*25} {'─'*10} {'─'*12} {'─'*18}")
print(f"  {'TOTAL':<25s} {total_docs:>10,} {'':>12s} ${total_amounts:>16,.0f}")

# ── Gap analysis ─────────────────────────────────────────

print(f"\n\n{'=' * 80}")
print(f"  GAP ANALYSIS vs. CURRENT PIPELINE")
print(f"{'=' * 80}")

ff_count = cur.execute("SELECT COUNT(*) FROM fund_flows_audited").fetchone()[0]
vw_count = cur.execute("SELECT COUNT(*) FROM verified_wires").fetchone()[0]

# check what types are already in fund_flows
try:
    existing_types = cur.execute("""
        SELECT DISTINCT
            CASE
                WHEN LOWER(context) LIKE '%chips%' THEN 'CHIPS'
                WHEN LOWER(context) LIKE '%fedwire%' THEN 'FEDWIRE'
                WHEN LOWER(context) LIKE '%book transfer%' THEN 'BOOK_TRANSFER'
                WHEN LOWER(context) LIKE '%internal funds%' THEN 'INTERNAL_TRANSFER'
                WHEN LOWER(context) LIKE '%ach%' THEN 'ACH'
                WHEN LOWER(context) LIKE '%swift%' THEN 'SWIFT'
                WHEN LOWER(context) LIKE '%check #%' OR LOWER(context) LIKE '%chk #%' THEN 'CHECKS'
                ELSE 'OTHER'
            END as ptype,
            COUNT(*) as cnt
        FROM fund_flows_audited
        GROUP BY ptype
        ORDER BY cnt DESC
    """).fetchall()
    print(f"\n  Current fund_flows_audited by type:")
    for ptype, cnt in existing_types:
        print(f"    {ptype:<25s} {cnt:,}")
except Exception as e:
    print(f"  Could not classify existing: {e}")

print(f"\n  Current totals:")
print(f"    fund_flows_audited: {ff_count:,}")
print(f"    verified_wires: {vw_count}")
print(f"\n  New payment types found in corpus but NOT in pipeline:")
for cat in ["CHIPS", "BOOK_TRANSFER", "INTERNAL_TRANSFER", "ACH", "CHECKS",
            "FX", "SWIFT", "TRUST_DISTRIBUTION", "BROKERAGE"]:
    data = results.get(cat, {})
    docs = data.get('docs', 0)
    if docs > 0:
        print(f"    {cat:<25s} {docs:>8,} documents → EXTRACTION NEEDED")

# ── Save results ─────────────────────────────────────────

out_file = "payment_scope_results.json"
with open(out_file, 'w') as f:
    # clean for JSON serialization
    clean = {}
    for k, v in results.items():
        clean[k] = {kk: vv for kk, vv in v.items() if kk != 'samples'}
        clean[k]['sample_count'] = len(v.get('samples', []))
    json.dump(clean, f, indent=2, default=str)
print(f"\n  Results saved: {out_file}")

print(f"\n{'=' * 80}")
print(f"  NEXT: Run payment_full_extract.py to extract all identified types")
print(f"  Paste this output into next session for extraction pipeline build")
print(f"{'=' * 80}")

conn.close()
