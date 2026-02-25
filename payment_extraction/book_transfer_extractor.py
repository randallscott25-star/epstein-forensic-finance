"""
book_transfer_extractor.py — Extract Book Transfers from EFTA corpus.

Book transfers = inter-account movements within same bank.
Critical for: reversal detection (bounced payments), inter-entity funding flows,
FX operations, and paired transaction forensics.

The Mandelson bounce (Jun 24 2004) proved this category holds forensic gold.

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import re
from extraction_framework import (
    extract_amounts, extract_dates, extract_beneficiaries,
    extract_routing, resolve_entity, score_transaction
)

# ── Book Transfer patterns ──────────────────────────────────────────────────

BT_PATTERNS = [
    # standard statement format
    re.compile(
        r'(?P<date_prefix>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})?'
        r'\s*'
        r'(?:BOOK\s+TRANSFER|BK\s+TRANS(?:FER)?|CB\s+FUNDS\s+TRANS(?:FER)?)'
        r'\s+'
        r'(?P<direction>DEBIT|CREDIT|DB|CR|DBT|CDT)'
        r'\s*'
        r'(?P<detail>.+?)$',
        re.IGNORECASE | re.MULTILINE
    ),
    # reversal-specific format
    re.compile(
        r'(?P<date_prefix>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})?'
        r'\s*'
        r'(?:CB\s+FUNDS\s+TRANS\s+SAMEDAY\s+CDT\s+RET)'
        r'\s*'
        r'(?P<detail>.+?)$',
        re.IGNORECASE | re.MULTILINE
    ),
]

# reversal indicators
REVERSAL_MARKERS = re.compile(
    r'CDT\s*RET|CREDIT\s*RETURN|REVERSAL\s+OF\s+ENTRY|'
    r'RETURN(?:ED)?|REJECTED|REFUSED|FAILED|'
    r'NEED\s+(?:BBK|VALID|CORRECT)|INVALID\s+(?:ACCT|ROUTING|BIC)',
    re.IGNORECASE
)

# FX marker
FX_MARKER = re.compile(r'(?:FX|FOREIGN\s+EXCHANGE|F/X|FOREX)', re.IGNORECASE)

# internal transfer (DDA to DDA, MMIA, Brokerage)
INTERNAL_PATTERN = re.compile(
    r'(?P<date_prefix>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2})?'
    r'\s*'
    r'(?:INTERNAL\s+FUNDS?\s+TRANS(?:FER)?)'
    r'\s*'
    r'(?P<detail>.+?)$',
    re.IGNORECASE | re.MULTILINE
)

# account type identifiers
ACCT_TYPES = re.compile(
    r'(?:DDA|MMIA|BRKRG|BROKERAGE|SAVINGS|TRUST|ESCROW|FBO)',
    re.IGNORECASE
)


def parse_book_transfers(text, bates, dataset, statement_year=None):
    """Extract book transfer and internal transfer entries from statement text."""
    records = []

    # book transfers
    for pat in BT_PATTERNS:
        for m in pat.finditer(text):
            groups = m.groupdict()
            detail = groups.get("detail", "")
            direction_raw = groups.get("direction", "")
            date_prefix = groups.get("date_prefix")

            record = {
                "bates": bates,
                "dataset": dataset,
                "payment_type": "BOOK_TRANSFER",
                "extraction_method": "statement_line",
            }

            # direction
            if direction_raw:
                record["direction"] = "DEBIT" if direction_raw.upper() in ("DEBIT", "DB", "DBT") else "CREDIT"
            elif "CDT RET" in m.group(0).upper():
                record["direction"] = "CREDIT"
            else:
                record["direction"] = "UNKNOWN"

            # date
            if date_prefix and statement_year:
                dates = extract_dates(f"{date_prefix}, {statement_year}")
                if dates:
                    record["date"] = dates[0]

            # amounts
            full_line = detail if detail else m.group(0)
            amounts = extract_amounts(full_line)
            if amounts:
                record["amount"] = amounts[0]
                if len(amounts) >= 2:
                    record["balance_after"] = amounts[-1]

            # beneficiary
            bens = extract_beneficiaries(full_line)
            if bens:
                record["beneficiary_raw"] = bens[0]
                canonical, conf = resolve_entity(bens[0])
                record["beneficiary_canonical"] = canonical
                record["entity_confidence"] = conf

            # reversal detection
            is_reversal = bool(REVERSAL_MARKERS.search(m.group(0)))
            record["is_reversal"] = is_reversal
            if is_reversal:
                # try to extract the original date reference
                orig_date = re.search(r'DD\s*(\d{2})/(\d{2})/(\d{2,4})', m.group(0))
                if orig_date:
                    record["reversal_ref"] = f"{orig_date.group(1)}/{orig_date.group(2)}/{orig_date.group(3)}"
                # extract reason
                reason = re.search(r'(?:NEED|INVALID|REJECTED|REFUSED)\s+(.+?)(?:\s+\$|$)', m.group(0), re.IGNORECASE)
                if reason:
                    record["notes"] = reason.group(0).strip()

            # FX flag
            if FX_MARKER.search(m.group(0)):
                record["notes"] = (record.get("notes", "") + " [FX OPERATION]").strip()

            # routing
            record["routing"] = extract_routing(full_line)

            record["raw_text"] = m.group(0)
            record["priority_score"] = score_transaction(record)
            records.append(record)

    # internal transfers
    for m in INTERNAL_PATTERN.finditer(text):
        detail = m.group("detail")
        date_prefix = m.group("date_prefix")

        record = {
            "bates": bates,
            "dataset": dataset,
            "payment_type": "INTERNAL_TRANSFER",
            "extraction_method": "statement_line",
        }

        # detect account types in the detail to determine flow direction
        acct_matches = ACCT_TYPES.findall(detail)
        if acct_matches:
            record["notes"] = " → ".join(a.upper() for a in acct_matches)

        # direction heuristic: if DDA appears and amount is negative or detail says debit
        if re.search(r'DEBIT|DB', detail, re.IGNORECASE):
            record["direction"] = "DEBIT"
        elif re.search(r'CREDIT|CR', detail, re.IGNORECASE):
            record["direction"] = "CREDIT"
        else:
            record["direction"] = "DEBIT"  # internal transfers from checking are usually debits

        if date_prefix and statement_year:
            dates = extract_dates(f"{date_prefix}, {statement_year}")
            if dates:
                record["date"] = dates[0]

        amounts = extract_amounts(detail)
        if amounts:
            record["amount"] = amounts[0]
            if len(amounts) >= 2:
                record["balance_after"] = amounts[-1]

        record["routing"] = {}
        record["raw_text"] = m.group(0)
        record["priority_score"] = score_transaction(record)
        records.append(record)

    return records


# ── Main extraction ─────────────────────────────────────────────────────────

def extract_book_transfers(conn, limit=None, verbose=True):
    """Run full Book Transfer + Internal Transfer extraction."""
    records = []
    docs_scanned = 0

    if verbose:
        print("[BOOK] Starting extraction...")

    cur = conn.cursor()
    query = """
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE (
            et.text_content LIKE '%BOOK TRANSFER%'
            OR et.text_content LIKE '%BK TRANS%'
            OR et.text_content LIKE '%CB FUNDS TRANS%'
            OR et.text_content LIKE '%CDT RET%'
            OR et.text_content LIKE '%REVERSAL OF ENTRY%'
            OR et.text_content LIKE '%INTERNAL FUNDS TRANS%'
            OR et.text_content LIKE '%INTERNAL FUND TRANS%'
        )
        ORDER BY f.title, et.page_num
    """
    if limit:
        query += f" LIMIT {limit}"

    cur.execute(query)
    rows = cur.fetchall()

    if verbose:
        print(f"[BOOK] Found {len(rows)} pages to process")

    for bates, dataset, page_num, text in rows:
        if not text:
            continue
        docs_scanned += 1

        stmt_year = None
        dates = extract_dates(text)
        if dates:
            stmt_year = dates[0].year

        page_records = parse_book_transfers(text, bates, dataset, stmt_year)
        records.extend(page_records)

    if verbose:
        bt_count = sum(1 for r in records if r["payment_type"] == "BOOK_TRANSFER")
        it_count = sum(1 for r in records if r["payment_type"] == "INTERNAL_TRANSFER")
        rev_count = sum(1 for r in records if r.get("is_reversal"))

        print(f"[BOOK] Extraction complete:")
        print(f"  Pages scanned: {docs_scanned}")
        print(f"  Book transfers: {bt_count}")
        print(f"  Internal transfers: {it_count}")
        print(f"  Reversals detected: {rev_count}")
        print(f"  Total records: {len(records)}")

        total = sum(r.get("amount", 0) for r in records)
        print(f"  Total dollar volume: ${total:,.2f}")

        # reversal breakdown
        if rev_count:
            print(f"  Reversal details:")
            for r in records:
                if r.get("is_reversal") and r.get("amount"):
                    ben = r.get("beneficiary_canonical", "UNKNOWN")
                    print(f"    {r.get('date', '?')} | ${r['amount']:,.2f} | {ben} | {r.get('notes', '')}")

    return records


if __name__ == "__main__":
    from extraction_framework import get_db
    conn = get_db()
    records = extract_book_transfers(conn, verbose=True)
    conn.close()
