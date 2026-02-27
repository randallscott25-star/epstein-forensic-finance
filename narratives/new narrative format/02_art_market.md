# Art Market as Liquidity Channel

**$18.9 million in auction proceeds entered the trust network through a single account — then dispersed across the shell structure.**

*All amounts are (Unverified) automated extractions from DOJ EFTA documents. Appearance in this analysis does not imply wrongdoing. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What I Found

The Haze Trust collected art market proceeds and redistributed them through the shell network. I pulled $18,974,417 (Unverified) in auction house proceeds flowing into The Haze Trust from Sotheby's and Christie's, followed by $49,727,941 (Unverified) in outflows to Southern Financial LLC and Southern Trust Company — the downstream shells.

It's on **Exhibit D** of the Deutsche Bank-SDNY production.

## The Auction Houses

Two transactions brought art market proceeds into the Haze Trust:

| Date | From | Amount (Unverified) | Source |
|------|------|------|--------|
| Jun 19, 2017 | Christie's Inc. | $7,725,000 | Exhibit D |
| Oct 24, 2017 | Sotheby's | $11,249,417 | Exhibit D |

**Total auction inflows: $18,974,417 (Unverified)**

Both went straight into the Haze Trust checking account at Deutsche Bank. June and October 2017 — spring and fall auction seasons.

## Where It Went Next

Once inside the Haze Trust, the money moved downstream. I found 8 outbound transfers:

| Date | To | Amount (Unverified) | Source |
|------|------|------|--------|
| Jun 22, 2018 | Southern Financial LLC (Checking) | $9,000,000 | Exhibit D |
| Aug 20, 2018 | Southern Financial LLC (Checking) | $5,000,000 | Exhibit D |
| Sep 17, 2018 | Southern Financial LLC (DBAGNY) | $5,000,000 | Exhibit D |
| Sep 28, 2018 | Southern Financial LLC (Checking) | $8,000,000 | Exhibit D |
| Oct 1, 2018 | Southern Trust Company Inc. (Checking) | $10,000,000 | Exhibit D |
| Oct 24, 2018 | Southern Financial LLC (Checking) | $5,000,000 | Exhibit D |
| Dec 19, 2018 | Southern Financial LLC (Checking) | $5,000,000 | Exhibit D |
| Jan 10, 2019 | The Haze Trust (DBAGNY → Checking) | $2,727,941 | Exhibit D |

**Total outflows to Southern entities: $49,727,941 (Unverified)**

## Other Money Coming In

Beyond the auction houses, the Haze Trust also got transfers from Deutsche Bank feeding the same outflow pattern:

| Date | Amount (Unverified) | Source |
|------|------|--------|
| Jul 16, 2014 | $2,500,000 | Phase 25 recovery |
| Aug 20, 2018 | $5,000,000 | Phase 25 recovery |
| Sep 28, 2018 | $8,000,000 | Phase 25 recovery |
| Dec 13, 2018 | $58,328 | Phase 25 recovery |
| Jan 10, 2019 | $6,000,000 | Phase 25 recovery |
| Jan 10, 2019 | $2,727,941 | Phase 25 recovery |
| Feb 19, 2019 | $7,000,000 | Phase 25 recovery |

An additional $58,328 arrived from HSBC Bank Bermuda Limited on December 13, 2018 (Exhibit D) — the only non-Deutsche Bank source feeding the Haze Trust.

## What It Means

The Haze Trust was a way-station. Art money came in through a legitimate-looking channel — major auction houses with their own compliance departments — and moved straight into the same Southern Trust / Southern Financial network that received money from every other source in the Epstein financial structure.

Look at the timing. Auction proceeds arrived mid-to-late 2017. Outflows to Southern entities didn't start until June 2018. The money sat in the Haze Trust for 8–12 months before moving.

The outflow amounts — $5M, $8M, $9M, $10M — are all round numbers. That's not someone liquidating specific positions. That's someone giving instructions.

## What I Can't Determine

- **What art was sold.** The wire transfers identify amounts and auction houses but not specific lots, artists, or buyers.
- **Whether the art was legitimately acquired.** Provenance of the art itself is outside the scope of financial wire extraction.
- **Where the money went after Southern Financial / Southern Trust.** The downstream disbursements from these entities are tracked separately in the chain-hop analysis.
- **The $3,738,700 outflow to FINANCIAL_TRUST.** One additional Haze Trust outflow went to an entity classified as FINANCIAL_TRUST. I have limited context on this entity.

---

*Source: DOJ EFTA Document Release, Deutsche Bank-SDNY Production, Exhibit D. All data extracted via automated pipeline. Supporting data: <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook (view-only)</a>. This finding appears in the [master wire ledger](../data/master_wire_ledger_phase5i.json) published with this repository.*

---

## Source Documents & Exhibits

### Primary Exhibit
**Exhibit D** (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>): Haze Trust activity at Deutsche Bank, including art auction proceeds.

### Wire Ledger Cross-Reference
11 wires verified, $68,760,686 total. All from Exhibit D.

| Wire | Amount | Date |
|------|--------|------|
| Christie's Inc. → The Haze Trust (Checking) | $7,725,000 | 2017-06-19 |
| Sotheby's → The Haze Trust (Checking) | $11,249,417 | 2017-10-24 |
| The Haze Trust (DBAGNY) → Southern Financial LLC (Checking) | $9,000,000 | 2018-06-22 |
| HSBC Bank Bermuda Limited → The Haze Trust (Checking) | $58,328 | 2018-08-20 |
| The Haze Trust (DBAGNY) → Southern Financial LLC (Checking) | $5,000,000 | 2018-08-20 |
| *(6 additional wires — see Master Wire Ledger, Exhibit D)* | | |

### Corpus Statistics Source
**Method**: Entity co-occurrence analysis across files containing "Haze Trust" and auction house entity variants.
**Database**: 1,476,377 files, 11.4M extracted entities (see [METHODOLOGY.md](../docs/METHODOLOGY.md)).

### Scope Note
Haze Trust also co-occurs with Financial Trust Company (19 shared files), which banked at Bear Stearns. The HSBC Bermuda wire ($58,328) confirms an offshore banking relationship beyond Deutsche Bank. See N11 for full multi-bank context.

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibit D — Art Market Proceeds (Sotheby's, Christie's → Haze Trust) |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse neighboring documents in Dataset 8 |

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — Exhibit D (Haze Trust wires) | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Shell Network — Haze Trust co-occurrence | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1040516313#gid=1040516313" target="_blank">📊 Open Tab</a> |
| Entity P&L — Haze Trust | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1497389416#gid=1497389416" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Wire data from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> Exhibit D. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
