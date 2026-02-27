# The Infrastructure of Access

**The people who moved the money are the same people victims named.**

*This analysis documents entity co-occurrence across 1.48 million DOJ EFTA files. It does not reproduce victim testimony, identify survivors, or attribute guilt. All findings are automated extractions. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What I Found

I searched 11.4 million entity records across 1.48 million DOJ documents for people who show up in three categories: financial records, victim-related documents, and travel records.

Ten names tested. Every single one appeared in victim-related documents. Several appeared in all three categories at once. The financial infrastructure and the abuse infrastructure were not separate systems. They shared personnel.

## The Data

I counted unique files per name, filtered by document type. Entities table (11.4 million rows) joined against files (1.48 million rows).

**Document categories:**
- **Financial**: doc_type = financial, spreadsheet, bank_statement; or summary contains wire, payment, account, check, invoice
- **Victim-related**: doc_type = police_report, court_filing; or summary contains victim, abuse, minor, massage, trafficking, Jane Doe
- **Travel**: doc_type = flight_log

## The Table

| Name | Role (Public Record) | Financial Docs | Victim Docs | Flight Docs | Total Corpus Files |
|------|---------------------|---------------|-------------|-------------|-------------------|
| **Ghislaine Maxwell** | Co-conspirator (convicted) | **204** | **1,312** | **53** | 6,145 |
| **Darren Indyke** | Estate attorney | **196** | **204** | **176** | 8,381 |
| **Lesley Groff** | Executive assistant | **134** | **153** | **20** | 73,144 |
| **Sarah Kellen** | Assistant / scheduler | 5 | **132** | 4 | 247 |
| **Alfredo Rodriguez** | Household staff (testified) | 6 | **128** | 1 | 253 |
| **Jean-Luc Brunel** | MC2 modeling agency | 14 | **120** | 4 | 1,896 |
| **Larry Visoski** | Pilot | **99** | 76 | **249** | 11,035 |
| **Juan Alessi** | Household staff (testified) | 0 | **61** | 2 | 125 |
| **Nadia Marcinkova** | Named by victims | 0 | **35** | 0 | 66 |
| **George Nader** | Convicted (child exploitation) | 11 | 11 | 0 | 68 |

## What the Names Show

**Ghislaine Maxwell** appears in 204 financial documents and 1,312 victim-related documents. She is the only person in this analysis who occupies the center of all three document universes at scale — financial (204), victim (1,312), and travel (53). She was convicted in 2021 on five federal charges including sex trafficking of a minor.

**Darren K. Indyke** appears in 196 financial documents, 204 victim-related documents, and 176 flight documents. He is the estate attorney who signed wire transfers on behalf of Epstein's trust entities. He appears on 5 verified wire transfers in the master ledger totaling $7.6 million. His name appears in victim-related documents because he is named in civil proceedings filed by Jane Doe plaintiffs against the Epstein estate — proceedings in which Southern Trust Company, which received $151.5 million in wire transfers (Exhibit A), is a named defendant.

**Lesley Groff** appears in 134 financial documents and 153 victim-related documents. She was Epstein's executive assistant who managed scheduling. Documents in the EFTA corpus place her name alongside victim references including "Jane Doe" (<a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00446172.pdf" target="_blank">EFTA00446172</a>), "Victim Payouts" (<a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00371439.pdf" target="_blank">EFTA00371439</a>), and "the Federal Crime Victims Rights Act" (<a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00429909.pdf" target="_blank">EFTA00429909</a>).

**Sarah Kellen** appears in 132 victim-related documents. Victims identified her as a scheduler who arranged their visits. Her financial footprint is small (5 documents), consistent with an operational role rather than a financial one.

**Larry Visoski** appears in 249 flight documents and 99 financial documents. He was Epstein's primary pilot. His victim-document presence (76 files) reflects his naming in depositions and legal proceedings where victims described travel to Epstein properties.

## The Co-Occurrence Documents

When a single document contains BOTH an operational name AND victim/trafficking language, that is a co-occurrence. These are not separate references in separate files — they are the same document discussing the same subject.

