#!/usr/bin/env python3
"""
SOURCE DOCUMENT CLASSIFIER
Goes back to the OCR source for every TRANSACTION record in
bank_statement_transactions and classifies the SOURCE PAGE as:

  BANK_STATEMENT   — actual bank/brokerage statement page
  SDNY_EXHIBIT     — SDNY prosecution exhibit with transaction tables
  COURT_FILING     — lawsuit, motion, complaint mentioning amounts
  FINCEN_REPORT    — BSA/SAR/FinCEN enforcement document
  LEGAL_LETTER     — attorney correspondence, subpoena responses
  ACCOUNT_SUMMARY  — account overview / relationship summary (not transactions)
  NEWS_REFERENCE   — news article or press coverage mentioning amounts
  OTHER            — can't determine

Then reclassifies:
  - BANK_STATEMENT + SDNY_EXHIBIT → keep as TRANSACTION
  - Everything else → demote to LEGAL_REFERENCE (described, not source data)

This is the inflation fix. A court filing saying "defendant wired $5M"
is NOT the same as a bank statement showing a $5M wire.

Author: Randall Scott Taylor
"""

import sqlite3, re, os, sys
from collections import Counter, defaultdict

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")

# ── Source document classification patterns ──

# BANK STATEMENT: actual financial institution statement
BANK_STMT_SIGNALS = [
    (3, r'(?i)office\s+servicing\s+your\s+account'),        # Bear Stearns header
    (3, r'(?i)your\s+portfolio\s+holdings'),                  # Brokerage statement
    (3, r'(?i)account\s+statement\s+for'),                    # Statement header
    (3, r'(?i)statement\s+period\s*:\s*\d'),                  # Statement period with date
    (3, r'(?i)resource\s+management\s+account'),              # UBS statement type
    (3, r'(?i)cash\s+activity\s+summary'),                    # UBS activity section
    (2, r'(?i)(opening|closing|ending)\s+balance\s*[\$:\d]'), # Balance with value
    (2, r'(?i)account\s+number\s*:?\s*[\dXx*]{4,}'),         # Account number masked
    (2, r'(?i)previous\s+balance\s*[\$:\d]'),
    (2, r'(?i)(visa|mastercard|credit\s+card)\s+statement'),
    (2, r'(?i)minimum\s+payment\s+due'),
    (2, r'(?i)payment\s+due\s+date'),
    (1, r'(?i)cleared\s+through\s+its'),                     # Bear Stearns sub-header
    (1, r'(?i)what.?s\s+in\s+this\s+statement'),
    (1, r'(?i)account\s+activity\s+detail'),
    (1, r'(?i)page\s+\d+\s+of\s+\d+'),                      # Statement pagination
]

# SDNY EXHIBIT: prosecution exhibits with real transaction tables
SDNY_EXHIBIT_SIGNALS = [
    (4, r'(?i)EXHIBIT\s+[A-E]\s*:\s*TRANSACTIONS'),          # "Exhibit E: Transactions involving..."
    (3, r'(?i)SDNY[_\s]GM[_\s]\d{8}'),                       # SDNY bates stamp
    (3, r'(?i)EXHIBIT\s+[A-E]\s*:.*ACCOUNT'),                # "Exhibit A: Account..."
    (2, r'(?i)government\s+exhibit'),
    (2, r'(?i)MMDA.*transactions'),                           # Money Market Deposit Account
    (1, r'(?i)exhibit\s+[A-E]\b'),                            # Generic exhibit ref
]

# COURT FILING: lawsuits, motions, complaints
COURT_FILING_SIGNALS = [
    (4, r'(?i)UNITED\s+STATES\s+DISTRICT\s+COURT'),
    (4, r'(?i)Case\s+\d+:\d+-cv-\d+.*Document\s+\d+'),      # Docket entry
    (4, r'(?i)Filed\s+\d{2}/\d{2}/\d{2,4}\s+Page'),
    (3, r'(?i)(plaintiff|defendant|respondent|petitioner)\s'),
    (3, r'(?i)(complaint|motion|memorandum|declaration|affidavit|indictment)'),
    (3, r'(?i)the\s+(court|jury)\s+(finds?|ruled|held|ordered)'),
    (3, r'(?i)conspiracy\s+to\s+(commit|defraud|launder)'),
    (2, r'(?i)(alleged|allegedly|purported)\s'),
    (2, r'(?i)in\s+re\s+:?\s*\w'),                           # "In re: ..."
    (2, r'(?i)cause\s+of\s+action'),
    (2, r'(?i)class\s+action'),
    (2, r'(?i)(judgment|verdict|settlement|decree)'),
    (1, r'(?i)(deposition|testimony|testified)'),
    (1, r'(?i)attorney.?s?\s+fees'),
]

