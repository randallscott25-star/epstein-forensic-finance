"""
swift_extractor.py — Extract SWIFT MT103 wire transfers from the EFTA corpus.

MT103 = Single Customer Credit Transfer. The standard international wire format.
Key fields: :20: ref, :32A: date+amount, :50K: originator, :59: beneficiary, :71A: charges

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import re
from datetime import date
from extraction_framework import (
    extract_amounts, extract_dates, extract_beneficiaries,
    extract_routing, resolve_entity, score_transaction, BIC_PATTERN
)

# ── MT103 message boundary detection ────────────────────────────────────────

MT103_START = re.compile(r'\{4:', re.MULTILINE)  # SWIFT message block 4 start
MT103_ALT_START = re.compile(r':20:[A-Z0-9/]+', re.MULTILINE)  # fallback: first tag

# fields specific to MT103
MT103_FIELDS = {
    "ref":         re.compile(r':20:\s*(.+?)$', re.MULTILINE),
    "related_ref": re.compile(r':21:\s*(.+?)$', re.MULTILINE),
    "op_code":     re.compile(r':23B:\s*(.+?)$', re.MULTILINE),
    "value_date":  re.compile(r':32A:(\d{6})([A-Z]{3})([\d,.]+)'),
    "currency_amt":re.compile(r':33B:([A-Z]{3})([\d,.]+)'),
    "originator":  re.compile(r':50[AK]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "ordering_inst":re.compile(r':52[AD]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "sender_corr": re.compile(r':53[ABD]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "receiver_corr":re.compile(r':54[ABD]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "intermediary": re.compile(r':56[ACD]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "acct_with":   re.compile(r':57[ABCD]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "beneficiary": re.compile(r':59[A]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "remittance":  re.compile(r':70:\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "charges":     re.compile(r':71A:\s*(.+?)$', re.MULTILINE),
    "sender_info": re.compile(r':72:\s*(.+?)(?=\n:\d|$)', re.DOTALL),
}


def is_mt103(text):
    """Quick check: does this text contain an MT103 message?"""
    # need at least :20: + :32A: + :59: to qualify
    has_ref = bool(MT103_FIELDS["ref"].search(text))
    has_value = bool(MT103_FIELDS["value_date"].search(text))
    has_ben = bool(MT103_FIELDS["beneficiary"].search(text))
    return (has_ref and has_value) or (has_ref and has_ben) or (has_value and has_ben)


def parse_mt103(text, bates, dataset):
    """Parse an MT103 SWIFT message into a payment record."""
    record = {
        "bates": bates,
        "dataset": dataset,
        "payment_type": "SWIFT",
        "direction": "DEBIT",  # MT103 = outgoing payment
        "extraction_method": "mt103",
        "currency": "USD",
    }

    # :32A: value date + currency + amount
    m = MT103_FIELDS["value_date"].search(text)
    if m:
        date_str, currency, amount_str = m.group(1), m.group(2), m.group(3)
        record["currency"] = currency
        try:
            y = 2000 + int(date_str[:2]) if int(date_str[:2]) < 50 else 1900 + int(date_str[:2])
            record["date"] = date(y, int(date_str[2:4]), int(date_str[4:6]))
        except:
            pass
        try:
            record["amount"] = float(amount_str.replace(",", ""))
        except:
            pass

    # :59: beneficiary
    m = MT103_FIELDS["beneficiary"].search(text)
    if m:
        raw = m.group(1).strip()
        # clean: strip account number prefix, collapse whitespace
        lines = [l.strip() for l in raw.split('\n') if l.strip()]
        # first line might be account number
        name_lines = []
        for line in lines:
            if re.match(r'^/?\d+$', line.strip()):
                record["source_account"] = line.strip().lstrip('/')
            else:
                name_lines.append(line)
        name = ' '.join(name_lines)
        name = re.sub(r'\s+', ' ', name).strip()
        record["beneficiary_raw"] = name
        canonical, conf = resolve_entity(name)
        record["beneficiary_canonical"] = canonical
        record["entity_confidence"] = conf

    # :50K: originator
    m = MT103_FIELDS["originator"].search(text)
    if m:
        raw = m.group(1).strip()
        record["source_entity"] = re.sub(r'\s+', ' ', raw).split('\n')[0]

    # :20: reference
    m = MT103_FIELDS["ref"].search(text)
    if m:
        record["reference"] = m.group(1).strip()

    # :72: sender to receiver info
    m = MT103_FIELDS["sender_info"].search(text)
    if m:
        record["notes"] = m.group(1).strip()

    # BIC codes — collect all
    bics = BIC_PATTERN.findall(text)
    noise = {"CRED", "DEBT", "ABAN", "BENM", "MARF", "IREF", "REMI", "UNRF"}
    bics = [b for b in bics if b not in noise and len(b) >= 8]
    routing = extract_routing(text)
    if bics:
        routing["bic_codes"] = list(set(bics))
    record["routing"] = routing

    # intermediary bank
    m = MT103_FIELDS["intermediary"].search(text) or MT103_FIELDS["acct_with"].search(text)
    if m:
        record["routing"]["intermediary"] = re.sub(r'\s+', ' ', m.group(1).strip()).split('\n')[0]

    # fallbacks
    if not record.get("amount"):
        amounts = extract_amounts(text)
        if amounts:
            record["amount"] = max(amounts)

    if not record.get("date"):
        dates = extract_dates(text)
        if dates:
            record["date"] = dates[0]

    record["raw_text"] = text[:2000]
    record["priority_score"] = score_transaction(record)
    return record


# ── Statement-embedded SWIFT references ─────────────────────────────────────

SWIFT_STMT_PATTERN = re.compile(
    r'(?:SWIFT|MT\s*103|INTL?\s+WIRE)\s+'
    r'(?P<direction>DEBIT|CREDIT|DB|CR|SENT|RCVD)'
    r'\s+(?P<detail>.+?)$',
    re.IGNORECASE | re.MULTILINE
)

def parse_statement_swift(text, bates, dataset, statement_year=None):
    """Extract SWIFT-related lines from bank statements."""
    records = []

    for m in SWIFT_STMT_PATTERN.finditer(text):
        detail = m.group("detail")
        direction = m.group("direction").upper()

        record = {
            "bates": bates,
            "dataset": dataset,
            "payment_type": "SWIFT",
            "extraction_method": "statement_line",
            "direction": "DEBIT" if direction in ("DEBIT", "DB", "SENT") else "CREDIT",
        }

        amounts = extract_amounts(detail)
        if amounts:
            record["amount"] = amounts[0]
            if len(amounts) >= 2:
                record["balance_after"] = amounts[-1]

        bens = extract_beneficiaries(detail)
        if bens:
            record["beneficiary_raw"] = bens[0]
            canonical, conf = resolve_entity(bens[0])
            record["beneficiary_canonical"] = canonical
            record["entity_confidence"] = conf

        record["routing"] = extract_routing(detail)
        record["raw_text"] = m.group(0)
        record["priority_score"] = score_transaction(record)
        records.append(record)

    return records


# ── Main extraction ─────────────────────────────────────────────────────────

def extract_swift(conn, limit=None, verbose=True):
    """Run full SWIFT extraction across the corpus."""
    records = []
    docs_scanned = 0
    mt103_count = 0
    stmt_count = 0

    if verbose:
        print("[SWIFT] Starting extraction...")

    cur = conn.cursor()
    query = """
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE (
            et.text_content LIKE '%:20:%'
            AND (et.text_content LIKE '%:32A:%' OR et.text_content LIKE '%:59:%')
        )
        OR et.text_content LIKE '%MT103%'
        OR et.text_content LIKE '%MT 103%'
        OR et.text_content LIKE '%SWIFT TRANSFER%'
        OR et.text_content LIKE '%SWIFT WIRE%'
        OR et.text_content LIKE '%SWIFT DEBIT%'
        OR et.text_content LIKE '%SWIFT CREDIT%'
        ORDER BY f.title, et.page_num
    """
    if limit:
        query += f" LIMIT {limit}"

    cur.execute(query)
    rows = cur.fetchall()

    if verbose:
        print(f"[SWIFT] Found {len(rows)} pages to process")

    for bates, dataset, page_num, text in rows:
        if not text:
            continue
        docs_scanned += 1

        if is_mt103(text):
            rec = parse_mt103(text, bates, dataset)
            if rec.get("amount") or rec.get("beneficiary_raw"):
                records.append(rec)
                mt103_count += 1

        stmt_recs = parse_statement_swift(text, bates, dataset)
        for r in stmt_recs:
            records.append(r)
            stmt_count += 1

    if verbose:
        print(f"[SWIFT] Extraction complete:")
        print(f"  Pages scanned: {docs_scanned}")
        print(f"  MT103 records: {mt103_count}")
        print(f"  Statement line records: {stmt_count}")
        print(f"  Total records: {len(records)}")

        entities = {}
        for r in records:
            ben = r.get("beneficiary_canonical", "UNKNOWN")
            entities[ben] = entities.get(ben, 0) + 1
        if entities:
            print(f"  Unique beneficiaries: {len(entities)}")
            for name, count in sorted(entities.items(), key=lambda x: -x[1])[:20]:
                print(f"    {name}: {count}")

        total = sum(r.get("amount", 0) for r in records)
        print(f"  Total dollar volume: ${total:,.2f}")

    return records


if __name__ == "__main__":
    from extraction_framework import get_db
    conn = get_db()
    records = extract_swift(conn, verbose=True)
    conn.close()
