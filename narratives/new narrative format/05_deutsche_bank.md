# Deutsche Bank's Role

**38 wires. $56.8 million. Every major Epstein entity touched Deutsche Bank accounts. Custodian or conduit?**

*All amounts are (Unverified) automated extractions from DOJ EFTA documents. Appearance in this analysis does not imply wrongdoing. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What I Found

Deutsche Bank shows up in more wire transfers than any other bank in the master ledger. I pulled 38 wires totaling $56,792,936 (Unverified) where Deutsche Bank was on one end or the other. These wires touched every major entity in the Epstein financial network: Haze Trust, Southern Trust, Butterfly Trust, Southern Financial, Gratitude America, and personal intermediaries including Darren Indyke (Epstein's attorney).

Deutsche Bank's Epstein relationship is public record — they paid $150 million to the New York State DFS in 2020. I'm not replicating that finding. What I'm adding is a wire-level map of where the money actually went.

## Outflows by Recipient

| Recipient | Wires | Total (Unverified) |
|-----------|-------|------|
| Haze Trust | 8 | $31,287,087 |
| Southern Trust | 2 | $8,896,579 |
| Butterfly Trust | 4 | $6,350,000 |
| Darren Indyke | 5 | $5,798,525 |
| Gratitude America | 4 | $877,025 |
| Southern Financial | 2 | $309,101 |
| JPMorgan | 2 | $276,400 |
| Tazia Smith | 2 | $273,000 |
| Bank of America | 3 | $272,622 |
| BNY Mellon | 1 | $170,031 |
| Jeffrey (personal) | 1 | $140,400 |
| Citibank | 1 | $100,000 |
| Shuliak | 2 | $42,166 |

**Total outflows: $54,792,936 (Unverified) across 37 wires**

One inflow: Southern Trust → Deutsche Bank, $2,000,000 (undated).

## Chronological Pattern

The dated wires span from October 2012 to February 2019:

**2012-2013 (early period):** Small transfers — $30K and $20K to Butterfly Trust, $20K to Shuliak, $200K to Gratitude America. Plus two large transfers to Indyke: $3M (Oct 2013) and $2M (Nov 2013).

**2014 (peak activity):** $698K and $525 to Indyke (May 2014), $100K to Indyke and $100K to Citibank (Nov 2014), $2.5M to Haze Trust (Jul 2014), $7.5K to Bank of America (Jan 2014).

**2016:** $500K to Gratitude America (Jul 2016).

**2018-2019 (late period — largest transfers):** The heaviest activity occurred in the final 6 months before Epstein's arrest. Between August 2018 and February 2019: $5M, $8M, $8M, $58K to Haze Trust. $6M, $6M, $7M, $2.7M also to Haze Trust. $8M to Southern Trust. $300K to Butterfly Trust.

**That concentration at the end is hard to ignore.** Over 75% of Deutsche Bank's outflow volume occurred in the last 6 months of the relationship.

## The Indyke Connection

Five wires totaling $5,798,525 (Unverified) went from Deutsche Bank to entities associated with Darren Indyke, Epstein's long-time attorney:

| Date | Amount (Unverified) |
|------|------|
| Oct 11, 2013 | $3,000,000 |
| Nov 13, 2013 | $2,000,000 |
| May 16, 2014 | $698,000 |
| Nov 17, 2014 | $100,000 |
| May 21, 2014 | $525 |

The $3M and $2M transfers are the largest non-trust disbursements from Deutsche Bank in the dataset. The $525 wire is the smallest transfer in the entire master ledger involving Deutsche Bank.

## Custodian or Conduit?

Was Deutsche Bank just holding and transferring assets at the client's direction? Or was it actively moving money through the shell network?

The data can't answer that. Here's what it does show:

- Deutsche Bank accounts held assets for Haze Trust, Butterfly Trust, Southern Trust, Southern Financial, Jeepers Inc., and Epstein's personal accounts
- Transfers between these entities frequently moved through Deutsche Bank
- The bank's compliance function either approved or failed to flag these transfers
- The concentration of large transfers in 2018-2019 occurred while Epstein was under heightened scrutiny

The 2020 DFS settlement confirms regulatory findings that Deutsche Bank's compliance failures were substantive, not merely procedural.

## What I Can't Determine

- **Whether Deutsche Bank personnel knew what these transfers were for.** Wire instructions typically carry limited beneficiary info.
- **What triggered the late-period surge.** The 2018-2019 concentration could reflect changed investment strategy, asset repositioning, or other factors not visible in the wire data.
- **Deutsche Bank's complete relationship with Epstein.** I am seeing wires that survived into the EFTA corpus. The bank's internal records, which would show the full scope of the relationship, are not part of the public release.

---

*Source: DOJ EFTA Document Release, Deutsche Bank-SDNY Production, Exhibits C, D, and E. All data extracted via automated pipeline. Supporting data: <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook (view-only)</a>. This finding appears in the [master wire ledger](../data/master_wire_ledger_phase5i.json) published with this repository.*

---

## Source Documents & Exhibits

### Primary Exhibits
**Exhibits C, D, E** (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>) plus expansion wires referencing Deutsche Bank.

74 wires verified involving Deutsche Bank accounts, across:

| Exhibit | Wires | Total Value |
|---------|-------|-------------|
| C | 24 | $57,876,640 |
| D | 9 | $49,786,269 |
| E | 4 | $5,800,000 |
| Expansion | 37 | $54,792,936 |

### Corpus Statistics Source
**Method**: Entity co-occurrence analysis for "Deutsche Bank" across all document types.
**Database**: Deutsche Bank appears in 1,564 financial files with 415,287 money-entity mentions.
**Context**: Bear Stearns has 2,381,211 money mentions (5.7× more). Deutsche Bank is the source of the wire production, not necessarily the highest-volume bank in the network. See N12.

### External Corroboration
- NYDFS consent order (2020): Deutsche Bank fined $150M for BSA/AML failures
- SDNY production: Exhibits A–E from Deutsche Bank compliance records

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibits C, D, E — 38 Deutsche Bank wires |
| <a href="https://www.dfs.ny.gov/reports_and_publications/press_releases/pr202007061" target="_blank">NYDFS Consent Order (2020)</a> | External | NYDFS $150M consent order re: Deutsche Bank Epstein accounts |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse neighboring documents in Dataset 8 |

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — Deutsche Bank wires | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Shell Network — Deutsche Bank co-occurrence | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1040516313#gid=1040516313" target="_blank">📊 Open Tab</a> |
| SAR Comparison | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1121979938#gid=1121979938" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Wire data from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
