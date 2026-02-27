# Chain-Hop Anatomy

**How money moved through the 4-tier trust network — and how I caught $311 million in inflation from counting the same dollar twice.**

*All amounts are (Unverified) automated extractions from DOJ EFTA documents. Appearance in this analysis does not imply wrongdoing. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What I Found

The network ran on layers. Money came in from external sources — Leon Black, Benjamin de Rothschild, Tudor Futures Fund, Narrow Holdings, auction houses. It passed through intermediate shells — Haze Trust, Southern Trust, Southern Financial. Then it reached operational entities or personal accounts. I mapped 67 wire transfers totaling $312,796,381 (Unverified) moving through this structure.

The same structure that makes this worth studying makes it dangerous to count. A single $10 million wire that moves from an external source → Southern Trust → Southern Financial → Haze Trust → personal account is one $10 million transfer — but a naive extraction pipeline would count it as four separate $10 million transfers, inflating the total to $40 million. That's the chain-hop problem. It's the single biggest methodological challenge in this whole analysis.

## The 4-Tier Structure

Based on the flow patterns visible in the wire data:

**Tier 1 — Accumulation Layer**: Southern Trust Company Inc. received the largest inflows from external sources. 17 inbound wires totaling $151.5M (Unverified) from Black Family Partners, Leon & Debra Black, Narrow Holdings, Benjamin de Rothschild, Tudor Futures Fund, and Edmond de Rothschild (Suisse) SA.

**Tier 2 — Distribution Layer**: Southern Financial LLC received $32M (Unverified) from The Haze Trust and $14M from other sources. It also disbursed $4.1M across 9 outbound wires including payments to Joichi Ito, Coatue Enterprises, and Neoteny 3 LP.

**Tier 3 — Transit Layer**: The Haze Trust received art market proceeds and Deutsche Bank transfers, then moved money downstream to Southern Financial and Southern Trust. $49.7M out (Unverified), plus $3.7M to an entity classified as FINANCIAL_TRUST.

**Tier 4 — Operational Layer**: Entities like Butterfly Trust, Gratitude America, and personal accounts that received disbursements from the upper tiers.

## The Chain-Hop Problem

In Phase 22 of the extraction pipeline, I identified and removed $311 million in chain-hop inflation. Here is a simplified example of what that looks like:

```
External Source sends $10,000,000 → Southern Trust
Southern Trust sends $10,000,000 → Southern Financial  
Southern Financial sends $10,000,000 → Haze Trust
```

If I count every row, I get $30 million. But only $10 million actually entered the network. The other $20 million is the same dollar being moved between internal accounts.

I solved this by classifying every entity as EPSTEIN_ENTITY, EXTERNAL_PARTY, or BANK/CUSTODIAN, then filtering for transfers that crossed the boundary between external and internal. Shell-to-shell transfers (43 identified in the master ledger) are tracked separately and flagged with `is_shell_to_shell` — they are visible in the data but not double-counted in the headline total.

## Key Flow Paths

**The Black → Southern Trust → Disbursement path:**
$106.5M entered Southern Trust from Black-affiliated entities (Exhibit A). Southern Trust then disbursed to ITO ($10.3M across 5 wires), Leon Black ($8M), Debra Black ($8.5M), and others.

**The Auction → Haze Trust → Southern Financial path:**
$18.9M entered Haze Trust from Sotheby's and Christie's (Exhibit D). Haze Trust then sent $49.7M to Southern Financial and Southern Trust — meaning the Haze Trust also received funding from sources beyond the auction houses (primarily Deutsche Bank transfers).

**The Rothschild → Southern Trust path:**
Benjamin Edmond de Rothschild sent $15M (Exhibit A), and Edmond de Rothschild (Suisse) SA sent $10M (Exhibit A), both to Southern Trust Company.

**The Narrow Holdings path:**
Narrow Holdings LLC c/o Elysium Management sent $20M to Southern Trust (Exhibit A) — the single largest individual wire in this subset.

## Matching-Amount Detection

One method I used to identify potential chain-hops was looking for identical dollar amounts appearing across multiple entity pairs within the shell network. If $5,000,000 appears as Southern Trust → Southern Financial and also as Haze Trust → Southern Financial, it may be the same $5M moving through the network.

I did not automatically remove these matches. Each was reviewed in the context of dates (when available), source documents, and entity classifications before determining whether it was a legitimate separate transfer or a chain-hop duplicate.

## What I Can't Determine

- **Complete flow paths end-to-end.** I can see individual wire segments. But the EFTA corpus doesn't always give me enough date precision to chain segment A → B → C → D into one traced path.
- **Whether all shell-to-shell transfers are internal movements.** Some may be genuine transactions between related-but-distinct legal entities.
- **The net economic reality.** Wires show gross flows. Offsetting positions, returns of capital, and loan repayments would shrink the net — but they look the same as one-way transfers in wire data.

---

*Source: DOJ EFTA Document Release, Deutsche Bank-SDNY Production, Exhibits A and D. Chain-hop removal methodology documented in [METHODOLOGY.md](../docs/METHODOLOGY.md), Phase 22. Entity classifications and shell-to-shell flags are included in the [master wire ledger](../data/master_wire_ledger_phase5i.json).*

---

## Source Documents & Exhibits

### Primary Exhibits
**All Exhibits A–E** (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>) plus expansion wires.

This narrative synthesizes the full 481-wire ledger to demonstrate inter-entity fund routing patterns.

| Exhibit | Wires | Total Value | Primary Entities |
|---------|-------|-------------|-----------------|
| A | 17 | $151,499,980 | Black entities → Southern Trust |
| B | 18 | $33,139,248 | Southern Financial ↔ investment funds |
| C | 64 | $89,372,037 | Jeepers → Epstein personal accounts |
| D | 11 | $68,760,686 | Haze Trust / art proceeds → Southern Financial |
| E | 12 | $6,253,493 | Gratitude America disbursements |
| Expansion | 260 | $208,927,537 | Multi-entity, multi-bank |

### Corpus Statistics Source
**Method**: Entity co-occurrence + wire pathway analysis across all shell entities.
**Database**: 1,476,377 files, 11.4M extracted entities (see [METHODOLOGY.md](../docs/METHODOLOGY.md)).

### Scope Note
The 4-tier model (intake → holding → distribution → personal) describes patterns visible in one bank's production. The full architecture includes Financial Trust Company (Bear Stearns), Outgoing Money Trust (7 banks), and other entities documented in N11–N13.

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibits A–E (all 5 exhibits, 481 wires, $973M) |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | Browse neighboring documents in Dataset 8 |

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — All Exhibits | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Money Flow Patterns | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2075093083#gid=2075093083" target="_blank">📊 Open Tab</a> |
| Shell Trust Hierarchy | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1943952132#gid=1943952132" target="_blank">📊 Open Tab</a> |
| Above-Cap Verified | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2071460294#gid=2071460294" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Wire data from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> Exhibits A–E. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
