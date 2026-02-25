#!/usr/bin/env python3
"""
MULTI-BANK STATEMENT PARSER
Extracts transactions from ALL non-JPM bank statement pages in EFTA corpus.

Banks covered: Deutsche Bank, Bear Stearns, First Bank PR, Citibank, UBS,
               HSBC, Barclays, BNY Mellon, Morgan Stanley, Credit Suisse,
               Navy Federal, Merchants Commercial, Charles Schwab

Architecture: Universal parser with bank-specific page filters.
Same approach as jpm_statement_parser.py but for every other bank.

Creates: bank_statement_transactions table

Author: Randall Scott Taylor
For the girls.
"""

import sqlite3, re, os, sys, json
from collections import defaultdict, Counter
from datetime import datetime

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")

# ── Regex patterns ──
DOLLAR = re.compile(r'\$\s*([\d,]+\.?\d{0,2})')
DOLLAR_STRICT = re.compile(r'\$([\d]{1,3}(?:,\d{3})*(?:\.\d{2}))')
DATE_MDY = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{2,4})')
DATE_ISO = re.compile(r'(\d{4})-(\d{2})-(\d{2})')

# ── Bank identification ──
BANK_SIGNATURES = {
    "Deutsche Bank": {
        'patterns': [
            re.compile(r'(?i)deutsche\s*bank', re.I),
        ],
        'strong_markers': [
            r'(?i)DB-SDNY-\d+',
            r'(?i)southern\s+financial\s+(relationship|llc)',
            r'(?i)haze\s+trust',
            r'(?i)exhibit\s+[A-E]',
            r'(?i)account\s+activity',
        ],
        'exclude': [
            r'(?i)from:\s+.*@.*\.(com|gov|org)',
            r'(?i)reuters|associated\s+press|wall\s+street\s+journal',
            r'(?i)wikipedia',
            r'(?i)drug\s+cartel|mexican\s+cartel|laundering\s+scheme',
            r'(?i)FinCEN\s+(I|SAR|Assess|Financial\s+Crimes)',
            r'(?i)Financial\s+Crimes\s+Enforcement\s+Network',
            r'(?i)BSAR\s+Transcript',
            r'(?i)Case\s+\d+:\d+-cv-\d+',
            r'(?i)UNITED\s+STATES\s+DISTRICT\s+COURT',
            r'(?i)bribe\s+payment|conspiracy\s+to\s+commit',
            r'(?i)Department\s+of\s+Justice',
            r'(?i)Filed\s+\d{2}/\d{2}/\d{2}',
            r'(?i)covered\s+action\s+\d{4}',
            r'(?i)Knight\s+Capital\s+TCR',
        ],
        'priority': 1,
    },
    "Bear Stearns": {
        'patterns': [
            re.compile(r'(?i)bear\s+stea?rns', re.I),
        ],
        'strong_markers': [
            r'(?i)office\s+servicing\s+your\s+account',
            r'(?i)portfolio\s+holdings',
            r'(?i)your\s+account\s+summary',
            r'(?i)cleared\s+through\s+its',
            r'(?i)cash\s+&\s+cash\s+equivalents',
            r'(?i)account\s+de[ao]',
        ],
        'exclude': [
            r'(?i)from:\s+.*@',
            r'(?i)grand\s+jury\s+subpoena',
        ],
        'priority': 1,
    },
    "First Bank PR": {
        'patterns': [
            re.compile(r'(?i)first\s*bank\s+(puerto|pr|virgin)', re.I),
            re.compile(r'(?i)firstbank(?!\s+national)', re.I),
        ],
        'strong_markers': [
            r'(?i)account\s+statement',
            r'(?i)statement\s+period',
            r'(?i)previous\s+balance',
            r'(?i)gratitude\s+america',
        ],
        'exclude': [
            r'(?i)from:\s+.*@',
            r'(?i)grand\s+jury\s+subpoena',
            r'(?i)kellerhals\s+ferguson',
            r'(?i)FinCEN\s+(I|Financial\s+Crimes)',
            r'(?i)Financial\s+Crimes\s+Enforcement\s+Network',
            r'(?i)BSAR\s+Transcript',
            r'(?i)Case\s+\d+:\d+-cv-\d+',
            r'(?i)Department\s+of\s+Justice',
            r'(?i)UNITED\s+STATES\s+DISTRICT\s+COURT',
            r'(?i)United\s+States\s+Attorney',
            r'(?i)PLLC|Professional\s+Building',
            r'(?i)law\s+firm|attorney|counsel',
        ],
        'priority': 1,
    },
    "Citibank": {
        'patterns': [
            re.compile(r'(?i)citibank', re.I),
            re.compile(r'(?i)citi\s+private\s+bank', re.I),
        ],
        'strong_markers': [
            r'(?i)exhibit\s+[A-E]',
            r'(?i)gratitude\s+america',
            r'(?i)mmda',
            r'(?i)money\s+market\s+deposit',
            r'(?i)account\s+(activity|statement)',
        ],
        'exclude': [
            r'(?i)from:\s+.*@',
            r'(?i)krieger.*kim.*lewin',
            r'(?i)credit\s+profile\s+from\s+experian',
            r'(?i)experian\s+inc',
            r'(?i)equifax|transunion',
            r'(?i)FinCEN\s+(I|Financial\s+Crimes)',
            r'(?i)Financial\s+Crimes\s+Enforcement\s+Network',
        ],
        'priority': 2,
    },
    "UBS": {
        'patterns': [
            re.compile(r'(?i)ubs\s+(ag|financial|securities|wealth|resource|bus)', re.I),
        ],
        'strong_markers': [
            r'(?i)resource\s+management\s+account',
            r'(?i)cash\s+activity\s+summary',
            r'(?i)account\s+name:',
            r'(?i)ghislaine\s+maxwell',
            r'(?i)loan\s+summary',
        ],
        'exclude': [
            r'(?i)FinCEN\s+Assess',
            r'(?i)from:\s+.*@',
            r'(?i)reuters',
        ],
        'priority': 2,
    },
    "Morgan Stanley": {
        'patterns': [
            re.compile(r'(?i)morgan\s+stanley', re.I),
        ],
        'strong_markers': [
            r'(?i)account\s+(statement|activity|summary)',
            r'(?i)investment\s+report',
        ],
        'exclude': [
            r'(?i)from:\s+.*@',
        ],
        'priority': 3,
    },
    "HSBC": {
        'patterns': [
            re.compile(r'(?i)hsbc', re.I),
        ],
        'strong_markers': [
            r'(?i)account\s+statement',
            r'(?i)statement\s+period',
        ],
        'exclude': [
            r'(?i)from:\s+.*@',
            r'(?i)DB-SDNY',
            r'(?i)bear\s+stearns',
            r'(?i)southern\s+financial\s+llc\s+checking',
            r'(?i)haze\s+trust\s+checking',
            r'(?i)FinCEN',
            r'(?i)Case\s+\d+:\d+',
        ],
        'priority': 3,
    },
    "Barclays": {
        'patterns': [
            re.compile(r'(?i)barclays', re.I),
        ],
        'strong_markers': [
            r'(?i)account\s+summary',
            r'(?i)form\s+8938',
        ],
        'exclude': [
            r'(?i)from:\s+.*@',
        ],
        'priority': 3,
    },
    "BNY Mellon": {
        'patterns': [
            re.compile(r'(?i)bny\s*mellon', re.I),
            re.compile(r'(?i)bank\s+of\s+new\s+york\s+mellon', re.I),
        ],
        'strong_markers': [
            r'(?i)account\s+statement',
        ],
        'exclude': [
            r'(?i)from:\s+.*@',
        ],
        'priority': 3,
    },
    "Credit Suisse": {
        'patterns': [
            re.compile(r'(?i)credit\s+suisse', re.I),
        ],
        'strong_markers': [
            r'(?i)account\s+(statement|summary)',
        ],
        'exclude': [
            r'(?i)from:\s+.*@',
        ],
        'priority': 3,
    },
    "Merchants Commercial": {
        'patterns': [
            re.compile(r'(?i)merchants\s+commercial', re.I),
        ],
        'strong_markers': [
            r'(?i)account\s+statement',
        ],
        'exclude': [],
        'priority': 3,
    },
    "Navy Federal": {
        'patterns': [
            re.compile(r'(?i)navy\s+federal', re.I),
        ],
        'strong_markers': [
            r'(?i)(visa|credit\s+card|minimum\s+payment)',
            r'(?i)account\s+number',
        ],
        'exclude': [],
        'priority': 3,
    },
    "Charles Schwab": {
        'patterns': [
            re.compile(r'(?i)charles\s+schwab', re.I),
        ],
        'strong_markers': [
            r'(?i)account\s+statement',
            r'(?i)brokerage\s+account',
        ],
        'exclude': [],
        'priority': 3,
    },
}

