# Narrative 13: Seven Banks, One Trust

**The Outgoing Money Trust distributed funds through seven separate banks. In financial compliance, this pattern has a name: structuring.**

---

## 180 Financial Records, Zero Wire Transfers

The Outgoing Money Trust shows up in 195 EFTA documents. 180 are financial. That's 92% financial records — one of the most financially documented entities in the network.

Zero wire transfer records in the Deutsche Bank production. Not one.

That's not because it didn't move money. It moved money through seven different banks.

## The Seven Banks

I ran co-occurrence on Outgoing Money Trust financial docs against banking entities. Clear disbursement architecture:

| Bank | Financial Files | Type |
|------|----------------|------|
| **Deutsche Bank Trust Co. Americas** | **180** | Primary account |
| **Wells Fargo Bank** | **63** | Secondary |
| **Bank of America** | **38** | Secondary |
| **TD Bank** | **23** | Secondary |
| **JPMorgan Chase Bank** | **14** | Secondary |
| **PNC Bank** | **12** | Secondary |
| **Sabadell United Bank** | **11** | Secondary |

Deutsche Bank is the primary bank — but the Outgoing Money Trust has no entries in the wire ledger. Its Deutsche Bank statements got captured in the broader production, but the individual wires never made it into the exhibit structure covering Southern Trust, Southern Financial, and the other ledger entities.

No other shell in the network used seven banks. Southern Trust banked at Deutsche Bank. Haze Trust banked at Deutsche Bank and HSBC. Gratitude America used Deutsche Bank and Morgan Stanley. The Outgoing Money Trust used **seven**.

## What the Statements Show

The money values extracted from Outgoing Money Trust financial documents cluster in a pattern consistent with recurring disbursements:

**Frequent transaction amounts:** $100,000 (61 mentions), $200,000 (50 combined variants), $175,000 (20), $500,000 (17), $400,000 (17), $250,000 (16), $230,000 (15), $50,000 (18), $7,000 (39), $7,200 (18).

The $100,000–$500,000 cluster is the operating range. These are not investment-scale transfers — they're disbursement-scale. The $7,000–$7,200 recurring amounts are consistent with management or service fees.

The account also shows a balance figure of **$2,668,832.43** appearing across 15 documents, suggesting a maintained operating balance in that range.

## The Named Operators

Two names recur across Outgoing Money Trust financial documents:

**Stewart Oldfield** — appears on 35 files across OCR variants (23 as "Stewart Oldfield," 12 as "Stewart Oldficld"). This is the most frequently named individual on Outgoing Money Trust records. External reporting from other EFTA researchers identifies a Stewart Oldfield as Deutsche Bank operations staff who processed Epstein-related transactions alongside colleagues Brigid Macias and Firdaus Madiar — suggesting Oldfield was the bank's representative on these accounts rather than an Epstein associate. His recurrence across 35 OMT files indicates he was the primary Deutsche Bank officer servicing this trust's disbursement activity.

**Lee McKenzie Consultants** — appears on 12 files. This entity appears as a payee, suggesting recurring consulting payments from the trust.

Neither name appears prominently on other Epstein shell entities' financial records at this frequency, suggesting their roles were concentrated in the Outgoing Money Trust's disbursement operations — Oldfield as the Deutsche Bank officer processing the transactions, and Lee McKenzie Consultants as a recurring payee.

## Why Seven Banks Matters

Under the Bank Secrecy Act, financial institutions are required to file Suspicious Activity Reports (SARs) when they observe transactions that appear designed to evade reporting requirements. One of the primary indicators for SAR filing is **structuring** — the practice of distributing transactions across multiple institutions or accounts to avoid triggering individual reporting thresholds.

One trust. Seven banks. Recurring disbursements in the $100K–$500K range. No clear commercial reason for the multi-bank setup. That's a textbook structuring profile.

I'm not making a legal conclusion. There may be legitimate reasons for the seven-bank structure. But the pattern is precisely what BSA/AML compliance programs are designed to detect, and it raises a question: did any of these seven banks file SARs on the Outgoing Money Trust's activity?

Deutsche Bank's Epstein-related SAR failures are a matter of public record — they were central to the $150 million DFS fine. Whether Wells Fargo, Bank of America, TD Bank, JPMorgan Chase, PNC Bank, or Sabadell United Bank filed SARs on the Outgoing Money Trust is unknown.

## The Name Says It All

Outgoing Money Trust. The name is the function. It was the network's payment processor — converting pooled funds into outgoing payments across multiple banking channels.

