"""
extraction_framework.py — Core infrastructure for the full payment extraction pipeline.
Shared config, regex patterns, DB helpers, entity resolver, scorer, transaction linker.

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import sqlite3
import re
import os
from collections import defaultdict
from difflib import SequenceMatcher
from datetime import datetime, timedelta

# ── DB paths (Mac) ──────────────────────────────────────────────────────────

DB_PATHS = [
    os.path.expanduser("~/Desktop/epstein_files.db"),                           # primary
    "/Volumes/My Book/epstein_project/epstein_files.db",                        # external HDD fallback
]

def get_db():
    for p in DB_PATHS:
        if os.path.exists(p):
            print(f"[DB] Connected: {p}")
            conn = sqlite3.connect(p)
            conn.row_factory = sqlite3.Row
            return conn
    raise FileNotFoundError(f"No database found. Checked: {DB_PATHS}")


# ── Payment type definitions ────────────────────────────────────────────────

PAYMENT_TYPES = {
    "CHIPS": {
        "search_patterns": [
            r"CHIPS\s+(?:DEBIT|CREDIT|RCVD|SENT)",
            r"VIA\s+(?:CHIPS|HSBC|BARCLAYS|CITIBANK|DEUTSCHE)",
            r"TAG\s*(?:59|72)\s*[:/]",
            r"CHIPS\s+(?:SSN|UID|SEQ)\s*[:#]?\s*\d+",
        ],
        "priority": 1,
        "signal": "HIGH",
    },
    "SWIFT": {
        "search_patterns": [
            r":20:[A-Z0-9]+",              # MT103 reference
            r":32A:\d{6}[A-Z]{3}[\d,]+",   # value date + currency + amount
            r":59:[/\w]",                   # beneficiary
            r"MT\s*103",
            r"SWIFT\s+(?:TRANSFER|MESSAGE|WIRE)",
            r"[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?",  # BIC code shape
        ],
        "priority": 2,
        "signal": "HIGH",
    },
    "BOOK_TRANSFER": {
        "search_patterns": [
            r"BOOK\s+TRANSFER\s+(?:DEBIT|CREDIT)",
            r"BK\s+TRANS\s+(?:DB|CR|CDT|DBT)",
            r"CB\s+FUNDS\s+TRANS",
            r"CDT\s+RET",    # credit return (reversal)
            r"REVERSAL\s+OF\s+ENTRY",
        ],
        "priority": 3,
        "signal": "HIGH",
    },
    "INTERNAL_TRANSFER": {
        "search_patterns": [
            r"INTERNAL\s+FUNDS?\s+TRANS",
            r"(?:DDA|MMIA|BRKRG)\s*(?:→|TO|FROM)\s*(?:DDA|MMIA|BRKRG)",
            r"INTERNAL\s+(?:DEBIT|CREDIT)",
            r"INTER-?ACCOUNT\s+TRANSFER",
        ],
        "priority": 4,
        "signal": "MEDIUM",
    },
    "CHECKS": {
        "search_patterns": [
            r"CHECK\s*#?\s*\d{3,6}",
            r"CHK\s*#?\s*\d{3,6}",
            r"PAID\s+CHECK\s+\d+",
        ],
        "priority": 5,
        "signal": "MEDIUM",
    },
    "FEDWIRE": {
        "search_patterns": [
            r"FEDWIRE\s+(?:DEBIT|CREDIT|SENT|RCVD)",
            r"FED\s+WIRE\s+(?:DEBIT|CREDIT)",
            r"FW\s+(?:DB|CR|DEBIT|CREDIT)",
        ],
        "priority": 6,
        "signal": "RE-SWEEP",
    },
}


# ── Amount extraction ───────────────────────────────────────────────────────

AMOUNT_PATTERN = re.compile(
    r'\$\s*([\d,]+(?:\.\d{2})?)'       # $1,234.56 or $1234
    r'|'
    r'([\d,]{4,}(?:\.\d{2})?)\s*USD'   # 1,234.56 USD
)

def extract_amounts(text):
    """Pull all dollar amounts from a text block. Returns list of floats."""
    hits = []
    for m in AMOUNT_PATTERN.finditer(text):
        raw = m.group(1) or m.group(2)
        try:
            val = float(raw.replace(",", ""))
            if val >= 100:  # skip dust
                hits.append(val)
        except ValueError:
            continue
    return hits


# ── Date extraction ─────────────────────────────────────────────────────────

DATE_PATTERNS = [
    (re.compile(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'), "MDY"),
    (re.compile(r'(\w{3,9})\s+(\d{1,2}),?\s+(\d{4})'), "MONTH_D_Y"),
    (re.compile(r'(\d{4})-(\d{2})-(\d{2})'), "ISO"),
    (re.compile(r':32A:(\d{6})'), "SWIFT_32A"),  # YYMMDD in MT103
]

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    "january": 1, "february": 2, "march": 3, "april": 4,
    "june": 6, "july": 7, "august": 8, "september": 9,
    "october": 10, "november": 11, "december": 12,
}

def extract_dates(text):
    """Pull dates from text. Returns list of datetime.date objects."""
    results = []
    for pat, fmt in DATE_PATTERNS:
        for m in pat.finditer(text):
            try:
                if fmt == "MDY":
                    mo, d, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
                    if y < 100:
                        y += 2000 if y < 50 else 1900
                    results.append(datetime(y, mo, d).date())
                elif fmt == "MONTH_D_Y":
                    mo = MONTHS.get(m.group(1).lower()[:3])
                    if mo:
                        results.append(datetime(int(m.group(3)), mo, int(m.group(2))).date())
                elif fmt == "ISO":
                    results.append(datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date())
                elif fmt == "SWIFT_32A":
                    s = m.group(1)
                    y, mo, d = 2000 + int(s[:2]), int(s[2:4]), int(s[4:6])
                    results.append(datetime(y, mo, d).date())
            except (ValueError, TypeError):
                continue
    return results


# ── Beneficiary / entity extraction ─────────────────────────────────────────

# Tag 59 (SWIFT/CHIPS beneficiary) — capture everything after the tag marker
TAG59_PATTERN = re.compile(
    r'(?:TAG\s*59|:59:?|/59[:/])\s*[:/]?\s*(.+?)(?=\n(?:TAG|:\d|/\d)|$)',
    re.IGNORECASE | re.DOTALL
)

# Tag 72 (sender-to-receiver info)
TAG72_PATTERN = re.compile(
    r'(?:TAG\s*72|:72:?|/72[:/])\s*[:/]?\s*(.+?)(?=\n(?:TAG|:\d|/\d)|$)',
    re.IGNORECASE | re.DOTALL
)

# Named beneficiary on statement lines
BEN_PATTERNS = [
    re.compile(r'(?:BEN|BENF?|BENEFICIARY)[:\s]+([A-Z][A-Z\s.,\'-]{3,50})', re.IGNORECASE),
    re.compile(r'(?:NC|ACCT?\s*NAME)[:\s]+([A-Z][A-Z\s.,\'-]{3,50})', re.IGNORECASE),
    re.compile(r'(?:FAVOR|FBO|F/O)[:\s]+([A-Z][A-Z\s.,\'-]{3,50})', re.IGNORECASE),
    re.compile(r'(?:PAY\s*TO|PAYEE)[:\s]+([A-Z][A-Z\s.,\'-]{3,50})', re.IGNORECASE),
]

# CHIPS SSN (not social security — CHIPS participant number)
SSN_PATTERN = re.compile(r'(?:SSN|CHIPS\s*(?:SSN|UID))\s*[:#]?\s*(\d{5,9})', re.IGNORECASE)

# SWIFT BIC
BIC_PATTERN = re.compile(r'\b([A-Z]{4}[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?)\b')

# Check number
CHECK_PATTERN = re.compile(r'(?:CHECK|CHK)\s*#?\s*(\d{3,6})', re.IGNORECASE)


def extract_beneficiaries(text):
    """Extract all beneficiary names from text. Returns list of strings."""
    names = []

    for m in TAG59_PATTERN.finditer(text):
        name = m.group(1).strip()
        # clean up multi-line tag content
        name = re.sub(r'\s+', ' ', name)
        name = name.split('/')[0].strip()  # drop account numbers after /
        if len(name) > 3 and not name.isdigit():
            names.append(name)

    for pat in BEN_PATTERNS:
        for m in pat.finditer(text):
            name = m.group(1).strip().rstrip('.')
            if len(name) > 3:
                names.append(name)

    return list(set(names))


def extract_routing(text):
    """Extract CHIPS SSN, BIC codes, and intermediary bank info."""
    routing = {}

    ssn = SSN_PATTERN.search(text)
    if ssn:
        routing["chips_ssn"] = ssn.group(1)

    bics = BIC_PATTERN.findall(text)
    # filter out common false positives
    noise = {"CHIPS", "SWIFT", "FEDWIRE", "CHECK", "DEBIT", "CREDIT", "TOTAL",
             "OPENING", "CLOSING", "BALANCE", "INTEREST", "TRANSFER"}
    bics = [b for b in bics if b not in noise and len(b) >= 8]
    if bics:
        routing["bic_codes"] = list(set(bics))

    # intermediary bank
    via = re.search(r'VIA\s+([A-Z][A-Z\s&]{3,40}?)(?:\s*/|\s+SSN|\s+BEN|\n)', text, re.IGNORECASE)
    if via:
        routing["intermediary"] = via.group(1).strip()

    return routing


# ── Entity resolver ─────────────────────────────────────────────────────────

# Known canonical entities from the project so far
CANONICAL_ENTITIES = {
    "GHISLAINE MAXWELL": [
        "GHISLAINE MAXWELL", "MISS GHISLAINE MAXWELL", "G MAXWELL",
        "G. MAXWELL", "MAXWELL GHISLAINE", "MS GHISLAINE MAXWELL",
    ],
    "PETER MANDELSON": [
        "PETER MANDELSON", "LORD MANDELSON", "P MANDELSON",
        "NC: PETER MANDELSON", "BEN: PETER MANDELSON",
    ],
    "TERRAMAR PROJECT INC": [
        "TERRAMAR PROJECT INC", "TERRAMAR PROJECT", "THE TERRAMAR PROJECT",
    ],
    "ELLMAX LLC": [
        "ELLMAX LLC", "ELLMAX", "ELL MAX LLC",
    ],
    "MAX HOTEL SERVICES CORP": [
        "MAX HOTEL SERVICES CORP", "MAX HOTEL SERVICES",
    ],
    "REINALDO AVILA DA SILVA": [
        "REINALDO AVILA DA SILVA", "REINALDO DA SILVA", "REINALDO AVILA",
        "R AVILA DA SILVA", "R. AVILA",
    ],
    "LSJ LLC": [
        "LSJ LLC", "L S J LLC", "LSJ",
    ],
    "LCP COMPANY": [
        "LCP COMPANY", "LCP CO", "LCP",
    ],
}

def resolve_entity(raw_name):
    """Match a raw beneficiary name to a canonical entity. Returns (canonical, confidence)."""
    cleaned = raw_name.upper().strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # exact match against aliases
    for canonical, aliases in CANONICAL_ENTITIES.items():
        if cleaned in aliases or cleaned == canonical:
            return canonical, 1.0

    # substring match
    for canonical, aliases in CANONICAL_ENTITIES.items():
        for alias in aliases:
            if alias in cleaned or cleaned in alias:
                return canonical, 0.9

    # fuzzy match
    best_score, best_match = 0, None
    for canonical, aliases in CANONICAL_ENTITIES.items():
        for alias in aliases:
            score = SequenceMatcher(None, cleaned, alias).ratio()
            if score > best_score:
                best_score = score
                best_match = canonical

    if best_score >= 0.75:
        return best_match, best_score

    return raw_name, 0.0  # unknown entity — keep raw name


# ── Scoring ─────────────────────────────────────────────────────────────────

# High-value targets get priority scores
TARGET_ENTITIES = {
    "GHISLAINE MAXWELL": 100,
    "PETER MANDELSON": 100,
    "REINALDO AVILA DA SILVA": 90,
    "TERRAMAR PROJECT INC": 95,
    "ELLMAX LLC": 90,
    "MAX HOTEL SERVICES CORP": 85,
    "LSJ LLC": 70,
    "LCP COMPANY": 60,
}

def score_transaction(record):
    """
    Score a parsed transaction for investigation priority.
    Returns int 0-100. Higher = more interesting.
    """
    score = 0

    # entity scoring
    ben = record.get("beneficiary_canonical", "")
    entity_score = TARGET_ENTITIES.get(ben, 0)
    score += entity_score

    # amount scoring — larger amounts are more interesting
    amount = record.get("amount", 0)
    if amount >= 1_000_000:
        score += 30
    elif amount >= 100_000:
        score += 20
    elif amount >= 25_000:
        score += 10
    elif amount >= 10_000:
        score += 5

    # date scoring — conviction-adjacent dates more interesting
    txn_date = record.get("date")
    if txn_date and hasattr(txn_date, 'year') and txn_date.year is not None:
        try:
            if 2005 <= txn_date.year <= 2019:
                score += 15
            elif 2000 <= txn_date.year <= 2004:
                score += 10
        except TypeError:
            pass

    # payment type bonus
    ptype = record.get("payment_type", "")
    if ptype == "CHIPS":
        score += 10  # underexplored
    elif ptype == "SWIFT":
        score += 10  # international, less visible

    # reversal/bounce indicator
    if record.get("is_reversal"):
        score += 15  # bounced payments = forensic gold

    # unknown entity bonus — new names are interesting
    if entity_score == 0 and ben and record.get("entity_confidence", 0) == 0:
        score += 20  # never seen before

    return min(score, 100)


# ── Transaction linker ──────────────────────────────────────────────────────

def link_transactions(records):
    """
    Find related transactions across payment types.
    Matches: same day + same amount + opposite direction (debit/credit)
    Returns records with 'linked_to' field populated.
    """
    by_date_amount = defaultdict(list)
    for i, r in enumerate(records):
        d = r.get("date")
        a = r.get("amount", 0)
        if d and a:
            key = (str(d), round(a, 2))
            by_date_amount[key].append(i)

    for key, indices in by_date_amount.items():
        if len(indices) < 2:
            continue

        # look for debit/credit pairs or reversal/retry pairs
        for i in indices:
            for j in indices:
                if i == j:
                    continue
                ri, rj = records[i], records[j]

                # opposite directions
                dir_i = ri.get("direction", "")
                dir_j = rj.get("direction", "")
                if (dir_i == "DEBIT" and dir_j == "CREDIT") or \
                   (dir_i == "CREDIT" and dir_j == "DEBIT"):
                    ri.setdefault("linked_to", []).append(j)
                    rj.setdefault("linked_to", []).append(i)
                    ri["link_type"] = "reversal_pair"
                    rj["link_type"] = "reversal_pair"

                # same direction, different payment type = possible duplicate
                elif ri.get("payment_type") != rj.get("payment_type"):
                    ri.setdefault("linked_to", []).append(j)
                    ri["link_type"] = "cross_type_match"

    # also check ±1 day for near-matches (retry next business day)
    for i, r in enumerate(records):
        d = r.get("date")
        a = r.get("amount", 0)
        if not d or not a:
            continue
        for offset in [1, -1]:
            try:
                adj_date = str(d + timedelta(days=offset)) if hasattr(d, '__add__') else None
            except:
                continue
            if adj_date:
                adj_key = (adj_date, round(a, 2))
                for j in by_date_amount.get(adj_key, []):
                    if j == i:
                        continue
                    if records[j].get("payment_type") != r.get("payment_type"):
                        r.setdefault("linked_to", []).append(j)
                        r["link_type"] = "adjacent_day_match"

    return records


# ── Deduplication ───────────────────────────────────────────────────────────

def dedup_records(records):
    """
    Remove duplicates across extractors. Same bates + same amount + same date = dupe.
    Also catches CORRESPONDENT_BANK overlap with CHIPS/SWIFT.
    """
    seen = set()
    unique = []
    dupes = 0

    for r in records:
        # primary key: bates number + amount + date
        bates = r.get("bates", "")
        amount = round(r.get("amount", 0), 2)
        date = str(r.get("date", ""))
        key = (bates, amount, date)

        if key in seen and bates:  # only dedup if we have a bates number
            dupes += 1
            continue
        seen.add(key)
        unique.append(r)

    if dupes:
        print(f"[DEDUP] Removed {dupes} duplicate records")
    return unique


# ── DB insertion ────────────────────────────────────────────────────────────

CREATE_EXTRACTED_PAYMENTS = """
CREATE TABLE IF NOT EXISTS extracted_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bates TEXT,
    dataset TEXT,
    payment_type TEXT,
    direction TEXT,
    date TEXT,
    amount REAL,
    currency TEXT DEFAULT 'USD',
    beneficiary_raw TEXT,
    beneficiary_canonical TEXT,
    entity_confidence REAL,
    source_account TEXT,
    source_entity TEXT,
    intermediary_bank TEXT,
    chips_ssn TEXT,
    bic_code TEXT,
    check_number TEXT,
    is_reversal INTEGER DEFAULT 0,
    reversal_ref TEXT,
    linked_payment_id INTEGER,
    link_type TEXT,
    priority_score INTEGER,
    balance_before REAL,
    balance_after REAL,
    ocr_confidence TEXT,
    raw_text TEXT,
    extraction_method TEXT,
    extracted_at TEXT,
    verified INTEGER DEFAULT 0,
    notes TEXT
);
"""

CREATE_STATEMENT_CHAIN = """
CREATE TABLE IF NOT EXISTS statement_chain (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    account_name TEXT,
    statement_start TEXT,
    statement_end TEXT,
    opening_balance REAL,
    closing_balance REAL,
    total_credits REAL,
    total_debits REAL,
    bates_start TEXT,
    bates_end TEXT,
    page_count INTEGER,
    extracted_at TEXT
);
"""

CREATE_ENTITY_REGISTRY = """
CREATE TABLE IF NOT EXISTS entity_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_name TEXT UNIQUE,
    aliases TEXT,
    entity_type TEXT,
    first_seen_date TEXT,
    last_seen_date TEXT,
    total_inflows REAL DEFAULT 0,
    total_outflows REAL DEFAULT 0,
    transaction_count INTEGER DEFAULT 0,
    notes TEXT
);
"""

def init_tables(conn):
    """Create extraction tables if they don't exist."""
    cur = conn.cursor()
    cur.execute(CREATE_EXTRACTED_PAYMENTS)
    cur.execute(CREATE_STATEMENT_CHAIN)
    cur.execute(CREATE_ENTITY_REGISTRY)

    # indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ep_bates ON extracted_payments(bates)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ep_type ON extracted_payments(payment_type)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ep_ben ON extracted_payments(beneficiary_canonical)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ep_date ON extracted_payments(date)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ep_score ON extracted_payments(priority_score DESC)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sc_acct ON statement_chain(account_number)")
    conn.commit()
    print("[DB] Extraction tables initialized")


