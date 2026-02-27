# The Plan D Question

**$18 million out to one man. Near-zero coming in. Where did Plan D LLC get its money?**

*All amounts are (Unverified) automated extractions from DOJ EFTA documents. Appearance in this analysis does not imply wrongdoing. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What I Found

Plan D LLC sent $18,000,000 (Unverified) to Leon Black across 4 wire transfers between 2014 and 2017. Coming the other direction? $1,125.03. One remittance advice entry. That's it. Plan D paid out $18 million with no visible funding source anywhere in the EFTA corpus.

Meanwhile, Leon & Debra Black and Black Family Partners LP sent $131,500,000 (Unverified) *into* Southern Trust Company Inc. — the network's central hub — across 12 wire transfers on **Exhibit A**.

## Plan D LLC Outflows

| Date | To | Amount (Unverified) | Source |
|------|------|------|--------|
| Apr 25, 2014 | Leon Black | $5,000,000 | Phase 25 recovery |
| Oct 22, 2014 | Leon Black | $3,000,000 | Phase 25 recovery |
| Oct 22, 2014 | Leon Black | $2,000,000 | Phase 25 recovery |
| Mar 31, 2017 | Leon Black | $8,000,000 | Phase 25 recovery |

**Total Plan D → Leon Black: $18,000,000 (Unverified)**

**Total Plan D inflows found: $1,125.03**

## Black Family → Southern Trust

The larger financial relationship between Leon Black and the Epstein network is visible through **Exhibit A** of the Deutsche Bank-SDNY production. I identified 12 transfers from Black-affiliated entities into Southern Trust Company Inc.:

| Date | From | Amount (Unverified) | Source |
|------|------|------|--------|
| Oct 15, 2013 | Leon & Debra Black | $8,500,000 | Exhibit A |
| Dec 18, 2013 | Black Family Partners LP c/o Apollo | $10,000,000 | Exhibit A |
| Apr 25, 2014 | Leon & Debra Black | $5,000,000 | Exhibit A |
| Apr 25, 2014 | Black Family Partners LP c/o Apollo | $5,000,000 | Exhibit A |
| Apr 29, 2014 | Leon & Debra Black | $15,000,000 | Exhibit A |
| Oct 16, 2014 | Leon & Debra Black | $7,000,000 | Exhibit A |
| Oct 16, 2014 | Black Family Partners LP c/o Apollo | $13,000,000 | Exhibit A |
| Oct 22, 2014 | Leon & Debra Black c/o Apollo Mgmt | $2,000,000 | Exhibit A |
| Oct 22, 2014 | Black Family Partners LP c/o Apollo | $3,000,000 | Exhibit A |
| Oct 13, 2015 | Leon & Debra Black c/o Apollo Mgmt | $5,000,000 | Exhibit A |
| Oct 13, 2015 | Black Family Partners LP c/o Apollo | $5,000,000 | Exhibit A |
| Dec 18, 2015 | Black Family Partners LP | $10,000,000 | Exhibit A |
| Dec 30, 2015 | Leon & Debra Black c/o Apollo Mgmt | $10,000,000 | Exhibit A |
| Apr 25, 2017 | Leon & Debra Black c/o Apollo Mgmt | $8,000,000 | Exhibit A |

**Total Black-affiliated → Southern Trust: $106,500,000 (Unverified)**

Additional Black-related transfers through other channels bring the total visible Black-network activity to approximately $163 million (Unverified) across 34 ledger entries.

## Two Directions at Once

Money was flowing both ways:

**Inbound to Epstein network**: $106.5M from Black-affiliated entities → Southern Trust Company (2013-2017)

**Outbound from Epstein network**: $18M from Plan D LLC → Leon Black (2014-2017)

Look at the dates. April 25, 2014 — Leon & Debra Black send $5M to Southern Trust (Exhibit A). Same day, Plan D LLC sends $5M to Leon Black (Phase 25 recovery). October 22, 2014 — Black Family Partners sends $3M to Southern Trust (Exhibit A). Same day, Plan D LLC sends $3M and $2M to Leon Black.

I'm showing the data. I'm not interpreting the business purpose. But the same-day matching of amounts in opposite directions is right there in the records.

## Additional Black-Network Activity

Beyond Plan D LLC and Southern Trust, I found transfers involving Debra Black through other channels:

- ALEXANDERSON → Debra Black: $5,000,000 (Apr 25, 2014)
- JPMorgan → Debra Black: $3,200,000 and $2,900,000 (undated)
- HANNAN → Debra Black: $1,770,000 (undated)
- Southern Trust → Debra Black: $8,500,000 (Oct 15, 2013)
- HALPERIN → Leon Black: $3,200,000 (undated)

## What I Can't Determine

- **What Plan D LLC was.** I know its outflows. I don't know its corporate structure, registration, or stated purpose.
- **Where Plan D LLC's money came from.** The $18M it disbursed has no visible funding source within the EFTA corpus.
- **The business purpose of the Black → Southern Trust transfers.** These could be investment allocations, loan payments, advisory fees, or other arrangements.
- **The relationship between the inbound and outbound flows.** Same-day matching is a data observation. I'm not drawing a conclusion about intent.

---

*Source: DOJ EFTA Document Release, Deutsche Bank-SDNY Production, Exhibits A and C. All data extracted via automated pipeline. Supporting data: <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook (view-only)</a>. This finding appears in the [master wire ledger](../data/master_wire_ledger_phase5i.json) published with this repository.*

---

## Source Documents & Exhibits

### Primary Source
Expansion wires (Phase 14–24 extraction) — not from Deutsche Bank Exhibits A–E. These wires were extracted from broader EFTA corpus financial documents referencing Plan D LLC.

### Wire Ledger Cross-Reference
5 wires verified, $18,001,125 total. Exhibit designation: expansion (non-exhibit wires).

| Wire | Amount | Date |
|------|--------|------|
| PLAN D LLC → LEON_BLACK | $8,000,000 | undated |
| PLAN D LLC → LEON_BLACK | $5,000,000 | undated |
| PLAN D LLC → LEON_BLACK | $3,000,000 | undated |
| PLAN D LLC → LEON_BLACK | $2,000,000 | undated |
| REMITTANCE ADVICE → PLAN D LLC | $1,125 | undated |

### Corpus Statistics Source
**Method**: Entity co-occurrence analysis across files containing "Plan D" (entity_type = ORG).
**Database**: 1,476,377 files, 11.4M extracted entities (see [METHODOLOGY.md](../docs/METHODOLOGY.md)).

### External Corroboration
- Dechert LLP review (2021): Documented $30.5M BV70 LLC → Plan D "loan" for "art transaction"
- rhowardstone EFTA research: Confirmed Plan D as intermediary vehicle between BV70 and Leon Black personal accounts

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibit A — Southern Trust Company Capitalization (Leon Black transfers) |
| Full EFTA Corpus | DS1–12 | Expansion wires extracted from broader corpus financial documents referencing Plan D LLC |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse neighboring documents in Dataset 8 |

**All 12 DOJ Datasets:** <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">1</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-2-files" target="_blank">2</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-3-files" target="_blank">3</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-4-files" target="_blank">4</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-5-files" target="_blank">5</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-6-files" target="_blank">6</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-7-files" target="_blank">7</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">8</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">9</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-10-files" target="_blank">10</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">11</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-12-files" target="_blank">12</a>

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — Expansion wires (Plan D) | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Entity P&L — Plan D LLC | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1497389416#gid=1497389416" target="_blank">📊 Open Tab</a> |
| Shell Trust Hierarchy | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1943952132#gid=1943952132" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
