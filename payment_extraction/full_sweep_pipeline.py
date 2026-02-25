"""
full_sweep_pipeline.py — Master orchestrator for payment extraction.

v2: Built around the JPM Transaction Detail parser (7,653 pages) as the
primary extractor, with MT103 (37 pages) as a secondary pass.
Replaces the six broken single-type extractors.

Usage:
    python full_sweep_pipeline.py                    # full run, dry mode
    python full_sweep_pipeline.py --live             # insert into DB
    python full_sweep_pipeline.py --limit 500        # cap pages (testing)

Epstein Forensic Finance Project
Analyst: Randall Scott Taylor
"""

import sys
import os
import json
from datetime import datetime
from collections import defaultdict

from extraction_framework import (
    get_db, init_tables, link_transactions, insert_payments,
    TARGET_ENTITIES, CANONICAL_ENTITIES
)
from jpm_statement_parser import run_jpm_parser
from mt103_extractor import run_mt103_extractor


def run_pipeline(live=False, limit=None, verbose=True):
    start_time = datetime.now()
    print("=" * 70)
    print("EPSTEIN FORENSIC FINANCE — PAYMENT EXTRACTION PIPELINE v2")
    print(f"Run started: {start_time.isoformat()}")
    print(f"Mode: {'LIVE — will write to DB' if live else 'DRY RUN'}")
    if limit:
        print(f"Page limit: {limit}")
    print("=" * 70)

    conn = get_db()
    db_path = conn.execute("PRAGMA database_list").fetchone()[2]

    if live:
        init_tables(conn)

    # ── Phase 1: JPM Transaction Detail pages (primary) ─────────────

    print("\n" + "─" * 50)
    print("PHASE 1: JPM TRANSACTION DETAIL (7,653 pages)")
    print("─" * 50)
    jpm_records = run_jpm_parser(db_path=db_path, limit=limit, verbose=verbose)

    # ── Phase 2: MT103 SWIFT messages (secondary) ───────────────────

    print("\n" + "─" * 50)
    print("PHASE 2: SWIFT MT103 (37 pages)")
    print("─" * 50)
    mt103_records = run_mt103_extractor(db_path=db_path, verbose=verbose)

    # ── Combine ─────────────────────────────────────────────────────

    all_records = jpm_records + mt103_records

    print("\n" + "─" * 50)
    print(f"COMBINED: {len(all_records)} records")
    print("─" * 50)

    # ── Phase 3: Transaction Linking ────────────────────────────────

    print("\n" + "─" * 50)
    print("PHASE 3: TRANSACTION LINKING")
    print("─" * 50)
    all_records = link_transactions(all_records)
    linked = sum(1 for r in all_records if r.get("linked_to"))
    rev_pairs = sum(1 for r in all_records if r.get("link_type") == "reversal_pair")
    cross = sum(1 for r in all_records if r.get("link_type") == "cross_type_match")
    adj = sum(1 for r in all_records if r.get("link_type") == "adjacent_day_match")
    print(f"  Linked records: {linked}")
    print(f"  Reversal pairs: {rev_pairs}")
    print(f"  Cross-type matches: {cross}")
    print(f"  Adjacent-day matches: {adj}")

    # ── Phase 4: DB Insertion ───────────────────────────────────────

    if live:
        print("\n" + "─" * 50)
        print("PHASE 4: DB INSERTION")
        print("─" * 50)
        inserted = insert_payments(conn, all_records)
    else:
        print("\n" + "─" * 50)
        print("PHASE 4: DB INSERTION (SKIPPED — DRY RUN)")
        print("─" * 50)
        print(f"  Would insert {len(all_records)} records")
        print(f"  Use --live flag to write to DB")

    # ── Final Report ────────────────────────────────────────────────

    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()

    # type breakdown
    type_counts = defaultdict(lambda: {"count": 0, "volume": 0.0})
    for r in all_records:
        pt = r.get("payment_type", "UNKNOWN")
        type_counts[pt]["count"] += 1
        type_counts[pt]["volume"] += r.get("amount") or 0

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)

    print(f"\n  {'Type':<22} {'Count':>8} {'Volume':>18}")
    print(f"  {'─'*22} {'─'*8} {'─'*18}")
    grand_count, grand_vol = 0, 0.0
    for pt in sorted(type_counts.keys()):
        c, v = type_counts[pt]["count"], type_counts[pt]["volume"]
        print(f"  {pt:<22} {c:>8,} ${v:>15,.2f}")
        grand_count += c
        grand_vol += v
    print(f"  {'─'*22} {'─'*8} {'─'*18}")
    print(f"  {'TOTAL':<22} {grand_count:>8,} ${grand_vol:>15,.2f}")

    # entities
    entity_data = defaultdict(lambda: {"count": 0, "volume": 0.0, "types": set()})
    new_entities = defaultdict(lambda: {"count": 0, "volume": 0.0})
    for r in all_records:
        ben = r.get("beneficiary_canonical") or r.get("beneficiary_raw")
        if not ben:
            continue
        amt = r.get("amount") or 0
        pt = r.get("payment_type", "")
        conf = r.get("entity_confidence", 0)

        if ben in TARGET_ENTITIES or ben in CANONICAL_ENTITIES:
            entity_data[ben]["count"] += 1
            entity_data[ben]["volume"] += amt
            entity_data[ben]["types"].add(pt)
        elif conf == 0:
            new_entities[ben]["count"] += 1
            new_entities[ben]["volume"] += amt

    if entity_data:
        print(f"\n  Known Entities:")
        for name in sorted(entity_data, key=lambda x: -entity_data[x]["volume"]):
            d = entity_data[name]
            types = ", ".join(sorted(d["types"]))
            print(f"    {name}: {d['count']} txns, ${d['volume']:,.2f} ({types})")

    if new_entities:
        top = sorted(new_entities.items(), key=lambda x: -x[1]["volume"])[:25]
        print(f"\n  Top 25 New Entities (of {len(new_entities)} total):")
        for name, d in top:
            print(f"    {name}: {d['count']} txns, ${d['volume']:,.2f}")

    # reversals
    reversals = [r for r in all_records if r.get("is_reversal")]
    print(f"\n  Reversals: {len(reversals)}")

    # data quality
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

    print(f"\n  Elapsed: {elapsed:.1f} seconds")
    print(f"  Mode: {'LIVE — records inserted' if live else 'DRY RUN'}")

    # save summary
    summary = {
        "run_time": start_time.isoformat(),
        "elapsed_seconds": elapsed,
        "live": live,
        "total_records": len(all_records),
        "total_volume": grand_vol,
        "type_breakdown": {k: v for k, v in type_counts.items()},
        "known_entities": {k: {"count": v["count"], "volume": v["volume"]}
                          for k, v in entity_data.items()},
        "new_entities_count": len(new_entities),
        "linked_records": linked,
        "reversals": len(reversals),
        "data_quality": {
            "with_amount": with_amount,
            "with_balance": with_balance,
            "with_beneficiary": with_ben,
            "with_date": with_date,
        },
    }

    summary_path = os.path.expanduser("~/Desktop/epstein-forensic-finance/pipeline_summary.json")
    try:
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2, default=str)
        print(f"  Summary: {summary_path}")
    except Exception as e:
        print(f"  (Could not save summary: {e})")

    print(f"\n  For the girls.\n")

    conn.close()
    return summary


if __name__ == "__main__":
    args = sys.argv[1:]
    live = "--live" in args
    limit = None
    for i, a in enumerate(args):
        if a == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])

    run_pipeline(live=live, limit=limit)
