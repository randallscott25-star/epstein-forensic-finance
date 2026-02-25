#!/usr/bin/env python3
"""
QUICK CHECK: Are the ICIJ tables populated?
Run first before the full cross-reference.

    python3 icij_quickcheck.py /path/to/database.db
"""
import sqlite3, sys

if len(sys.argv) < 2:
    print("Usage: python3 icij_quickcheck.py /path/to/database.db")
    sys.exit(1)

conn = sqlite3.connect(sys.argv[1])
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# All tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print(f"ALL TABLES ({len(tables)}):")
for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM [{t}]")
    c = cur.fetchone()[0]
    flag = " ← ICIJ" if 'icij' in t.lower() else ""
    flag = flag or (" ← FAA" if 'faa' in t.lower() else "")
    flag = flag or (" ← FINCEN" if 'fincen' in t.lower() else "")
    flag = flag or (" ★ WIRE LEDGER" if 'master_wire' in t.lower() else "")
    flag = flag or (" ★ FUND FLOWS" if t == 'fund_flows' else "")
    flag = flag or (" ★ AUDITED" if 'audited' in t.lower() else "")
    flag = flag or (" ★ FINANCIAL HITS" if 'financial_hit' in t.lower() else "")
    flag = flag or (" ★ TRUST" if 'trust_transfer' in t.lower() else "")
    flag = flag or (" ★ REDACTION" if 'redact' in t.lower() else "")
    print(f"  {t}: {c:>12,} rows{flag}")

# ICIJ detail
print("\n" + "=" * 60)
for t in tables:
    if 'icij' in t.lower():
        print(f"\n{t} SCHEMA:")
        cur.execute(f"PRAGMA table_info([{t}])")
        for col in cur.fetchall():
            print(f"  {col['name']} ({col['type']})")
        cur.execute(f"SELECT * FROM [{t}] LIMIT 2")
        for row in cur.fetchall():
            print(f"  SAMPLE: {dict(row)}")

conn.close()
