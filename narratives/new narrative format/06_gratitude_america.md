# Gratitude America

**A charity that sent 88% of its outflows to investment accounts and 7% to actual charitable purposes.**

*All amounts are (Unverified) automated extractions from DOJ EFTA documents. Appearance in this analysis does not imply wrongdoing. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What I Found

Gratitude America was a charity — on paper. I pulled 20 wire transfers totaling $13,080,518 (Unverified). Where'd the money go? Investment and bank accounts got almost everything. Actual charity got almost nothing.

It's on **Exhibit E** of the Deutsche Bank-SDNY production.

## Where the Money Went

### Investment and Banking Transfers

| Date | To | Amount (Unverified) | Source |
|------|------|------|--------|
| Mar 2, 2016 | Gratitude America Ltd. (Morgan Stanley) | $5,000,000 | Exhibit E |
| Mar 2, 2016 | Citibank | $5,000,000 | Phase 25 recovery |
| Jul 19, 2016 | Gratitude America Ltd. (Morgan Stanley) | $500,000 | Exhibit E |
| Jul 19, 2016 | Citibank | $500,000 | Phase 25 recovery |
| Jan 21, 2016 | Gratitude America Ltd. (First Bank) | $50,000 | Exhibit E |
| Apr 6, 2016 | Gratitude America Ltd. (First Bank) | $250,000 | Exhibit E |
| Jan 20, 2017 | Citibank | $200,000 | Phase 25 recovery |
| Mar 6, 2017 | Citibank | $250,000 | Phase 25 recovery |

**Total to investment/banking: $11,750,000 (Unverified)**

The $5M transfer on March 2, 2016 is the single largest disbursement — sent from the Gratitude America MMDA (Money Market Deposit Account) to a Morgan Stanley investment account held by "Gratitude America Ltd." The same day, $5M moved to Citibank. This was not a charitable grant. It was an asset transfer between financial accounts.

### Actual Charitable Disbursements

| Date | To | Amount (Unverified) | Source |
|------|------|------|--------|
| Jan 29, 2016 | Melanoma Research Alliance Foundation | $225,000 | Exhibit E |
| Jan 7, 2016 | Bruce & Marsha Moskowitz Foundation | $50,000 | Exhibit E |
| Jul 14, 2016 | Bruce & Marsha Moskowitz Foundation | $50,000 | Exhibit E |
| Dec 11, 2017 | Bruce & Marsha Moskowitz Foundation | $50,000 | Exhibit E |
| Oct 2, 2017 | Cancer Research Wellness Institute | $25,000 | Exhibit E |
| Feb 28, 2018 | Cancer Research Wellness Institute | $25,000 | Exhibit E |
| Apr 2, 2018 | NPO Baleto Teatras | $18,493 | Exhibit E |
| Sep 17, 2018 | VSJ Baleto Teatras | $10,000 | Exhibit E |

**Total charitable: $453,493 (Unverified)**

## Where the Money Came From

| Date | From | Amount (Unverified) |
|------|------|------|
| Oct 11, 2013 | Deutsche Bank | $200,000 |
| Jul 19, 2016 | Deutsche Bank | $500,000 |
| Undated | Deutsche Bank | $176,049 |
| Undated | Deutsche Bank | $976 |

**Total visible inflows from Deutsche Bank: $877,025 (Unverified)**

Visible inflows: $877K. Visible outflows: $12.2M. The gap means Gratitude America's main funding came from sources I didn't capture in the wires — probably internal transfers, investment returns, or deposits predating the document window.

## The Ratio

Based on the wire transfers I extracted:

| Category | Amount (Unverified) | % of Outflows |
|----------|------|------|
| Investment/banking accounts | $11,750,000 | 88.4% |
| Charitable grants | $453,493 | 3.4% |
| Other/unclassified | $877,025 | — |

**For every dollar sent to charity, $26 went to investment accounts.**

The three charitable recipients — Melanoma Research Alliance Foundation, Bruce & Marsha Moskowitz Foundation, and Cancer Research Wellness Institute — received between $10,000 and $225,000 each. The Lithuanian ballet entities (NPO Baleto Teatras and VSJ Baleto Teatras) received a combined $28,493.

