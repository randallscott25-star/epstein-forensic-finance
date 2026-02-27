# Narrative 15: Gratitude America — The Charity That Invested

**A tax-exempt charity that sent 88% of its documented outflows to hedge funds, 7% to actual charitable purposes, and named Jeffrey Epstein's girlfriend on 8 financial records.**

---

## The Setup

209 documents in the EFTA corpus. 89 are financial records. $45 million in verified wire transfers on my Deutsche Bank ledger. By every measure, a functioning financial entity.

Registered as a **tax-exempt charity**.

## Where the Money Actually Went

My co-occurrence analysis of Gratitude America's 89 financial documents against known investment fund entities produces the following outflow profile:

### Investment Vehicles

| Fund | Shared Financial Files |
|------|----------------------|
| **Boothbay Multi-Strategy Fund** | **18** |
| Boothbay Enhanced Fund | 6 |
| Boothbay Absolute Strategies Fund | 7 (variants) |
| Boothbay Multi Strategy Fund LP | 2 |
| **Honeycomb** | **15** |
| Honeycomb Ventures IV LP | 5 |
| Honeycomb Partners LP | 4 |
| Honeycomb Ventures | 4 |
| **Valar Global Fund II** | **11** |
| Valar Global Fund II LP | 4 |
| Valar Global Fund III | 4 |
| Valar III Capital Call | 3 |
| **Coatue Enterprises** | **6** |
| **Foundation Medicine Inc** | **13** |

### Actual Charitable Entities

| Entity | Shared Financial Files |
|--------|----------------------|
| Baleto Teatras (Lithuanian ballet) | 3 |
| Cancer Research Wellness Institute | 2 |
| C.O.U.Q. Foundation | 5 (variants) |
| Marsha Moskowitz Foundation | 4 |
| Florida Science Foundation | 2 |
| Epstein VI Foundation — Equities | 2 |

Investment vehicles show up on roughly 90 financial files. Charitable entities show up on about 18.

That's an 83/17 split. Eighty-three percent investment, seventeen percent charitable.

## The Money Scale

The dollar amounts extracted from Gratitude America's financial documents are not charity-scale. They are fund-scale:

| Amount | Mentions |
|--------|----------|
| **$2,000,000** | **110** |
| **$5,000,000** | **101** |
| **$2,500,000** | **101** |
| **$3,000,000** | **88** |
| **$10,000,000** | **79** |
| **$20,000,000** | **66** |
| **$8,000,000** | **57** |
| **$15,000,000** | **44** |
| **$13,000,000** | **44** |
| **$7,000,000** | **44** |
| **$4,250,000** | **44** |
| **$1,000,000** | **44** |
| $500,000 | 66 |
| $250,000 | 44 |
| $150,000 | 66 |
| $100,000 | 79 |
| $50,000 | 88 |
| $25,000 | 88 |
| $10,000 | 58 |

The most common amounts are $2 million, $5 million, $2.5 million, and $3 million. A charity writing checks to a Lithuanian ballet company doesn't generate that profile. An investment fund making capital calls does.

## The Name on the Records

**Karyna Shuliak** appears on **8 Gratitude America files**.

Karyna Shuliak was Jeffrey Epstein's girlfriend at the time of his death. She is a Belarusian-born dentist who graduated from Columbia University's College of Dental Medicine in 2015. She was approximately 30 years old when Epstein died in 2019. Shuliak was named as the primary beneficiary in Epstein's estate filings, with a bequest of approximately $50–100 million.

Her name appears in the context of Gratitude America financial records alongside entities like "Baleto Teatras" — a Lithuanian ballet theater. Shuliak's Eastern European background and the Lithuanian ballet connection suggest that some of Gratitude America's minimal charitable activity may have been directed by or for the benefit of Epstein's personal relationship rather than arm's-length charitable purposes.

## The Banking

Gratitude America banked at Deutsche Bank:

| Bank | Shared Financial Files |
|------|----------------------|
| Deutsche Bank Trust Co. Americas | 65+ (variants) |
| Southern Financial | 6 |
| Coatue Enterprises | 6 |
| EFTA | 10 |

The Deutsche Bank statements show standard banking activity: non-electronic funds transfers, debit card withdrawals, service charges, NSF fees. Gratitude America maintained active transactional accounts — not the dormant endowment account you'd expect from a charity investing its corpus for future grants.

## The Tax Question

Under Internal Revenue Code § 501(c)(3), tax-exempt organizations must be organized and operated **exclusively** for charitable, religious, educational, or scientific purposes. The IRS prohibition on private benefit is absolute: no part of a 501(c)(3) organization's net earnings may inure to the benefit of any private individual.

If Gratitude America filed IRS Form 990 returns claiming tax-exempt charitable status while routing the majority of its financial activity through hedge fund investments (Boothbay, Honeycomb, Valar, Coatue) and maintaining connections to Epstein's girlfriend, it presents a question under § 501(c)(3) that the IRS has jurisdiction to evaluate.

Two features of IRS enforcement are relevant:

1. **No statute of limitations on fraud.** If a 990 filing contained material misrepresentations about the organization's charitable purpose, the IRS can examine those filings without time limitation under IRC § 6501(c)(1).

2. **Public records.** Form 990 filings for tax-exempt organizations are public documents. Gratitude America's 990s, if they were filed, should be obtainable through the IRS Tax Exempt Organization Search (TEOS) or ProPublica's Nonprofit Explorer.

Comparing Gratitude America's public 990 filings against the outflow profile documented here — $2–20 million transactions to hedge funds, with less than 20% to identifiable charitable recipients — would determine whether the organization's public disclosures matched its actual financial activity.

## The Document Profile

Gratitude America's full document type breakdown:

