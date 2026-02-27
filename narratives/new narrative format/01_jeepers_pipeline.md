# The Jeepers Pipeline

**$57,876,640 through a brokerage shell into personal checking — all documented, all dated, all on one exhibit.**

*All amounts are (Unverified) automated extractions from DOJ EFTA documents. Appearance in this analysis does not imply wrongdoing. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What I Found

Jeepers Inc. was a Deutsche Bank brokerage entity. Its job: capitalize Jeffrey Epstein's personal NOW and SuperNow checking accounts. Between October 2013 and February 2019, I pulled 24 wire transfers totaling $57,876,640 (Unverified) flowing from Jeepers through its Deutsche Bank brokerage account into Epstein's personal checking.

Every wire is on **Exhibit C** of the Deutsche Bank-SDNY production: "Capitalization of Jeffrey Epstein's NOW/SuperNow Accounts." Every wire has a bates stamp. Every wire has a date. This is the highest-confidence finding in the entire analysis.

## The Pipeline

Same mechanism every time. Jeepers Inc. held assets in a Deutsche Bank brokerage account and periodically moved large sums into Epstein's personal NOW/SuperNow checking at the same bank. Three of the transfers moved money first from Jeepers Inc. (the entity) into the Jeepers Inc. DB Brokerage Account before the onward transfer — an internal staging step.

| Date | Amount (Unverified) | Bates Reference |
|------|------|------|
| Oct 11, 2013 | $3,000,000 | DB-SDNY-0002926 |
| Nov 14, 2013 | $2,000,000 | DB-SDNY-0002994 |
| Dec 20, 2013 | $2,000,000 | DB-SDNY-0003427 |
| Jan 30, 2014 | $2,000,000 | DB-SDNY-0003538 |
| Feb 20, 2014 | $4,000,000 | DB-SDNY-0003640 |
| Apr 11, 2014 | $3,400,000 | DB-SDNY-0003769 |
| May 6, 2014 | $2,000,000 | DB-SDNY-0003832 |
| Jun 11, 2014 | $3,000,000 | DB-SDNY-0003896 |
| Jul 16, 2014 | $2,000,000 | DB-SDNY-0003960 |
| Aug 19, 2014 | $2,500,000 | DB-SDNY-0004022 |
| Oct 2, 2014 | $2,500,000 | DB-SDNY-0004126 |
| Jan 5, 2015 | $2,500,000 | DB-SDNY-0004296 |
| Mar 13, 2015 | $2,000,000 | DB-SDNY-0004431 |
| Mar 27, 2015 | $2,000,000 | DB-SDNY-0004432 |
| Apr 16, 2015 | $2,000,000 | DB-SDNY-0004509 |
| May 18, 2015 | $2,000,000 | DB-SDNY-0004587 |
| Jun 12, 2015 | $2,000,000 | DB-SDNY-0004665 |
| Jul 9, 2015 | $3,200,000 | DB-SDNY-0004736 |
| Aug 20, 2015 | $2,000,000 | DB-SDNY-0004807 |
| Oct 7, 2015 | $2,000,000 | DB-SDNY-0004937 |
| Oct 29, 2015 | $2,500,000 | DB-SDNY-0004938 |
| Sep 9, 2016 | $2,000,000 | DB-SDNY-0005683 |
| Oct 26, 2016 | $2,000,000 | DB-SDNY-0005748 |
| Feb 7, 2019 | $3,276,640 | DB-SDNY-0008016 |

**Total: $57,876,640 (Unverified) across 24 wires.**

## What It Means

Look at the cadence. From October 2013 through October 2015, transfers arrived like clockwork — monthly or near-monthly, in round amounts between $2M and $4M. Brokerage positions liquidated into cash on a schedule.

The bates numbers run sequential (DB-SDNY-0002926 through DB-SDNY-0008016), which tells me these were produced as a coherent set from Deutsche Bank's records. No gaps in the exhibit — I got every wire on Exhibit C that involved Jeepers Inc.

After October 2015, the cadence breaks. Two transfers in late 2016, then nothing until a single $3,276,640 transfer on February 7, 2019 — five months before Epstein's arrest on July 6, 2019.

## What I Can't Determine

This analysis traces the pipeline — money flowing from Jeepers Inc. brokerage into Epstein's personal checking. What I cannot determine from the EFTA corpus:

- **What funded Jeepers Inc.** The brokerage account was the intermediary, not the origin. The upstream source of these assets is not visible in the documents I extracted.
- **What the NOW/SuperNow accounts paid for.** The outbound spending from Epstein's personal checking is a separate question requiring different document analysis.
- **Whether Jeepers Inc. had other functions.** I only see the wire transfers. Jeepers may have held other positions or served other purposes within the financial network.

## OCR Note

Several bates stamps show OCR artifacts in entity names: "Jee ers Inc." appears in place of "Jeepers Inc." at DB-SDNY-0003427, 0004431, 0004432, 0004509, 0004587, 0005683. Entity normalization resolved these to the correct name. The amounts and dates were unaffected.

---

*Source: DOJ EFTA Document Release, Deutsche Bank-SDNY Production, Exhibit C. All data extracted via automated pipeline; no manual adjustments to amounts or dates. 24/24 entries dated (100%). Supporting data: <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook (view-only)</a>. This finding appears in the [master wire ledger](../data/master_wire_ledger_phase5i.json) published with this repository.*

---

## Source Documents & Exhibits

### Primary Exhibit
**Exhibit C** (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>): Jeepers Inc. brokerage account activity at Deutsche Bank, 2013–2019.

### Wire Ledger Cross-Reference
24 wires verified, $57,876,640 total. All from Exhibit C.

| Wire | Amount | Date |
|------|--------|------|
| Jeepers Inc. (DB Brokerage) → Jeffrey Epstein NOW/SuperNow Account | $3,000,000 | 2013-10-11 |
| Jeepers Inc. (DB Brokerage) → Jeffrey Epstein NOW/SuperNow Account | $2,000,000 | 2013-11-14 |
| Jeepers Inc. → Jeepers Inc. (DB Brokerage) | $2,000,000 | 2013-12-20 |
| *(21 additional wires — see Master Wire Ledger, Exhibit C)* | | |

### Corpus Statistics Source
**Method**: Entity co-occurrence analysis across files containing "Jeepers" entity variants.
**Database**: 1,476,377 files, 11.4M extracted entities (see [METHODOLOGY.md](../docs/METHODOLOGY.md)).

### Scope Note
Wire data sourced exclusively from Deutsche Bank production (Exhibits A–E). Jeepers Inc. also co-occurs with Financial Trust Company (125 shared files), which banked primarily at Bear Stearns — indicating additional financial activity outside this production's scope. See N11 (Shell Map) and N12 (Bear Stearns) for multi-bank context.

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibit C — Capitalization of Epstein's NOW/SuperNow Accounts |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse neighboring documents in Dataset 8 |

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — Exhibit C (Jeepers wires) | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Shell Network — Jeepers co-occurrence | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1040516313#gid=1040516313" target="_blank">📊 Open Tab</a> |
| Entity P&L — Jeepers Inc. | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1497389416#gid=1497389416" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
All EFTA document IDs are from the public DOJ release under the Epstein Files Transparency Act at <a href="https://efts.gov" target="_blank">efts.gov</a>. Wire data from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> Exhibit C. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