# FINCEN/ENFORCEMENT: BSA, SAR, FinCEN documents
FINCEN_SIGNALS = [
    (5, r'(?i)Financial\s+Crimes\s+Enforcement\s+Network'),
    (5, r'(?i)FinCEN'),
    (4, r'(?i)BSAR\s+Transcript'),
    (4, r'(?i)Suspicious\s+Activity\s+Report'),
    (3, r'(?i)(civil\s+money|monetary)\s+penalty'),
    (3, r'(?i)anti.?money\s+laundering'),
    (3, r'(?i)bank\s+secrecy\s+act'),
    (2, r'(?i)(AML|BSA|KYC|CDD)\s+(compliance|violation|failure|program)'),
    (2, r'(?i)consent\s+order'),
]

# LEGAL LETTER: attorney correspondence, subpoena responses
LEGAL_LETTER_SIGNALS = [
    (3, r'(?i)(dear\s+)?(mr\.|ms\.|counsel|judge|honor)'),
    (3, r'(?i)(PLLC|LLP|Esq\.?|Attorney\s+at\s+Law)'),
    (3, r'(?i)(subpoena|duces\s+tecum|summons)'),
    (3, r'(?i)grand\s+jury'),
    (2, r'(?i)(enclosed|attached)\s+(please\s+find|herewith|are)'),
    (2, r'(?i)Department\s+of\s+Justice'),
    (2, r'(?i)United\s+States\s+Attorney'),
    (2, r'(?i)(respectfully|sincerely|regards)\s*,'),
    (2, r'(?i)pursuant\s+to'),
    (1, r'(?i)law\s+(firm|office|group)'),
]

# ACCOUNT SUMMARY: overview docs (not individual transactions)
ACCOUNT_SUMMARY_SIGNALS = [
    (3, r'(?i)SUMMARY\s+OF\s+.*ACCOUNTS?\s+AS\s+OF'),       # "Summary of accounts as of..."
    (3, r'(?i)FINANCIAL\s+INSTUTITION'),                     # Typo in Maxwell docs
    (3, r'(?i)relationship\s+summary'),
    (2, r'(?i)Form\s+8938'),                                  # Foreign account reporting
    (2, r'(?i)FBAR|foreign\s+bank\s+account\s+report'),
    (2, r'(?i)schedule\s+of\s+(assets|accounts|investments)'),
    (1, r'(?i)total\s+(assets|liabilities|net\s+worth)'),
]

# NEWS: articles, press coverage
NEWS_SIGNALS = [
    (3, r'(?i)(reuters|associated\s+press|bloomberg|wsj|nyt|cnn)'),
    (3, r'(?i)www\.\w+\.(com|org|net)/.*article'),
    (2, r'(?i)(reported|according\s+to\s+sources|press\s+release)'),
    (2, r'(?i)(journalist|reporter|editor|correspondent)'),
]