Selected examples from 50 co-occurrence documents identified:

| Document | Type | Operational Names | Victim References |
|----------|------|-------------------|-------------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00023049.pdf" target="_blank">EFTA00023049</a> | document | Maxwell | Minor, Minor Victim-3 |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00065479.pdf" target="_blank">EFTA00065479</a> | email | Ghislaine Maxwell, Groff | Trafficking Victims Protection Act |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00073465.pdf" target="_blank">EFTA00073465</a> | court filing | Ghislaine Maxwell | Crime Victims' Rights Act, Victim Notification System |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00173201.pdf" target="_blank">EFTA00173201</a> | document | Leslie Groff, Ghislaine Maxwell | Jeffrey Epstein-Victim, Sex Trafficking |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00371439.pdf" target="_blank">EFTA00371439</a> | email | Groff | Victim Payouts |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00429909.pdf" target="_blank">EFTA00429909</a> | email | Lesley Groff | Federal Crime Victims Rights Act |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00446172.pdf" target="_blank">EFTA00446172</a> | email | Lesley Groff | Jane Doe |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00067267.pdf" target="_blank">EFTA00067267</a> | subpoena | Sarah Kellen | Victim |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00261508.pdf" target="_blank">EFTA00261508</a> | document | Maxwell | VICTIM |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00313632.pdf" target="_blank">EFTA00313632</a> | court filing | Ghislaine Maxwell | Plaintiff Jane Doe |

These documents span the investigative lifecycle: FBI emails referencing "Crimes Against Children/Human Trafficking" alongside Maxwell's name, court filings where Jane Doe plaintiffs name operational staff, and victim impact statements that reference the same individuals who appear on financial records.

## The Financial Thread

The operational staff did not merely appear alongside victim references in legal proceedings. Several of them are directly connected to the wire transfer infrastructure documented in the [master wire ledger](../data/master_wire_ledger_phase5i.json):

**Darren Indyke** — Named on 5 verified wire transfers:
- Received $5.8 million from Deutsche Bank (5 wires, Exhibit C)
- Co-signed $1.2 million in transfers with Michelle Saipher to Epstein's NOW/SuperNow account
- Named as estate attorney on Southern Trust Company — the entity that received $151.5 million (Exhibit A)

**Ghislaine Maxwell** — NES LLC, an entity linked to Maxwell, received $554,000 through the shell network (Narrative 4: Chain-Hop Anatomy). Maxwell appears in 204 financial documents spanning bank records, trust administration, and property transactions.

**Lesley Groff** — Appears in 134 financial documents. While not directly on wire transfers, her presence in financial records alongside her 153 victim-document appearances places her at the intersection of the money and the harm.

**Richard Kahn** — The attorney appears in 110 financial documents and 28 flight documents. He received $9.3 million through the wire transfer network for disbursement to third parties including Paul Morris.

## The Three-Circle Pattern

The EFTA corpus is not one collection of documents. It is at minimum three overlapping collections:

1. **Financial records**: Bank statements, wire confirmations, trust documents, account records
2. **Victim records**: Police reports, court filings, FBI investigations, victim impact statements, Jane Doe lawsuits
3. **Travel records**: Flight logs, itineraries, APIS passenger manifests, aircraft purchase agreements

Most people in the corpus appear in one circle. Victims appear in victim records. Bankers appear in financial records. Pilots appear in travel records.

The operational staff — Maxwell, Indyke, Groff, Kellen, Visoski — appear in all three. They are the connective tissue. The same names managing the money appear in the documents where victims describe what happened to them.

This is not a finding about guilt. It is a finding about structure. The financial infrastructure documented in Narratives 1–7 was not a separate system from the abuse infrastructure documented in victim testimony. They shared the same people.

## What I Can't Determine

