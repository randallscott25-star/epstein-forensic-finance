# Epstein Financial Forensics

**Automated forensic financial reconstruction from 1.48 million DOJ EFTA documents + 503K cataloged media items**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## What This Is

This repository contains the methodology, findings, and documentation for a computational forensic analysis of the U.S. Department of Justice's Epstein Files Transparency Act (EFTA) corpus.

I built this project as a solo effort — writing all extraction code, designing the database schema, developing the financial classification pipeline, and performing the forensic analysis myself, with AI assistance for development acceleration and quality assurance. The underlying methodology draws from my professional background in multi-affiliate financial reconciliation, budget variance analysis, and automated exception reporting at institutional scale.

To my knowledge, this represents the first systematic attempt to reconstruct the complete financial infrastructure visible in the EFTA corpus using quantitative forensic methods — moving beyond narrative analysis of individual documents to model the full network of fund flows, entity relationships, and shell trust hierarchies at scale.

---

## The Database

**8.03 GB | 33 tables | 26.6 million rows | 19 datasets**

| Metric | This Project | Largest Narrative Repo | Largest Search Platform | Others |
| --- | --- | --- | --- | --- |
| **Total files indexed** | **1,476,377** + 503K media | 1,380,937 | 1,120,000 | < 20,000 |
| **Datasets covered** | **19** (DS1-12 + DS98-104) | 12 | 12 | 1-3 |
| **Extracted text records** | **2.87M** (page-level) | 993,406 pages | — | — |
| **Entity extraction (NLP)** | **11.4M entities** | ~4,000 curated | 1,589 manual | < 500 |
| **Unique persons identified** | **734,122** | 1,536 registry | 1,589 | — |
| **Financial transactions modeled** | **81,451** (tiered) + **23,832** (directional) | ~186 normalized | 0 | 0 |
| **Directional fund flows (A→B)** | **23,832** | qualitative | 0 | 0 |
| **Wire transfers in master ledger** | **481** (Phase 5I audited) | 0 | 0 | 0 |
| **Relational database tables** | **33** | 3-4 | — | — |
| **Confidence-tiered scoring** | ✅ 5-axis | — | — | — |
| **Redaction proximity analysis** | ✅ | ✅ (different method) | — | — |
| **SAR cross-validation** | ✅ **104.6%** | — | — | — |
| **Multi-phase dedup pipeline** | ✅ 3-stage evolution | — | — | — |
| **Shell hierarchy mapping** | ✅ 4-tier | — | — | — |

> **Note:** The largest narrative repo's 1,380,937 figure counts individual *pages* as records; their unique PDF file count is ~519,548. My 1,476,377 are unique files each with a distinct DOJ URL or registered serial, plus 503,154 separately cataloged media items from DS10 evidence photos and videos. Multiple projects in this space are doing valuable, complementary work — narrative forensic reporting, searchable archives, community preservation. This project's lane is systematic financial reconstruction at scale.

---

## Headline Results

> ⚠️ **All findings are navigational tools derived from automated extraction. They have not been independently verified and should not be treated as established fact. See [COMPLIANCE.md](COMPLIANCE.md) for full professional standards disclaimers.**

| Metric | Value |
| --- | --- |
| **Total Financial Activity Extracted** | **$1,964,229,742** (Unverified) |
| **FinCEN SAR Benchmark** | $1,878,000,000 |
| **Extraction Coverage** | **104.6%** |
| **Wire Transfers in Master Ledger** | 481 |
| **Unique Entities (Entity-Resolved)** | 228 |
| **Bank Coverage** | 14 banks |
| **Bates Number Coverage** | 51% |
| **Shell-to-Shell Transfers Identified** | 43 |
| **Shell Trust Hierarchy Tiers Mapped** | 4 |
| **Contamination Bugs Caught & Fixed** | 9 |

### Three-Tier Confidence Framework

| Tier | Amount (Unverified) | % of SAR | What's Included | Duplication Risk |
| --- | --- | --- | --- | --- |
| **Conservative** | $1,843,653,804 | 98.2% | v2-20 amount-unique + Phase 23 date recovery | Zero |
| **Publication** ★ | $1,964,229,742 | 104.6% | Tier 1 + 8 above-cap court-verified wires | Zero — all exhibit-verified |
| **Expanded** | $1,956,153,971 | 104.2% | Tier 2 + PROVEN entity expansion | Minor name overlap risk |

