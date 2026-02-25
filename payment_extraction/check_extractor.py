"""
check_extractor.py — Extract check payments from EFTA corpus.

Checks are lower priority but still valuable: named payees (Maxwell Check #1070 visible
in scope scan), large round-number payments, and checks to entities vs. individuals.

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import re
from extraction_framework import (
    extract_amounts, extract_dates, resolve_entity, score_transaction
)

# ── Check patterns ──────────────────────────────────────────────────────────

CHECK_LINE = re.compile(
    r'(?P<date_prefix>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})?'
    r'\s*'
    r'(?:CHECK|CHK|PAID\s+CHECK)\s*#?\s*(?P<check_num>\d{3,6})'
    r'\s*'
    r'(?P<detail>.*?)$',
    re.IGNORECASE | re.MULTILINE
)

# check image / cleared check format (sometimes has payee)
CHECK_IMAGE = re.compile(
    r'(?:PAY\s+TO\s+THE\s+ORDER\s+OF|PAYEE|PAY\s+TO)[:\s]+(?P<payee>[A-Z][A-Z\s.,\'-]{3,60})',
    re.IGNORECASE
)

# check register / list format
CHECK_REGISTER = re.compile(
    r'#?\s*(?P<num>\d{3,6})\s+'
    r'(?P<date>\d{1,2}[/-]\d{1,2}[/-]\d{2,4})?\s*'
    r'(?P<payee>[A-Z][A-Z\s.,\'-]{3,40})?\s*'
    r'\$?\s*(?P<amount>[\d,]+(?:\.\d{2})?)',
    re.MULTILINE
)


def parse_checks(text, bates, dataset, statement_year=None):
    """Extract check entries from bank statement or check register text."""
    records = []

    # statement line format
    for m in CHECK_LINE.finditer(text):
        check_num = m.group("check_num")
        detail = m.group("detail") or ""
        date_prefix = m.group("date_prefix")

        record = {
            "bates": bates,
            "dataset": dataset,
            "payment_type": "CHECK",
            "direction": "DEBIT",
            "extraction_method": "statement_line",
            "check_number": check_num,
            "routing": {},
        }

        if date_prefix and statement_year:
            dates = extract_dates(f"{date_prefix}, {statement_year}")
            if dates:
                record["date"] = dates[0]

        amounts = extract_amounts(detail)
        if amounts:
            record["amount"] = amounts[0]
            if len(amounts) >= 2:
                record["balance_after"] = amounts[-1]

        # check for payee in the detail
        payee_match = CHECK_IMAGE.search(detail)
        if payee_match:
            raw = payee_match.group("payee").strip()
            record["beneficiary_raw"] = raw
            canonical, conf = resolve_entity(raw)
            record["beneficiary_canonical"] = canonical
            record["entity_confidence"] = conf

        record["raw_text"] = m.group(0)
        record["priority_score"] = score_transaction(record)
        records.append(record)

    # also look for check images / cleared check pages with payee info
    for m in CHECK_IMAGE.finditer(text):
        # only add if we didn't already capture this from a statement line
        payee = m.group("payee").strip()
        # find nearby check number
        nearby = re.search(r'(?:CHECK|CHK)\s*#?\s*(\d{3,6})', text[max(0, m.start()-200):m.end()+200], re.IGNORECASE)

        already_captured = any(
            r.get("beneficiary_raw", "").upper() == payee.upper() and r.get("bates") == bates
            for r in records
        )
        if already_captured:
            continue

        record = {
            "bates": bates,
            "dataset": dataset,
            "payment_type": "CHECK",
            "direction": "DEBIT",
            "extraction_method": "check_image",
            "routing": {},
        }

        record["beneficiary_raw"] = payee
        canonical, conf = resolve_entity(payee)
        record["beneficiary_canonical"] = canonical
        record["entity_confidence"] = conf

        if nearby:
            record["check_number"] = nearby.group(1)

        amounts = extract_amounts(text[max(0, m.start()-100):m.end()+200])
        if amounts:
            record["amount"] = amounts[0]

        dates = extract_dates(text[max(0, m.start()-200):m.end()+200])
        if dates:
            record["date"] = dates[0]

        record["raw_text"] = text[max(0, m.start()-50):m.end()+100]
        record["priority_score"] = score_transaction(record)
        records.append(record)

    return records


def extract_checks(conn, limit=None, verbose=True):
    """Run full check extraction."""
    records = []
    docs_scanned = 0

    if verbose:
        print("[CHECK] Starting extraction...")

    cur = conn.cursor()
    query = """
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE (
            et.text_content LIKE '%CHECK #%'
            OR et.text_content LIKE '%CHK #%'
            OR et.text_content LIKE '%PAID CHECK%'
            OR et.text_content LIKE '%PAY TO THE ORDER%'
            OR (et.text_content LIKE '%CHECK %' AND et.text_content LIKE '%$%')
        )
        ORDER BY f.title, et.page_num
    """
    if limit:
        query += f" LIMIT {limit}"

    cur.execute(query)
    rows = cur.fetchall()

    if verbose:
        print(f"[CHECK] Found {len(rows)} pages to process")

    for bates, dataset, page_num, text in rows:
        if not text:
            continue
        docs_scanned += 1

        stmt_year = None
        dates = extract_dates(text)
        if dates:
            stmt_year = dates[0].year

        page_records = parse_checks(text, bates, dataset, stmt_year)
        records.extend(page_records)

    if verbose:
        print(f"[CHECK] Extraction complete:")
        print(f"  Pages scanned: {docs_scanned}")
        print(f"  Check records: {len(records)}")
        with_payee = sum(1 for r in records if r.get("beneficiary_raw"))
        print(f"  With named payee: {with_payee}")
        total = sum(r.get("amount", 0) for r in records)
        print(f"  Total dollar volume: ${total:,.2f}")

        # notable checks
        for r in sorted(records, key=lambda x: x.get("priority_score", 0), reverse=True)[:10]:
            ben = r.get("beneficiary_canonical", r.get("check_number", "?"))
            print(f"    Score {r.get('priority_score', 0):3d} | #{r.get('check_number', '?'):>6s} | "
                  f"${r.get('amount', 0):>12,.2f} | {ben}")

    return records


if __name__ == "__main__":
    from extraction_framework import get_db
    conn = get_db()
    records = extract_checks(conn, verbose=True)
    conn.close()
