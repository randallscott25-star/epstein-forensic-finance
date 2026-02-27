# Narrative QA Report — N1 through N18
## February 27, 2026

---

## SUMMARY

18 narrative MD files reviewed for internal consistency, cross-narrative accuracy, and factual alignment. **3 discrepancies flagged**, **2 minor notes**, **0 critical errors** in core findings.

All key anchor numbers are consistent across the corpus:
- ✅ 481 wires / $973M master ledger total
- ✅ 1,476,377 files (1.48M) corpus size
- ✅ 11.4M extracted entities
- ✅ Bear Stearns 5.7× Deutsche Bank by money-mention volume
- ✅ Deutsche Bank $150M DFS fine (2020)
- ✅ JPMorgan $290M settlement (2023)
- ✅ Jeepers: $57,876,640 across 24 wires
- ✅ Gratitude America: 88% investment / 7% charity
- ✅ Flight correlation: 4.3× (4.29× exact) above random
- ✅ Round numbers: 84.3%
- ✅ Southern Trust Exhibit A: $151,499,980 across 17 wires
- ✅ Southern Trust total (all channels): $244M

---

## FLAGGED DISCREPANCIES

### 🔴 N3 — Leon Black → Southern Trust: Header vs. Table Mismatch

**Location:** N3 "The Plan D Question", paragraph 2

**Header claim:** "Leon & Debra Black and Black Family Partners LP sent **$131,500,000** (Unverified) into Southern Trust Company Inc. — the network's central hub — across **12 wire transfers** on Exhibit A."

**Table shows:** 14 entries totaling **$106,500,000**

**Body total:** "$106,500,000 (Unverified)"

**Discrepancy:** The $131.5M header figure does not match the $106.5M table sum. The "12 wire transfers" claim does not match the 14-row table. The body total confirms $106.5M.

**Recommendation:** Reconcile the header. Either:
- (a) The header should read $106.5M across 14 transfers, matching the table, OR
- (b) The table is missing entries that bring the total to $131.5M, in which case add them

**Note:** N14 cites "$168 million" per court exhibits (from Dechert/other researchers) and "$60.5 million independently verified," which is a different scope. N4 uses $106.5M for the Exhibit A subset, consistent with N3's table.

---

### 🟡 N8/N9 — Indyke Wire Total: $7.6M vs. $5.8M + $1.2M

**Location:** N8 "Infrastructure of Access" and N9 "734,122 Names"

**N8 claim:** "He appears on 5 verified wire transfers in the master ledger totaling **$7.6 million**."

**N5 detail:** Indyke: 5 wires, **$5,798,525**

**N8 breakdown:** "$5.8 million from Deutsche Bank (5 wires, Exhibit C)" + "Co-signed $1.2 million in transfers with Michelle Saipher"

**Math:** $5.8M + $1.2M = **$7.0M**, not $7.6M

**Discrepancy:** The $7.6M figure appears to be ~$600K too high based on the component breakdown. Either the co-signed transfers total more than $1.2M, or the $7.6M figure includes additional transfers not itemized.

**Recommendation:** Verify the Indyke wire total from the master ledger. If $7.0M is correct, update to $7.0M. If $7.6M includes additional non-itemized wires, add the detail.

---

### 🟡 N5 — Deutsche Bank Wire Counts: Multiple Scope Figures

**Location:** N5 "Deutsche Bank's Role"

**Not a true discrepancy** but worth noting for reader clarity:
- Header: "38 wires. $56.8 million." (expansion wires where DB was counterparty)
- Body: "Total outflows: $54,792,936 across **37 wires**" + 1 inflow = 38 total ✅
- Source appendix: "**74 wires verified** involving Deutsche Bank accounts" (includes Exhibit C/D/E + expansion)
- Exhibit breakdown: C=24, D=9, E=4, Expansion=37 → Total 74 ✅

**Status:** Consistent but uses multiple scope definitions. Reader may initially confuse 38 vs 74. Consider adding a clarifying note that 38 = expansion wires, 74 = all exhibits + expansion.

---

## MINOR NOTES

### N6 — Gratitude America Outflow Arithmetic

Total wires = $13,080,518. Investment ($11,750,000) + Charitable ($453,493) = $12,203,493. Delta = $877,025 — which is exactly the Deutsche Bank inflow total. The text explains the gap as "inflows from Deutsche Bank: $877,025." This is correctly handled but the categorization table omits the $877K from the "Other/unclassified" row percentage. Not a factual error — just a presentation note.

### N10 — 185 vs 481 Wire Count

N10 tests "185 verified wire transfers" against Benford's Law. This is the **dated** subset of the 481 master ledger. The scope is clearly stated ("from the Deutsche Bank-SDNY production, Exhibits A–E"). Not a discrepancy — just a subset. But the source appendix then says "481 wire transfer amounts tested" which contradicts the body text. Should be 185.

**Recommendation:** Source appendix line "Exhibits A–E: 481 wire transfer amounts tested against Benford's Law" should read "185" to match the body.

---

## CROSS-NARRATIVE CONSISTENCY MATRIX

| Fact | N1 | N3 | N4 | N5 | N8 | N9 | N10 | N11 | N12 | N14 |
|------|----|----|----|----|----|----|-----|-----|-----|-----|
| Master ledger: 481 wires | — | — | ✅ | — | — | — | ✅* | ✅ | ✅ | — |
| Corpus: 1,476,377 files | — | — | — | — | ✅ | ✅ | — | ✅ | — | ✅ |
| Entities: 11.4M | — | — | — | — | ✅ | ✅ | — | ✅ | — | — |
| S. Trust Exhibit A: $151.5M | — | — | ✅ | — | ✅ | ✅ | — | — | — | — |
| Bear Stearns 5.7× | — | — | — | — | — | — | — | ✅ | ✅ | — |
| DB Fine: $150M (2020) | — | — | — | ✅ | — | — | — | ✅ | ✅ | — |
| Jeepers: $57.9M / 24 wires | ✅ | — | — | — | — | — | — | — | — | — |
| Black → S. Trust: $106.5M | — | ✅ | ✅ | — | — | — | — | — | — | ✅ |

*N10 source appendix says 481 but body says 185 (subset) — see Minor Note above.

---

## HTML CONVERSION NOTES

All 18 narratives converted to N19/N20 visual format:
- Navy/gold/ice color scheme
- Cormorant Garamond + IBM Plex Sans + IBM Plex Mono typography
- Stats bars with key metrics per narrative
- Section breaks with Roman numerals
- Styled data tables (gold monospace for money, ice for Bates stamps)
- Source Documents appendix with workbook links
- Footer with disclaimer and "For the girls" dedication
- All DOJ EFTA links preserved as clickable anchors
- Google Sheets workbook links preserved
- Mobile-responsive layout

Files delivered: `/mnt/user-data/outputs/narratives_html/01-18_*.html`
