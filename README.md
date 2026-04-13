
# Epstein Financial Forensics

**Forensic financial reconstruction from 1,476,437 unique DOJ EFTA document files (2.87 million pages) + 503K cataloged media items**

*Last validated: April 12, 2026*

![Visitors](https://komarev.com/ghpvc/?username=randallscott25-star&label=visitors&color=555555&style=flat)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

# Questions Related to the Project
    theproject@isipp.com

---

## The Projects — the-projects.org

**Website:** https://the-projects.org  
**Research Terminal:** https://cloud-efp.com — credentialed access  
**Request Access:** https://cloud-efp.com/register  
**Contact:** theproject@isipp.com

---

> **ℹ️ Notice to Media, Researchers & Repository Forks**
> 
> This repository is a published output of an active forensic investigation. The underlying database is under continuous review — records are re-validated against primary bank documents, entities are reclassified as new source material is processed, and figures are corrected when the data demands it. What you are reading reflects the state of the analysis as of **April 12, 2026**.
>
> If you are forking, archiving, or citing this work: snapshots capture a moment in time. Do not treat cached versions as authoritative. Always reference the live repository for current figures. Last validated: **April 12, 2026**.

---

## What This Is

We took 1,476,437 documents (2.87 million pages) the DOJ released under the Epstein Files Transparency Act and built a forensic financial database from scratch. Wrote all the extraction code. Designed the schema. Built the classification pipeline. Ran the analysis. Team project, start to finish. AI tools helped us write code faster — same way you'd use a calculator. The analytical calls are ours.

Our team background spans multi-affiliate financial reconciliation, budget variance analysis, automated exception reporting at institutional scale, forensic financial analysis, and legal review. We applied those same methods here.

As far as we can tell, nobody else has tried to reconstruct the complete financial infrastructure in the EFTA corpus using quantitative forensic methods. Plenty of good narrative work out there. Plenty of search engines. This is the first attempt to model the full network — fund flows, entity relationships, shell trust hierarchies — at scale.

For the girls.

---

## 📌 Start Here


> **2 data narratives** reconstruct how $2.146 billion moved through 14 shell entities across 8+ banking institutions. All figures reflect the deduplication-verified publication ledger (6,767 unique records as of March 11, 2026). Every claim is anchored to specific court exhibits and bates stamps.
>
> **→ [Read the Data Narratives](narratives/)** · **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/narratives/20_the_verification_wall.html" target="_blank">The Verification Wall (N20)</a>** · **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/narratives/19_grand_opus_narrative.html" target="_blank">Blueprint of a Financial Machine (N19)</a>** · **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/shell_network.html" target="_blank">Explore the Interactive Network</a>** · **<a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">View the Forensic Workbook</a>**

| # | Narrative | Key Finding |
|---|-----------|-------------|
| **19** | **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/narratives/19_grand_opus_narrative.html" target="_blank">Blueprint of a Financial Machine</a>** | **$2.378B across 6,310 unique transactions. 123 nodes, 313 edges. Every bank, shell, operator, and key person mapped. <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/19_blueprint_financial_machine.html" target="_blank">Visualization</a>** |
| **20** | **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/narratives/20_the_verification_wall.html" target="_blank">The Verification Wall</a>** | ** Every document has a Bates number — the wall tests what's behind it. 8 noise POIs ($144.4M, $0 bank docs) vs. Leon Black ($310.5M, 42 verified wires, 15 bank docs). NLP phantom autopsy with clickable EFTA source documents.** |



## The Database

**8.64 GB | 49 tables | 26.7 million rows | 19 datasets**

| Metric | This Project | Largest Narrative Repo | Largest Search Platform | Others |
|--------|:------------:|:----------------------:|:----------------------:|:------:|
| **Total files indexed** | **1,476,437** + 503K media | 1,380,937 | 1,120,000 | < 20,000 |
| **Datasets covered** | **19** (<a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">DS1</a>-12 + DS98-104) | 12 | 12 | 1-3 |
| **Extracted text records** | **2.87M** (page-level) | 993,406 pages | — | — |
| **Entity extraction (NLP)** | **11.4M entities** | ~4,000 curated | 1,589 manual | < 500 |
| **Unique persons identified** | **734,125** | 1,536 registry | 1,589 | — |
| **Financial transactions modeled** | **81,451** (tiered) + **23,832** (directional) | ~186 normalized | 0 | 0 |
| **Directional fund flows (A→B)** | **23,832** | qualitative | 0 | 0 |
| **Wire transfers in master ledger** | **481** (Phase 5I audited) | 0 | 0 | 0 |
| **Relational database tables** | **43** | 3-4 | — | — |
| **Confidence-tiered scoring** | ✅ 5-axis | — | — | — |
| **Redaction proximity analysis** | ✅ | ✅ (different method) | — | — |
| **SAR cross-validation** | ✅ **126.6%** | — | — | — |
| **Multi-phase dedup pipeline** | ✅ 3-stage evolution | — | — | — |
| **Shell hierarchy mapping** | ✅ 4-tier | — | — | — |

> **Note:** The largest narrative repo counts individual *pages* as records — their unique PDF file count is ~519,548. Our 1,476,437 are unique files, each with a distinct DOJ URL or registered serial. The 503,154 media items are separately cataloged from <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-10-files" target="_blank">DS10</a> evidence photos and videos. Other projects in this space are doing solid work — narrative forensic reporting, searchable archives, community preservation. Our lane is systematic financial reconstruction at scale.

---

## Headline Results

> ⚠️ **Findings reflect the publication ledger's confidence tier. T1–T3 figures are anchored to court exhibits and Bates-stamped DOJ source documents. T4 (Unclassified) figures and automated extractions outside the verified ledger are navigational tools, not established fact. See [COMPLIANCE.md](docs/COMPLIANCE.md) for full professional standards disclaimers.**

| Metric | Value |
|--------|-------|
| **Publication Ledger Total** | **$2,146,000,000** (6,310 deduplicated transactions) |
| **FinCEN SAR Benchmark** | $1,878,000,000 |
| **T1–T3 Coverage of SAR** | **126.6%** ($1,960,500,000) |
| **Payment Types Classified** | 10 |
| **Wire Transfers in Master Ledger** | 481 |
| **Unique Entities (Entity-Resolved)** | 228 |
| **Bank Coverage** | 14 banks |
| **Bates Number Coverage** | 51% |
| **Shell-to-Shell Transfers Identified** | 43 |
| **Shell Trust Hierarchy Tiers Mapped** | 4 |
| **Contamination Bugs Caught & Fixed** | 9 |
| **Amador Expert Legal Total** | $55,635,697 (36 firms, EFTA02810827) |
| **SDNY Prosecution Exhibit Captured** | $172,036 ← **323× gap** |
| **Largest Firm Absent from Prosecution** | Burman Critton Luttier & Coleman — $17,565,139 |
| **Amador Shell Transfer Total** | $556,723,680 (22 entities — cross-validates our pipeline) |

### Four-Tier GAGAS-Aligned Confidence Framework

| Tier | Classification | Amount | % of Total |
|------|---------------|-------:|:----------:|
| **T1** | Epstein-Controlled Entities | $1,609,500,000 | 75.0% |
| **T2** | Known Associates | $343,400,000 | 16.0% |
| **T3** | Extended Network | $7,600,000 | 0.4% |
| **T4** | Unclassified | $185,500,000 | 8.6% |
| **T1–T3** | **Auditable Subtotal** | **$1,960,500,000** | **126.6% of SAR** |
| **Total** | **Publication Ledger** | **$2,146,000,000** | — |

### Why T1–T3 Exceeds 100%

The SAR benchmark ($1.878B) only counts transactions banks flagged as suspicious. The EFTA corpus has the complete financial record — including legitimate stuff like Sotheby's auction proceeds ($11.2M), Tudor Futures returns ($12.8M), Kellerhals law firm settlements ($23M), and Blockchain Capital VC investments ($10.5M). Total financial flows should exceed the suspicious subset. That's just how it works: SAR ⊂ Total Financial Activity. T4 (Unclassified) gets excluded from the SAR comparison because those transactions don't have enough entity resolution to classify.

---

## The Money Circuit: 4-Tier Trust Hierarchy

> Full annotated flow diagram: **[NETWORK.md](docs/NETWORK.md)**

```
TIER 1 — HOLDING TRUSTS (received external deposits)
  Southern Trust Company Inc.        $151.5M in  ← Black, Rothschild, Narrow Holdings
  The 2017 Caterpillar Trust          $15.0M in  ← Blockchain Capital

TIER 2 — DISTRIBUTION TRUSTS (redistributed internally)
  The Haze Trust (DBAGNY)             $49.7M out → Southern Financial, Southern Trust
  The Haze Trust (Checking)           $21.8M in  ← Sotheby's, Christie's
  Southern Financial LLC              $14.0M in  ← Tudor Futures
  Southern Financial (Checking)       $32.0M in  ← Haze Trust

TIER 3 — OPERATING SHELLS (paid beneficiaries)
  Jeepers Inc. (DB Brokerage)         $51.9M out → Epstein personal account (21 wires)
  Plan D LLC                          $18.0M out → Leon Black (4 wires)
  Gratitude America MMDA               $6.3M out → Morgan Stanley, charities
  Richard Kahn (attorney)              $9.3M out → Paul Morris, others
  NES LLC                              $554K out → Ghislaine Maxwell

TIER 4 — PERSONAL ACCOUNTS (terminal destinations)
  Jeffrey Epstein NOW/SuperNow        $83.4M in  ← Jeepers, Kellerhals, law firms
  Darren Indyke (estate attorney)      $6.4M in  ← Deutsche Bank
```

Amounts reflect intermediate pipeline snapshots. Final verified figures are in the publication ledger. See [FINDINGS.md](docs/FINDINGS.md) for details.

### Money Flow Direction Analysis

*Phase 14–24 intermediate snapshot (382-wire ledger, pre-Phase 5I entity resolution)*

| Direction | Wires | Amount | Share |
|-----------|------:|-------:|------:|
| **MONEY IN** — External → Epstein entities | 91 | $232,538,043 | 41.7% |
| **INTERNAL MOVE** — Shell → Shell reshuffling | 39 | $112,610,112 | 20.2% |
| **PASS-THROUGH** — Attorney/trust administration | 130 | $72,433,003 | 13.0% |
| **MONEY OUT** — Epstein entities → External | 51 | $63,266,349 | 11.3% |
| **BANK → SHELL** — Custodian disbursements | 27 | $53,717,045 | 9.6% |
| Other (Shell→Bank, Interbank, External→Bank) | 44 | $23,504,429 | 4.2% |

### SAR Benchmark (Public Record)

| Bank | Reported SARs |
|------|:------------:|
| JPMorgan Chase | ~$1.1B (4,700+ transactions) |
| Deutsche Bank | ~$400M |
| Bank of New York Mellon | ~$378M |
| **Total known SARs** | **$1.878B** |

*Sources: U.S. Senate Permanent Subcommittee on Investigations; NYDFS Consent Order (2020); JPMorgan USVI Settlement (2023)*

---

## Database Schema (43 Tables)

> Full architecture diagram: **[SCHEMA.md](docs/SCHEMA.md)**

Not a search index. A relational forensic database. **8.64 GB, 49 tables, 26.7 million rows.**

**Financial Analysis (17 tables)**
- `publication_ledger` — 6,310 deduplicated transactions ($2.378B, dedup_status='UNIQUE') with four-tier GAGAS classification (T1–T4), payment type, source exhibit
- `master_wire_ledger` — 481 court-exhibit authenticated wire transfers, entity-resolved, 14-bank coverage, 51% Bates
- `extracted_payments` — 10,118 raw payment extractions across 10 payment types (pre-dedup input to publication ledger)
- `bank_statement_transactions` — 24,563 multi-bank statement records from 13 institutions (1,202 verified after 11-layer cleanup)
- `verified_wires` — 185 court-exhibit authenticated wire transfers with dates, bates numbers, and exhibits
- `fund_flows` — 23,832 directional money movements (entity_from → entity_to, amount, date, confidence)
- `fund_flows_audited` — 7,355 classified flows (5-tier: PROVEN/STRONG/MODERATE/WEAK/VERY_WEAK) with FinCEN/ICIJ match flags
- `financial_hits` — 81,451 financial content extractions across 19 categories and 3 verification tiers (C1/C2/C3)
- `financial_redactions` — 2,395 recovered dollar amounts near redaction markers with confidence scoring
- `fincen_transactions` — 4,507 FinCEN suspicious activity report transaction records
- `fincen_bank_connections` — 5,498 bank-to-bank SAR relationship mappings
- `ctr_transactions` — 10 Currency Transaction Report records
- `statement_chain` — statement continuity chain (scaffolded, pending population)
- `expert_legal_payments` — 36 law firms from Amador expert report (EFTA02810827) — $55.6M total, 323× prosecution gap
- `expert_shell_transfers` — 22 shell entities from Amador expert report — $556.7M total cross-validation
- `shell_entity_registry` — 47 classified shell entities with tier, jurisdiction, and control flags
- `entity_aliases` — 186 raw text → canonical name resolution rules

**Entity Intelligence (5 tables)**
- `entities` — 11,438,134 extracted entities with NLP classification (PERSON, ORG, GPE, MONEY, NORP, FAC, LOC, LAW)
- `entity_roles` — 74 classified entities with total inflow, outflow, net position, wire counts, and exhibit references
- `entity_registry` — canonical entity registry (scaffolded, pending population)
- `poi_rankings` — 2,000 persons of interest scored by multi-axis corpus frequency (file count, financial count, flight count, redaction dollars, direct dollars)
- `evidence_index` — 1,077,516 evidentiary chain records linking documents across datasets with bates numbers, checksums, and source types

**Redaction Analysis (3 tables)**
- `redaction_recovery` — 157,984 content fragments recovered from under redaction overlays (with financial/names/dates flags and interest scoring)
- `redaction_markers` — 140,060 systematic redaction position records across corpus
- `redaction_summary` — 131,860 aggregated redaction analysis per document

**Corpus Infrastructure (5 tables)**
- `files` — 1,476,437 file records with 30 columns: metadata, classification, dates, extraction status, doc types
- `extracted_text` — 2,866,804 page-level text records with classification and extraction method
- `dates_found` — 2,411,188 temporal references extracted across entire corpus with context
- `media_evidence` — 503,154 DS10 image/video catalog with custodian, doc_type, confidentiality markings
- `media_catalog` — 2,663 cataloged media records with metadata
- `media_files` — media file registry (scaffolded, pending population)

**External Cross-Reference — FEC Political Contributions (4 tables)**
- `fec_contributions` — 10,101 FEC contribution records cross-referenced against network entities
- `fec_forensic_clean` — 23 high-confidence forensic matches (entity-resolved, amount/date verified)
- `fec_network_summary` — 23 network-level contribution summaries by donor entity
- `fec_network_summary_clean` — 24 cleaned network summaries with dedup and alias resolution

**External Cross-Reference — FAA Aviation (7 tables)**
- `faa_master` — 309,849 active aircraft registrations
- `faa_dereg` — 381,869 deregistered aircraft records with cancellation dates
- `faa_acftref` — 93,521 aircraft type/model reference
- `faa_engine` — 4,743 engine type reference
- `faa_dealer` — 12,485 aircraft dealer registrations
- `faa_reserved` — 126,504 reserved N-numbers
- `faa_docindex` — 11,440 FAA document index

**External Cross-Reference — ICIJ Offshore Leaks (6 tables)**
- `icij_entities` — 814,344 offshore entities from Panama Papers, Paradise Papers, Pandora Papers, and other ICIJ investigations
- `icij_officers` — 771,315 officers/directors of offshore entities
- `icij_relationships` — 3,339,267 entity relationship records
- `icij_addresses` — 402,246 offshore entity addresses worldwide
- `icij_intermediaries` — 25,629 shell company formation agents
- `icij_others` — 2,989 other offshore entities

---

## Pipeline Architecture

```
Phase 1    DOJ EFTA Scraper + Community Gap-Fill → 1.48M files + 503K media registered
Phase 2    Download & Verify → local corpus with integrity checks
Phase 3    Extract, Classify & Enrich → text, doc types, dates
Phase 3B   Entity Extraction (spaCy NLP) → 11.4M entities, 734K persons
Phase 5A   Person-of-Interest Network → news-filtered, multi-source scoring
Phase 5B   Operational Cost Model → confidence-tiered financial extraction
Phase 5C   Entity-to-Entity Fund Flows → directional A→B with 5-axis scoring
Phase 5D   Payment-Travel-Victim Correlation → temporal pattern analysis
Phase 5E   Redaction Map → navigational tool for document analysis
Phases 14-24  Wire Transfer Extraction Pipeline → 382-wire ledger (pre-5I), $1.964B
Phase 5I   Entity Resolution & Bank Expansion → 481-wire ledger, $973M entity-resolved, 14-bank coverage
Phase 5J   Multi-Bank Statement Parser → 1,202 verified transactions from 13 banks
Phase 5K   Payment Type Expansion → CHIPS, SWIFT, checks, bank statements beyond wire transfers
Phase 5L   Publication Ledger Assembly → 6,310 unique transactions (dedup-verified), $2.378B, four-tier GAGAS framework
```

### Financial Extraction Pipeline (Phases 14–5L)

| Phase | What Happened | Impact |
|-------|--------------|--------|
| 14.5-15 | Known entity fund flows + wire indicators | +$105M |
| 16.1-16.2 | Transaction-line parser + round-wire extractor | +$83M |
| 17-18 | Trust transfers + full category sweep | +$17M |
| 19 | Self-dedup bug fix (table checking against itself) | +$60M recovered |
| 20-21 | Verified wires + STRONG/MODERATE new amounts | +$63M |
| 22 | Forensic scrub — chain-hop inflation removed | -$311M removed |
| 23 | Date-aware census (same amount, different dates) | +$189M recovered |
| 24 | Above-cap verified wires + bank custodian audit | +$121M / -$113M |
| 25 | Date recovery from source context fields | +75 dates (31.9%→51.6%), 0 collisions |
| **5I** | **Entity resolution: 481 wires, 228 entities, 14 banks, 51% Bates coverage** | **$973M entity-resolved** |
| 5J | Multi-bank statement parser: 1,202 transactions from 13 institutions | +$430K verified statements |
| 5K | Payment type expansion: CHIPS, SWIFT, checks, bank statements | 10 payment types classified |
| **5L** | **Publication ledger: 6,310 dedup-verified transactions, four-tier GAGAS, T1–T3 = 126.6% SAR** | **$2.378B total** |

Full phase-by-phase details: **[METHODOLOGY.md](docs/METHODOLOGY.md)**

---

## Financial Methodology: 5-Axis Forensic Scoring

Every financial record gets scored independently across five axes:

| Axis | Weight | What It Measures |
|------|:------:|-----------------|
| Context Language | ×3 | Transaction vocabulary (wire, routing, SWIFT) vs. noise (lawsuit, net worth) |
| Amount Specificity | ×1 | $2,473,891.55 scores high; $10,000,000.00 exactly scores low |
| Date Presence | ×1 | Full date > year only > no date |
| Entity Quality | ×2 | 28 known banks, 64 financial actors, 71+ garbage entity exclusions |
| Source Document Type | ×1 | Financial/spreadsheet > email > general document |

**Classification Tiers:**
- **PROVEN** (≥12): Bank statement language, multi-axis confirmation, ctx_txn ≥ 2
- **STRONG** (8-11): Good signals, minor gaps
- **MODERATE** (5-7): Mixed signals
- **WEAK** / **VERY_WEAK** / **REJECT**: Not enough evidence or known noise

**Validation:** v6.2 spot-check hit 93% accuracy on top-30 PROVEN transactions (28/30), with 0% balance contamination (down from 47% in v5).

---

## GAP Analysis

### What's Still Missing

| Gap Source | Estimable? | Reason |
|-----------|:----------:|--------|
| **WEAK/VERY_WEAK tier exclusions** | **Yes — $5M-$15M** | $991M excluded as low-confidence; manual review of top entries could recover $5-15M |
| **Sealed/withheld documents** | No | Court-sealed records inaccessible to EFTA; dollar value unknown |
| **Attempted vs. completed transactions** | No | SARs count attempted; we extract completed only; gap is real but unquantifiable |
| **Destroyed pre-retention records** | No | Bank retention policies may have purged records; unquantifiable |
| **Cross-bank SAR duplication** | No (directional) | Same wire triggering SARs at both banks inflates the benchmark — *reduces* the gap |

One gap has a credible dollar estimate ($5-15M in excluded tiers). The rest are real information gaps with unknown values. We're not putting specific ranges on things we can't measure.


---

## Amador Cross-Validation

Jorge Amador CPA/CFF/Esq. (Axia Advisors LLC) filed a court-certified expert report on July 25, 2023 in *USVI v. JPMorgan Chase* (Case 1:22-cv-10904-JSR) under GAAS/AICPA SSFS No. 1 standards at $570/hr. His analysis drew directly from JPMorgan's full production (JPM-SDNYLIT series). Source document: **EFTA02810827** (161 pages).

### Prosecution Gap — Legal Payments

Amador identified **$55,635,697** in legal payments across 36 law firms from JPMorgan account records.

The SDNY prosecution exhibit captured **$172,036** — 0.3% of the confirmed total. **34 of 36 firms appear nowhere in the prosecution exhibit.**

| Firm | Amador Total | In SDNY Exhibit |
|------|-------------:|:---------------:|
| Burman Critton Luttier & Coleman LLP | $17,565,139 | NO |
| Darren K. Indyke PLLC | $8,320,000 | NO |
| Alan M. Dershowitz | $4,040,238 | YES — $122,036 only |
| Black Srebnick Kopman & Stumpf PA | $3,793,883 | NO |
| Gerald B. Lefcourt PC | $3,100,000 | NO |
| Kirkland and Ellis LLP | $2,905,138 | NO |
| MG Weinberg PC | $2,567,827 | NO |
| *(29 additional firms)* | *$13,343,472* | NO |
| **TOTAL** | **$55,635,697** | **$172,036 (323×gap)** |

### Shell Transfer Validation

Amador identified **$556,723,680** across 22 shell entities — independently corroborating our pipeline figures.

| Entity | Amador Total | Source Account |
|--------|-------------:|:--------------:|
| Financial Trust Company Inc. | $232,080,036 | #5001 |
| Southern Financial LLC | $62,994,225 | #9006 |
| Jeepers Inc. | $58,910,979 | #5005 |
| LSJ LLC | $32,976,000 | #0438 |
| Southern Trust Company Inc. | $32,850,050 | #0245 |
| NES LLC | $23,620,000 | #0438 |
| JEGE Inc. | $11,750,316 | #0438 |
| *(15 additional entities)* | *$101,542,075* | #0438 |
| **TOTAL** | **$556,723,680** | |

### Key Findings from Amador Source Document

**Highbridge quid pro quo** — JPMorgan paid $15M to Financial Trust Company Inc. on December 31, 2004 to facilitate JPM's acquisition of Highbridge Capital. Source: HIGHBRIDGE_00000506-07.

**Duffy structuring memo** — March 28, 2012: JPM Private Bank CEO advised Epstein to route cash through Hyperion Air disguised as fuel payments, including payments to OFAC-listed countries. Source: JPM-SDNYLIT-00020772.

**LSJE LLC pipeline** — Little Saint James Estate LLC received $8.215M across 63 transfers from account #0438. Final tail: payments to "Miss [Redacted]" via Barclays account 42959295 (January and April 2019, $32,236).

---

## Data Narratives

**→ [Read all Data Narratives](narratives/)**

| # | Title | Key Finding | Data Scope |
|---|-------|-------------|------------|
| **19** | **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/narratives/19_grand_opus_narrative.html" target="_blank">Blueprint of a Financial Machine</a>** | ** $2.378B, 123 nodes, 313 edges. Full network mapped. <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/19_blueprint_financial_machine.html" target="_blank">Visualization</a>** | **6,310 txns · 123 nodes · $2.378B** |
| **20** | **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/narratives/20_the_verification_wall.html" target="_blank">The Verification Wall</a>** | ** Narrative 20. Every document has a Bates number — the wall tests what's behind it. 8 noise POIs ($144.4M claimed, Bates stamps → news/court filings, $0 bank docs) vs. Leon Black ($310.5M, 42 verified wires, 15 bank docs). NLP phantom autopsy with clickable EFTA source documents.** | **9 POIs · 15 bank docs · $310.5M verified** |

Source workbook: **[Forensic Workbook v10](https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true)** · [Interactive Shell Network](https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/shell_network.html)

*Every claim anchored to specific wire transfers, entity classifications, and court exhibit references from the master ledger.*
---

## Repository Contents

```
├── README.md                              ← You are here
├── docs/
│   ├── METHODOLOGY.md                     ← 25-phase pipeline, 9 bugs, 5-axis scoring, limitations
│   ├── FINDINGS.md                        ← GAP analysis, 8 key discoveries, recommendations
│   ├── COMPLIANCE.md                      ← Professional standards, GAAS conformance, legal disclaimers
│   ├── SCHEMA.md                          ← Database architecture diagram
│   ├── NETWORK.md                         ← Trust network flow diagram
│   └── SOURCE_APPENDIX_TEMPLATE.md        ← Standard template for source appendices
├── narratives/                            ← 2 forensic data narratives with source appendices
├── data/
│   ├── publication_ledger_phase5l.json    ← 6,310 deduplicated transactions, four-tier (publication dataset)
│   ├── master_wire_ledger_phase5i.json    ← 481 wires (wire-specific subset)
│   └── entity_classification.json         ← Entity → type mapping (228 entities)
├── visualizations/                        ← Interactive shell network diagram
└── tools/
    ├── narrative_sql_tools.py             ← SQL query functions for all 2 narrative data sources
    ├── linkify_efta.py                    ← Auto-link EFTA IDs → DOJ PDFs in .md files
    ├── convert_links_new_tab.py           ← Convert external links to target="_blank"
    ├── inject_efta_source_table.py        ← Add source document tables to narratives
    └── append_source_appendices.py        ← Append source appendices to narratives
```

### Visual Guides

- **[SCHEMA.md](docs/SCHEMA.md)** — Full database architecture showing how 49 tables, 11.4M entities, and 1.48M files feed into the 6,310-transaction deduplicated publication ledger
- **[NETWORK.md](docs/NETWORK.md)** — Annotated trust network flow diagram with dollar amounts on every edge

### Forensic Workbook v10

| Tab | Name | Description |
|:---:|------|-------------|
|:---:|------|-------------|
| 1 | Executive Summary | Headline $2.378B, four-tier GAGAS framework, publication ledger |
| 2 | Extraction Phases | Full pipeline with running totals, bug fixes color-coded |
| 3 | **Money Flow Patterns** | Every wire classified: MONEY IN / INTERNAL MOVE / MONEY OUT |
| 4 | **Shell Trust Hierarchy** | 4-tier network with actual dollar flows per entity |
| 5 | Master Wire Ledger | 481 wires with flow direction, entity types, recovery flags |
| 6 | Above-Cap Verified | Court-verified wires above $10M ($120.6M) |
| 7 | Date Recovery | Same-amount different-date analysis (95 Phase 23 + 75 Phase 25 recoveries) |
| 8 | Entity P&L | 228 entities with inflow/outflow/net, shell flags |
| 9 | Shell Network | Shell-involved wires, 43 shell-to-shell |
| 10 | SAR Comparison | Bank-by-bank vs FinCEN benchmarks |
| 11 | Methodology | 9 bugs documented, data sources, 10 limitations |
| 12 | Bank Coverage | 14 banks mapped with wire counts and volumes |
| 13 | Entity Resolution | 228 canonical entities with alias mapping |
| 14 | Bates Index | 51% Bates coverage with exhibit cross-references |

---

## What Makes This Different

**We didn't read the documents. We audited the money.**

Other projects build search engines, write narrative reports, or create browsable archives. Good work, all of it. We took a different approach. We applied the same methodology used professionally — multi-affiliate reconciliation, exception reporting, variance analysis, confidence tiering — and pointed it at the EFTA corpus.

The question isn't "what do the documents say?" It's: **"Where did the money go, who moved it, and what did the DOJ redact around it?"**

---

## Why Findings Only — No Source Code or Database

This repo publishes methodology, findings, and summary data. The source code, database, and raw extraction pipeline are not included. That's intentional.

- **AICPA SSFS No. 1** says forensic practitioners maintain control over working papers, proprietary methodologies, and analytical tools. Work product privilege protects the analytical process.
- **AICPA AU-C §230** says audit documentation is the property of the practitioner. Sufficient documentation is provided for a knowledgeable reviewer to understand the work performed.
- **Chain of custody**: The 8.64GB forensic database is a consolidated analytical environment. Releasing it in fragments invites miscontextualization of intermediate results without the full pipeline logic.
- **Reproducibility**: The methodology docs, scoring weights, classification rules, and dedup logic are fully described. You can replicate it without our tooling.
- **Ongoing analysis**: The database and pipeline are still active. Premature release could compromise forthcoming narratives and follow-on investigations.

The master wire ledger (481 wires) and entity classification data are published in full in the `data/` directory. Those are the final audited outputs and they're sufficient for independent verification of everything published here.

---

## Project Team

**Anne Mitchell, Esq.** (Project Lead)

**R.S. Taylor** (Lead Analyst)

BS Network & Cyber Security, Wilmington University
MS Applied Data Science, Syracuse University

We built this project — every line of extraction code, every database table, every classification rule, every phase of the pipeline. AI tools (Claude, Anthropic) helped us write code faster. The analytical judgments, methodology design, and forensic interpretations are ours.

Team background: multi-affiliate financial reconciliation, automated classification and exception reporting systems, large-scale data operations, forensic financial analysis, and legal review.

---

## Ethical Standards

- **Victim protection**: No victim names, identifying details, or testimony content is stored, published, or extractable from any output. Victim-adjacent redactions are noted by proximity only.
- **SSFS alignment**: All outputs include frozen Row 1 caveats, confidence tier labels, and navigational-tool disclaimers where applicable.
- **No attribution of guilt**: Financial flows are documented as they appear in DOJ documents. Appearance in this analysis does not imply wrongdoing.
- **Open methodology**: Every extraction rule, scoring weight, and classification threshold is documented and reproducible.

---

## Disclaimer

This analysis does not constitute an audit, examination, or review performed in accordance with GAAS, GAGAS, or AICPA SSFS No. 1. See **[COMPLIANCE.md](docs/COMPLIANCE.md)** for details.

All financial amounts outside the publication ledger's T1–T3 verified tier are automated extractions subject to error. Entity classifications are based on OCR text extraction with automated normalization and may contain errors. Shell entity designations are analytical classifications, not legal determinations.

---

## Press Coverage

| Outlet | Author | Piece | Date |
|--------|--------|-------|------|
| **The Observer (UK)** | Alexi Mostrous | <a href="https://observer.co.uk/news/international/article/sibling-revelry-doj-files-suggest-ghislaine-not-the-only-maxwell-who-took-epstein-cash" target="_blank">"Sibling Revelry"</a> — names R.S. Taylor analysis, $92.5M Ghislaine finding | March 8, 2026 |
| **The Observer (UK)** | Alexi Mostrous | <a href="https://observer.co.uk/news/international/article/the-epstein-files-citizen-sleuths-examine-16-billion-in-financial-transactions" target="_blank">The Epstein Files: Citizen Sleuths</a> — EFP financial analysis cited | March 3, 2026 |
| **Ouest-France** | Arnaud Wajdzik | <a href="https://www.ouest-france.fr/monde/etats-unis/jeffrey-epstein/enquete-lart-les-trusts-et-les-millions-les-coulisses-du-montage-financier-qui-lie-les-lang-a-la-galaxie-epstein-5f525dae-1544-11f1-8725-6cea811c3c37" target="_blank">Lang family / trust network investigation</a> — DOJ corpus financial analysis contributed | March 2026 |
| **Ouest-France** | Arnaud Wajdzik | <a href="https://www.ouest-france.fr/monde/etats-unis/jeffrey-epstein/contribuable-discret-jeffrey-epstein-a-paye-limpot-sur-la-fortune-en-france-pendant-8-ans-a0e3d360-1968-11f1-9fa1-ca7616976f61" target="_blank">Epstein's 8 years paying French wealth tax</a> — ISF records / DOJ corpus analysis contributed | March 2026 |
| **ResearchBuzz** | — | <a href="https://researchbuzz.me/2026/02/23/epstein-financial-forensics-ai-impact-summit-wikipedia-seismograph-more-monday-researchbuzz-february-23-2026/" target="_blank">Featured</a> | February 23, 2026 |

---

## Citation

```
Taylor, R.S. (2026). Epstein Financial Forensics: Automated forensic financial
reconstruction from 1.48 million DOJ EFTA documents. GitHub.
https://github.com/randallscott25-star/epstein-forensic-finance#readme
```

---

## License

This work is licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank">Creative Commons Attribution-NonCommercial 4.0 International</a>.

The underlying DOJ documents are U.S. government publications in the public domain. This repository contains only metadata, extracted analysis, and methodology — no copyrighted source material is reproduced.

---

## Project Timeline

| Date | Milestone |
|------|-----------|
| Feb 7, 2026 | Project started — DOJ scraper built, first dataset indexed |
| Feb 8 | <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">DS11</a> (76,969 financial ledgers) fully scraped |
| Feb 10 | 633,842 files indexed — published to GitHub and Archive.org |
| Feb 12 | Phase 3 text extraction complete (513K files) |
| Feb 14 | Entity extraction (3B) launched — 565K files queued |
| Feb 15 | Corpus expanded to 1.48M files + 503K media with <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-10-files" target="_blank">DS10</a> + community gap-fill |
| Feb 16 | Phase 5 financial analysis chain operational |
| Feb 18 | 19 datasets online (<a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">DS1</a>-12 + DS98-DS104) |
| Feb 20 | Fund flows audit v6.2: $1.43B in P+S transactions, 39% SAR coverage |
| Feb 21 | Wire extraction pipeline (Phases 14-24): $1.964B, 104.6% SAR coverage |
| Feb 21 | Forensic workbook v6.1 published (11 tabs, 382-wire master ledger) |
| Feb 21 | Phase 25: Date recovery from context fields — 75 dates (31.9%→51.6%), 0 collisions (credit: u/miraculum_one) |
| Feb 22 | Repository made public. 17 Data Narratives published. 30 GitHub stars in 5 hours |
| Feb 24 | Phase 5I: 481 wires, $973M entity-resolved, 228 entities, 14-bank coverage, 51% Bates |
| Feb 24 | Workbook v7 published (14 tabs). Full database audit: 33 tables, 8.03GB, 26.6M rows |
| Feb 25 | Phase 5J: Multi-bank statement parser. 1,202 verified transactions from 13 banks ($430K) |
| Feb 25 | Workbook v8 (19 tabs). N18 published. JSON v26 community dataset. |
| Feb 25 | Phase 5K–5L: Payment type expansion + publication ledger assembly. 10,964 raw records assembled; 6,310 dedup-verified unique transactions, $2.378B, four-tier GAGAS framework |
| Feb 25 | Workbook v9. 19 data narratives live. |
| Feb 26 | N19: Blueprint of a Financial Machine — capstone narrative. 123 nodes, 313 edges, full $2.378B corpus mapped. Timeline v9 with 69 vetted persons of interest. |
| Feb 27 | Workbook v10 published (21 tabs). Amador cross-validation tab added — $55.6M legal gap, $556.7M shell validation, Duffy structuring memo, Highbridge quid pro quo. |
| Feb 27 | N20: The Verification Wall. Bates distinction framework. 8 noise POIs ($144.4M → $0 bank docs) vs. Leon Black ($310.5M, 42 wires, 15 bank docs). Clickable EFTA source documents. |
| Mar 11, 2026 | N19/N20/timeline figures corrected to dedup-verified baseline (6,310 / $2.378B). Media & fork notice added to all published narratives. |
| Mar 15, 2026 | EFP Terminal deployed to private server. Browser-based research interface with secure per-user logins and named lanes. Features: Bates Lookup with 6-method document clustering, full-corpus full-text search, media tab with transcriptions and facial recognition, audio cleanup and filtering, corpus email client, iPhone/SMS viewer, geolocation map, Bates queue with PDF report generation. |
| Mar 27, 2026 | The Projects website launched (the-projects.org). EFP Terminal migrated to cloud-efp.com with full authentication system — login wall, access request registration, admin approval dashboard, credentialed external access. Congressional oversight interest active. |
| Ongoing | Deep dive forensic analysis — no further narratives planned |
