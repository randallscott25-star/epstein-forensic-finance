# Source Documents & Exhibits — Standard Template (v2)

## Purpose

Every data narrative published in this repository must include a **Source Documents & Exhibits** appendix section at the end of the document. This section ties every analytical claim back to verifiable source material in the public DOJ release, with direct links to the supporting workbook tabs.

## Required Components

### 1. Primary Exhibit Mapping

Identify which exhibits from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> (Deutsche Bank Wire Production) feed the narrative:

| Exhibit | Description | Wires in Narrative | Value |
|---------|-------------|-------------------|-------|
| A | Incoming wires to Southern Trust Company | — | — |
| B | Southern Financial LLC activity | — | — |
| C | Jeepers Inc. / Epstein personal accounts | — | — |
| D | Haze Trust / art market proceeds | — | — |
| E | Gratitude America disbursements | — | — |

### 2. Key EFTA Document References

Cite the specific EFTA file IDs that anchor the critical claims. Format:

> **Claim**: [specific factual claim from the narrative]
> **Source**: EFTA[document ID] — [brief description of what the document contains]

Not every claim needs a citation — focus on the **anchor documents** that a journalist or researcher would want to verify first.

### 3. Corpus Statistics Source

For claims derived from database co-occurrence analysis, entity counts, or money-mention volumes, cite:

> **Method**: Co-occurrence analysis across [X] files in the EFTA corpus containing entity "[Entity Name]"
> **Database**: 1,476,377 files, 11.4M extracted entities, 19 datasets (see METHODOLOGY.md)
> **Query pattern**: [brief description of the analytical method]

### 4. Wire Ledger Cross-Reference

For claims involving specific dollar amounts from verified wire transfers:

> **Wire**: [Entity From] → [Entity To], $[Amount], [Date]
> **Ledger row**: Master Wire Ledger, Exhibit [X], Row [N]
> **Verification**: Compare against <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> Exhibit [X] at efts.gov

### 5. External Corroboration (where applicable)

For claims validated against external reporting:

> **External**: [Source name and date] — [brief description]
> **Note**: External sources cited for corroboration only; all primary data derived from EFTA corpus

### 6. 📊 Verify in Forensic Workbook (REQUIRED)

Deep-linked table pointing readers directly to the relevant workbook tabs. Use this format:

```markdown
### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| [Description of what to check] | [📊 Open Tab](DEEP_LINK_URL) |
```

**Workbook base URL**: `https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=`

**Available tabs and GIDs:**

| Tab Name | GID | Use For |
|----------|-----|---------|
| Executive Summary | 1804001356 | High-level overview, tier framework |
| Extraction Phases | 308915370 | Phase-by-phase extraction history |
| Money Flow Patterns | 2075093083 | Inter-entity fund routing |
| Shell Trust Hierarchy | 1943952132 | Shell entity structure and relationships |
| Master Wire Ledger | 2043824625 | All 481 verified wires by exhibit |
| Above-Cap Verified | 2071460294 | Court-verified wires above dedup cap |
| Date Recovery | 339305346 | Phase 23 date recovery results |
| Entity P&L | 1497389416 | Entity-level profit/loss analysis |
| Shell Network | 1040516313 | Shell entity co-occurrence matrix |
| SAR Comparison | 1121979938 | FinCEN SAR benchmark comparison |
| Methodology | 1840632994 | Full extraction methodology |

**Rules for selecting tabs:**
- ALWAYS include **Methodology** tab
- Include **Master Wire Ledger** if narrative references specific wire amounts
- Include **Shell Network** if narrative references entity co-occurrence
- Include **Entity P&L** if narrative profiles a specific entity
- Include **Executive Summary** for corpus-wide narratives
- Include all tabs whose data supports a key claim in the narrative

### 7. Verification Instructions

Standard footer for every narrative:

---

### How to Verify
All EFTA document IDs cited above are drawn from the public DOJ release under the Epstein Files Transparency Act. Documents can be accessed at <a href="https://efts.gov" target="_blank">efts.gov</a> by searching the document ID (e.g., <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>). Wire transfer data is from Exhibit attachments to <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> (Deutsche Bank production, SDNY). Full extraction methodology is documented in [METHODOLOGY.md](METHODOLOGY.md).

---

## Reporting Standard

Effective with this template (v2), every published narrative includes:
1. Source appendix section with exhibit mapping, corpus statistics, and external corroboration
2. Deep-linked workbook verification table (📊 Verify in Forensic Workbook)
3. Standard verification footer

Narratives 1–11 retroactively updated. All future narratives (N17+) must include this appendix before publication.