- **Whether any specific wire transfer funded any specific act of abuse.** The temporal and personnel overlap is documented. The causal chain is not.
- **What victims experienced.** This analysis does not access, reproduce, or summarize victim testimony. It measures entity co-occurrence at the document level only.
- **Whether operational staff knew the purpose of the financial transfers they facilitated.** Indyke signing a wire transfer is a legal act. Whether he knew where the money ultimately went is a question for investigators, not forensic accountants.
- **Whether all co-occurrences are meaningful.** Maxwell appearing in a court filing alongside "Jane Doe" may reflect a lawsuit naming both — it does not necessarily mean a direct interaction. The co-occurrence is structural, not necessarily evidentiary.
- **The full scope of the operational network.** This analysis tested 10 names. The EFTA corpus contains 734,122 unique persons. The operational network may be larger than what is measured here.

---

*Source: DOJ EFTA Document Release — 11.4 million entity records across 1.48 million files. Entity co-occurrence measured by unique file count per document category. Wire transfer data from Deutsche Bank-SDNY Production (Exhibits A–E), 185 verified wires. Document type classifications from automated pipeline with manual validation. Supporting data: <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook (view-only)</a>. This analysis is published as part of the <a href="https://github.com/randallscott25-star/epstein-forensic-finance#readme" target="_blank">Epstein Financial Forensics</a> repository.*

*For the girls.*

---

## Source Documents & Exhibits

### Primary Source
Corpus-wide entity co-occurrence analysis — not limited to any single exhibit.

### Corpus Statistics Source
**Method**: Person × document co-occurrence analysis identifying 10 operational staff members who appear across multiple document types and shell entities.
**Database**: 1,476,377 files, 11.4M extracted entities, 734,122 unique persons (see [METHODOLOGY.md](../docs/METHODOLOGY.md)).
**Finding**: 50 co-occurrence documents linking operational staff to shell network.

### Scope Note
This narrative draws from the full EFTA corpus, not limited to Deutsche Bank wire production. Staff identification based on cross-document-type presence (email + financial + court filing + fax).

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00023049.pdf" target="_blank">EFTA00023049</a> | DS8 | Maxwell — Minor, Minor Victim-3 document |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00065479.pdf" target="_blank">EFTA00065479</a> | DS9 | Maxwell/Groff email — Trafficking Victims Protection Act |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00073465.pdf" target="_blank">EFTA00073465</a> | DS9 | Maxwell court filing — Crime Victims' Rights Act |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00173201.pdf" target="_blank">EFTA00173201</a> | DS9 | Groff/Maxwell — Jeffrey Epstein-Victim, Sex Trafficking |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00371439.pdf" target="_blank">EFTA00371439</a> | DS9 | Groff email — Victim Payouts |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00429909.pdf" target="_blank">EFTA00429909</a> | DS9 | Lesley Groff — Federal Crime Victims Rights Act |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00446172.pdf" target="_blank">EFTA00446172</a> | DS9 | Lesley Groff — Jane Doe reference |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00067267.pdf" target="_blank">EFTA00067267</a> | DS9 | Sarah Kellen subpoena — Victim |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00261508.pdf" target="_blank">EFTA00261508</a> | DS9 | Maxwell document — VICTIM |
| <a href="https://www.justice.gov/epstein/files/DataSet%209/EFTA00313632.pdf" target="_blank">EFTA00313632</a> | DS9 | Maxwell court filing — Plaintiff Jane Doe |
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibits A–E (185 verified wires for staff cross-reference) |
| Full EFTA Corpus | DS1–12 | 11.4M entity records across 1,476,377 files — person × document co-occurrence |

**All 12 DOJ Datasets:** <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">1</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-2-files" target="_blank">2</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-3-files" target="_blank">3</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-4-files" target="_blank">4</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-5-files" target="_blank">5</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-6-files" target="_blank">6</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-7-files" target="_blank">7</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">8</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">9</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-10-files" target="_blank">10</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">11</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-12-files" target="_blank">12</a>

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Shell Network — Staff co-occurrence | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1040516313#gid=1040516313" target="_blank">📊 Open Tab</a> |
| Shell Trust Hierarchy | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1943952132#gid=1943952132" target="_blank">📊 Open Tab</a> |
| Executive Summary | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1804001356#gid=1804001356" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