# ── Epstein entity names for linking ──
EPSTEIN_ENTITIES = [
    'southern trust', 'southern financial', 'haze trust', 'the haze trust',
    'butterfly trust', 'gratitude america', 'plan d', 'bv70', 'honeycomb',
    'boothbay', 'caterpillar trust', 'valar', 'jege', 'lsj',
    'zorro', 'hyperion', 'nes llc', 'jeffrey epstein', 'epstein',
    'ghislaine maxwell', 'maxwell', 'jeepers', 'indyke', 'kahn',
    'ellmax', 'maple inc', 'terramar', 'air ghislaine',
    '116 east 65th', '301 east 66th', '9 east 71st',
    'financial trust company', 'ftc', 'borgerson',
    'leon black', 'les wexner', 'wexner',
    'dreyfus', 'bear stearns', 'southern country',
    'nautilus', 'hercules', 'cobalt',
]

# ── Transaction type classifiers ──
TX_TYPE_PATTERNS = {
    'wire_transfer': [
        r'(?i)(fed\s*wire|wire\s+transfer|wire\s+in|wire\s+out|incoming\s+wire|outgoing\s+wire)',
        r'(?i)(IMAD|OMAD|fed\s+ref)',
        r'(?i)chips?\s+(debit|credit|transfer)',
    ],
    'book_transfer': [
        r'(?i)book\s+(transfer|entry)',
        r'(?i)internal\s+transfer',
        r'(?i)journal\s+entry',
    ],
    'check': [
        r'(?i)check\s*#?\s*\d+',
        r'(?i)check\s+paid',
        r'(?i)cashier.?s\s+check',
    ],
    'deposit': [
        r'(?i)(deposit|credit\s+memo)',
    ],
    'withdrawal': [
        r'(?i)(withdrawal|debit\s+memo)',
    ],
    'interest': [
        r'(?i)(interest\s+(paid|earned|credited)|int\s+pd)',
    ],
    'fee': [
        r'(?i)(service\s+charge|maintenance\s+fee|account\s+fee|wire\s+fee)',
    ],
    'dividend': [
        r'(?i)(dividend|div\s+payment)',
    ],
    'securities': [
        r'(?i)(bought|sold|purchase|sale)\s+\d',
        r'(?i)(settlement|trade\s+date)',
    ],
}