### Why the Total Exceeds 100%

The SAR benchmark ($1.878B) represents only transactions banks flagged as **suspicious**. The EFTA corpus contains the **complete** financial record — including legitimate, non-suspicious transactions such as Sotheby's auction proceeds ($11.2M), Tudor Futures investment returns ($12.8M), Kellerhals law firm settlements ($23M), and Blockchain Capital VC investments ($10.5M). Total financial flows **should** exceed the suspicious subset. Standard forensic accounting: SAR ⊂ Total Financial Activity.

---

## The Money Circuit: 4-Tier Trust Hierarchy

> See full annotated flow diagram: **[NETWORK.md](NETWORK.md)**

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

All amounts are (Unverified) automated extractions. See [FINDINGS.md](FINDINGS.md) for detailed analysis.

### Money Flow Direction Analysis

| Direction | Wires | Amount (Unverified) | Share |
| --- | --- | --- | --- |
| **MONEY IN** — External → Epstein entities | 91 | $232,538,043 | 41.7% |
| **INTERNAL MOVE** — Shell → Shell reshuffling | 39 | $112,610,112 | 20.2% |
| **PASS-THROUGH** — Attorney/trust administration | 130 | $72,433,003 | 13.0% |
| **MONEY OUT** — Epstein entities → External | 51 | $63,266,349 | 11.3% |
| **BANK → SHELL** — Custodian disbursements | 27 | $53,717,045 | 9.6% |
| Other (Shell→Bank, Interbank, External→Bank) | 44 | $23,504,429 | 4.2% |

### SAR Benchmark (Public Record, Independently Verified)

| Bank | Reported SARs |
| --- | --- |
| JPMorgan Chase | ~$1.1B (4,700+ transactions) |
| Deutsche Bank | ~$400M |
| Bank of New York Mellon | ~$378M |
| **Total known SARs** | **$1.878B** |

*Sources: U.S. Senate Permanent Subcommittee on Investigations; NYDFS Consent Order (2020); JPMorgan USVI Settlement (2023)*

---

## Database Schema (33 Tables)

> See full database architecture diagram: **[SCHEMA.md](SCHEMA.md)**

This is not a search index. This is a relational forensic database. **8.03 GB, 33 tables, 26.6 million rows.**

### Financial Analysis (10 tables)

* `fund_flows` — 23,832 directional money movements (entity_from → entity_to, amount, date, confidence)
* `fund_flows_audited` — 7,355 classified flows (5-tier: PROVEN/STRONG/MODERATE/WEAK/VERY_WEAK) with FinCEN/ICIJ match flags, composite scoring, entity classification
* `verified_wires` — 185 court-exhibit authenticated wire transfers (dates, bates numbers, exhibits)
* `financial_hits` — 81,451 financial content extractions across 19 categories and 3 verification tiers (C1/C2/C3)
* `financial_redactions` — 2,395 recovered dollar amounts near redaction markers with confidence scoring
* `fincen_transactions` — 4,507 FinCEN suspicious activity report transaction records
* `fincen_bank_connections` — 5,498 bank-to-bank SAR relationship mappings
* `entity_aliases` — 186 raw text → canonical name resolution rules
* `entity_roles` — 74 classified entities with total inflow, outflow, net position, wire counts, and exhibit references

### Entity Intelligence (3 tables)

* `entities` — 11,438,134 extracted entities with NLP classification (PERSON, ORG, GPE, MONEY, NORP, FAC, LOC, LAW)
* `poi_rankings` — 2,000 persons of interest scored by multi-axis corpus frequency (file count, financial count, flight count, redaction dollars, direct dollars)
* `evidence_index` — 1,077,516 evidentiary chain records linking documents across datasets with bates numbers, checksums, and source types

### Redaction Analysis (3 tables)

* `redaction_recovery` — 157,984 content fragments recovered from under redaction overlays (with financial/names/dates flags and interest scoring)
* `redaction_markers` — 140,060 systematic redaction position records across corpus
* `redaction_summary` — 131,860 aggregated redaction analysis per document

### Corpus Infrastructure (4 tables)

* `files` — 1,476,377 file records with 30 columns: metadata, classification, dates, extraction status, doc types
* `extracted_text` — 2,866,239 page-level text records with classification and extraction method
* `dates_found` — 2,411,188 temporal references extracted across entire corpus with context
* `media_evidence` — 503,154 DS10 image/video catalog with custodian, doc_type, confidentiality markings

