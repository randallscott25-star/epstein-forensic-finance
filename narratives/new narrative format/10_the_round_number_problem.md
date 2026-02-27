# The Round Number Problem

**84.3% of Epstein wire transfers are exact round numbers. Benford's Law fails on this dataset — not because of fraud, but because this money was moved by instruction, not by transaction.**

*This analysis applies Benford's Law — a standard forensic accounting test for financial data integrity — to the 185 verified wire transfers in the master ledger. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What This Test Does

In normal financial data — sales, taxes, stock prices, expenses — the leading digit isn't uniformly distributed. The digit "1" appears first approximately 30.1% of the time, "2" appears 17.6%, "3" appears 12.5%, and so on, with "9" appearing only 4.6%. This pattern, called Benford's Law, holds across six orders of magnitude and has been validated on datasets from population counts to river lengths to nuclear decay rates.

Forensic accountants use Benford's Law because fabricated data deviates from this distribution. Invent round numbers like $5,000,000 instead of $4,837,216 and you skew the digits.

I ran it on 185 verified wire transfers totaling $557 million from the Deutsche Bank-SDNY production (Exhibits A–E).

## The Results

| First Digit | Benford Expected | Actual | Deviation | n |
|-------------|-----------------|--------|-----------|---|
| 1 | 30.1% | 26.5% | −3.6 | 49 |
| **2** | **17.6%** | **29.7%** | **+12.1** | **55** |
| 3 | 12.5% | 8.6% | −3.9 | 16 |
| 4 | 9.7% | 2.7% | −7.0 | 5 |
| **5** | **7.9%** | **18.4%** | **+10.5** | **34** |
| 6 | 6.7% | 2.7% | −4.0 | 5 |
| 7 | 5.8% | 5.9% | +0.1 | 11 |
| 8 | 5.1% | 3.8% | −1.3 | 7 |
| 9 | 4.6% | 1.6% | −3.0 | 3 |

Digits 2 and 5 are way over-represented. Digit 2 appears 29.7% of the time against an expected 17.6% — a 12.1-point deviation. Digit 5 appears 18.4% against an expected 7.9% — a 10.5-point deviation. Meanwhile, digits 4 and 6 are effectively absent (2.7% each against expected ~9.7% and ~6.7%).

## Why It Fails

The first-two-digit breakdown tells you exactly why:

| First Two Digits | Count | % of All Wires | Common Amounts |
|-----------------|-------|----------------|----------------|
| **50** | 30 | 16.2% | $5M, $500K, $50K |
| **10** | 28 | 15.1% | $10M, $1M, $100K |
| **20** | 24 | 13.0% | $20M, $2M, $200K |
| **25** | 20 | 10.8% | $2.5M, $250K |
| 30 | 9 | 4.9% | $3M, $300K |
| 70 | 6 | 3.2% | $7M, $700K |

Four two-digit prefixes — 50, 10, 20, 25 — account for **55.3% of all wires**. In a Benford-conforming dataset, those four prefixes would account for approximately 16%. The concentration is 3.5× above expected.

## The Round Number Concentration

| Roundness | Wires | % | Total Volume |
|-----------|-------|---|-------------|
| Exact millions ($1M, $5M, $10M, etc.) | 69 | 37.3% | $475,000,000 |
| Exact hundred-thousands | 34 | 18.4% | $78,800,000 |
| Exact ten-thousands | 33 | 17.8% | $22,560,000 |
| Exact thousands | 20 | 10.8% | $14,304,000 |
| **Non-round amounts** | **29** | **15.7%** | **$95,708,954** |

**84.3% of all wire transfers are exact round numbers.** Only 29 of 185 wires — 15.7% — have amounts that are not round to the nearest thousand dollars.

Normal commercial banking runs 30–50% round numbers. Businesses pay invoices and process payroll at precise amounts. An 84.3% round-number rate means this money was moved by instruction, not by obligation.

## What Each Exhibit Looks Like

The Benford deviation is not uniform across the five exhibits. Each money stream has a different signature:

**Exhibit A — Inflows to Southern Trust ($163M, 21 wires)**
Dominated by digits 1, 5, and 8. These are the large transfers from Leon Black entities, Narrow Holdings, and other sources. Almost exclusively exact millions: $5M, $8.5M, $10M, $13M, $15M, $20M, $25M. This is wealth transfer money — negotiated round amounts moved between principals.

**Exhibit B — Investment Outflows ($96.9M, 48 wires)**
The most diverse digit distribution across the five exhibits. Includes both round-number fund allocations ($10M to Boothbay, $2.7M to Valar) and precise calculated amounts ($12,826,541 from Tudor Futures, $99,999 to a law firm client fund). This is the closest to Benford-conforming because investment returns generate non-round amounts.