def identify_bank(text):
    """Identify which bank this page belongs to."""
    snippet = text[:1500]

    # Universal noise exclusion — applies to ALL banks
    UNIVERSAL_NOISE = [
        r'(?i)FinCEN\s+(I\s+)?Financial\s+Crimes',
        r'(?i)Financial\s+Crimes\s+Enforcement\s+Network',
        r'(?i)BSAR\s+Transcript',
        r'(?i)UNITED\s+STATES\s+DISTRICT\s+COURT',
        r'(?i)Case\s+\d+:\d+-cv-\d+.*Filed',
        r'(?i)Department\s+of\s+(Justice|the\s+Treasury)',
    ]
    first_300 = snippet[:300]
    for noise_pat in UNIVERSAL_NOISE:
        if re.search(noise_pat, first_300):
            # Exception: SDNY exhibits with actual transaction data
            if re.search(r'(?i)EXHIBIT\s+[A-E]:\s+TRANSACTIONS', text[:500]):
                break  # Allow through — these are real
            return None, 'UNIVERSAL_NOISE'

    for bank, config in sorted(BANK_SIGNATURES.items(), key=lambda x: x[1]['priority']):
        for pat in config['patterns']:
            if pat.search(snippet):
                # Check excludes
                excluded = False
                for ex in config['exclude']:
                    if re.search(ex, snippet[:500]):
                        excluded = True
                        break
                if excluded:
                    return None, 'EXCLUDED'

                # Check strong markers
                strong = sum(1 for sm in config['strong_markers'] if re.search(sm, text[:3000]))

                # For high-noise banks, require at least 1 strong marker
                HIGH_NOISE_BANKS = ['Deutsche Bank', 'First Bank PR', 'HSBC']
                if bank in HIGH_NOISE_BANKS and strong == 0:
                    return None, 'NO_STRONG_MARKER'

                return bank, strong
    return None, 0


