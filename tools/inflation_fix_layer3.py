#!/usr/bin/env python3
"""
INFLATION FIX — LAYER 3
Targets remaining $4.1B inflation, concentrated in Deutsche Bank ($3.09B).

Root cause: DB Private Wealth Management statement pages have portfolio
totals, allocation breakdowns, income projections, and sub-account values.
Every dollar figure on the page got extracted as a "transaction."

Fixes:
1. Wealth management summary language detection
2. Per-bank statistical outlier removal (IQR-based)
3. Cover page / header detection
4. Repeated-value-across-bates detection (portfolio printed on multiple statements)

Author: Randall Scott Taylor
"""

import sqlite3, re, os, math
from collections import Counter, defaultdict

DB_PATH = os.path.expanduser("~/Desktop/epstein_files.db")


# ── Wealth management / portfolio summary patterns ──
# These appear on DB PWM statement pages alongside dollar amounts
# but are NOT individual transactions
WM_SUMMARY_PATTERNS = [
    # Allocation language
    (r'(?i)review\s+your\s+allocation\s+periodically', 'ALLOCATION_REVIEW'),
    (r'(?i)asset\s+(allocation|summary|mix)', 'ASSET_ALLOCATION'),
    (r'(?i)(equity|fixed\s+income|alternative|cash)\s+allocation', 'ALLOCATION_LINE'),
    (r'(?i)investment\s+(objective|strategy|profile)', 'INVESTMENT_PROFILE'),

    # Income / yield estimates
    (r'(?i)estimated\s+annual\s+income', 'ANNUAL_INCOME'),
    (r'(?i)(projected|estimated|expected)\s+(income|yield|return)', 'PROJECTED_INCOME'),
    (r'(?i)your\s+investm[ea]nt\s+return', 'INVESTMENT_RETURN'),
    (r'(?i)dividend\s+(yield|rate|income)\s*:', 'DIVIDEND_YIELD'),

    # Net cash flow summaries (not individual transactions)
    (r'(?i)net\s+cash\s+deposits\s+a[ni]d\s+withdrawals', 'NET_CASH_SUMMARY'),
    (r'(?i)net\s+(change|movement|flow|activity)', 'NET_CHANGE'),
    (r'(?i)(total|net)\s+(deposits|withdrawals|disbursements)\s+for', 'PERIOD_TOTAL'),

    # Relationship manager / cover page
    (r'(?i)(MARTIN\s+ZEM[AE]N|JOSHUA\s+SHOSHAN)', 'RM_NAME'),
    (r'(?i)relationship\s+manager', 'RM_HEADER'),
    (r'(?i)private\s+(wealth|banking)\s+(management|advisor|client)', 'PWM_HEADER'),
    (r'(?i)wealth\s+management\s+(group|division|services)', 'WM_HEADER'),

    # Protective order / legal cover
    (r'(?i)CONFIDENTIAL.*PURSUANT\s+TO', 'PROTECTIVE_ORDER'),
    (r'(?i)FED\.?\s+R\.?\s+CRIM', 'CRIM_RULE'),
    (r'(?i)UNDER\s+SEAL', 'UNDER_SEAL'),

    # Portfolio/account value lines
    (r'(?i)total\s+(portfolio|account|relationship)\s+value', 'PORTFOLIO_VALUE'),
    (r'(?i)(portfolio|account)\s+(summary|overview|snapshot)', 'PORTFOLIO_SUMMARY'),
    (r'(?i)asset\s+summary\s+disclosure', 'ASSET_SUMMARY'),
    (r'(?i)see\s+the\s+asset\s+summary', 'ASSET_SUMMARY_REF'),
    (r'(?i)total\s+managed\s+assets', 'MANAGED_ASSETS'),
    (r'(?i)total\s+relationship', 'TOTAL_RELATIONSHIP'),
    (r'(?i)accrued\s+(interest|income|literal)', 'ACCRUED'),

    # Sub-account breakdowns
    (r'(?i)(checking|savings|money\s+market|investment|custody)\s+account\s+value', 'SUBACCOUNT_VALUE'),
    (r'(?i)original\s+cost\s+bas[ise]', 'COST_BASIS'),
    (r'(?i)unrealized\s+(gain|loss)', 'UNREALIZED_GL'),
    (r'(?i)current\s+market\s+value', 'CURRENT_MV'),

    # Brokerage-specific (Bear Stearns, Morgan Stanley)
    (r'(?i)(total|net)\s+liquidat(ion|ing)\s+value', 'LIQUIDATION_VALUE'),
    (r'(?i)total\s+securities\s+value', 'SECURITIES_VALUE'),
    (r'(?i)margin\s+(balance|debit|equity)', 'MARGIN_LINE'),
]