### External Cross-Reference — FAA Aviation (7 tables)

* `faa_master` — 309,849 active aircraft registrations
* `faa_dereg` — 381,869 deregistered aircraft records with cancellation dates
* `faa_acftref` — 93,521 aircraft type/model reference
* `faa_engine` — 4,743 engine type reference
* `faa_dealer` — 12,485 aircraft dealer registrations
* `faa_reserved` — 126,504 reserved N-numbers
* `faa_docindex` — 11,440 FAA document index

### External Cross-Reference — ICIJ Offshore Leaks (6 tables)

* `icij_entities` — 814,344 offshore entities from Panama Papers, Paradise Papers, Pandora Papers, and other ICIJ investigations
* `icij_officers` — 771,315 officers/directors of offshore entities
* `icij_relationships` — 3,339,267 entity relationship records
* `icij_addresses` — 402,246 offshore entity addresses worldwide
* `icij_intermediaries` — 25,629 shell company formation agents
* `icij_others` — 2,989 other offshore entities

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
Phases 14-24  Wire Transfer Extraction Pipeline → 382-wire ledger, $1.964B
Phase 5I   Entity Resolution & Bank Expansion → 481-wire ledger, $973M entity-resolved, 14-bank coverage
```

### Wire Transfer Extraction Pipeline (Phases 14–5I)

| Phase | What Happened | Impact |
| --- | --- | --- |
| 14.5-15 | Known entity fund flows + wire indicators | +$105M |
| 16.1-16.2 | Transaction-line parser + round-wire extractor | +$83M |
| 17-18 | Trust transfers + full category sweep | +$17M |
| 19 | Self-dedup bug fix (table checking against itself) | +$60M recovered |
| 20-21 | Verified wires + STRONG/MODERATE new amounts | +$63M |
| 22 | Forensic scrub — chain-hop inflation removed | -$311M removed |
| 23 | Date-aware census (same amount, different dates) | +$189M recovered |
| 24 | Above-cap verified wires + bank custodian audit | +$121M / -$113M |
| **5I** | **Entity resolution: 481 wires, 228 entities, 14 banks, 51% Bates coverage** | **$973M entity-resolved** |

Full phase-by-phase details: **[METHODOLOGY.md](METHODOLOGY.md)**

---

## Financial Methodology: 5-Axis Forensic Scoring

Every financial record is independently scored across five axes:

| Axis | Weight | What It Measures |
| --- | --- | --- |
| Context Language | ×3 | Transaction vocabulary (wire, routing, SWIFT) vs. noise (lawsuit, net worth) |
| Amount Specificity | ×1 | $2,473,891.55 scores high; $10,000,000.00 exactly scores low |
| Date Presence | ×1 | Full date > year only > no date |
| Entity Quality | ×2 | 28 known banks, 64 financial actors, 71+ garbage entity exclusions |
| Source Document Type | ×1 | Financial/spreadsheet > email > general document |

**Classification Tiers:**

* **PROVEN** (≥12): Bank statement language, multi-axis confirmation, ctx_txn ≥ 2
* **STRONG** (8-11): Good signals, minor gaps
* **MODERATE** (5-7): Mixed signals
* **WEAK** / **VERY_WEAK** / **REJECT**: Insufficient evidence or known noise

**Validation:** v6.2 spot-check achieved 93% accuracy on top-30 PROVEN transactions (28/30), with 0% balance contamination (down from 47% in v5).

---

## GAP Analysis

### What's Still Missing

| Gap Source | Estimable? | Reason |
| --- | --- | --- |
| **WEAK/VERY_WEAK tier exclusions** | **Yes — $5M-$15M** | $991M excluded as low-confidence; manual review of top entries could recover $5-15M |
| **Sealed/withheld documents** | No | Court-sealed records inaccessible to EFTA; dollar value unknown |
| **Attempted vs. completed transactions** | No | SARs count attempted; I extract completed only; gap is real but unquantifiable |
| **Destroyed pre-retention records** | No | Bank retention policies may have purged records; unquantifiable |
| **Cross-bank SAR duplication** | No (directional) | Same wire triggering SARs at both banks inflates the benchmark — *reduces* the gap |

Only one gap ($5-15M excluded tiers) has a credible dollar estimate. The others are real information gaps with unknown values. I am not going to put specific ranges on things I cannot measure.

---

## Data Narratives

The financial data tells stories that numbers alone cannot convey. As I complete deeper analysis of specific fund flow patterns, entity relationships, and temporal correlations, I will publish detailed narrative reports in this section — connecting the quantitative forensic findings to the broader picture of how this financial infrastructure operated.

**Forthcoming:**

* The Jeepers Pipeline: Tracing $51.9M through a brokerage shell to personal accounts
* Art Market Liquidity: How auction house proceeds moved through Haze Trust
* The Plan D Question: $18M out, near-zero in — where did the money come from?
* Chain-Hop Anatomy: How $10M becomes $50M across five entities
* Deutsche Bank's Role: 78 wires and the custodian question
* Gratitude America: When 7% goes to charity and 88% goes to investment accounts

*These narratives will be data-driven — every claim anchored to specific wire transfers, entity classifications, and court exhibit references from the master ledger.*

---

## Repository Contents

```
├── README.md                              ← You are here
├── METHODOLOGY.md                         ← Pipeline phases, 9 bugs, 5-axis scoring, limitations
├── FINDINGS.md                            ← GAP analysis, 8 key discoveries, recommendations
├── COMPLIANCE.md                          ← Professional standards, GAAS conformance, legal disclaimers
├── SCHEMA.md                              ← Database architecture diagram
├── NETWORK.md                             ← Trust network flow diagram
├── data/
│   ├── master_wire_ledger_phase24.json    ← 481 wires (publication dataset)
│   └── entity_classification.json         ← Entity → type mapping (228 entities)
└── workbook/
    ├── EPSTEIN_FORENSIC_WORKBOOK_v7.xlsx  ← 14-tab forensic workbook
    └── forensic_workbook_v7.py            ← Python script to regenerate workbook