def is_financial_page(text, bank=None):
    """Check if page has real financial data (not just mentions)."""
    dollars = DOLLAR.findall(text[:3000])

    # High-noise banks need stronger evidence
    HIGH_NOISE = ['Deutsche Bank', 'First Bank PR', 'HSBC']
    min_dollars = 3 if bank in HIGH_NOISE else 2
    min_signals = 2 if bank in HIGH_NOISE else 1

    if len(dollars) < min_dollars:
        return False

    financial_signals = [
        r'(?i)(opening|closing|ending|beginning|previous|available|current)\s+balance',
        r'(?i)account\s+(number|no|#|activity|statement|summary)',
        r'(?i)(debit|credit|deposit|withdrawal|transfer|payment)',
        r'(?i)statement\s+(period|date|of)',
        r'(?i)(total|subtotal|net)\s+(debit|credit|amount|balance)',
        r'(?i)(wire|check|ach)\s+(in|out|transfer|paid)',
        r'(?i)portfolio\s+holdings',
        r'(?i)cash\s+(activity|equivalents|management)',
    ]
    signals = sum(1 for fp in financial_signals if re.search(fp, text[:2000]))
    return signals >= min_signals


def classify_tx_type(text_block):
    """Classify transaction type from text."""
    for tx_type, patterns in TX_TYPE_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text_block):
                return tx_type
    return 'unknown'


def extract_date(text):
    """Extract first date from text."""
    m = DATE_MDY.search(text)
    if m:
        month, day, year = m.groups()
        if len(year) == 2:
            yr = int(year)
            year = str(2000 + yr) if yr < 50 else str(1900 + yr)
        try:
            return f"{year}-{int(month):02d}-{int(day):02d}"
        except:
            pass
    m = DATE_ISO.search(text)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def extract_amounts(text):
    """Extract dollar amounts from text block."""
    amounts = []
    for m in DOLLAR_STRICT.findall(text):
        try:
            val = float(m.replace(',', ''))
            if 0.01 < val < 500_000_000:
                amounts.append(val)
        except:
            continue
    if not amounts:
        for m in DOLLAR.findall(text):
            try:
                val = float(m.replace(',', ''))
                if 0.01 < val < 500_000_000:
                    amounts.append(val)
            except:
                continue
    return amounts


def extract_year_from_page(text):
    """Try to get year from statement period or dates on page."""
    patterns = [
        r'(?i)statement\s+(?:period|date)[:\s]+.*?(\d{4})',
        r'(?i)(?:for\s+)?(?:the\s+)?(?:period|month)\s+(?:of|ending)\s+.*?(\d{4})',
        r'(?i)(\d{4})\s+(?:statement|account)',
    ]
    for pat in patterns:
        m = re.search(pat, text[:1000])
        if m:
            yr = int(m.group(1))
            if 1990 <= yr <= 2025:
                return yr
    dates = DATE_MDY.findall(text[:2000])
    for month, day, year in dates:
        yr = int(year)
        if len(year) == 2:
            yr = 2000 + yr if yr < 50 else 1900 + yr
        if 1990 <= yr <= 2025:
            return yr
    return None