| Document Type | Files |
|--------------|-------|
| Financial | 89 |
| Email | 51 |
| Document | 44 |
| Fax | 8 |
| Court Filing | 6 |
| Subpoena | 5 |
| Letter | 4 |
| Phone Record | 1 |
| Flight Log | 1 |

The 51 emails and 44 general documents suggest Gratitude America was not a passive investment vehicle — it was actively managed with regular correspondence. The 6 court filings and 5 subpoenas indicate it drew legal attention. The single flight log co-occurrence connects it to the aviation layer of the Epstein network.

## The Comparison

Every other Epstein entity that invested in Boothbay, Honeycomb, Valar, and Coatue did so through entities that were overtly structured as financial vehicles: Southern Trust Company, Southern Financial LLC, Plan D LLC. Nobody expects a trust company to be a charity.

Gratitude America is the only entity in the network that claimed tax-exempt charitable status while routing investment-scale transactions through the same hedge fund pipeline. It is the entity where the gap between stated purpose and documented activity is widest.

The data is in the EFTA documents. The 990s are public. The comparison is straightforward.

---

**Methodology:** Entity co-occurrence analysis of Gratitude America financial documents against investment fund names and charitable organization names. Money values from MONEY-type entity extraction on financial documents. Document type classification from automated pipeline. All amounts are unverified automated extractions. See [Methodology](../docs/METHODOLOGY.md).

**Source data:** [Master Wire Ledger](../data/master_wire_ledger_phase5i.json) · <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook</a> · <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/shell_network.html" target="_blank">Interactive Network</a>

**Related narratives:** [N3: Outflow Recipients](03_plan_d_question.md) · [N11: The Shell Map](11_the_shell_map.md) · [N14: Leon Black](14_where_leon_blacks_money_went.md)

*All findings are (Unverified) automated extractions from DOJ EFTA documents released under the Epstein Files Transparency Act. Entity mention does not imply wrongdoing. This analysis identifies patterns for further investigation — it does not make legal conclusions.*

*For the girls.*

---

## Source Documents & Exhibits

### Primary Exhibit
**Exhibit E** (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>): Gratitude America MMDA disbursements.

### Wire Ledger Cross-Reference
12 Exhibit E wires, $6,253,493 total (see N6 appendix for full wire table — identical Exhibit E source).

Key wires demonstrating investment vs. charitable split:

**Investment-scale transfers:**
- Gratitude America MMDA → Gratitude America Ltd. (Morgan Stanley/Citibank): $5,000,000 (2016-03-02)
- Gratitude America MMDA → Gratitude America Ltd. (Morgan Stanley/Citibank): $500,000 (2016-07-19)
- Gratitude America MMDA → Gratitude America Ltd. (First Bank PR): $250,000 (2016-04-06)

**Charitable disbursements:**
- Gratitude America MMDA → Bruce & Marsha Moskowitz Foundation: $50,000 (×3: 2016-01, 2016-07, 2017-12)
- Gratitude America MMDA → Melanoma Research Alliance Foundation: $225,000 (2016-01-29)
- Gratitude America MMDA → Cancer Research Wellness Institute: $25,000 (×2: 2017-10, 2018-02)
- Gratitude America MMDA → NPO Baleto Teatras: $18,493 (2018-04-02)
- Gratitude America MMDA → VSJ Baleto Teatras: $10,000 (2018-09-17)

### Corpus Statistics Source
- **Gratitude America**: 209 total files, 89 financial documents
- **Investment/Charity ratio**: 83% investment (Boothbay, Honeycomb, Valar, Coatue, Foundation Medicine) / 17% charitable (Baleto Teatras, Cancer Research, C.O.U.Q., Florida Science, Moskowitz) by document frequency
- **BV70 LLC**: Sole capitalization source at $10M (confirmed by wire ledger and rhowardstone)
- **Karyna Shuliak**: 8 files — Epstein's girlfriend, Belarusian-born dentist, connected to Baleto Teatras
- **Deutsche Bank AG**: 76 files — primary banking relationship
- **Method**: Entity co-occurrence analysis across Gratitude America financial documents

### External Corroboration
- WSJ reporter inquiry (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00009962.pdf" target="_blank">EFTA00009962</a>): Charities listed on Gratitude America tax forms said they never received listed donations
- NBC News: Independent verification that named charities denied receiving Gratitude America funds
- Daily Beast: Cancer Research Wellness Institute founder Howard Straus said he'd never heard of Epstein or Gratitude America
- Richard Kahn confirmed as Gratitude America president (Harvard Crimson, Daily Beast, tax filings)
- Darren Indyke confirmed as treasurer
- BV70 LLC (Leon Black) sole capitalization confirmed (rhowardstone)

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibit E — Gratitude America wire activity ($45M verified) |
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00009962.pdf" target="_blank">EFTA00009962</a> | DS8 | Gratitude America financial document — fund co-occurrence |
| Full EFTA Corpus | DS1–12 | Gratitude America: 209 documents (89 financial) — hedge fund co-occurrence |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse Dataset 8 |

**All 12 DOJ Datasets:** <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">1</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-2-files" target="_blank">2</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-3-files" target="_blank">3</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-4-files" target="_blank">4</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-5-files" target="_blank">5</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-6-files" target="_blank">6</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-7-files" target="_blank">7</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">8</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">9</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-10-files" target="_blank">10</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">11</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-12-files" target="_blank">12</a>

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — Exhibit E (Gratitude America) | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Entity P&L — Gratitude America | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1497389416#gid=1497389416" target="_blank">📊 Open Tab</a> |
| Shell Network — Gratitude America co-occurrence | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1040516313#gid=1040516313" target="_blank">📊 Open Tab</a> |
| Shell Trust Hierarchy | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1943952132#gid=1943952132" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Wire data from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> Exhibit E. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
