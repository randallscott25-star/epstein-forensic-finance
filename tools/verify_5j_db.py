"""
Phase 5J Database Verification
Run on Mac: python verify_5j_db.py
Checks all Phase 5J data persisted correctly in epstein_files.db
"""
import sqlite3
from pathlib import Path
from collections import Counter

DB = Path.home() / "Desktop" / "epstein_files.db"

def main():
    if not DB.exists():
        print(f"ERROR: DB not found at {DB}")
        return False

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    ok = True

    print("=" * 70)
    print("  PHASE 5J DATABASE VERIFICATION")
    print("=" * 70)

    # ── CHECK 1: bank_statement_transactions table exists ──
    tbl = conn.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='bank_statement_transactions'
    """).fetchone()
    if not tbl:
        print("\n❌ FAIL: bank_statement_transactions table MISSING")
        return False
    print("\n✅ bank_statement_transactions table exists")

    # ── CHECK 2: Total record count ──
    total = conn.execute("SELECT COUNT(*) c FROM bank_statement_transactions").fetchone()['c']
    print(f"\n  Total records: {total:,}")
    if total == 24563:
        print("  ✅ Expected 24,563 — MATCH")
    else:
        print(f"  ⚠️  Expected 24,563 — GOT {total:,}")
        ok = False

    # ── CHECK 3: Record type breakdown ──
    print("\n  Record type breakdown:")
    types = conn.execute("""
        SELECT record_type, COUNT(*) c, SUM(tx_amount) vol
        FROM bank_statement_transactions
        GROUP BY record_type
        ORDER BY c DESC
    """).fetchall()
    
    txn_count = 0
    txn_vol = 0
    for t in types:
        rt = t['record_type'] or 'NULL'
        vol = t['vol'] or 0
        flag = " ← VERIFIED CLEAN" if rt == 'TRANSACTION' else ""
        print(f"    {rt:30s} {t['c']:>6,}  ${vol:>20,.2f}{flag}")
        if rt == 'TRANSACTION':
            txn_count = t['c']
            txn_vol = vol

    if txn_count == 1202:
        print(f"\n  ✅ TRANSACTION count: {txn_count} — MATCH")
    else:
        print(f"\n  ⚠️  TRANSACTION count: {txn_count} — Expected 1,202")
        ok = False

    if abs(txn_vol - 430479.32) < 1.0:
        print(f"  ✅ TRANSACTION volume: ${txn_vol:,.2f} — MATCH")
    else:
        print(f"  ⚠️  TRANSACTION volume: ${txn_vol:,.2f} — Expected $430,479.32")
        ok = False

    # ── CHECK 4: Per-bank verified counts ──
    print("\n  Per-bank verified transactions:")
    expected_banks = {
        'Deutsche Bank': 808, 'UBS': 236, 'Navy Federal': 98,
        'Citibank': 45, 'BNY Mellon': 7, 'Barclays': 5,
        'Credit Suisse': 2, 'Bear Stearns': 1
    }
    banks = conn.execute("""
        SELECT bank, COUNT(*) c, SUM(tx_amount) vol
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        GROUP BY bank ORDER BY vol DESC
    """).fetchall()
    
    for b in banks:
        exp = expected_banks.get(b['bank'], '?')
        match = "✅" if b['c'] == exp else "⚠️"
        print(f"    {match} {b['bank']:20s} {b['c']:>5} records  ${b['vol']:>12,.2f}  (expected {exp})")

    # ── CHECK 5: Key verified transactions ──
    print("\n  Key verified transactions:")
    key_txns = [
        ("Larry Visoski $225K", "Visoski", 225000),
        ("Larry Visoski $16.7K", "Visoski", 16676),
        ("Designs LLC $20K", "Designs", 20000),
        ("South Street Capital", "South Street", 12142.86),
    ]
    for label, search, expected_amt in key_txns:
        hit = conn.execute("""
            SELECT tx_amount, description, bank FROM bank_statement_transactions
            WHERE record_type = 'TRANSACTION' 
            AND description LIKE ? AND ABS(tx_amount - ?) < 1
        """, (f"%{search}%", expected_amt)).fetchone()
        if hit:
            print(f"    ✅ {label}: ${hit['tx_amount']:,.2f} at {hit['bank']}")
        else:
            print(f"    ⚠️  {label}: NOT FOUND (${expected_amt:,.2f})")
            ok = False

    # ── CHECK 6: Entity matches ──
    print("\n  Entity matches in verified records:")
    entities = conn.execute("""
        SELECT entity_match, COUNT(*) c, SUM(tx_amount) vol
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION' AND entity_match IS NOT NULL AND entity_match != ''
        GROUP BY entity_match ORDER BY vol DESC
    """).fetchall()
    for e in entities:
        print(f"    {e['entity_match']:25s} {e['c']:>3} txns  ${e['vol']:>10,.2f}")

    # ── CHECK 7: extracted_payments (Phase 5I) still intact ──
    print("\n  Phase 5I extracted_payments:")
    ep = conn.execute("SELECT COUNT(*) c, SUM(amount) vol FROM extracted_payments").fetchone()
    print(f"    Records: {ep['c']:,}  Volume: ${ep['vol']:,.2f}")
    if ep['c'] == 10118:
        print("    ✅ 10,118 records — MATCH")
    else:
        print(f"    ⚠️  Expected 10,118 — GOT {ep['c']:,}")
        ok = False

    # ── CHECK 8: wire_ledger still intact ──
    wl = conn.execute("SELECT COUNT(*) c FROM wire_ledger").fetchone()
    print(f"\n  wire_ledger: {wl['c']} records")

    # ── CHECK 9: Column inventory ──
    print("\n  bank_statement_transactions columns:")
    cols = conn.execute("PRAGMA table_info(bank_statement_transactions)").fetchall()
    for c in cols:
        print(f"    {c['name']:25s} {c['type']}")

    # ── CHECK 10: Full DB table inventory ──
    print("\n  Full DB table inventory:")
    tables = conn.execute("""
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
    """).fetchall()
    print(f"    {len(tables)} tables total")
    for t in tables:
        cnt = conn.execute(f'SELECT COUNT(*) c FROM "{t["name"]}"').fetchone()['c']
        print(f"    {t['name']:40s} {cnt:>10,} rows")

    conn.close()

    print("\n" + "=" * 70)
    if ok:
        print("  ✅ ALL CHECKS PASSED — Phase 5J data verified")
    else:
        print("  ⚠️  SOME CHECKS FAILED — review above")
    print("=" * 70)
    return ok

if __name__ == '__main__':
    main()