def extract_description(text_block, max_len=200):
    """Extract meaningful description from a transaction block."""
    # Remove dates and dollar signs
    clean = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4}', '', text_block)
    clean = re.sub(r'\$[\d,]+\.?\d*', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()

    # Look for entity-like content
    for entity in EPSTEIN_ENTITIES:
        if entity.lower() in clean.lower():
            # Extract surrounding context
            idx = clean.lower().find(entity.lower())
            start = max(0, idx - 30)
            end = min(len(clean), idx + len(entity) + 50)
            return clean[start:end].strip()

    # Return first meaningful chunk
    if len(clean) > 10:
        return clean[:max_len].strip()
    return ''


def find_epstein_entity(text_block):
    """Check if any known Epstein entity appears in this transaction."""
    lower = text_block.lower()
    for entity in EPSTEIN_ENTITIES:
        if entity in lower:
            return entity.title()
    return None


def parse_exhibit_table(text, bank, bates):
    """Parse SDNY exhibit-style transaction tables (Exhibit A-E format).
    These are structured tables with columns: Date | Description | Amount | Balance."""
    records = []
    lines = text.split('\n')

    for i, line in enumerate(lines):
        # Look for lines with date + dollar amount
        date_match = DATE_MDY.search(line)
        amounts = extract_amounts(line)

        if date_match and amounts:
            date_str = extract_date(line)
            tx_amount = max(amounts) if amounts else None
            desc = extract_description(line)
            tx_type = classify_tx_type(line)
            entity = find_epstein_entity(line)

            # Look at next 1-2 lines for additional description
            context = line
            for j in range(1, min(3, len(lines) - i)):
                context += ' ' + lines[i + j]
            if not entity:
                entity = find_epstein_entity(context)
            if not desc or len(desc) < 5:
                desc = extract_description(context)

            records.append({
                'bank': bank,
                'bates': bates,
                'tx_date': date_str,
                'tx_amount': tx_amount,
                'tx_type': tx_type,
                'description': desc[:300] if desc else '',
                'entity_match': entity,
                'year': int(date_str[:4]) if date_str and len(date_str) >= 4 else None,
            })

    return records


def parse_statement_page(text, bank, bates):
    """Universal statement page parser.
    Splits text into transaction blocks and extracts structured data."""
    records = []

    # Strategy 1: Line-by-line scan for date+amount co-occurrence
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if len(line.strip()) < 5:
            continue

        date_str = extract_date(line)
        amounts = extract_amounts(line)

        if not date_str and not amounts:
            continue

        # Build context from this line + next 2
        context = line
        for j in range(1, min(3, len(lines) - i)):
            next_line = lines[i + j] if i + j < len(lines) else ''
            context += ' ' + next_line
            if not date_str:
                date_str = extract_date(next_line)
            if not amounts:
                amounts = extract_amounts(next_line)

        if not amounts:
            continue

        tx_amount = max(amounts)
        tx_type = classify_tx_type(context)
        desc = extract_description(context)
        entity = find_epstein_entity(context)

        # Dedup: don't add if same date+amount already in records
        sig = f"{date_str}|{tx_amount:.2f}"
        if any(f"{r['tx_date']}|{r['tx_amount']:.2f}" == sig for r in records):
            continue

        records.append({
            'bank': bank,
            'bates': bates,
            'tx_date': date_str,
            'tx_amount': tx_amount,
            'tx_type': tx_type,
            'description': desc[:300] if desc else '',
            'entity_match': entity,
            'year': int(date_str[:4]) if date_str and len(date_str) >= 4 else None,
        })

    return records


def create_table(conn):
    """Create bank_statement_transactions table."""
    conn.execute("DROP TABLE IF EXISTS bank_statement_transactions")
    conn.execute("""
        CREATE TABLE bank_statement_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bank TEXT NOT NULL,
            bates TEXT,
            tx_date TEXT,
            tx_amount REAL,
            tx_type TEXT,
            description TEXT,
            entity_match TEXT,
            year INTEGER,
            dedup_status TEXT DEFAULT 'RAW',
            validation_tier TEXT,
            extracted_at TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bst_bank ON bank_statement_transactions(bank)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bst_amount ON bank_statement_transactions(tx_amount)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bst_date ON bank_statement_transactions(tx_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bst_entity ON bank_statement_transactions(entity_match)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bst_bates ON bank_statement_transactions(bates)")
    conn.commit()


def validate_against_fincen(conn, records):
    """Cross-validate amounts against fincen_transactions."""
    c = conn.cursor()
    try:
        c.execute("SELECT amount FROM fincen_transactions WHERE amount > 0")
        fincen_amounts = set()
        for row in c:
            amt = float(row[0])
            fincen_amounts.add(round(amt, 2))

        for rec in records:
            amt = round(rec['tx_amount'], 2) if rec['tx_amount'] else 0
            if amt in fincen_amounts:
                rec['validation_tier'] = 'FINCEN_AMOUNT_MATCH'
            elif any(abs(amt - fa) / max(fa, 1) < 0.05 for fa in fincen_amounts if fa > 1000):
                rec['validation_tier'] = 'FINCEN_RANGE_MATCH'
            else:
                rec['validation_tier'] = 'STATEMENT_ONLY'
    except Exception as e:
        for rec in records:
            rec['validation_tier'] = 'STATEMENT_ONLY'


def main():
    live = '--live' in sys.argv

    print("=" * 70)
    print("MULTI-BANK STATEMENT PARSER")
    print(f"Mode: {'LIVE — will write to DB' if live else 'DRY RUN'}")
    print("=" * 70)

    if not os.path.exists(DB_PATH):
        print(f"ERROR: DB not found: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get existing JPM bates to skip
    c.execute("SELECT DISTINCT bates FROM extracted_payments")
    jpm_bates = set(r[0] for r in c.fetchall() if r[0])
    print(f"[DB] Skipping {len(jpm_bates):,} bates already in extracted_payments")

    all_records = []
    bank_stats = Counter()
    bank_pages_parsed = Counter()
    bank_pages_skipped = Counter()
    rejection_reasons = Counter()
    errors = 0

    # Process in batches
    c.execute("SELECT COUNT(*) FROM extracted_text WHERE text_content IS NOT NULL")
    total_pages = c.fetchone()[0]
    print(f"[DB] Total OCR pages: {total_pages:,}")
    print(f"[DB] Scanning for non-JPM bank statement pages...\n")

    BATCH = 50000
    offset = 0
    start_time = datetime.now()

    while offset < total_pages:
        c.execute("""
            SELECT et.file_id, et.page_num, et.text_content,
                   REPLACE(f.title, '.pdf', '') as bates
            FROM extracted_text et
            JOIN files f ON f.id = et.file_id
            WHERE et.text_content IS NOT NULL
            LIMIT ? OFFSET ?
        """, (BATCH, offset))

        rows = c.fetchall()
        if not rows:
            break

        for row in rows:
            text = row['text_content']
            bates = row['bates'] or ''
            if not text or len(text) < 50:
                continue

            # Skip if already extracted by JPM parser
            if bates in jpm_bates:
                continue

            try:
                # Identify bank
                bank, strength = identify_bank(text)
                if not bank:
                    if isinstance(strength, str):
                        rejection_reasons[strength] += 1
                    continue

                # Must be financial page
                if not is_financial_page(text, bank=bank):
                    bank_pages_skipped[bank] += 1
                    rejection_reasons[f'{bank}:NOT_FINANCIAL'] += 1
                    continue

                bank_pages_parsed[bank] += 1

                # Check if this is an exhibit table (SDNY format)
                is_exhibit = bool(re.search(r'(?i)exhibit\s+[A-E]', text[:500]))

                if is_exhibit:
                    page_records = parse_exhibit_table(text, bank, bates)
                else:
                    page_records = parse_statement_page(text, bank, bates)

                for rec in page_records:
                    bank_stats[bank] += 1
                    all_records.append(rec)

            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  ERROR on {bates}: {e}")

        offset += BATCH
        elapsed = (datetime.now() - start_time).total_seconds()
        pct = min(offset, total_pages) / total_pages * 100
        print(f"  {min(offset, total_pages):,}/{total_pages:,} ({pct:.0f}%) | "
              f"{len(all_records):,} records | {elapsed:.0f}s")

    elapsed = (datetime.now() - start_time).total_seconds()

    # Validate against FinCEN
    print(f"\n[VALIDATE] Cross-referencing {len(all_records):,} records against FinCEN...")
    validate_against_fincen(conn, all_records)

    # Dedup: same bank + bates + date + amount
    seen = set()
    deduped = []
    dupes = 0
    for rec in all_records:
        sig = f"{rec['bank']}|{rec['bates']}|{rec['tx_date']}|{rec['tx_amount']:.2f}" if rec['tx_amount'] else None
        if sig and sig in seen:
            dupes += 1
            continue
        if sig:
            seen.add(sig)
        rec['dedup_status'] = 'UNIQUE'
        deduped.append(rec)

    print(f"  Deduped: {len(all_records):,} → {len(deduped):,} ({dupes:,} duplicates removed)")

    # Results
    print(f"\n{'=' * 70}")
    print("RESULTS")
    print(f"{'=' * 70}")
    print(f"\n  {'Bank':<25} {'Pages':>8} {'Records':>10} {'Volume':>18}")
    print("  " + "─" * 63)

    total_vol = 0
    for bank in sorted(bank_stats.keys(), key=lambda b: -bank_stats[b]):
        bank_recs = [r for r in deduped if r['bank'] == bank]
        vol = sum(r['tx_amount'] or 0 for r in bank_recs)
        total_vol += vol
        pages = bank_pages_parsed[bank]
        print(f"  {bank:<25} {pages:>8,} {len(bank_recs):>10,} ${vol:>16,.2f}")

    print("  " + "─" * 63)
    total_pages_parsed = sum(bank_pages_parsed.values())
    print(f"  {'TOTAL':<25} {total_pages_parsed:>8,} {len(deduped):>10,} ${total_vol:>16,.2f}")

    # Transaction types
    type_counts = Counter(r['tx_type'] for r in deduped)
    print(f"\n  Transaction Types:")
    for tx_type, cnt in type_counts.most_common():
        print(f"    {tx_type:<25} {cnt:>8,}")

    # Entity matches
    entity_hits = [r for r in deduped if r['entity_match']]
    entity_counts = Counter(r['entity_match'] for r in entity_hits)
    print(f"\n  Epstein Entity Matches: {len(entity_hits):,}/{len(deduped):,}")
    for entity, cnt in entity_counts.most_common(15):
        vol = sum(r['tx_amount'] or 0 for r in entity_hits if r['entity_match'] == entity)
        print(f"    {entity:<30} {cnt:>6} txns  ${vol:>14,.2f}")

    # Validation tiers
    tier_counts = Counter(r.get('validation_tier', 'UNKNOWN') for r in deduped)
    print(f"\n  Validation Tiers:")
    for tier, cnt in tier_counts.most_common():
        print(f"    {tier:<30} {cnt:>8,}")

    print(f"\n  Errors: {errors}")

    # Show rejection reasons
    print(f"\n  Noise Rejection Summary:")
    for reason, cnt in rejection_reasons.most_common(15):
        print(f"    {reason:<40} {cnt:>8,}")

    print(f"  Elapsed: {elapsed:.1f}s")

    # Insert to DB
    if live:
        print(f"\n[DB] Creating bank_statement_transactions table...")
        create_table(conn)
        now = datetime.now().isoformat()
        inserted = 0
        for rec in deduped:
            try:
                conn.execute("""
                    INSERT INTO bank_statement_transactions
                    (bank, bates, tx_date, tx_amount, tx_type, description,
                     entity_match, year, dedup_status, validation_tier, extracted_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rec['bank'], rec['bates'], rec['tx_date'], rec['tx_amount'],
                    rec['tx_type'], rec['description'], rec['entity_match'],
                    rec['year'], rec['dedup_status'], rec.get('validation_tier', 'STATEMENT_ONLY'),
                    now
                ))
                inserted += 1
            except Exception as e:
                if inserted < 3:
                    print(f"  INSERT ERROR: {e}")
        conn.commit()
        print(f"[DB] Inserted {inserted:,} records into bank_statement_transactions")
    else:
        print(f"\n  DRY RUN — use --live to write {len(deduped):,} records to DB")

    conn.close()
    print(f"\n  For the girls.")


if __name__ == "__main__":
    main()