def insert_payments(conn, records):
    """Batch insert parsed payment records into extracted_payments."""
    cur = conn.cursor()
    now = datetime.now().isoformat()
    inserted = 0

    for r in records:
        # check for existing record with same bates + amount + date
        if r.get("bates"):
            cur.execute("""
                SELECT id FROM extracted_payments 
                WHERE bates = ? AND amount = ? AND date = ?
            """, (r["bates"], r.get("amount"), str(r.get("date", ""))))
            if cur.fetchone():
                continue

        routing = r.get("routing", {})
        cur.execute("""
            INSERT INTO extracted_payments (
                bates, dataset, payment_type, direction, date, amount, currency,
                beneficiary_raw, beneficiary_canonical, entity_confidence,
                source_account, source_entity, intermediary_bank,
                chips_ssn, bic_code, check_number,
                is_reversal, reversal_ref, link_type,
                priority_score, balance_before, balance_after,
                ocr_confidence, raw_text, extraction_method, extracted_at, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get("bates"),
            r.get("dataset"),
            r.get("payment_type"),
            r.get("direction"),
            str(r.get("date", "")),
            r.get("amount"),
            r.get("currency", "USD"),
            r.get("beneficiary_raw"),
            r.get("beneficiary_canonical"),
            r.get("entity_confidence"),
            r.get("source_account"),
            r.get("source_entity"),
            routing.get("intermediary"),
            routing.get("chips_ssn"),
            ",".join(routing.get("bic_codes", [])) if routing.get("bic_codes") else None,
            r.get("check_number"),
            1 if r.get("is_reversal") else 0,
            r.get("reversal_ref"),
            r.get("link_type"),
            r.get("priority_score", 0),
            r.get("balance_before"),
            r.get("balance_after"),
            r.get("ocr_confidence"),
            r.get("raw_text", "")[:2000],  # cap raw text
            r.get("extraction_method"),
            now,
            r.get("notes"),
        ))
        inserted += 1

    conn.commit()
    print(f"[DB] Inserted {inserted} new payment records")
    return inserted


# ── Utility ─────────────────────────────────────────────────────────────────

def get_doc_texts(conn, payment_type, limit=None):
    """
    Pull extracted text pages for documents matching a payment type's search patterns.
    Yields (bates, dataset, page_num, text) tuples.
    """
    patterns = PAYMENT_TYPES[payment_type]["search_patterns"]
    where_clauses = " OR ".join([f"et.text LIKE '%' || ? || '%'" for _ in patterns])

    # we need simpler LIKE patterns — convert regex to substring searches
    like_terms = []
    for p in patterns:
        # strip regex metacharacters, extract the core keyword
        simple = re.sub(r'[\\()|?+*\[\]{}^$]', '', p)
        simple = re.sub(r'\s+', ' ', simple).strip()
        if simple:
            like_terms.append(simple)

    if not like_terms:
        return

    # build query using the keywords
    conditions = " OR ".join(["et.text_content LIKE ?" for _ in like_terms])
    like_values = [f"%{t}%" for t in like_terms]

    query = f"""
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE ({conditions})
        ORDER BY f.title, et.page_num
    """
    if limit:
        query += f" LIMIT {limit}"

    cur = conn.cursor()
    cur.execute(query, like_values)

    for row in cur:
        yield row[0], row[1], row[2], row[3]


def bates_to_url(bates):
    """Convert EFTA bates number to DOJ source PDF URL."""
    if not bates or not bates.startswith("EFTA"):
        return None
    num = bates.replace("EFTA", "")
    return f"https://www.justice.gov/d9/2025-01/EFTA{num}.pdf"


if __name__ == "__main__":
    print("Extraction framework loaded.")
    print(f"Payment types defined: {list(PAYMENT_TYPES.keys())}")
    print(f"Canonical entities: {len(CANONICAL_ENTITIES)}")
    print(f"Target entities: {len(TARGET_ENTITIES)}")