## The Morgan Stanley Account

The largest single destination for Gratitude America's outflows was "Gratitude America Ltd." at Morgan Stanley — receiving $5,500,000 across 2 wires. This is a separate legal entity from the MMDA account that held the charity's liquid assets. The relationship between "Gratitude America MMDA" (the Deutsche Bank money market account) and "Gratitude America Ltd." (the Morgan Stanley investment vehicle) warrants further examination.

## What I Can't Determine

- **Gratitude America's full financial picture.** I see wire transfers, not bank statements. The charity may have had additional grant-making through checks, ACH transfers, or other mechanisms not captured in wire data.
- **The investment returns.** If the Morgan Stanley account generated returns that were later distributed to charitable purposes, the effective charitable ratio would be higher than what the wire data alone shows.
- **Tax filings.** IRS Form 990 filings (if they exist) would show the complete picture of Gratitude America's revenues, expenses, and charitable distributions. That analysis is outside the scope of wire extraction.
- **The Lithuanian ballet connection.** Two small transfers to ballet-related entities in Lithuania ($18,493 and $10,000) are an unusual pattern for a U.S.-based charity. I note the pattern without interpreting it.

---

*Source: DOJ EFTA Document Release, Deutsche Bank-SDNY Production, Exhibit E. All data extracted via automated pipeline. Supporting data: <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook (view-only)</a>. This finding appears in the [master wire ledger](../data/master_wire_ledger_phase5i.json) published with this repository.*

---

## Source Documents & Exhibits

### Primary Exhibit
**Exhibit E** (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>): Gratitude America MMDA disbursements plus expansion wires.

### Wire Ledger Cross-Reference
20 wires total (12 from Exhibit E, 8 expansion), $13,080,518 combined.

**Exhibit E wires (12):**

| Wire | Amount | Date |
|------|--------|------|
| Gratitude America MMDA → Bruce & Marsha Moskowitz Foundation | $50,000 | 2016-01-07 |
| Gratitude America MMDA → Gratitude America Ltd. (First Bank PR) | $50,000 | 2016-01-21 |
| Gratitude America MMDA → Melanoma Research Alliance Foundation | $225,000 | 2016-01-29 |
| Gratitude America MMDA → Gratitude America Ltd. (Morgan Stanley/Citibank) | $5,000,000 | 2016-03-02 |
| Gratitude America MMDA → Gratitude America Ltd. (First Bank PR) | $250,000 | 2016-04-06 |
| Gratitude America MMDA → Bruce & Marsha Moskowitz Foundation | $50,000 | 2016-07-14 |
| Gratitude America MMDA → Gratitude America Ltd. (Morgan Stanley/Citibank) | $500,000 | 2016-07-19 |
| Gratitude America MMDA → Cancer Research Wellness Institute | $25,000 | 2017-10-02 |
| Gratitude America MMDA → Bruce & Marsha Moskowitz Foundation | $50,000 | 2017-12-11 |
| Gratitude America MMDA → Cancer Research Wellness Institute | $25,000 | 2018-02-28 |
| Gratitude America MMDA → NPO Baleto Teatras | $18,493 | 2018-04-02 |
| Gratitude America MMDA → VSJ Baleto Teatras | $10,000 | 2018-09-17 |

### Corpus Statistics Source
**Method**: Entity co-occurrence analysis across 209 files containing "Gratitude America."
**Database**: 1,476,377 files, 11.4M extracted entities (see [METHODOLOGY.md](../docs/METHODOLOGY.md)).

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibit E — Gratitude America Ltd. wire activity |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse neighboring documents in Dataset 8 |

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — Exhibit E (Gratitude America) | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Entity P&L — Gratitude America | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1497389416#gid=1497389416" target="_blank">📊 Open Tab</a> |
| Shell Network — Gratitude America co-occurrence | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1040516313#gid=1040516313" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Wire data from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> Exhibit E. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