def classify_source_page(text):
    """Classify what kind of document this OCR page comes from."""
    if not text or len(text) < 30:
        return 'OTHER', {}

    # Use first 2000 chars for classification (header/intro area)
    header = text[:2000]
    # But check deeper for some patterns
    deep = text[:4000]

    scores = {
        'BANK_STATEMENT': 0,
        'SDNY_EXHIBIT': 0,
        'COURT_FILING': 0,
        'FINCEN_REPORT': 0,
        'LEGAL_LETTER': 0,
        'ACCOUNT_SUMMARY': 0,
        'NEWS_REFERENCE': 0,
    }

    matched = defaultdict(list)

    for weight, pat in BANK_STMT_SIGNALS:
        if re.search(pat, deep):
            scores['BANK_STATEMENT'] += weight
            matched['BANK_STATEMENT'].append(pat[:40])

    for weight, pat in SDNY_EXHIBIT_SIGNALS:
        if re.search(pat, deep):
            scores['SDNY_EXHIBIT'] += weight
            matched['SDNY_EXHIBIT'].append(pat[:40])

    for weight, pat in COURT_FILING_SIGNALS:
        if re.search(pat, header):
            scores['COURT_FILING'] += weight
            matched['COURT_FILING'].append(pat[:40])

    for weight, pat in FINCEN_SIGNALS:
        if re.search(pat, header):
            scores['FINCEN_REPORT'] += weight
            matched['FINCEN_REPORT'].append(pat[:40])

    for weight, pat in LEGAL_LETTER_SIGNALS:
        if re.search(pat, header):
            scores['LEGAL_LETTER'] += weight
            matched['LEGAL_LETTER'].append(pat[:40])

    for weight, pat in ACCOUNT_SUMMARY_SIGNALS:
        if re.search(pat, deep):
            scores['ACCOUNT_SUMMARY'] += weight
            matched['ACCOUNT_SUMMARY'].append(pat[:40])

    for weight, pat in NEWS_SIGNALS:
        if re.search(pat, header):
            scores['NEWS_REFERENCE'] += weight
            matched['NEWS_REFERENCE'].append(pat[:40])

    # Winner
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return 'OTHER', scores

    # Tie-breaking: SDNY_EXHIBIT beats COURT_FILING if both present
    # (exhibits have real data even if they're part of court proceedings)
    if scores['SDNY_EXHIBIT'] >= 3 and scores['COURT_FILING'] > 0:
        return 'SDNY_EXHIBIT', scores

    # BANK_STATEMENT beats everything if strong enough
    if scores['BANK_STATEMENT'] >= 4:
        return 'BANK_STATEMENT', scores

    return best, scores


