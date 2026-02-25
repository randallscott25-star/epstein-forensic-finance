"""
fedwire_resweep.py — Re-sweep Fedwire documents to catch what the original 481-wire pipeline missed.

The scope scan found 3,298 docs containing Fedwire references but the original pipeline
only extracted 481. This re-sweep uses broader patterns and cross-references against
existing fund_flows_audited to avoid duplicates.

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import re
from extraction_framework import (
    extract_amounts, extract_dates, extract_beneficiaries,
    extract_routing, resolve_entity, score_transaction
)

# ── Fedwire patterns (broader than original pipeline) ───────────────────────

FW_PATTERNS = [
    # standard statement format
    re.compile(
        r'(?P<date_prefix>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})?'
        r'\s*'
        r'(?:FEDWIRE|FED\s+WIRE|FW)\s+'
        r'(?P<direction>DEBIT|CREDIT|DB|CR|SENT|RCVD)'
        r'\s+'
        r'(?P<detail>.+?)$',
        re.IGNORECASE | re.MULTILINE
    ),
    # abbreviated format
    re.compile(
        r'(?P<date_prefix>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})?'
        r'\s*'
        r'(?:FW\s+(?:DB|CR))'
        r'\s+'
        r'(?P<detail>.+?)$',
        re.IGNORECASE | re.MULTILINE
    ),
    # wire transfer generic (on statements)
    re.compile(
        r'(?P<date_prefix>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})?'
        r'\s*'
        r'(?:WIRE\s+TRANSFER\s+(?:DEBIT|CREDIT|DB|CR|OUT|IN))'
        r'\s+'
        r'(?P<detail>.+?)$',
        re.IGNORECASE | re.MULTILINE
    ),
]

# Fedwire-specific structured format (ABA routing, etc.)
ABA_PATTERN = re.compile(r'(?:ABA|RTN?|ROUTING)\s*[:#]?\s*(\d{9})', re.IGNORECASE)
IMAD_PATTERN = re.compile(r'(?:IMAD|OMAD)\s*[:#]?\s*([A-Z0-9]+)', re.IGNORECASE)


def parse_fedwire_lines(text, bates, dataset, statement_year=None):
    """Extract Fedwire entries from bank statement or wire log text."""
    records = []

    for pat in FW_PATTERNS:
        for m in pat.finditer(text):
            groups = m.groupdict()
            detail = groups.get("detail", "")
            direction_raw = groups.get("direction", "")
            date_prefix = groups.get("date_prefix")

            record = {
                "bates": bates,
                "dataset": dataset,
                "payment_type": "FEDWIRE",
                "extraction_method": "statement_line_resweep",
            }

            # direction
            if direction_raw:
                d = direction_raw.upper()
                record["direction"] = "DEBIT" if d in ("DEBIT", "DB", "SENT", "OUT") else "CREDIT"
            else:
                record["direction"] = "DEBIT"

            # date
            if date_prefix and statement_year:
                dates = extract_dates(f"{date_prefix}, {statement_year}")
                if dates:
                    record["date"] = dates[0]

            # amounts
            amounts = extract_amounts(detail)
            if amounts:
                record["amount"] = amounts[0]
                if len(amounts) >= 2:
                    record["balance_after"] = amounts[-1]

            # beneficiary
            bens = extract_beneficiaries(detail)
            if bens:
                record["beneficiary_raw"] = bens[0]
                canonical, conf = resolve_entity(bens[0])
                record["beneficiary_canonical"] = canonical
                record["entity_confidence"] = conf

            # routing
            routing = extract_routing(detail)
            aba = ABA_PATTERN.search(detail)
            if aba:
                routing["aba"] = aba.group(1)
            imad = IMAD_PATTERN.search(detail)
            if imad:
                routing["imad"] = imad.group(1)
            record["routing"] = routing

            # bank name extraction from detail
            bank = re.search(
                r'(?:VIA|TO|FROM|AT)\s+([A-Z][A-Z\s&.]+?(?:BANK|TRUST|FINANCIAL|SECURITIES|LLC|INC|CORP))',
                detail, re.IGNORECASE
            )
            if bank:
                record["routing"]["intermediary"] = bank.group(1).strip()

            record["raw_text"] = m.group(0)
            record["priority_score"] = score_transaction(record)
            records.append(record)

    return records


def get_existing_fedwire_bates(conn):
    """Pull bates numbers already in fund_flows_audited to avoid duplicates."""
    cur = conn.cursor()
    existing = set()

    # check fund_flows_audited
    try:
        cur.execute("SELECT DISTINCT source_doc FROM fund_flows_audited WHERE source_doc IS NOT NULL")
        existing.update(row[0] for row in cur)
    except:
        pass

    # check extracted_payments
    try:
        cur.execute("SELECT DISTINCT bates FROM extracted_payments WHERE payment_type = 'FEDWIRE' AND bates IS NOT NULL")
        existing.update(row[0] for row in cur)
    except:
        pass

    return existing


def extract_fedwire_resweep(conn, limit=None, verbose=True):
    """Re-sweep Fedwire documents, skipping already-extracted wires."""
    records = []
    docs_scanned = 0
    skipped_existing = 0

    existing_bates = get_existing_fedwire_bates(conn)

    if verbose:
        print(f"[FEDWIRE] Re-sweep starting...")
        print(f"[FEDWIRE] {len(existing_bates)} bates numbers already extracted (will skip)")

    cur = conn.cursor()
    query = """
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE (
            et.text_content LIKE '%FEDWIRE DEBIT%'
            OR et.text_content LIKE '%FEDWIRE CREDIT%'
            OR et.text_content LIKE '%FED WIRE DEBIT%'
            OR et.text_content LIKE '%FED WIRE CREDIT%'
            OR et.text_content LIKE '%FW DB%'
            OR et.text_content LIKE '%FW CR%'
            OR et.text_content LIKE '%WIRE TRANSFER DEBIT%'
            OR et.text_content LIKE '%WIRE TRANSFER CREDIT%'
            OR et.text_content LIKE '%WIRE TRANSFER OUT%'
            OR et.text_content LIKE '%WIRE TRANSFER IN%'
        )
        ORDER BY f.title, et.page_num
    """
    if limit:
        query += f" LIMIT {limit}"

    cur.execute(query)
    rows = cur.fetchall()

    if verbose:
        print(f"[FEDWIRE] Found {len(rows)} pages to process")

    for bates, dataset, page_num, text in rows:
        if not text:
            continue

        if bates in existing_bates:
            skipped_existing += 1
            continue

        docs_scanned += 1

        stmt_year = None
        dates = extract_dates(text)
        if dates:
            stmt_year = dates[0].year

        page_records = parse_fedwire_lines(text, bates, dataset, stmt_year)
        records.extend(page_records)

    if verbose:
        print(f"[FEDWIRE] Re-sweep complete:")
        print(f"  Pages scanned (new): {docs_scanned}")
        print(f"  Skipped (already extracted): {skipped_existing}")
        print(f"  New Fedwire records: {len(records)}")
        total = sum(r.get("amount", 0) for r in records)
        print(f"  New dollar volume: ${total:,.2f}")

        entities = {}
        for r in records:
            ben = r.get("beneficiary_canonical", "UNKNOWN")
            entities[ben] = entities.get(ben, 0) + 1
        if entities:
            print(f"  Unique beneficiaries: {len(entities)}")
            for name, count in sorted(entities.items(), key=lambda x: -x[1])[:10]:
                print(f"    {name}: {count}")

    return records


if __name__ == "__main__":
    from extraction_framework import get_db
    conn = get_db()
    records = extract_fedwire_resweep(conn, verbose=True)
    conn.close()
