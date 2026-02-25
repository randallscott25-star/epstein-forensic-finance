"""
jpm_statement_parser.py — Unified parser for JPMorgan Transaction Detail pages.

v3 fixes:
  1. Page filter tightened: requires "Transaction Detail" + "Primary Account" or
     "Transaction Detail CONTINUED" to exclude non-JPM pages
  2. Foreign Remittance: "Fx USD Incomingfedchipsdda" is JPM's internal FX clearing
     account — blocklisted from entity names, real counterparty pulled from Ogb: field
  3. Entity name cleaning: catches 'mad: leak, European amounts (100.000.00),
     city names after "And Co", bates numbers in names
  4. Amount extraction: blocks without amounts try harder — scan continuation lines,
     handle OCR where amount appears on its own line

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import re
import sqlite3
import os
from collections import defaultdict
from datetime import date, datetime

from extraction_framework import (
    resolve_entity, score_transaction, TARGET_ENTITIES, CANONICAL_ENTITIES
)

# ── Transaction type classification ─────────────────────────────────────────

TX_CLASSIFIERS = [
    ("CHIPS_DEBIT",          re.compile(r'Chips\s+(?:Debit|Db)\s+Via:', re.IGNORECASE)),
    ("CHIPS_CREDIT",         re.compile(r'Chips\s+(?:Credit|Cr)\s+Via:', re.IGNORECASE)),
    ("FEDWIRE_DEBIT",        re.compile(r'Fedwire\s+Debit\s+Via:', re.IGNORECASE)),
    ("FEDWIRE_CREDIT",       re.compile(r'Fedwire\s+Credit\s+Via:', re.IGNORECASE)),
    ("BOOK_TRANSFER_CREDIT", re.compile(r'Book\s+Transfer\s+Credit', re.IGNORECASE)),
    ("BOOK_TRANSFER_DEBIT",  re.compile(r'Book\s+Transfer(?!\s+Credit)', re.IGNORECASE)),
    ("FOREIGN_REMITTANCE",   re.compile(r'Foreign\s+Remittance\s+(?:Debit|Credit)', re.IGNORECASE)),
    ("INTERNAL_TRANSFER",    re.compile(r'Internal\s+(?:Transfer\s+of\s+Funds|Funds?\s+Transfer)', re.IGNORECASE)),
    ("CHECK",                re.compile(r'Check\s+#?\s*\d{3,6}', re.IGNORECASE)),
    ("CHASE_CARD",           re.compile(r'Payment\s+To\s+Chase\s+Card', re.IGNORECASE)),
    ("ONLINE_TRANSFER",      re.compile(r'Online\s+Transfer\s+To', re.IGNORECASE)),
    ("ACH",                  re.compile(r'ACH\s+(?:Pmt|Payment|Debit|Credit)', re.IGNORECASE)),
    ("INTEREST",             re.compile(r'(?:Overdraft\s+)?Interest\s+(?:Applied|Paid|Earned)', re.IGNORECASE)),
    ("LETTER_FROM_CLIENT",   re.compile(r'Letter\s+From\s+Client', re.IGNORECASE)),
]

DIRECTION_MAP = {
    "CHIPS_DEBIT": "DEBIT", "CHIPS_CREDIT": "CREDIT",
    "FEDWIRE_DEBIT": "DEBIT", "FEDWIRE_CREDIT": "CREDIT",
    "BOOK_TRANSFER_DEBIT": "DEBIT", "BOOK_TRANSFER_CREDIT": "CREDIT",
    "FOREIGN_REMITTANCE": "DEBIT", "INTERNAL_TRANSFER": "DEBIT",
    "CHECK": "DEBIT", "CHASE_CARD": "DEBIT",
    "ONLINE_TRANSFER": "DEBIT", "ACH": "DEBIT",
}

TYPE_MAP = {
    "CHIPS_DEBIT": "CHIPS", "CHIPS_CREDIT": "CHIPS",
    "FEDWIRE_DEBIT": "FEDWIRE", "FEDWIRE_CREDIT": "FEDWIRE",
    "BOOK_TRANSFER_DEBIT": "BOOK_TRANSFER", "BOOK_TRANSFER_CREDIT": "BOOK_TRANSFER",
    "FOREIGN_REMITTANCE": "FOREIGN_REMITTANCE", "INTERNAL_TRANSFER": "INTERNAL_TRANSFER",
    "CHECK": "CHECK", "CHASE_CARD": "CHASE_CARD",
    "ONLINE_TRANSFER": "ONLINE_TRANSFER", "ACH": "ACH",
}


# ── Year extraction ─────────────────────────────────────────────────────────

PERIOD_PATTERNS = [
    re.compile(r'(?:Period|Peeled|Penod|Per[il]od)\s+(\d{1,2})/(\d{1,2})/(\d{2,4})\s+to\s+(\d{1,2})/(\d{1,2})/(\d{2,4})', re.IGNORECASE),
    re.compile(r'to\s+\d{1,2}/\d{1,2}/(\d{2,4})', re.IGNORECASE),
]
FALLBACK_DATE = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{2,4})')
YEAR_IN_TEXT = re.compile(r'20[0-2]\d')


def extract_statement_year(text):
    for pat in PERIOD_PATTERNS:
        m = pat.search(text[:600])
        if m:
            y_str = m.groups()[-1]
            try:
                y = int(y_str)
                if y < 100:
                    y += 2000
                if 1990 <= y <= 2030:
                    return y
            except ValueError:
                continue

    for m in FALLBACK_DATE.finditer(text[:600]):
        try:
            y = int(m.group(3))
            if y < 100:
                y += 2000
            if 1990 <= y <= 2030:
                return y
        except ValueError:
            continue

    m = YEAR_IN_TEXT.search(text[:800])
    if m:
        return int(m.group(0))

    full_date = re.search(r'(\d{2})/(\d{2})/(\d{4})', text)
    if full_date:
        try:
            return int(full_date.group(3))
        except ValueError:
            pass

    return None


def extract_account_info(text):
    info = {}
    m = re.search(r'Primary\s+Account[:\s]*(?:Number)?[:\s]*(\d{6,15})', text[:400], re.IGNORECASE)
    if m:
        info["account_number"] = m.group(1)
    else:
        m = re.search(r'^(\d{9,15})\s*$', text[:300], re.MULTILINE)
        if m:
            info["account_number"] = m.group(1)

    skip = {"TRANSACTION", "PRIMARY", "CONTINUED", "SUMMARY", "CHECKING", "SAVINGS", "PRIVATE"}
    for line in text[:500].split('\n')[:8]:
        line = line.strip()
        if line and len(line) > 4 and re.match(r'^[A-Z][A-Z\s.,]+$', line):
            if not set(line.split()).intersection(skip):
                info["account_entity"] = line.strip()
                break
    return info


# ── Transaction block splitting ─────────────────────────────────────────────

TX_KEYWORDS = re.compile(
    r'(?:Chips|Fedwire|Book\s+Transfer|Foreign\s+Remittance|Internal|'
    r'Check\s+#|Payment\s+To\s+Chase|Online\s+Transfer|ACH\s+(?:Pmt|Payment)|'
    r'Interest\s+(?:Applied|Paid)|Letter\s+From\s+Client|'
    r'Overdraft\s+Interest|Payment\s+To\s+Chase\s+Card)',
    re.IGNORECASE
)


def split_into_transactions(text):
    lines = text.split('\n')
    blocks = []
    current_lines = []
    current_date = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        m_solo = re.match(r'^(\d{2}/\d{2})\s*$', stripped)
        m_inline = re.match(r'^(\d{2}/\d{2})\s+(.+)', stripped)

        if m_solo:
            if current_lines and current_date:
                blocks.append((current_date, '\n'.join(current_lines)))
            current_date = m_solo.group(1)
            current_lines = []
        elif m_inline:
            candidate_date = m_inline.group(1)
            rest = m_inline.group(2)

            if TX_KEYWORDS.search(rest):
                if current_lines and current_date:
                    blocks.append((current_date, '\n'.join(current_lines)))
                current_date = candidate_date
                current_lines = [rest]
            elif not current_date:
                current_date = candidate_date
                current_lines = [rest]
            else:
                current_lines.append(stripped)
        else:
            if current_date is not None:
                current_lines.append(stripped)

    if current_lines and current_date:
        blocks.append((current_date, '\n'.join(current_lines)))

    return blocks


# ── Amount extraction ───────────────────────────────────────────────────────

DOLLAR_AMOUNT = re.compile(r'(?<!\d)([\d,]{1,12}\.\d{2})(?!\d)')
# OCR garble: periods where commas should be — "24.074.00", "884.714.72"
DOLLAR_OCR_PERIOD = re.compile(r'(?<!\d)(\d{1,3}(?:\.\d{3})+\.\d{2})(?!\d)')


def fix_ocr_amount(s):
    """Convert OCR period-as-comma amounts: 24.074.00 -> 24074.00"""
    parts = s.split('.')
    if len(parts) >= 3:
        # last part is cents, everything before is the integer with periods as thousands sep
        cents = parts[-1]
        integer = ''.join(parts[:-1])
        return float(integer + '.' + cents)
    return None


def extract_amounts_from_block(block_text):
    """
    Pull transaction amount and running balance.
    JPM layout: amounts appear as bare numbers. On a well-formed line,
    the last number is balance, second-to-last is amount.
    
    If the block only has one number, check if it looks like a balance
    (matches a nearby balance chain) vs a transaction amount.
    """
    all_amounts = []
    # first try OCR period-as-comma pattern (more specific, check first)
    for m in DOLLAR_OCR_PERIOD.finditer(block_text):
        val = fix_ocr_amount(m.group(1))
        if val and val > 0:
            all_amounts.append(val)

    # then try standard comma-separated pattern
    if not all_amounts:
        for m in DOLLAR_AMOUNT.finditer(block_text):
            try:
                val = float(m.group(1).replace(',', ''))
                if val > 0:
                    all_amounts.append(val)
            except ValueError:
                continue

    if len(all_amounts) >= 2:
        return all_amounts[-2], all_amounts[-1]
    elif len(all_amounts) == 1:
        # single number — if it's on its own line, it's probably the balance
        # and the amount was on the previous block or missing
        # but if the whole block is short, it's likely the amount
        lines = [l.strip() for l in block_text.split('\n') if l.strip()]
        if len(lines) <= 2:
            return all_amounts[0], None
        # check if the number appears on its own line (= balance)
        for line in lines:
            if re.match(r'^[\d,]+\.\d{2}$', line.strip()):
                # standalone number line = likely balance
                return None, all_amounts[0]
        return all_amounts[0], None
    return None, None


# ── Beneficiary extraction ──────────────────────────────────────────────────

BEN_PATTERNS = [
    re.compile(r'(?:NC|A/C)[:\s!]+\s*([A-Za-z][A-Za-z0-9\s.,\'-]{2,})', re.IGNORECASE),
    re.compile(r'Ben[:\s]+\s*([A-Za-z][A-Za-z0-9\s.,\'-]{2,})', re.IGNORECASE),
    re.compile(r'B/O[:\s]+\s*([A-Za-z][A-Za-z0-9\s.,\'-]{2,})', re.IGNORECASE),
]

# FX clearing account — this is JPM internal, NOT a real beneficiary
FX_CLEARING = re.compile(r'Fx\s+USD\s+Incomingfedchipsdda', re.IGNORECASE)
# the real FX counterparty is in Ogb: or after "Org:"
FX_COUNTERPARTY = re.compile(r'Ogb:\s*([A-Za-z][A-Za-z\s]+?)(?:\s+(?:New\s+York|Newark|Bournemouth)|\n|$)', re.IGNORECASE)

NAME_TERMINATORS = re.compile(
    r'\b(?:Ref|Ssn|[Il]mad|Trn|Tm|Org|Aba|Web|Phone|Invoice|As Per|'
    r'Registration|Serial|Inv|Account|Payment|Purchase|Time|Acc|'
    r'For\s|Re:|Dt[d:]|Cust\b|/Time|Ending\s+IN)\b'
    r'|'
    r'\d{5,}'              # long number sequences
    r'|'
    r'\$'                  # dollar sign
    r'|'
    r'(?<!\d)\d{1,3}(?:,\d{3})+\.\d{2}'  # US format amounts
    r'|'
    r'(?<!\d)\d{1,3}(?:\.\d{3})+(?:,\d{2})?'  # European format amounts (100.000.00)
    r'|'
    r'\b[A-Z]{2}\s+\d{5}'  # state + zip
    r'|'
    r'\bEFTA\d+'           # bates number leak
    r'|'
    r"'\s*mad:"            # IMAD with OCR apostrophe
, re.IGNORECASE)

STATES = {'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN',
          'IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV',
          'NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN',
          'TX','UT','VT','VA','WA','WV','WI','WY','VI','PR','DC'}

NOT_ENTITIES = {
    'NEW YORK', 'NEWARK', 'CHARLOTTE AMALIE', 'MIAMI', 'FORT LAUDERDALE',
    'TAMPA', 'BROOKLYN', 'SAN FRANCISCO', 'LOS ANGELES', 'CHICAGO',
    'BOURNEMOUTH', 'LONDON', 'NASSAU', 'ST THOMAS', 'HOUSTON',
    'GAINESVILLE', 'WHIPPANY', 'CINCINNATI', 'THOMASVILLE',
    'FX OPERATIONS', 'FX USD INCOMINGFEDCHIPSDDA',
    'JPMORGAN CHASE BANK', 'JPMORGAN CHASE', 'CHASE BANK',
}


def clean_entity_name(raw):
    if not raw:
        return None

    name = re.sub(r'\s+', ' ', raw).strip()

    # block FX clearing account names
    if FX_CLEARING.search(name):
        return None

    # truncate at first terminator
    m = NAME_TERMINATORS.search(name)
    if m and m.start() > 3:
        name = name[:m.start()].strip()

    # strip trailing "City, ST" or "City ST ZIP"
    name = re.sub(r',?\s+[A-Z]{2}\s*\d{5}[-\d]*\s*$', '', name)
    # strip trailing state abbreviation
    words = name.split()
    if len(words) > 1 and words[-1].upper() in STATES:
        name = ' '.join(words[:-1])

    # strip city names that crept in after company names
    # "Brown Brothers Harriman And Conew York" -> "Brown Brothers Harriman And Co"
    # "Sikorsky Aircraft Corp Fundingwindsor" -> "Sikorsky Aircraft Corp"
    # OCR merges city into previous word — look for lowercase-to-uppercase transition
    name = re.sub(r'(\b(?:Corp|Inc|LLC|Ltd|Co|LP|PA|Trust|Company))\s*\w*(?:new\s*york|newark|miami|tampa|brooklyn|whippany|gainesville|windsor|lauderdale)', 
                  r'\1', name, flags=re.IGNORECASE)

    name = name.rstrip('.,;:(-/ ')
    name = re.sub(r'^[/\s:!]+', '', name)

    # reject garbage
    if len(name) < 3:
        return None
    if re.match(r'^[\d\s.,/]+$', name):
        return None
    if name.upper().strip() in NOT_ENTITIES:
        return None
    # reject if mostly digits
    digit_count = sum(1 for c in name if c.isdigit())
    if digit_count > len(name) * 0.5:
        return None

    return name.strip()


def extract_beneficiary(block_text, tx_type=None):
    """Extract beneficiary. For Foreign Remittance, skip FX clearing accounts."""
    text = block_text

    # Foreign Remittance: the NC: field is JPM internal FX clearing.
    # Real counterparty is in Ogb: field if present
    if tx_type == "FOREIGN_REMITTANCE":
        m = FX_COUNTERPARTY.search(text)
        if m:
            cleaned = clean_entity_name(m.group(1))
            if cleaned:
                return cleaned
        # if no Ogb: field, skip — don't extract the FX clearing name
        if FX_CLEARING.search(text):
            return None

    for pat in BEN_PATTERNS:
        m = pat.search(text)
        if m:
            raw = m.group(1)
            end_pos = m.end()
            remainder = text[end_pos:]
            extra_lines = remainder.split('\n')
            for extra in extra_lines[:2]:
                extra = extra.strip()
                if extra and re.match(r'^[A-Z]', extra) and not re.match(r'^(?:Ref|Ssn|[Il]mad|Trn|Tm|Org|Aba|\d{2}/\d{2})', extra):
                    if re.match(r'^[\d,]+\.\d{2}$', extra):
                        break
                    raw += ' ' + extra
                else:
                    break

            cleaned = clean_entity_name(raw)
            if cleaned:
                return cleaned

    # NC at end of line (OCR break)
    nc_break = re.search(r'\bNC[:\s!]*$', text, re.MULTILINE | re.IGNORECASE)
    if nc_break:
        after = text[nc_break.end():].strip()
        first_line = after.split('\n')[0].strip()
        if first_line and not re.match(r'^(?:Ssn|Trn|Tm|[Il]mad|\d)', first_line, re.IGNORECASE):
            cleaned = clean_entity_name(first_line)
            if cleaned:
                return cleaned

    # Book transfer name after keyword
    bt_match = re.search(r'Book\s+Transfer\s*(?:Credit|Debit)?\s*\n\s*(?:B/O\s+|NC:\s+)?([A-Za-z].+)', text, re.IGNORECASE)
    if bt_match:
        raw = bt_match.group(1)
        end_pos = bt_match.end()
        remainder = text[end_pos:]
        next_line = remainder.split('\n')[0].strip() if remainder else ""
        if next_line and re.match(r'^[A-Z]', next_line) and not re.match(r'^(?:Ref|Org|Aba|\d)', next_line):
            raw += ' ' + next_line
        cleaned = clean_entity_name(raw)
        if cleaned:
            return cleaned

    return None


# ── Routing info ────────────────────────────────────────────────────────────

VIA_BANK = re.compile(r'Via:\s+([A-Za-z][A-Za-z\s&.,]+?)(?:/\d|\s+NC|\s+A/C|\s+Ben|\n|$)', re.IGNORECASE)
SSN_PAT = re.compile(r'Ssn:\s*(\d{5,9})', re.IGNORECASE)
IMAD_PAT = re.compile(r'[Il]mad:\s*(\S+)', re.IGNORECASE)
TRN_PAT = re.compile(r'(?:Trn|Tm):\s*(\S+)', re.IGNORECASE)
CHECK_NUM_PAT = re.compile(r'Check\s+#\s*(\d{3,6})', re.IGNORECASE)
REVERSAL_PAT = re.compile(r'Reversal\s+of\s+Entry|Bnf\s+Ac\s+Closed|CDT\s+RET|Cb\s+Funds\s+Transfer\s+Same', re.IGNORECASE)


def extract_routing(text):
    info = {}
    m = VIA_BANK.search(text)
    if m:
        info["intermediary"] = m.group(1).strip().rstrip(',.')
    m = SSN_PAT.search(text)
    if m:
        info["chips_ssn"] = m.group(1)
    m = IMAD_PAT.search(text)
    if m:
        info["imad"] = m.group(1)
    trns = TRN_PAT.findall(text)
    if trns:
        info["trn"] = trns[-1]
    m = CHECK_NUM_PAT.search(text)
    if m:
        info["check_number"] = m.group(1)
    return info


# ── Scoring (None-safe) ────────────────────────────────────────────────────

def safe_score(record):
    try:
        return score_transaction(record)
    except TypeError:
        temp = dict(record)
        temp.pop("date", None)
        try:
            return score_transaction(temp)
        except:
            return 0


# ── Parse one transaction block ─────────────────────────────────────────────

def classify_transaction(text):
    for tx_type, pattern in TX_CLASSIFIERS:
        if pattern.search(text):
            return tx_type
    return "OTHER"


def parse_transaction_block(tx_date_str, block_text, stmt_year, bates, dataset, account_info):
    tx_type = classify_transaction(block_text)
    if tx_type in ("LETTER_FROM_CLIENT", "INTEREST", "OTHER"):
        return None

    direction = DIRECTION_MAP.get(tx_type, "UNKNOWN")
    payment_type = TYPE_MAP.get(tx_type, tx_type)

    # date
    tx_date = None
    if tx_date_str and stmt_year:
        try:
            mo = int(tx_date_str[:2])
            day = int(tx_date_str[3:5])
            if 1 <= mo <= 12 and 1 <= day <= 31:
                tx_date = date(stmt_year, mo, day)
        except (ValueError, IndexError):
            pass

    # amounts
    tx_amount, balance = extract_amounts_from_block(block_text)

    # beneficiary (pass tx_type for FX handling)
    ben_raw = extract_beneficiary(block_text, tx_type)
    ben_canonical, entity_conf = None, 0.0
    if ben_raw:
        ben_canonical, entity_conf = resolve_entity(ben_raw)

    # routing
    routing = extract_routing(block_text)

    # reversal
    is_reversal = bool(REVERSAL_PAT.search(block_text))
    if is_reversal and direction == "DEBIT":
        direction = "CREDIT"

    record = {
        "bates": bates,
        "dataset": dataset,
        "payment_type": payment_type,
        "direction": direction,
        "date": tx_date,
        "amount": tx_amount,
        "currency": "USD",
        "beneficiary_raw": ben_raw,
        "beneficiary_canonical": ben_canonical,
        "entity_confidence": entity_conf,
        "source_account": account_info.get("account_number"),
        "source_entity": account_info.get("account_entity"),
        "routing": routing,
        "check_number": routing.get("check_number"),
        "is_reversal": is_reversal,
        "balance_after": balance,
        "raw_text": block_text[:2000],
        "extraction_method": "jpm_statement_parser_v3",
    }

    record["priority_score"] = safe_score(record)
    return record


# ── Page filter ─────────────────────────────────────────────────────────────

def is_jpm_transaction_detail(text):
    """
    Strict filter: is this page a JPMorgan Transaction Detail page?
    Must have "Transaction Detail" AND one of:
      - "Primary Account"
      - "CONTINUED" (multi-page statements)
      - JPM header pattern (entity name + period + column headers)
    Rejects pages that just mention "transaction detail" in prose.
    """
    if 'Transaction Detail' not in text and 'transaction detail' not in text.lower():
        return False

    # strong signals
    has_primary = bool(re.search(r'Primary\s+Account', text[:600], re.IGNORECASE))
    has_continued = bool(re.search(r'Transaction\s+Detail\s+CONTINUED', text[:300], re.IGNORECASE))
    has_period = bool(re.search(r'(?:Period|Peeled|Penod)\s+\d', text[:600], re.IGNORECASE))
    has_date_col = bool(re.search(r'^Date\s+Description', text, re.MULTILINE | re.IGNORECASE))
    has_jpm = bool(re.search(r'JPMorgan|J\.\s*P\.\s*Morgan|Private\s+Bank|Private\s+Cli', text[:800], re.IGNORECASE))
    has_epstein_entity = bool(re.search(r'JEFFREY\s+E\s+EPSTEIN|EPSTEIN\s+INTERESTS|AIR\s+GHISLAINE|SOUTHERN\s+TRUST|FINANCIAL\s+TRUST', text[:500], re.IGNORECASE))

    # reject known non-JPM banks
    is_other_bank = bool(re.search(r'Navy\s+Federal|Fifth\s+Third|Credit\s+Union|Grand\s+Jury\s+Subpoena', text[:800], re.IGNORECASE))
    if is_other_bank:
        return False

    # need at least one strong signal + must have date-like entries in body
    has_balance = bool(re.search(r'Balance', text[:600], re.IGNORECASE))
    signals = sum([has_primary, has_continued, has_period, has_date_col, has_jpm])
    # 2+ signals = definitely JPM. 1 signal + Balance = probably JPM.
    if signals >= 2:
        return True
    if signals >= 1 and has_balance:
        return True
    return False


# ── Main extraction ─────────────────────────────────────────────────────────

def get_db_path():
    paths = [
        os.path.expanduser("~/Desktop/epstein_files.db"),
        "/Volumes/My Book/epstein_project/epstein_files.db",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"No DB found. Checked: {paths}")


def run_jpm_parser(db_path=None, limit=None, verbose=True):
    if not db_path:
        db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if verbose:
        print("=" * 70)
        print("JPM TRANSACTION DETAIL PARSER v3")
        print("=" * 70)
        print(f"[JPM] Database: {db_path}")

    query = """
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE et.text_content LIKE '%Transaction Detail%'
        ORDER BY f.title, et.page_num
    """
    if limit:
        query += f" LIMIT {limit}"

    cur.execute(query)
    rows = cur.fetchall()

    if verbose:
        print(f"[JPM] Candidate pages from DB: {len(rows)}")

    all_records = []
    pages_parsed = 0
    pages_filtered = 0
    pages_with_year = 0
    tx_by_type = defaultdict(int)
    vol_by_type = defaultdict(float)
    entities_seen = defaultdict(lambda: {"count": 0, "volume": 0.0})
    errors = 0

    for bates, dataset, page_num, text in rows:
        if not text or len(text) < 50:
            continue

        # strict page filter
        if not is_jpm_transaction_detail(text):
            pages_filtered += 1
            continue

        pages_parsed += 1

        stmt_year = extract_statement_year(text)
        if stmt_year:
            pages_with_year += 1
        account_info = extract_account_info(text)

        blocks = split_into_transactions(text)

        for tx_date_str, block_text in blocks:
            try:
                record = parse_transaction_block(
                    tx_date_str, block_text, stmt_year,
                    bates, dataset, account_info
                )
                if record and (record.get("amount") or record.get("beneficiary_raw")):
                    all_records.append(record)
                    pt = record["payment_type"]
                    tx_by_type[pt] += 1
                    amt = record.get("amount") or 0
                    vol_by_type[pt] += amt

                    ben = record.get("beneficiary_canonical") or record.get("beneficiary_raw")
                    if ben:
                        entities_seen[ben]["count"] += 1
                        entities_seen[ben]["volume"] += amt
            except Exception as e:
                errors += 1
                if verbose and errors <= 5:
                    print(f"  [ERR] {bates} p{page_num}: {e}")

    conn.close()

    if verbose:
        print(f"\n[JPM] Parsing complete.")
        print(f"  Candidate pages: {pages_parsed + pages_filtered}")
        print(f"  Filtered out (non-JPM): {pages_filtered}")
        print(f"  Pages parsed: {pages_parsed}")
        print(f"  Pages with year resolved: {pages_with_year}/{pages_parsed} ({100*pages_with_year/max(pages_parsed,1):.1f}%)")
        print(f"  Total records: {len(all_records)}")
        print(f"  Errors: {errors}")

        print(f"\n  Transaction Type Breakdown:")
        print(f"  {'Type':<22} {'Count':>8} {'Volume':>18}")
        print(f"  {'─'*22} {'─'*8} {'─'*18}")
        grand_count, grand_vol = 0, 0.0
        for pt in sorted(tx_by_type.keys()):
            c, v = tx_by_type[pt], vol_by_type[pt]
            print(f"  {pt:<22} {c:>8,} ${v:>15,.2f}")
            grand_count += c
            grand_vol += v
        print(f"  {'─'*22} {'─'*8} {'─'*18}")
        print(f"  {'TOTAL':<22} {grand_count:>8,} ${grand_vol:>15,.2f}")

        known = {k: v for k, v in entities_seen.items() if k in TARGET_ENTITIES}
        if known:
            print(f"\n  Known Target Entities:")
            for name in sorted(known, key=lambda x: -known[x]["volume"]):
                d = known[name]
                print(f"    {name}: {d['count']} txns, ${d['volume']:,.2f}")

        unknown = {k: v for k, v in entities_seen.items()
                   if k not in TARGET_ENTITIES and k not in CANONICAL_ENTITIES}
        if unknown:
            top = sorted(unknown.items(), key=lambda x: -x[1]["volume"])[:25]
            print(f"\n  Top 25 New Entities (of {len(unknown)} total):")
            for name, data in top:
                print(f"    {name}: {data['count']} txns, ${data['volume']:,.2f}")

        reversals = [r for r in all_records if r.get("is_reversal")]
        print(f"\n  Reversals: {len(reversals)}")

        with_amount = sum(1 for r in all_records if r.get("amount"))
        with_balance = sum(1 for r in all_records if r.get("balance_after"))
        with_ben = sum(1 for r in all_records if r.get("beneficiary_raw"))
        with_date = sum(1 for r in all_records if r.get("date"))
        n = max(len(all_records), 1)
        print(f"\n  Data Quality:")
        print(f"    With amount:      {with_amount:>6,}/{len(all_records):,} ({100*with_amount/n:.1f}%)")
        print(f"    With balance:     {with_balance:>6,}/{len(all_records):,} ({100*with_balance/n:.1f}%)")
        print(f"    With beneficiary: {with_ben:>6,}/{len(all_records):,} ({100*with_ben/n:.1f}%)")
        print(f"    With date:        {with_date:>6,}/{len(all_records):,} ({100*with_date/n:.1f}%)")

    return all_records


if __name__ == "__main__":
    import sys
    limit = None
    for i, a in enumerate(sys.argv[1:]):
        if a == "--limit" and i + 1 < len(sys.argv[1:]):
            limit = int(sys.argv[i + 2])
    run_jpm_parser(limit=limit, verbose=True)
