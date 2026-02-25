"""
statement_chain.py — Build account balance timelines from monthly statement headers.

The June 2004 balance walk proved statements link via opening/closing balances.
This script builds the full chain for every Epstein account, then identifies
"orphan" balance movements — periods where the balance changes more than the
sum of extracted transactions, meaning we're missing payments.

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import re
from extraction_framework import extract_amounts, extract_dates

# ── Statement header patterns ───────────────────────────────────────────────

# account number
ACCT_PATTERN = re.compile(
    r'(?:ACCT|ACCOUNT)\s*(?:#|NO|NUMBER)?[:\s]*(\d{3}[-\s]?\d{5,8})',
    re.IGNORECASE
)

# account name / entity
ACCT_NAME = re.compile(
    r'(?:ACCOUNT\s+NAME|STATEMENT\s+FOR)[:\s]+([A-Z][A-Z\s.,\'-]{3,60})',
    re.IGNORECASE
)

# statement period
PERIOD_PATTERN = re.compile(
    r'(?:STATEMENT\s+PERIOD|PERIOD)[:\s]*'
    r'(\w+\s+\d{1,2},?\s+\d{4})\s*(?:TO|THROUGH|–|-)\s*(\w+\s+\d{1,2},?\s+\d{4})',
    re.IGNORECASE
)

# balances
OPENING_BAL = re.compile(
    r'(?:OPENING|BEGINNING|PREVIOUS|PRIOR)\s+BALANCE[:\s]*\$?\s*([\d,]+\.\d{2})',
    re.IGNORECASE
)
CLOSING_BAL = re.compile(
    r'(?:CLOSING|ENDING|NEW)\s+BALANCE[:\s]*\$?\s*([\d,]+\.\d{2})',
    re.IGNORECASE
)
TOTAL_CREDITS = re.compile(
    r'TOTAL\s+(?:CREDITS|DEPOSITS)[:\s]*\$?\s*([\d,]+\.\d{2})',
    re.IGNORECASE
)
TOTAL_DEBITS = re.compile(
    r'TOTAL\s+(?:DEBITS|WITHDRAWALS|CHECKS?\s+AND\s+DEBITS)[:\s]*\$?\s*([\d,]+\.\d{2})',
    re.IGNORECASE
)


def parse_statement_header(text, bates, dataset):
    """Extract statement metadata from a page likely containing a statement header."""
    header = {
        "bates_start": bates,
        "dataset": dataset,
    }

    # account number
    m = ACCT_PATTERN.search(text)
    if m:
        header["account_number"] = m.group(1).replace(" ", "").replace("-", "-")

    # account name
    m = ACCT_NAME.search(text)
    if m:
        header["account_name"] = m.group(1).strip()

    # period
    m = PERIOD_PATTERN.search(text)
    if m:
        start_dates = extract_dates(m.group(1))
        end_dates = extract_dates(m.group(2))
        if start_dates:
            header["statement_start"] = str(start_dates[0])
        if end_dates:
            header["statement_end"] = str(end_dates[0])

    # balances
    for label, pattern, key in [
        ("opening", OPENING_BAL, "opening_balance"),
        ("closing", CLOSING_BAL, "closing_balance"),
        ("credits", TOTAL_CREDITS, "total_credits"),
        ("debits", TOTAL_DEBITS, "total_debits"),
    ]:
        m = pattern.search(text)
        if m:
            try:
                header[key] = float(m.group(1).replace(",", ""))
            except:
                pass

    # only return if we got something useful
    has_balance = "opening_balance" in header or "closing_balance" in header
    has_acct = "account_number" in header
    if has_balance or has_acct:
        return header
    return None


def build_statement_chain(conn, limit=None, verbose=True):
    """
    Scan corpus for statement headers and build account timelines.
    Returns list of statement records and a gap analysis.
    """
    statements = []
    pages_scanned = 0

    if verbose:
        print("[CHAIN] Building statement chain...")

    cur = conn.cursor()
    # look for pages that have statement header markers
    query = """
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE (
            (et.text_content LIKE '%OPENING BALANCE%' OR et.text_content LIKE '%BEGINNING BALANCE%')
            AND (et.text_content LIKE '%CLOSING BALANCE%' OR et.text_content LIKE '%ENDING BALANCE%')
        )
        OR (
            et.text_content LIKE '%STATEMENT PERIOD%'
            AND et.text_content LIKE '%BALANCE%'
        )
        ORDER BY f.title, et.page_num
    """
    if limit:
        query += f" LIMIT {limit}"

    cur.execute(query)
    rows = cur.fetchall()

    if verbose:
        print(f"[CHAIN] Found {len(rows)} potential statement header pages")

    for bates, dataset, page_num, text in rows:
        if not text:
            continue
        pages_scanned += 1

        header = parse_statement_header(text, bates, dataset)
        if header:
            statements.append(header)

    # group by account and sort by date
    accounts = {}
    for s in statements:
        acct = s.get("account_number", "UNKNOWN")
        accounts.setdefault(acct, []).append(s)

    for acct, stmts in accounts.items():
        stmts.sort(key=lambda x: x.get("statement_start", ""))

    # gap analysis: check continuity
    gaps = []
    for acct, stmts in accounts.items():
        for i in range(1, len(stmts)):
            prev_close = stmts[i-1].get("closing_balance")
            curr_open = stmts[i].get("opening_balance")
            if prev_close is not None and curr_open is not None:
                if abs(prev_close - curr_open) > 0.01:
                    gaps.append({
                        "account": acct,
                        "prev_period_end": stmts[i-1].get("statement_end"),
                        "curr_period_start": stmts[i].get("statement_start"),
                        "prev_closing": prev_close,
                        "curr_opening": curr_open,
                        "discrepancy": curr_open - prev_close,
                        "prev_bates": stmts[i-1].get("bates_start"),
                        "curr_bates": stmts[i].get("bates_start"),
                    })

    if verbose:
        print(f"[CHAIN] Results:")
        print(f"  Pages scanned: {pages_scanned}")
        print(f"  Statement headers found: {len(statements)}")
        print(f"  Unique accounts: {len(accounts)}")
        for acct, stmts in sorted(accounts.items()):
            name = stmts[0].get("account_name", "")
            date_range = f"{stmts[0].get('statement_start', '?')} → {stmts[-1].get('statement_end', '?')}"
            print(f"    {acct}: {name} ({len(stmts)} statements, {date_range})")

        if gaps:
            print(f"\n  ⚠ Balance continuity gaps: {len(gaps)}")
            for g in gaps:
                print(f"    Account {g['account']}: "
                      f"{g['prev_period_end']} → {g['curr_period_start']} | "
                      f"Discrepancy: ${g['discrepancy']:,.2f} | "
                      f"Bates: {g['prev_bates']} → {g['curr_bates']}")
        else:
            print(f"  ✓ No balance continuity gaps found")

    return statements, gaps, accounts


def insert_statement_chain(conn, statements):
    """Insert statement chain records into the database."""
    from datetime import datetime
    cur = conn.cursor()
    now = datetime.now().isoformat()
    inserted = 0

    for s in statements:
        # check for existing
        if s.get("bates_start"):
            cur.execute("SELECT id FROM statement_chain WHERE bates_start = ?", (s["bates_start"],))
            if cur.fetchone():
                continue

        cur.execute("""
            INSERT INTO statement_chain (
                account_number, account_name, statement_start, statement_end,
                opening_balance, closing_balance, total_credits, total_debits,
                bates_start, extracted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s.get("account_number"),
            s.get("account_name"),
            s.get("statement_start"),
            s.get("statement_end"),
            s.get("opening_balance"),
            s.get("closing_balance"),
            s.get("total_credits"),
            s.get("total_debits"),
            s.get("bates_start"),
            now,
        ))
        inserted += 1

    conn.commit()
    print(f"[CHAIN] Inserted {inserted} statement records")
    return inserted


if __name__ == "__main__":
    from extraction_framework import get_db
    conn = get_db()
    statements, gaps, accounts = build_statement_chain(conn, verbose=True)
    conn.close()