def main():
    print("=" * 70)
    print("SOURCE DOCUMENT CLASSIFIER — INFLATION FIX")
    print("=" * 70)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Add source_doc_type column
    try:
        c.execute("ALTER TABLE bank_statement_transactions ADD COLUMN source_doc_type TEXT")
        conn.commit()
        print("[DB] Added source_doc_type column")
    except:
        # Reset it
        c.execute("UPDATE bank_statement_transactions SET source_doc_type = NULL")
        conn.commit()
        print("[DB] source_doc_type column exists — resetting")

    # Get all records grouped by bates (one page lookup per bates)
    c.execute("""
        SELECT DISTINCT bates FROM bank_statement_transactions
        WHERE bates IS NOT NULL
    """)
    all_bates = [r[0] for r in c.fetchall()]
    print(f"[DB] {len(all_bates):,} unique bates pages to classify")

    # Classify each source page
    bates_doc_type = {}
    classified = 0
    no_text = 0

    for i, bates in enumerate(all_bates):
        # Get OCR text for this page
        c.execute("""
            SELECT et.text_content
            FROM extracted_text et
            JOIN files f ON f.id = et.file_id
            WHERE REPLACE(f.title, '.pdf', '') = ?
            ORDER BY et.page_num
            LIMIT 3
        """, (bates,))
        rows = c.fetchall()

        if not rows:
            no_text += 1
            bates_doc_type[bates] = 'OTHER'
            continue

        # Combine first few pages for better classification
        combined = ' '.join(r[0][:2000] for r in rows if r[0])
        doc_type, scores = classify_source_page(combined)
        bates_doc_type[bates] = doc_type
        classified += 1

        if (i + 1) % 500 == 0:
            print(f"  Classified {i+1:,}/{len(all_bates):,} bates pages...")

    print(f"  Classified: {classified:,} | No text: {no_text:,}")

    # Apply to records
    print(f"\n[DB] Applying source_doc_type to records...")
    for bates, doc_type in bates_doc_type.items():
        c.execute("UPDATE bank_statement_transactions SET source_doc_type = ? WHERE bates = ?",
                 (doc_type, bates))
    conn.commit()

    # Now the key move: reclassify record_type based on source
    # Only BANK_STATEMENT and SDNY_EXHIBIT pages have real transaction data
    print(f"\n[RECLASSIFY] Demoting non-statement TRANSACTION records...")

    c.execute("""
        SELECT id, source_doc_type, record_type, bank, tx_amount
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
    """)
    txn_rows = c.fetchall()

    demoted = 0
    kept = 0
    demotion_stats = Counter()

    for rec_id, doc_type, rec_type, bank, amount in txn_rows:
        if doc_type in ('BANK_STATEMENT', 'SDNY_EXHIBIT'):
            kept += 1
        else:
            # Demote to LEGAL_REFERENCE
            c.execute("""
                UPDATE bank_statement_transactions 
                SET record_type = 'LEGAL_REFERENCE'
                WHERE id = ?
            """, (rec_id,))
            demoted += 1
            demotion_stats[f"{bank}:{doc_type}"] += 1

    conn.commit()
    print(f"  Kept as TRANSACTION: {kept:,}")
    print(f"  Demoted to LEGAL_REFERENCE: {demoted:,}")

    # Results
    print(f"\n{'=' * 70}")
    print("SOURCE DOCUMENT CLASSIFICATION")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT source_doc_type, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        GROUP BY source_doc_type
        ORDER BY COUNT(*) DESC
    """)
    print(f"\n  {'Source Type':<25} {'Records':>8} {'Volume':>20}")
    print("  " + "─" * 55)
    for doc_type, cnt, vol in c.fetchall():
        vol = vol or 0
        print(f"  {doc_type or 'NULL':<25} {cnt:>8,} ${vol:>18,.2f}")

    # Record types after reclassification
    print(f"\n{'=' * 70}")
    print("RECORD TYPES AFTER RECLASSIFICATION")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT record_type, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        GROUP BY record_type
        ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Record Type':<25} {'Records':>8} {'Volume':>20}")
    print("  " + "─" * 55)
    for rtype, cnt, vol in c.fetchall():
        vol = vol or 0
        marker = " ← REAL" if rtype == 'TRANSACTION' else ""
        print(f"  {rtype:<25} {cnt:>8,} ${vol:>18,.2f}{marker}")

    # Per-bank TRANSACTION only
    print(f"\n{'=' * 70}")
    print("TRANSACTION RECORDS BY BANK (source-verified)")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        GROUP BY bank
        ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Bank':<25} {'TXN Records':>12} {'Volume':>20}")
    print("  " + "─" * 60)
    total_txn_vol = 0
    for bank, cnt, vol in c.fetchall():
        vol = vol or 0
        total_txn_vol += vol
        print(f"  {bank:<25} {cnt:>12,} ${vol:>18,.2f}")
    print("  " + "─" * 60)
    print(f"  {'TOTAL':<25} {'':>12} ${total_txn_vol:>18,.2f}")

    # Demotion breakdown
    print(f"\n  Demotion detail (bank:source → LEGAL_REFERENCE):")
    for key, cnt in demotion_stats.most_common(20):
        print(f"    {key:<45} {cnt:>6,}")

    # Entity matches on clean TRANSACTION records
    print(f"\n{'=' * 70}")
    print("ENTITY MATCHES (TRANSACTION only, source-verified)")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT entity_match, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE entity_match IS NOT NULL
        AND record_type = 'TRANSACTION'
        GROUP BY entity_match
        ORDER BY SUM(tx_amount) DESC
        LIMIT 20
    """)
    for entity, cnt, vol in c.fetchall():
        vol = vol or 0
        print(f"  {entity:<30} {cnt:>6} txns  ${vol:>14,.2f}")

    # Before/after comparison
    print(f"\n{'=' * 70}")
    print("INFLATION FIX SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Raw parser output:          $68,745,222,404.77  (24,563 records)")
    print(f"  After record classifier:    $23,695,632,641.86  (10,513 TRANSACTION)")
    print(f"  After source doc classifier: ${total_txn_vol:>18,.2f}  ({kept:,} TRANSACTION)")
    
    if total_txn_vol > 0:
        reduction = (1 - total_txn_vol / 68_745_222_404.77) * 100
        print(f"  Total inflation removed:     {reduction:.1f}%")

    conn.close()
    print(f"\n  Source classification complete.")


if __name__ == "__main__":
    main()
