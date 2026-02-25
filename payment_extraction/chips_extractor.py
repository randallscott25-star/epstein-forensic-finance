"""
chips_extractor.py — Extract CHIPS wire transfers from the EFTA corpus.

Two document types:
1. Tag 59/72 format — JPMorgan internal wire processing records (structured)
2. Statement lines — CHIPS DEBIT/CREDIT entries on monthly bank statements

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import re
from extraction_framework import (
    extract_amounts, extract_dates, extract_beneficiaries,
    extract_routing, resolve_entity, score_transaction
)

# ── Tag 59/72 structured record parser ──────────────────────────────────────

TAG_FIELDS = {
    "20": re.compile(r':20:\s*(.+)', re.MULTILINE),            # transaction ref
    "23B": re.compile(r':23B:\s*(.+)', re.MULTILINE),          # bank operation code
    "32A": re.compile(r':32A:\s*(\d{6})([A-Z]{3})([\d,.]+)', re.MULTILINE),  # date+currency+amount
    "33B": re.compile(r':33B:\s*([A-Z]{3})([\d,.]+)', re.MULTILINE),         # currency+instructed amount
    "50K": re.compile(r':50K?:\s*(.+?)(?=\n:\d|$)', re.DOTALL),  # ordering customer
    "52A": re.compile(r':52A?:\s*(.+?)(?=\n:\d|$)', re.DOTALL),  # ordering institution
    "53A": re.compile(r':53A?:\s*(.+?)(?=\n:\d|$)', re.DOTALL),  # sender's correspondent
    "56A": re.compile(r':56A?:\s*(.+?)(?=\n:\d|$)', re.DOTALL),  # intermediary
    "57A": re.compile(r':57A?:\s*(.+?)(?=\n:\d|$)', re.DOTALL),  # account with institution
    "59": re.compile(r':59:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),    # beneficiary
    "70": re.compile(r':70:\s*(.+?)(?=\n:\d|$)', re.DOTALL),     # remittance info
    "71A": re.compile(r':71A:\s*(.+)', re.MULTILINE),            # charges
    "72": re.compile(r':72:\s*(.+?)(?=\n:\d|$)', re.DOTALL),     # sender to receiver info
}

# alternative tag format seen in JPMorgan internal records
ALT_TAG_FIELDS = {
    "tag59": re.compile(r'TAG\s*59\s*[:/]\s*(.+?)(?=TAG\s*\d|$)', re.DOTALL | re.IGNORECASE),
    "tag72": re.compile(r'TAG\s*72\s*[:/]\s*(.+?)(?=TAG\s*\d|$)', re.DOTALL | re.IGNORECASE),
}

# CHIPS-specific markers
CHIPS_MARKERS = [
    re.compile(r'CHIPS\s+(?:DEBIT|DB)', re.IGNORECASE),
    re.compile(r'CHIPS\s+(?:CREDIT|CR|RCVD)', re.IGNORECASE),
    re.compile(r'VIA\s+CHIPS', re.IGNORECASE),
    re.compile(r'RCVD\s+VIA\s+CHIPS', re.IGNORECASE),
]


def is_tag_format(text):
    """Check if text contains SWIFT/CHIPS tag-formatted wire records."""
    tag_count = 0
    for field, pat in TAG_FIELDS.items():
        if pat.search(text):
            tag_count += 1
    # also check alt format
    for field, pat in ALT_TAG_FIELDS.items():
        if pat.search(text):
            tag_count += 1
    return tag_count >= 2  # at least two tags present = structured record


def parse_tag_record(text, bates, dataset):
    """Parse a Tag 59/72 format wire record into a structured dict."""
    record = {
        "bates": bates,
        "dataset": dataset,
        "payment_type": "CHIPS",
        "extraction_method": "tag_59_72",
        "currency": "USD",
    }

    # extract standard SWIFT/CHIPS tags
    for field, pat in TAG_FIELDS.items():
        m = pat.search(text)
        if m:
            if field == "32A":
                # date + currency + amount
                date_str, currency, amount_str = m.group(1), m.group(2), m.group(3)
                record["currency"] = currency
                try:
                    y = 2000 + int(date_str[:2])
                    mo, d = int(date_str[2:4]), int(date_str[4:6])
                    from datetime import date
                    record["date"] = date(y, mo, d)
                except:
                    pass
                try:
                    record["amount"] = float(amount_str.replace(",", ""))
                except:
                    pass

            elif field == "59":
                raw = m.group(1).strip()
                raw = re.sub(r'\s+', ' ', raw)
                # clean account numbers from beneficiary
                name = re.sub(r'^/\d+\s*', '', raw)  # strip leading /acctnum
                name = name.split('\n')[0].strip()
                record["beneficiary_raw"] = name
                canonical, conf = resolve_entity(name)
                record["beneficiary_canonical"] = canonical
                record["entity_confidence"] = conf

            elif field == "50K":
                raw = m.group(1).strip()
                record["source_entity"] = re.sub(r'\s+', ' ', raw).split('\n')[0]

            elif field == "72":
                record["tag72_info"] = m.group(1).strip()

            elif field == "20":
                record["reference"] = m.group(1).strip()

    # try alt format
    for field, pat in ALT_TAG_FIELDS.items():
        m = pat.search(text)
        if m and field == "tag59" and not record.get("beneficiary_raw"):
            raw = m.group(1).strip()
            raw = re.sub(r'\s+', ' ', raw)
            record["beneficiary_raw"] = raw
            canonical, conf = resolve_entity(raw)
            record["beneficiary_canonical"] = canonical
            record["entity_confidence"] = conf

    # extract routing info
    routing = extract_routing(text)
    record["routing"] = routing

    # determine direction
    if re.search(r'CHIPS\s+(?:DEBIT|DB|SENT)', text, re.IGNORECASE):
        record["direction"] = "DEBIT"
    elif re.search(r'CHIPS\s+(?:CREDIT|CR|RCVD)', text, re.IGNORECASE):
        record["direction"] = "CREDIT"
    else:
        record["direction"] = "UNKNOWN"

    # fallback amount extraction if 32A didn't give us one
    if not record.get("amount"):
        amounts = extract_amounts(text)
        if amounts:
            record["amount"] = max(amounts)  # largest amount is usually the wire

    # fallback date extraction
    if not record.get("date"):
        dates = extract_dates(text)
        if dates:
            record["date"] = dates[0]

    record["raw_text"] = text[:2000]
    record["priority_score"] = score_transaction(record)

    return record


# ── Statement line parser ───────────────────────────────────────────────────

# Pattern for CHIPS entries on bank statements
# examples:
#   "Jun 24  CHIPS Debit VIA HSBC BANK USA  $25,000  $1,137,075.07"
#   "CHIPS DEBIT VIA BARCLAYS BANK PLC /0257  $25,000.00"
STATEMENT_CHIPS = re.compile(
    r'(?P<date_prefix>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})?'
    r'\s*'
    r'CHIPS\s+(?P<direction>DEBIT|CREDIT|DB|CR)'
    r'\s+'
    r'(?P<detail>.+?)$',
    re.IGNORECASE | re.MULTILINE
)

# balance at end of statement line
BALANCE_TRAIL = re.compile(r'\$?\s*([\d,]+\.\d{2})\s*$')


def parse_statement_chips(text, bates, dataset, statement_year=None):
    """Extract CHIPS entries from bank statement text."""
    records = []

    for m in STATEMENT_CHIPS.finditer(text):
        detail = m.group("detail")
        direction_raw = m.group("direction").upper()
        date_prefix = m.group("date_prefix")

        record = {
            "bates": bates,
            "dataset": dataset,
            "payment_type": "CHIPS",
            "extraction_method": "statement_line",
        }

        # direction
        record["direction"] = "DEBIT" if direction_raw in ("DEBIT", "DB") else "CREDIT"

        # date
        if date_prefix and statement_year:
            dates = extract_dates(f"{date_prefix}, {statement_year}")
            if dates:
                record["date"] = dates[0]

        # amounts from the detail line
        amounts = extract_amounts(detail)
        if amounts:
            # first amount is usually the transaction, last is running balance
            record["amount"] = amounts[0]
            if len(amounts) >= 2:
                record["balance_after"] = amounts[-1]

        # beneficiary from detail
        bens = extract_beneficiaries(detail)
        if bens:
            record["beneficiary_raw"] = bens[0]
            canonical, conf = resolve_entity(bens[0])
            record["beneficiary_canonical"] = canonical
            record["entity_confidence"] = conf

        # routing
        record["routing"] = extract_routing(detail)

        # intermediary bank from "VIA xxx"
        via = re.search(r'VIA\s+([A-Z][A-Z\s&.]+?)(?:\s*/\d|\s+(?:BEN|NC|SSN)|$)', detail, re.IGNORECASE)
        if via:
            record["routing"]["intermediary"] = via.group(1).strip()

        # reversal detection
        if re.search(r'CDT\s*RET|REVERSAL|RETURN|REJECTED', detail, re.IGNORECASE):
            record["is_reversal"] = True
            record["direction"] = "CREDIT"  # reversals are always credits

        record["raw_text"] = m.group(0)
        record["priority_score"] = score_transaction(record)
        records.append(record)

    return records


# ── Main extraction entry point ─────────────────────────────────────────────

def extract_chips(conn, limit=None, verbose=True):
    """
    Run full CHIPS extraction across the corpus.
    Returns list of parsed payment records.
    """
    from extraction_framework import get_doc_texts

    records = []
    docs_scanned = 0
    tag_records = 0
    stmt_records = 0

    if verbose:
        print("[CHIPS] Starting extraction...")
        print(f"[CHIPS] Scanning extracted_text for CHIPS keywords...")

    # query for CHIPS-related pages
    cur = conn.cursor()
    query = """
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE (
            et.text_content LIKE '%CHIPS DEBIT%'
            OR et.text_content LIKE '%CHIPS CREDIT%'
            OR et.text_content LIKE '%CHIPS DB%'
            OR et.text_content LIKE '%CHIPS CR%'
            OR et.text_content LIKE '%VIA CHIPS%'
            OR et.text_content LIKE '%RCVD VIA CHIPS%'
            OR et.text_content LIKE '%TAG 59%'
            OR et.text_content LIKE '%:59:%'
            OR et.text_content LIKE '%CHIPS SSN%'
            OR et.text_content LIKE '%CHIPS UID%'
        )
        ORDER BY f.title, et.page_num
    """
    if limit:
        query += f" LIMIT {limit}"

    cur.execute(query)
    rows = cur.fetchall()

    if verbose:
        print(f"[CHIPS] Found {len(rows)} pages to process")

    for bates, dataset, page_num, text in rows:
        if not text:
            continue
        docs_scanned += 1

        # try tag format first
        if is_tag_format(text):
            rec = parse_tag_record(text, bates, dataset)
            if rec.get("amount") or rec.get("beneficiary_raw"):
                records.append(rec)
                tag_records += 1

        # also check for statement-embedded CHIPS lines
        # (a page can have both tag records AND statement lines)
        stmt_year = None
        year_dates = extract_dates(text)
        if year_dates:
            stmt_year = year_dates[0].year

        stmt_recs = parse_statement_chips(text, bates, dataset, stmt_year)
        for r in stmt_recs:
            records.append(r)
            stmt_records += 1

    if verbose:
        print(f"[CHIPS] Extraction complete:")
        print(f"  Pages scanned: {docs_scanned}")
        print(f"  Tag 59/72 records: {tag_records}")
        print(f"  Statement line records: {stmt_records}")
        print(f"  Total records: {len(records)}")

        # entity breakdown
        entities = {}
        for r in records:
            ben = r.get("beneficiary_canonical", "UNKNOWN")
            entities[ben] = entities.get(ben, 0) + 1
        if entities:
            print(f"  Unique beneficiaries: {len(entities)}")
            for name, count in sorted(entities.items(), key=lambda x: -x[1])[:20]:
                print(f"    {name}: {count}")

        # amount summary
        total = sum(r.get("amount", 0) for r in records)
        print(f"  Total dollar volume: ${total:,.2f}")

    return records


if __name__ == "__main__":
    from extraction_framework import get_db
    conn = get_db()
    records = extract_chips(conn, verbose=True)
    conn.close()