Other shells collected and concentrated money. Southern Trust ($244M) and Southern Financial ($139M) were the hubs. The Outgoing Money Trust did the opposite: disaggregation. Concentrated funds distributed across seven banks in disbursement-sized amounts.

Combined with the Outgoing Money Trust's co-occurrence with the broader Epstein entity network — it shares files with Deutsche Bank Trust Company Americas (157), Southern Trust Company via cross-references, and shows the standard bank statement formatting (Non-Electronic Funds Transfers, Preauthorized Debit, Debit Card Withdrawals) — this entity operated as the network's outflow engine.

Seven banks. Recurring disbursements. One trust.

---

**Methodology:** Entity co-occurrence analysis of Outgoing Money Trust financial documents against bank-name entities. Money value clustering based on automated MONEY-type entity extraction. Named person identification from PERSON-type entities co-occurring on financial documents. All amounts are unverified automated extractions. See [Methodology](../docs/METHODOLOGY.md).

**Source data:** [Master Wire Ledger](../data/master_wire_ledger_phase5i.json) · <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook</a> · <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/shell_network.html" target="_blank">Interactive Network</a>

**Related narratives:** [N1: Money Pipeline](01_jeepers_pipeline.md) · [N5: Bear Stearns vs. Deutsche Bank](05_deutsche_bank.md) · [N11: The Shell Map](11_the_shell_map.md) · [N12: The Bank Nobody Prosecuted](12_the_bank_nobody_prosecuted.md)

*All findings are (Unverified) automated extractions from DOJ EFTA documents released under the Epstein Files Transparency Act. Entity mention does not imply wrongdoing. This analysis identifies patterns for further investigation — it does not make legal conclusions.*

*For the girls.*

---

## Source Documents & Exhibits

### Primary Source
Corpus-wide analysis of Outgoing Money Trust entity co-occurrence with banking institutions.

### Key EFTA Corpus Statistics
- **Outgoing Money Trust**: 195 total files, 180 financial documents, zero wires in Master Wire Ledger
- **7-Bank Architecture** (from entity co-occurrence in financial docs):

| Bank | Shared Files with OMT |
|------|----------------------|
| Deutsche Bank | 180 |
| Wells Fargo | 63 |
| Bank of America | 38 |
| TD Bank | 23 |
| JPMorgan Chase | 14 |
| PNC Bank | 12 |
| Sabadell United Bank | 11 |

**Method**: Bank entity co-occurrence with "Outgoing Money Trust" in financial documents.

### Disbursement Amount Clustering
Top recurring amounts: $100K (61 mentions), $200K (50), $175K (20), $500K (17), $400K (17), $250K (16), $230K (15)
Recurring fees: $7,000 (39 mentions), $7,200 (18)
**Method**: Money-entity extraction from OMT financial documents.

### Key Persons
- Stewart Oldfield: 35 files — identified as Deutsche Bank operations staff (per rhowardstone INVESTIGATION_8)
- **Method**: Person entity extraction from OMT financial documents, cross-referenced with external reporting

### External Corroboration
- rhowardstone INVESTIGATION_8: Identifies Stewart Oldfield alongside Brigid Macias, Firdaus Madiar, Monica Gilkins, Rachel Wachs as Deutsche Bank staff processing Epstein transactions
- BSA structuring threshold: $10,000 (31 U.S.C. § 5324) — OMT disbursement pattern shows amounts clustered below and at round thresholds

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| Full EFTA Corpus | DS1–12 | Outgoing Money Trust: 195 documents (180 financial), 7 banking relationships |
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibits A–E (trust network wires for cross-reference) |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse Dataset 8 |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">Dataset 9</a> | DS9 | Browse Dataset 9 — multi-bank financial records |

**All 12 DOJ Datasets:** <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">1</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-2-files" target="_blank">2</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-3-files" target="_blank">3</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-4-files" target="_blank">4</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-5-files" target="_blank">5</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-6-files" target="_blank">6</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-7-files" target="_blank">7</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">8</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">9</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-10-files" target="_blank">10</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">11</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-12-files" target="_blank">12</a>

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Shell Network — Outgoing Money Trust × 7 banks | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1040516313#gid=1040516313" target="_blank">📊 Open Tab</a> |
| Shell Trust Hierarchy — OMT position | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1943952132#gid=1943952132" target="_blank">📊 Open Tab</a> |
| Money Flow Patterns — Disbursement clustering | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2075093083#gid=2075093083" target="_blank">📊 Open Tab</a> |
| Entity P&L — Outgoing Money Trust | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1497389416#gid=1497389416" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
