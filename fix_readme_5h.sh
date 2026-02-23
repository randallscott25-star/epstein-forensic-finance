#!/bin/bash
# ══════════════════════════════════════════════════════════════
# fix_readme_5h.sh — Catch all remaining stale numbers
# Run from repo root: bash fix_readme_5h.sh
# ══════════════════════════════════════════════════════════════
set -e
cd ~/Desktop/epstein-forensic-finance

echo "Fixing README.md..."

# Wire count 382 → 420 (all occurrences)
sed -i '' 's/\*\*382\*\* (Phase 24 audited)/**420** (Phase 5H audited)/g' README.md
sed -i '' 's/382-wire master ledger/420-wire master ledger/g' README.md
sed -i '' 's/382 Phase 24-audited/420 Phase 5H-audited/g' README.md
sed -i '' 's/| 382 |/| 420 |/g' README.md
sed -i '' 's/382 wires/420 wires/g' README.md
sed -i '' 's/(382 wires)/(420 wires)/g' README.md

# Shell-to-shell 43 → 45 (headline only - careful not to hit flow table)
sed -i '' 's/Shell-to-Shell Transfers Identified\*\* | 43/Shell-to-Shell Transfers Identified** | 45/g' README.md

# Table count 28+ → 35
sed -i '' 's/\*\*28+\*\*/\*\*35\*\*/g' README.md
sed -i '' 's/28+ tables/35 tables/g' README.md
sed -i '' 's/(28+ Tables)/(35 Tables)/g' README.md

# financial_hits
sed -i '' 's/35,375 raw/81,451 raw/g' README.md

# Workbook v6 → v7
sed -i '' 's/Workbook v6\.1 (11 Tabs)/Workbook v7 (14 Tabs)/g' README.md
sed -i '' 's/EPSTEIN_FORENSIC_WORKBOOK_v6\.xlsx/EPSTEIN_FORENSIC_WORKBOOK_v7.xlsx/g' README.md
sed -i '' 's/forensic_workbook_v6\.py/forensic_workbook_v7.py/g' README.md
sed -i '' 's/11-tab forensic workbook/14-tab forensic workbook/g' README.md

# Entity count 158 → 202
sed -i '' 's/158 entities/202 entities/g' README.md

# Shell counts in tab 9
sed -i '' 's/221 shell-involved, 43 shell-to-shell/247 shell-involved, 45 shell-to-shell/g' README.md
sed -i '' 's/221 shell-involved/247 shell-involved/g' README.md

# Data file reference
sed -i '' 's/master_wire_ledger_phase24\.json/master_wire_ledger_phase5h.json/g' README.md

# Tab 5 description
sed -i '' 's/382 wires with flow direction/420 wires with flow direction/g' README.md

# Money Flow Direction table - replace the 6-row old table
# Use Python for this multi-line replacement
python3 << 'PYEOF'
import re

with open("README.md", "r") as f:
    text = f.read()

old_table = """| **MONEY IN** — External → Epstein entities | 91 | $232,538,043 | 41.7% |
| **INTERNAL MOVE** — Shell → Shell reshuffling | 39 | $112,610,112 | 20.2% |
| **PASS-THROUGH** — Attorney/trust administration | 130 | $72,433,003 | 13.0% |
| **MONEY OUT** — Epstein entities → External | 51 | $63,266,349 | 11.3% |
| **BANK → SHELL** — Custodian disbursements | 27 | $53,717,045 | 9.6% |
| Other (Shell→Bank, Interbank, External→Bank) | 44 | $23,504,429 | 4.2% |"""

new_table = """| **MONEY IN** — External → Epstein entities | 102 | $238,376,891 | 36.9% |
| **INTERNAL MOVE** — Shell → Shell reshuffling | 43 | $189,608,168 | 29.3% |
| **PASS-THROUGH** — Attorney/trust administration | 141 | $73,965,062 | 11.4% |
| **MONEY OUT** — Epstein entities → External | 63 | $65,841,728 | 10.2% |
| **BANK → SHELL** — Custodian disbursements | 26 | $53,576,645 | 8.3% |
| **SHELL → BANK** — Returns to custodian | 10 | $14,726,112 | 2.3% |
| **BANK → EXTERNAL** — Direct bank payments | 22 | $8,690,228 | 1.3% |
| Other (External→Bank, Interbank) | 13 | $1,510,070 | 0.2% |"""

if old_table in text:
    text = text.replace(old_table, new_table)
    print("  ✅ Money flow table replaced")
else:
    print("  ⚠️  Money flow table not found (may already be updated)")

# Add tabs 12-14 if not present
if "Multi-Bank Wires" not in text:
    tab11_line = "| 11 | Methodology | 9 bugs documented, data sources, 10 limitations |"
    if tab11_line in text:
        text = text.replace(tab11_line, tab11_line + """
| 12 | **Multi-Bank Wires** ★ | 949 wires across verified + bank statement transactions |
| 13 | **Bank Statement Coverage** ★ | 14 banks × 25 years heat map (1999-2023) |
| 14 | **Multi-Bank Summary** ★ | Pipeline comparison, validation tiers, 2003-04 gap analysis |""")
        print("  ✅ Tabs 12-14 added")
    else:
        print("  ⚠️  Tab 11 line not found for insertion")
else:
    print("  ✅ Tabs 12-14 already present")

# Add Phase 5H to pipeline table if not present
if "Multi-bank statement promotion" not in text:
    phase24_line = "| 24 | Above-cap verified wires + bank custodian audit | +$121M / -$113M |"
    if phase24_line in text:
        text = text.replace(phase24_line, phase24_line + "\n| 5H | Multi-bank statement promotion (38 net-new entity-linked wires) | +$88M |")
        print("  ✅ Phase 5H pipeline row added")
else:
    print("  ✅ Phase 5H already in pipeline")

# Add Phase 5H to timeline if not present
if "Phase 5H" not in text:
    ongoing_line = "| Ongoing | Data narratives and follow-on analysis |"
    if ongoing_line in text:
        text = text.replace(ongoing_line, "| Feb 23, 2026 | Phase 5H: Multi-bank wire promotion (382→420), workbook v7 (14 tabs) |\n" + ongoing_line)
        print("  ✅ Timeline entry added")
else:
    print("  ✅ Phase 5H already in timeline")

# DB size 6.9GB → 8GB
text = text.replace("6.9GB forensic database", "8GB forensic database")

# Session count 70+ → 75+
text = text.replace("200+ hours across 70+ sessions", "200+ hours across 75+ sessions")

with open("README.md", "w") as f:
    f.write(text)
print("  ✅ README.md written")
PYEOF

# Also remove old data file if still tracked
git rm -f data/master_wire_ledger_phase24.json 2>/dev/null || true

# Verify
echo ""
echo "Checking for remaining '382' references..."
grep -n "382" README.md || echo "  ✅ No '382' references remain"
echo "Checking for remaining 'v6' references..."
grep -n "v6\." README.md || echo "  ✅ No 'v6' references remain"
echo "Checking for remaining '28+' references..."
grep -n "28+" README.md || echo "  ✅ No '28+' references remain"

echo ""
echo "Ready to push. Review with: git diff README.md"
echo "Then: git add . && git commit -m 'Fix remaining stale numbers: 382→420, v6→v7, 28+→35' && git push"
