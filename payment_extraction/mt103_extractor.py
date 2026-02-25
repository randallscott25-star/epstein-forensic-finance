"""
mt103_extractor.py — Extract the 37 real SWIFT MT103 messages from EFTA corpus.

Filters out false positives (fax logs, call records, police reports) that
were contaminating the old SWIFT extractor.

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import re
import sqlite3
import os
from datetime import date

from extraction_framework import resolve_entity, score_transaction, BIC_PATTERN

# noise sources that match :20:/:32A:/:59: patterns but aren't SWIFT messages
NOISE_FILTERS = [
    'MetroPCS', 'Police', 'Fax Activity', 'Call Detail',
    'Lieutenant', 'hp LaserJet', 'BILLED PHONE',
]

MT103_FIELDS = {
    "ref":        re.compile(r':20:\s*(.+?)$', re.MULTILINE),
    "value_date": re.compile(r':32A:(\d{6})([A-Z]{3})([\d,.]+)'),
    "originator": re.compile(r':50[AK]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "beneficiary":re.compile(r':59[A]?:?\s*(.+?)(?=\n:\d|$)', re.DOTALL),
    "sender_info":re.compile(r':72:\s*(.+?)(?=\n:\d|$)', re.DOTALL),
}


def is_noise(text):
    for noise in NOISE_FILTERS:
        if noise in text:
            return True
    return False


def has_real_mt103_structure(text):
    """Must have at least :20: + :32A: + :59: and NOT be noise."""
    has_ref = bool(MT103_FIELDS["ref"].search(text))
    has_val = bool(MT103_FIELDS["value_date"].search(text))
    has_ben = bool(MT103_FIELDS["beneficiary"].search(text))
    return has_ref and has_val and has_ben and not is_noise(text)


def parse_mt103(text, bates, dataset):
    record = {
        "bates": bates,
        "dataset": dataset,
        "payment_type": "SWIFT_MT103",
        "direction": "DEBIT",
        "extraction_method": "mt103_strict",
        "currency": "USD",
        "routing": {},
    }

    m = MT103_FIELDS["value_date"].search(text)
    if m:
        ds, currency, amt = m.group(1), m.group(2), m.group(3)
        record["currency"] = currency
        try:
            y = 2000 + int(ds[:2]) if int(ds[:2]) < 50 else 1900 + int(ds[:2])
            record["date"] = date(y, int(ds[2:4]), int(ds[4:6]))
        except:
            pass
        try:
            record["amount"] = float(amt.replace(",", ""))
        except:
            pass

    m = MT103_FIELDS["beneficiary"].search(text)
    if m:
        raw = m.group(1).strip()
        lines = [l.strip() for l in raw.split('\n') if l.strip()]
        name_parts = [l for l in lines if not re.match(r'^/?\d+$', l)]
        name = ' '.join(name_parts)
        name = re.sub(r'\s+', ' ', name).strip()
        record["beneficiary_raw"] = name
        canonical, conf = resolve_entity(name)
        record["beneficiary_canonical"] = canonical
        record["entity_confidence"] = conf

    m = MT103_FIELDS["originator"].search(text)
    if m:
        record["source_entity"] = re.sub(r'\s+', ' ', m.group(1).strip()).split('\n')[0]

    m = MT103_FIELDS["ref"].search(text)
    if m:
        record["notes"] = f"Ref: {m.group(1).strip()}"

    bics = BIC_PATTERN.findall(text)
    noise_bics = {"CRED", "DEBT", "ABAN", "BENM", "MARF"}
    bics = [b for b in bics if b not in noise_bics and len(b) >= 8]
    if bics:
        record["routing"]["bic_codes"] = list(set(bics))

    record["raw_text"] = text[:2000]
    record["priority_score"] = score_transaction(record)
    return record


def run_mt103_extractor(db_path=None, verbose=True):
    if not db_path:
        paths = [
            os.path.expanduser("~/Desktop/epstein_files.db"),
            "/Volumes/My Book/epstein_project/epstein_files.db",
        ]
        for p in paths:
            if os.path.exists(p):
                db_path = p
                break

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if verbose:
        print("\n" + "=" * 70)
        print("MT103 SWIFT EXTRACTOR (strict)")
        print("=" * 70)

    cur.execute("""
        SELECT REPLACE(f.title, '.pdf', ''), f.dataset, et.page_num, et.text_content
        FROM extracted_text et
        JOIN files f ON f.id = et.file_id
        WHERE et.text_content LIKE '%:32A:%'
        AND et.text_content LIKE '%:59:%'
        AND et.text_content LIKE '%:20:%'
        AND et.text_content NOT LIKE '%MetroPCS%'
        AND et.text_content NOT LIKE '%Police%'
        AND et.text_content NOT LIKE '%Fax Activity%'
        AND et.text_content NOT LIKE '%Call Detail%'
        AND et.text_content NOT LIKE '%LaserJet%'
    """)
    rows = cur.fetchall()
    conn.close()

    if verbose:
        print(f"[MT103] Candidate pages: {len(rows)}")

    records = []
    seen_wires = set()  # dedup by (date, amount, beneficiary)
    for bates, dataset, page_num, text in rows:
        if not text:
            continue
        if has_real_mt103_structure(text):
            rec = parse_mt103(text, bates, dataset)
            if rec.get("amount") or rec.get("beneficiary_raw"):
                # dedup key: date + amount + first 20 chars of beneficiary
                ben_key = (rec.get("beneficiary_canonical") or rec.get("beneficiary_raw") or "")[:20].upper()
                dedup_key = (str(rec.get("date")), rec.get("amount"), ben_key)
                if dedup_key in seen_wires:
                    continue
                seen_wires.add(dedup_key)
                records.append(rec)

    if verbose:
        print(f"[MT103] Extracted: {len(records)} records")
        total = sum(r.get("amount", 0) for r in records)
        print(f"[MT103] Volume: ${total:,.2f}")
        for r in records:
            ben = r.get("beneficiary_canonical") or r.get("beneficiary_raw") or "?"
            print(f"  {r.get('date', '?')} | ${r.get('amount', 0):,.2f} | {ben} | {r.get('bates')}")

    return records


if __name__ == "__main__":
    run_mt103_extractor(verbose=True)