# OCR artifacts that indicate garbled numbers, not real amounts
OCR_GARBAGE_PATTERNS = [
    r'^\d{3,}\s+\d{3,}$',           # Two big numbers jammed together
    r'(?i)^[\d,\.\s\$]+$',          # Line is ONLY numbers (no context)
    r'(?i)RED\s+HOOK\s+QUARTER',    # Address fragment near numbers
    r'(?i)CON\s*FID\s*[OE]N',       # "CONFIDENTIAL" garbled by OCR
    r'\d{4,}\s+[A-Z]{2,4}\s+\d',    # Random alphanumeric sequences
]


def detect_wm_summary(description):
    """Check if description matches wealth management summary patterns."""
    if not description:
        return None
    for pat, label in WM_SUMMARY_PATTERNS:
        if re.search(pat, description):
            return label
    return None


def detect_ocr_garbage(description):
    """Check if description is OCR garbage (numbers without context)."""
    if not description:
        return True  # No description = no context = suspicious
    for pat in OCR_GARBAGE_PATTERNS:
        if re.search(pat, description.strip()):
            return True
    return False


def compute_iqr_cap(amounts):
    """Compute IQR-based outlier threshold.
    Returns the value above which records are statistical outliers.
    Uses 3x IQR above Q3 (generous — standard is 1.5x)."""
    if len(amounts) < 10:
        return max(amounts) if amounts else 0

    sorted_a = sorted(amounts)
    n = len(sorted_a)
    q1 = sorted_a[n // 4]
    q3 = sorted_a[3 * n // 4]
    iqr = q3 - q1

    # Use 3x IQR for generous threshold (keeps more legitimate large txns)
    threshold = q3 + 3 * iqr

    # But never below a reasonable floor per bank
    return max(threshold, 10000)  # At least $10K


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("=" * 70)
    print("INFLATION FIX — LAYER 3: WEALTH MANAGEMENT & STATISTICAL OUTLIERS")
    print("=" * 70)

    # Get current TRANSACTION records
    c.execute("""
        SELECT id, bank, bates, tx_amount, tx_date, description,
               source_doc_type
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        ORDER BY bank, tx_amount DESC
    """)
    txn_rows = c.fetchall()
    print(f"[IN] TRANSACTION records: {len(txn_rows):,}")
    print(f"[IN] Volume: ${sum(r[3] or 0 for r in txn_rows):,.2f}")

    fixes = Counter()
    fix_vol = Counter()
    fix_details = defaultdict(list)

    # ── FIX 1: Wealth management summary detection ──
    print(f"\n[FIX 1] Scanning for wealth management summary language...")

    wm_labels = Counter()
    for rec_id, bank, bates, amount, date, desc, stype in txn_rows:
        label = detect_wm_summary(desc)
        if label:
            c.execute("UPDATE bank_statement_transactions SET record_type = 'WM_SUMMARY' WHERE id = ?",
                     (rec_id,))
            fixes['WM_SUMMARY'] += 1
            fix_vol['WM_SUMMARY'] += (amount or 0)
            wm_labels[label] += 1

    print(f"  Demoted {fixes['WM_SUMMARY']:,} records (${fix_vol['WM_SUMMARY']:,.2f})")
    print(f"  Labels found:")
    for label, cnt in wm_labels.most_common(15):
        print(f"    {label:<30} {cnt:>6}")

    # ── FIX 2: OCR garbage / no-context amounts ──
    print(f"\n[FIX 2] Detecting OCR garbage and context-free amounts...")

    # Re-fetch remaining TRANSACTION records
    c.execute("""
        SELECT id, bank, bates, tx_amount, description
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        AND tx_amount > 1000000
    """)
    for rec_id, bank, bates, amount, desc in c.fetchall():
        if detect_ocr_garbage(desc):
            # Only demote if amount is large (small amounts could be legit even without context)
            c.execute("UPDATE bank_statement_transactions SET record_type = 'OCR_NOISE' WHERE id = ?",
                     (rec_id,))
            fixes['OCR_NOISE'] += 1
            fix_vol['OCR_NOISE'] += (amount or 0)

    print(f"  Demoted {fixes['OCR_NOISE']:,} records (${fix_vol['OCR_NOISE']:,.2f})")

    # ── FIX 3: Per-bank IQR-based statistical outlier removal ──
    print(f"\n[FIX 3] Statistical outlier detection (IQR method)...")

    # Re-fetch remaining TRANSACTION records grouped by bank
    c.execute("""
        SELECT id, bank, tx_amount
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        AND tx_amount IS NOT NULL
    """)
    bank_records = defaultdict(list)
    for rec_id, bank, amount in c.fetchall():
        bank_records[bank].append((rec_id, amount))

    for bank, records in bank_records.items():
        amounts = [r[1] for r in records if r[1] > 0]
        if len(amounts) < 20:
            continue  # Not enough data for statistical analysis

        threshold = compute_iqr_cap(amounts)

        outlier_count = 0
        outlier_vol = 0
        for rec_id, amount in records:
            if amount > threshold:
                c.execute("""
                    UPDATE bank_statement_transactions 
                    SET record_type = 'STAT_OUTLIER' 
                    WHERE id = ?
                """, (rec_id,))
                outlier_count += 1
                outlier_vol += amount

        if outlier_count > 0:
            median = sorted(amounts)[len(amounts)//2]
            print(f"  {bank:<22} median=${median:>12,.2f}  threshold=${threshold:>12,.2f}  "
                  f"outliers={outlier_count:>4}  vol=${outlier_vol:>14,.2f}")
            fixes[f'STAT_OUTLIER:{bank}'] = outlier_count
            fix_vol[f'STAT_OUTLIER:{bank}'] = outlier_vol

    # ── FIX 4: Cross-bates value dedup (same amount on diff pages of same statement) ──
    print(f"\n[FIX 4] Cross-bates value dedup (same bank+amount, different pages)...")

    c.execute("""
        SELECT id, bank, bates, tx_amount, tx_date
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        AND tx_amount > 10000
        ORDER BY bank, tx_amount DESC, id
    """)
    remaining = c.fetchall()

    # Group by bank + rounded amount (within 1% tolerance for OCR variation)
    amount_groups = defaultdict(list)
    for rec_id, bank, bates, amount, date in remaining:
        if not amount:
            continue
        # Round to nearest $100 for grouping (catches OCR-variant copies)
        rounded = round(amount / 100) * 100
        key = f"{bank}|{rounded}"
        amount_groups[key].append((rec_id, bates, amount, date))

    cross_dedup = 0
    cross_vol = 0
    for key, recs in amount_groups.items():
        if len(recs) <= 1:
            continue
        # If same amount appears on 3+ different bates pages, it's a running balance
        unique_bates = set(r[1] for r in recs)
        if len(unique_bates) >= 3:
            # Keep one, demote the rest
            for rec_id, bates, amount, date in recs[1:]:
                c.execute("""
                    UPDATE bank_statement_transactions 
                    SET record_type = 'BALANCE_REPEAT' 
                    WHERE id = ?
                """, (rec_id,))
                cross_dedup += 1
                cross_vol += amount

    print(f"  Demoted {cross_dedup:,} records (${cross_vol:,.2f}) as BALANCE_REPEAT")
    fixes['BALANCE_REPEAT'] = cross_dedup
    fix_vol['BALANCE_REPEAT'] = cross_vol

    conn.commit()

    # ═══════════════════════════════════════════════════════
    # FINAL RESULTS
    # ═══════════════════════════════════════════════════════

    print(f"\n{'=' * 70}")
    print("FINAL RESULTS AFTER LAYER 3")
    print(f"{'=' * 70}")

    c.execute("""
        SELECT record_type, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        GROUP BY record_type
        ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Record Type':<25} {'Records':>8} {'Volume':>20}")
    print("  " + "─" * 55)
    final_txn_vol = 0
    final_txn_count = 0
    for rtype, cnt, vol in c.fetchall():
        vol = vol or 0
        marker = " ← REAL" if rtype == 'TRANSACTION' else ""
        print(f"  {rtype:<25} {cnt:>8,} ${vol:>18,.2f}{marker}")
        if rtype == 'TRANSACTION':
            final_txn_vol = vol
            final_txn_count = cnt

    # Per-bank final
    print(f"\n{'=' * 70}")
    print("TRANSACTION RECORDS BY BANK (final)")
    print(f"{'=' * 70}")
    c.execute("""
        SELECT bank, COUNT(*), SUM(tx_amount),
               MIN(tx_amount), MAX(tx_amount), AVG(tx_amount)
        FROM bank_statement_transactions
        WHERE record_type = 'TRANSACTION'
        GROUP BY bank
        ORDER BY SUM(tx_amount) DESC
    """)
    print(f"\n  {'Bank':<22} {'Recs':>6} {'Volume':>16} {'Max':>14} {'Median~Avg':>14}")
    print("  " + "─" * 76)
    grand = 0
    for bank, cnt, vol, mn, mx, avg in c.fetchall():
        vol = vol or 0
        grand += vol
        print(f"  {bank:<22} {cnt:>6,} ${vol:>14,.2f} ${mx or 0:>12,.2f} ${avg or 0:>12,.2f}")
    print("  " + "─" * 76)
    print(f"  {'TOTAL':<22} {final_txn_count:>6,} ${grand:>14,.2f}")

    # Entity matches
    print(f"\n{'=' * 70}")
    print("ENTITY MATCHES (clean TRANSACTION)")
    print(f"{'=' * 70}")
    c.execute("""
        SELECT entity_match, COUNT(*), SUM(tx_amount)
        FROM bank_statement_transactions
        WHERE entity_match IS NOT NULL AND record_type = 'TRANSACTION'
        GROUP BY entity_match
        ORDER BY SUM(tx_amount) DESC
        LIMIT 20
    """)
    for entity, cnt, vol in c.fetchall():
        print(f"  {entity:<30} {cnt:>6} txns  ${vol or 0:>14,.2f}")

    # Progression
    print(f"\n{'=' * 70}")
    print("FULL INFLATION FIX PROGRESSION")
    print(f"{'=' * 70}")
    print(f"  Layer 0 (raw parser):          $68,745,222,404.77  (24,563 records)")
    print(f"  Layer 1 (record classifier):   $23,695,632,641.86  (10,513 records)")
    print(f"  Layer 2 (source doc type):     $14,612,679,834.57  ( 8,123 records)")
    print(f"  Layer 3 (outlier+dedup caps):  $ 4,113,970,148.71  ( 7,374 records)")
    print(f"  Layer 4 (WM+stats+IQR):       ${final_txn_vol:>18,.2f}  ({final_txn_count:,} records)")
    if final_txn_vol > 0:
        reduction = (1 - final_txn_vol / 68_745_222_404.77) * 100
        print(f"  Total inflation removed:       {reduction:.1f}%")
        # Compare to plausible range
        print(f"\n  Plausible range check:")
        print(f"    If real activity was ~$300M:  {'CLOSE' if 100_000_000 < final_txn_vol < 1_000_000_000 else 'STILL OFF'}")
        print(f"    If real activity was ~$500M:  {'CLOSE' if 200_000_000 < final_txn_vol < 1_500_000_000 else 'STILL OFF'}")

    conn.close()
    print(f"\n  Layer 3 complete.")


if __name__ == "__main__":
    main()