```

### Visual Guides

* **[SCHEMA.md](SCHEMA.md)** — Full database architecture showing how 33 tables, 11.4M entities, and 1.48M files feed into the 481-wire master ledger
* **[NETWORK.md](NETWORK.md)** — Annotated trust network flow diagram with dollar amounts on every edge

### Forensic Workbook v7 (14 Tabs)

| Tab | Name | Description |
| --- | --- | --- |
| 1 | Executive Summary | Headline $1.964B (Unverified), three-tier framework, why >100% |
| 2 | Extraction Phases | Full pipeline with running totals, bug fixes color-coded |
| 3 | **Money Flow Patterns** | Every wire classified: MONEY IN / INTERNAL MOVE / MONEY OUT |
| 4 | **Shell Trust Hierarchy** | 4-tier network with actual dollar flows per entity |
| 5 | Master Wire Ledger | 481 wires with flow direction, entity types, recovery flags |
| 6 | Above-Cap Verified | Court-verified wires above $10M ($120.6M) |
| 7 | Date Recovery | Same-amount different-date analysis (95 recovered instances) |
| 8 | Entity P&L | 228 entities with inflow/outflow/net, shell flags |
| 9 | Shell Network | Shell-involved wires, 43 shell-to-shell |
| 10 | SAR Comparison | Bank-by-bank vs FinCEN benchmarks |
| 11 | Methodology | 9 bugs documented, data sources, 10 limitations |
| 12 | Bank Coverage | 14 banks mapped with wire counts and volumes |
| 13 | Entity Resolution | 228 canonical entities with alias mapping |
| 14 | Bates Index | 51% Bates coverage with exhibit cross-references |

---

## What Makes This Different

**I didn't read the documents. I audited the money.**

Other projects in this space build search engines, write narrative reports, or create browsable archives. All valuable work. This project applies the same methodology I use in professional public-sector financial auditing — multi-affiliate reconciliation, exception reporting, variance analysis, confidence tiering — to computationally reconstruct the financial infrastructure visible in the EFTA corpus.

The question I set out to answer isn't "what do the documents say?" It's: **"Where did the money go, who moved it, and what did the DOJ redact around it?"**

---

## Why Findings Only — No Source Code or Database

This repository publishes methodology, findings, and summary data. The underlying source code, database, and raw extraction pipeline are not included. This is intentional and consistent with forensic accounting standards:

* **AICPA SSFS No. 1 (Statement on Standards for Forensic Services)** establishes that forensic practitioners maintain control over working papers, proprietary methodologies, and analytical tools. Work product privilege protects the analytical process.
* **AICPA AU-C §230 (Audit Documentation)** provides that audit documentation is the property of the practitioner and should be retained under the practitioner's control. Sufficient documentation is provided for a knowledgeable reviewer to understand the work performed.
* **Chain of custody**: The 8.03GB forensic database represents a consolidated analytical environment. Releasing it in fragments could enable miscontextualization of intermediate results without the full pipeline logic that produced them.
* **Reproducibility through transparency**: The methodology documentation, scoring weights, classification rules, and dedup logic are fully described — enabling independent replication without distributing the tooling itself.
* **Ongoing analysis**: The database and pipeline remain active analytical tools. Premature release could compromise the integrity of forthcoming data narratives and follow-on investigations.

The master wire ledger (481 wires) and entity classification data are published in full in the `data/` directory. These represent the final audited outputs and are sufficient for independent verification of all published findings.

---

## Author

**Randall Scott Taylor**
Director of Finance Administration, large municipal government agency
BS Network & Cyber Security, Wilmington University
MS Applied Data Science, Syracuse University

I built this project — every line of extraction code, every database table, every classification rule, every phase of the pipeline — as a solo effort over 200+ hours across 80+ sessions. AI tools (Claude, Anthropic) were used for development acceleration and quality assurance, the same way a solo practitioner might use a calculator or reference library. The analytical judgments, methodology design, and forensic interpretations are mine.

Professional background: multi-affiliate financial reconciliation, budget auditing, automated classification and exception reporting systems, and large-scale fiscal operations for institutional financial data.

---

## Ethical Standards

* **Victim protection**: No victim names, identifying details, or testimony content is stored, published, or extractable from any output. Victim-adjacent redactions are noted by proximity only.
* **SSFS alignment**: All outputs include frozen Row 1 caveats, (Unverified) column tags, and navigational-tool disclaimers consistent with professional standards.
* **No attribution of guilt**: Financial flows are documented as they appear in DOJ documents. Appearance in this analysis does not imply wrongdoing.
* **Open methodology**: Every extraction rule, scoring weight, and classification threshold is documented and reproducible.

---

## Disclaimer

This analysis does not constitute an audit, examination, or review performed in accordance with GAAS, GAGAS, or AICPA SSFS No. 1. See **[COMPLIANCE.md](COMPLIANCE.md)** for a detailed discussion of applicable professional standards and how this analysis relates to them.

All financial amounts are (Unverified) automated extractions unless explicitly noted otherwise. Entity classifications are based on OCR text extraction with automated normalization and may contain errors. Shell entity designations are analytical classifications, not legal determinations.

---

## Citation

```
Taylor, R.S. (2026). Epstein Financial Forensics: Automated forensic financial
reconstruction from 1.48 million DOJ EFTA documents. GitHub.
https://github.com/randallscott25-star/epstein-forensic-finance
```

---

## License

This work is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).

The underlying DOJ documents are U.S. government publications in the public domain. This repository contains only metadata, extracted analysis, and methodology — no copyrighted source material is reproduced.

---

## Project Timeline

| Date | Milestone |
| --- | --- |
| Feb 7, 2026 | Project started — DOJ scraper built, first dataset indexed |
| Feb 8 | DS11 (76,969 financial ledgers) fully scraped |
| Feb 10 | 633,842 files indexed — published to GitHub and Archive.org |
| Feb 12 | Phase 3 text extraction complete (513K files) |
| Feb 14 | Entity extraction (3B) launched — 565K files queued |
| Feb 15 | Corpus expanded to 1.48M files + 503K media with DS10 + community gap-fill |
| Feb 16 | Phase 5 financial analysis chain operational |
| Feb 18 | 19 datasets online (DS1-12 + DS98-DS104) |
| Feb 20 | Fund flows audit v6.2: $1.43B in P+S transactions, 39% SAR coverage |
| Feb 21 | Wire extraction pipeline (Phases 14-24): $1.964B, 104.6% SAR coverage |
| Feb 21 | Forensic workbook v6.1 published (11 tabs, 382-wire master ledger) |
| Feb 22 | Repository made public. 30 GitHub stars in 5 hours. |
| Feb 24 | Phase 5I: 481 wires, $973M entity-resolved, 228 entities, 14-bank coverage, 51% Bates |
| Feb 24 | Workbook v7 published (14 tabs). Full database audit: 33 tables, 8.03GB, 26.6M rows |
| Ongoing | Data narratives and follow-on analysis |



---