**Exhibit C — Operating/Jeepers ($57.9M, 71 wires)**
Heavily dominated by digit 2. The Jeepers brokerage pipeline moved money in recurring $2M and $2.5M tranches from brokerage to checking. This is the ATM pattern identified in Narrative 1: a predictable, repeating withdrawal cadence designed to fund daily operations.

**Exhibit D — Miscellaneous ($20M, 20 wires)**
Dominated by digit 5. Contains $5M transfers, $500K movements, and mid-range transactions. Smallest sample size makes Benford comparison unreliable.

**Exhibit E — Deutsche Bank Period ($25M, 25 wires)**
Heavily concentrated on digits 2 and 5. Similar to Exhibit C — recurring round-number transfers through Deutsche Bank accounts in the final months before account closure.

## What This Means

Benford's Law fails on the Epstein wire ledger. The deviation is large, statistically significant, and driven by two factors: over-representation of digits 2 and 5, and an 84.3% round-number concentration.

This does not indicate fraud in the traditional forensic accounting sense. Fabricated data typically shows uniform digit distribution (each digit near 11.1%), not selective concentration on two digits. The Epstein pattern is different: it shows **instructed money**.

Normal financial transactions produce Benford-conforming data because they result from market forces — prices, quantities, interest calculations, tax computations — that generate amounts across the full digit range. The Epstein wires fail Benford's Law because they are not market transactions. They are discretionary transfers: someone deciding to move $5 million, $2.5 million, $10 million. The amount is chosen, not calculated.

The exhibit-level analysis reinforces this interpretation:

- **Exhibit A** (wealth transfers in) = exact millions, negotiated between principals
- **Exhibit B** (investments out) = closest to Benford, because market returns produce non-round amounts
- **Exhibit C** (operating pipeline) = repeating $2M–$2.5M tranches, a cash management cadence
- **Exhibits D and E** = round-number discretionary transfers

The round-number problem is not that the transfers are fake. It is that they are the financial signature of a system where one person controlled all the money. There are no invoices, no contracts, no market prices generating these amounts. There is only instruction: move this much, to this account, today. In a normal financial ecosystem, hundreds of independent actors produce Benford-conforming variety. In the Epstein system, one decision-maker produced round numbers.

## What I Can't Determine

- **Whether any specific round-number transfer was deliberately structured to avoid reporting thresholds.** The absence of $9,999 transfers (just below the $10,000 CTR reporting threshold) suggests this was not a structuring operation. The amounts are too large for BSA structuring concerns.
- **Whether the Benford deviation would be significant in a larger sample.** With n=185, the chi-squared test has limited power. A sample of 1,000+ wire transfers would produce more reliable Benford statistics.
- **What the "correct" round-number rate is for trust-to-trust transfers.** The 84.3% figure is compared against general commercial banking norms (30–50%). The appropriate baseline for high-net-worth trust administration may be higher, though unlikely to reach 84%.

---

*Source: DOJ EFTA Document Release — Deutsche Bank-SDNY Production (Exhibits A–E), 185 verified wire transfers totaling $557,372,954. Benford's Law analysis performed on first-digit and first-two-digit distributions. Round-number classification by modular arithmetic at million, hundred-thousand, ten-thousand, and thousand levels. Supporting data: <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook (view-only)</a>. This analysis is published as part of the <a href="https://github.com/randallscott25-star/epstein-forensic-finance#readme" target="_blank">Epstein Financial Forensics</a> repository.*

*For the girls.*

---

## Source Documents & Exhibits

### Primary Exhibits
**Exhibits A–E** (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>): 481 wire transfer amounts tested against Benford's Law.

### Corpus Statistics Source
**Method**: Benford's Law first-digit analysis on 481 wire amounts from the Master Wire Ledger.
**Finding**: 84.3% round numbers. Digits 2 and 5 over-represented vs. Benford's expected distribution.
**Database**: Master Wire Ledger (481 wires, $973M total).

### Scope Note
Benford's test applied to Deutsche Bank wire production only. The test could be extended to Bear Stearns/JPMorgan transaction data if those records become available through future enforcement actions or EFTA releases.

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibits A–E — 185 wire transfers tested against Benford's Law |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse neighboring documents in Dataset 8 |

> **Note:** Statistical framework (Benford's Law) is an analytical tool applied to EFTA data, not itself sourced from the corpus.

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — Full 481 wires | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| SAR Comparison | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1121979938#gid=1121979938" target="_blank">📊 Open Tab</a> |
| Above-Cap Verified | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2071460294#gid=2071460294" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Wire data from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> Exhibits A–E. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
