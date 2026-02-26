# Epstein Financial Forensics

**Automated forensic financial reconstruction from 1.48 million DOJ EFTA documents + 503K cataloged media items**

![Visitors](https://komarev.com/ghpvc/?username=randallscott25-star&label=visitors&color=555555&style=flat)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## What This Is

This repository contains the methodology, findings, and documentation for a computational forensic analysis of the U.S. Department of Justice's Epstein Files Transparency Act (EFTA) corpus.

I built this project as a solo effort — writing all extraction code, designing the database schema, developing the financial classification pipeline, and performing the forensic analysis myself, with AI assistance for development acceleration and quality assurance. The underlying methodology draws from my professional background in multi-affiliate financial reconciliation, budget variance analysis, and automated exception reporting at institutional scale.

To my knowledge, this represents the first systematic attempt to reconstruct the complete financial infrastructure visible in the EFTA corpus using quantitative forensic methods — moving beyond narrative analysis of individual documents to model the full network of fund flows, entity relationships, and shell trust hierarchies at scale. For the girls. 

---

## 📌 Start Here

### 🔺 New: Blueprint of a Financial Machine

> I audited $2.1 billion in Epstein financial records. Here's every name the money touched. 123 nodes, 313 financial links, 8 shell entities, 12 key persons, 8 operators, 5 banks — mapped across the full $2.146B corpus. **Season 1 finale.**
>
> **→ <a href="https://randallscott25-star.github.io/epstein-forensic-finance/narratives/19_grand_opus_narrative.html" target="_blank">Read Narrative 19</a>** · **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/19_blueprint_financial_machine.html" target="_blank">Interactive Visualization</a>** · **[Offshore Architecture (N18)](narratives/18_offshore_architecture.md)** · **[One-Way Money (N17)](narratives/17_the_architecture.md)**


> **19 data narratives** reconstruct how $2.146 billion moved through 14 shell entities across 8+ banking institutions. Every claim is anchored to specific court exhibits and bates stamps.
>
> **→ [Read the Data Narratives](narratives/)** · **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/shell_network.html" target="_blank">Explore the Interactive Network</a>** · **<a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">View the Forensic Workbook</a>**

| # | Narrative | Key Finding |
|---|-----------|-------------|
| 1 | [The Jeepers Pipeline](narratives/01_jeepers_pipeline.md) | $57.9M brokerage shell → personal checking, every wire dated |
| 2 | [Art Market as Liquidity Channel](narratives/02_art_market.md) | Sotheby's + Christie's proceeds entered through Haze Trust |
| 3 | [The Plan D Question](narratives/03_plan_d_question.md) | $18M out to Leon Black, near-zero inflow — where did it come from? |
| 4 | [Chain-Hop Anatomy](narratives/04_chain_hop_anatomy.md) | 4-tier shell network mapped, $311M double-counting removed |
| 5 | [Deutsche Bank's Role](narratives/05_deutsche_bank.md) | 38 wires, 75% of volume in last 6 months — and DB ranks 3rd by volume |
| 6 | [Gratitude America](narratives/06_gratitude_america.md) | 88% to investments, 7% to charity — a "charity" that isn't one |
| 7 | [Follow the Money, Follow the Plane](narratives/07_follow_the_money_follow_the_plane.md) | Wire-flight correlation at 4.3× random chance; $169M near St. Thomas flights |
| 8 | [The Infrastructure of Access](narratives/08_infrastructure_of_access.md) | The people who moved the money are the people victims named |
| 9 | [734,122 Names](narratives/09_734122_names.md) | Every person in 1.48M files scanned. 57 bridgers. No one hiding. |
| 10 | [The Round Number Problem](narratives/10_the_round_number_problem.md) | Benford's Law fails: 84.3% exact round numbers. One decision-maker. |
| 11 | [The Shell Map](narratives/11_the_shell_map.md) | 14 shells, 8 banks. Bear Stearns has 5.7× more activity than Deutsche Bank. |
| 12 | [The Bank Nobody Prosecuted](narratives/12_the_bank_nobody_prosecuted.md) | Bear Stearns: 5.7× Deutsche Bank volume, zero enforcement action |
| 13 | [Seven Banks, One Trust](narratives/13_seven_banks_one_trust.md) | Outgoing Money Trust used 7 banks for disbursement — textbook structuring |
| 14 | [Where Leon Black's Money Went](narratives/14_where_leon_blacks_money_went.md) | 1,600 files. Every shell. $60.5M in, Apollo Management out the other side |
| 15 | [Gratitude America: The Charity That Invested](narratives/15_gratitude_america.md) | Tax-exempt charity routing $2–20M to Boothbay, Honeycomb, Valar, Coatue |
| 16 | [The Accountant](narratives/16_the_accountant.md) | Richard Kahn / HBRK Associates: 18,833 emails, 11,153 files, touches every shell |
| **17** | **[One-Way Money](narratives/17_the_architecture.md)** | **$272M in. $63M out. First multi-institution balance sheet. [Visualization](https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/17_one_way_money.html)** |
| **18** | **[Offshore Architecture: The Brunel–BVI–ICIJ Bridge](narratives/18_offshore_architecture.md)** | **DOJ subpoena names BVI shell. ICIJ confirms. Scouting International — Tortola, 2003, defunct. 172 docs, 3 databases cross-referenced.** |
| **19** | **<a href="https://randallscott25-star.github.io/epstein-forensic-finance/narratives/19_grand_opus_narrative.html" target="_blank">Blueprint of a Financial Machine</a>** | **Season 1 finale. $2.146B, 123 nodes, 313 edges. Every bank, shell, operator, and key person mapped. <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/19_blueprint_financial_machine.html" target="_blank">Visualization</a>** |



## The Database

**8.03 GB | 36 tables | 26.6 million rows | 19 datasets**

| Metric | This Project | Largest Narrative Repo | Largest Search Platform | Others |
|--------|:------------:|:----------------------:|:----------------------:|:------:|
| **Total files indexed** | **1,476,377** + 503K media | 1,380,937 | 1,120,000 | < 20,000 |
| **Datasets covered** | **19** (<a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">DS1</a>-12 + DS98-104) | 12 | 12 | 1-3 |
| **Extracted text records** | **2.87M** (page-level) | 993,406 pages | — | — |
| **Entity extraction (NLP)** | **11.4M entities** | ~4,000 curated | 1,589 manual | < 500 |
| **Unique persons identified** | **734,122** | 1,536 registry | 1,589 | — |
| **Financial transactions modeled** | **81,451** (tiered) + **23,832** (directional) | ~186 normalized | 0 | 0 |
| **Directional fund flows (A→B)** | **23,832** | qualitative | 0 | 0 |
| **Wire transfers in master ledger** | **481** (Phase 5I audited) | 0 | 0 | 0 |
| **Relational database tables** | **36** | 3-4 | — | — |
| **Confidence-tiered scoring** | ✅ 5-axis | — | — | — |
| **Redaction proximity analysis** | ✅ | ✅ (different method) | — | — |
| **SAR cross-validation** | ✅ **104.4%** | — | — | — |
| **Multi-phase dedup pipeline** | ✅ 3-stage evolution | — | — | — |
| **Shell hierarchy mapping** | ✅ 4-tier | — | — | — |

> **Note:** The largest narrative repo's 1,380,937 figure counts individual *pages* as records; their unique PDF file count is ~519,548. My 1,476,377 are unique files each with a distinct DOJ URL or registered serial, plus 503,154 separately cataloged media items from <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-10-files" target="_blank">DS10</a> evidence photos and videos. Multiple projects in this space are doing valuable, complementary work — narrative forensic reporting, searchable archives, community preservation. This project's lane is systematic financial reconstruction at scale.

---

## Headline Results

> ⚠️ **All findings are navigational tools derived from automated extraction. They have not been independently verified and should not be treated as established fact. See [COMPLIANCE.md](docs/COMPLIANCE.md) for full professional standards disclaimers.**

| Metric | Value |
|--------|-------|
| **Publication Ledger Total** | **$2,146,000,000** (6,310 unique transactions) |
| **FinCEN SAR Benchmark** | $1,878,000,000 |
| **T1–T3 Coverage of SAR** | **104.4%** ($1,960,600,000) |
| **Payment Types Classified** | 10 |
| **Wire Transfers in Master Ledger** | 481 |
| **Unique Entities (Entity-Resolved)** | 228 |
| **Bank Coverage** | 14 banks |
| **Bates Number Coverage** | 51% |
| **Shell-to-Shell Transfers Identified** | 43 |
| **Shell Trust Hierarchy Tiers Mapped** | 4 |
| **Contamination Bugs Caught & Fixed** | 9 |

### Four-Tier GAGAS-Aligned Confidence Framework

| Tier | Classification | Amount | % of Total |
|------|---------------|-------:|:----------:|
| **T1** | Epstein-Controlled Entities | $1,610,000,000 | 75.0% |
| **T2** | Known Associates | $343,000,000 | 16.0% |
| **T3** | Extended Network | $7,600,000 | 0.4% |
| **T4** | Unclassified | $185,000,000 | 8.6% |
| **T1–T3** | **Auditable Subtotal** | **$1,960,600,000** | **104.4% of SAR** |
| **Total** | **Publication Ledger** | **$2,146,000,000** | — |

### Why T1–T3 Exceeds 100%

The SAR benchmark ($1.878B) represents only transactions banks flagged as **suspicious**. The EFTA corpus contains the **complete** financial record — including legitimate, non-suspicious transactions such as Sotheby's auction proceeds ($11.2M), Tudor Futures investment returns ($12.8M), Kellerhals law firm settlements ($23M), and Blockchain Capital VC investments ($10.5M). Total financial flows **should** exceed the suspicious subset. Standard forensic accounting: SAR ⊂ Total Financial Activity. The T4 (Unclassified) tier is excluded from the SAR comparison because those transactions lack sufficient entity resolution for classification.

---

## The Money Circuit: 4-Tier Trust Hierarchy

> See full annotated flow diagram: **[NETWORK.md](docs/NETWORK.md)**

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

All amounts are (Unverified) automated extractions. See [FINDINGS.md](docs/FINDINGS.md) for detailed analysis.

### Money Flow Direction Analysis

| Direction | Wires | Amount (Unverified) | Share |
|-----------|------:|-------:|------:|
| **MONEY IN** — External → Epstein entities | 91 | $232,538,043 | 41.7% |
| **INTERNAL MOVE** — Shell → Shell reshuffling | 39 | $112,610,112 | 20.2% |
| **PASS-THROUGH** — Attorney/trust administration | 130 | $72,433,003 | 13.0% |
| **MONEY OUT** — Epstein entities → External | 51 | $63,266,349 | 11.3% |
| **BANK → SHELL** — Custodian disbursements | 27 | $53,717,045 | 9.6% |
| Other (Shell→Bank, Interbank, External→Bank) | 44 | $23,504,429 | 4.2% |

### SAR Benchmark (Public Record, Independently Verified)

| Bank | Reported SARs |
|------|:------------:|
| JPMorgan Chase | ~$1.1B (4,700+ transactions) |
| Deutsche Bank | ~$400M |
| Bank of New York Mellon | ~$378M |
| **Total known SARs** | **$1.878B** |

*Sources: U.S. Senate Permanent Subcommittee on Investigations; NYDFS Consent Order (2020); JPMorgan USVI Settlement (2023)*

---

## Database Schema (36 Tables)

> See full database architecture diagram: **[SCHEMA.md](docs/SCHEMA.md)**

This is not a search index. This is a relational forensic database. **8.03 GB, 36 tables, 26.6 million rows.**

**Financial Analysis (13 tables)**
- `publication_ledger` — 6,310 deduplicated transactions ($2.146B) with four-tier GAGAS classification (T1–T4), payment type, source exhibit
- `fund_flows` — 23,832 directional money movements (entity_from → entity_to, amount, date, confidence)
- `fund_flows_audited` — 7,355 classified flows (5-tier: PROVEN/STRONG/MODERATE/WEAK/VERY_WEAK) with FinCEN/ICIJ match flags, composite scoring, entity classification
- `verified_wires` — 185 court-exhibit authenticated wire transfers (dates, bates numbers, exhibits)
- `verified_bank_statements` — 1,202 multi-bank statement transactions from 13 institutions with statement dates and balance context
- `financial_hits` — 81,451 financial content extractions across 19 categories and 3 verification tiers (C1/C2/C3)
- `financial_redactions` — 2,395 recovered dollar amounts near redaction markers with confidence scoring
- `fincen_transactions` — 4,507 FinCEN suspicious activity report transaction records
- `fincen_bank_connections` — 5,498 bank-to-bank SAR relationship mappings
- `entity_aliases` — 186 raw text → canonical name resolution rules
- `entity_roles` — 74 classified entities with total inflow, outflow, net position, wire counts, and exhibit references
- `payment_type_registry` — 10 classified payment types (wire, CHIPS, SWIFT, bank statement, check, etc.)
- `dedup_audit_log` — Deduplication decision trail for publication ledger assembly

**Entity Intelligence (3 tables)**
- `entities` — 11,438,134 extracted entities with NLP classification (PERSON, ORG, GPE, MONEY, NORP, FAC, LOC, LAW)
- `poi_rankings` — 2,000 persons of interest scored by multi-axis corpus frequency (file count, financial count, flight count, redaction dollars, direct dollars)
- `evidence_index` — 1,077,516 evidentiary chain records linking documents across datasets with bates numbers, checksums, and source types

**Redaction Analysis (3 tables)**
- `redaction_recovery` — 157,984 content fragments recovered from under redaction overlays (with financial/names/dates flags and interest scoring)
- `redaction_markers` — 140,060 systematic redaction position records across corpus
- `redaction_summary` — 131,860 aggregated redaction analysis per document

**Corpus Infrastructure (4 tables)**
- `files` — 1,476,377 file records with 30 columns: metadata, classification, dates, extraction status, doc types
- `extracted_text` — 2,866,239 page-level text records with classification and extraction method
- `dates_found` — 2,411,188 temporal references extracted across entire corpus with context
- `media_evidence` — 503,154 DS10 image/video catalog with custodian, doc_type, confidentiality markings

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
Phases 14-24  Wire Transfer Extraction Pipeline → 382-wire ledger, $1.964B
Phase 5I   Entity Resolution & Bank Expansion → 481-wire ledger, $973M entity-resolved, 14-bank coverage
Phase 5J   Multi-Bank Statement Parser → 1,202 verified transactions from 13 banks
Phase 5K   Payment Type Expansion → CHIPS, SWIFT, checks, bank statements beyond wire transfers
Phase 5L   Publication Ledger Assembly → 6,310 unique transactions, $2.146B, four-tier GAGAS framework
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
| **5L** | **Publication ledger: 6,310 unique transactions, four-tier GAGAS, T1–T3 = 104.4% SAR** | **$2.146B total** |

Full phase-by-phase details: **[METHODOLOGY.md](docs/METHODOLOGY.md)**

---

## Financial Methodology: 5-Axis Forensic Scoring

Every financial record is independently scored across five axes:

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
- **WEAK** / **VERY_WEAK** / **REJECT**: Insufficient evidence or known noise

**Validation:** v6.2 spot-check achieved 93% accuracy on top-30 PROVEN transactions (28/30), with 0% balance contamination (down from 47% in v5).

---

## GAP Analysis

### What's Still Missing

| Gap Source | Estimable? | Reason |
|-----------|:----------:|--------|
| **WEAK/VERY_WEAK tier exclusions** | **Yes — $5M-$15M** | $991M excluded as low-confidence; manual review of top entries could recover $5-15M |
| **Sealed/withheld documents** | No | Court-sealed records inaccessible to EFTA; dollar value unknown |
| **Attempted vs. completed transactions** | No | SARs count attempted; I extract completed only; gap is real but unquantifiable |
| **Destroyed pre-retention records** | No | Bank retention policies may have purged records; unquantifiable |
| **Cross-bank SAR duplication** | No (directional) | Same wire triggering SARs at both banks inflates the benchmark — *reduces* the gap |

Only one gap ($5-15M excluded tiers) has a credible dollar estimate. The others are real information gaps with unknown values. I am not going to put specific ranges on things I cannot measure.

---

## Data Narratives

**→ [Read all Data Narratives](narratives/)**

| # | Title | Key Finding | Data Scope |
|---|-------|-------------|------------|
| 1 | [The Jeepers Pipeline](narratives/01_jeepers_pipeline.md) | $57.9M brokerage shell → personal checking, all dated, all on Exhibit C | 24 wires · $57,876,640 |
| 2 | [Art Market as Liquidity Channel](narratives/02_art_market.md) | Sotheby's + Christie's proceeds entered the shell network through Haze Trust | 20 wires · $103,786,473 |
| 3 | [The Plan D Question](narratives/03_plan_d_question.md) | $18M out to Leon Black, near-zero inflow — where did Plan D get its money? | 34 wires · $163,097,604 |
| 4 | [Chain-Hop Anatomy](narratives/04_chain_hop_anatomy.md) | 4-tier shell network mapped — and $311M in double-counting removed | 67 wires · $312,796,381 |
| 5 | [Deutsche Bank's Role](narratives/05_deutsche_bank.md) | 38 wires across every major Epstein entity, 75% of volume in last 6 months | 38 wires · $56,792,936 |
| 6 | [Gratitude America](narratives/06_gratitude_america.md) | 88% of outflows to investment accounts, 7% to charitable purposes | 20 wires · $13,080,518 |
| 7 | [Follow the Money, Follow the Plane](narratives/07_follow_the_money_follow_the_plane.md) | Wire-flight temporal correlation at 4.3× random chance; $169M near St. Thomas flights | 185 wires · 321 flights · $575M |
| 8 | [The Infrastructure of Access](narratives/08_infrastructure_of_access.md) | The people who moved the money are the same people victims named — Maxwell in 204 financial docs and 1,312 victim docs | 11.4M entities · 1.48M files |
| 9 | [734,122 Names](narratives/09_734122_names.md) | Asked every person in 1.48M files who bridges financial and victim docs. 57 real names. 10 operational staff | 734,122 persons · 57 bridgers |
| 10 | [The Round Number Problem](narratives/10_the_round_number_problem.md) | Benford's Law fails: digits 2 and 5 at 29.7% and 18.4%. 84.3% of wires are exact round numbers | 185 wires · $557M |
| 11 | [The Shell Map](narratives/11_the_shell_map.md) | Wire ledger captured 7 entities. The corpus contains 14 — with 178K money references | 14 shells · 178K money refs |
| 12 | [The Bank Nobody Prosecuted](narratives/12_the_bank_nobody_prosecuted.md) | Bear Stearns had 2.4M money mentions (5.7× Deutsche Bank) — zero fines, zero investigation | 2.4M money refs · 66 shared files |
| 13 | [Seven Banks, One Trust](narratives/13_seven_banks_one_trust.md) | Outgoing Money Trust disbursed through DB, Wells Fargo, BofA, TD, JPMorgan, PNC, Sabadell | 180 financial docs · 7 banks |
| 14 | [Where Leon Black's Money Went](narratives/14_where_leon_blacks_money_went.md) | 1,600 files, every shell, "Black Family Partners LP c/o Apollo Management" — the round trip | 1,600 files · $60.5M · 7 shells |
| 15 | [Gratitude America: The Charity That Invested](narratives/15_gratitude_america.md) | Tax-exempt charity routing $2–20M to Boothbay, Honeycomb, Valar, Coatue | 89 financial · $45M wires |
| 16 | [The Accountant](narratives/16_the_accountant.md) | Richard Kahn / HBRK Associates: 18,833 emails, 11,153 files, touches every shell | 18,833 emails · 11,153 files |
| 17 | [One-Way Money](narratives/17_the_architecture.md) | $272M in. $63M out. $209M gap. First multi-institution balance sheet | 481 wires · 228 entities · $558M |
| **18** | **[Offshore Architecture: The Brunel–BVI–ICIJ Bridge](narratives/18_offshore_architecture.md)** | **DOJ subpoena names BVI shell. ICIJ Offshore Leaks confirms. 3 databases cross-referenced** | **172 docs · 3 databases · 8,526 pages** |

Source workbook: **[Forensic Workbook](https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true)** · [Interactive Shell Network](https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/shell_network.html)

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
├── narratives/                            ← 18 forensic data narratives with source appendices
├── data/
│   ├── publication_ledger_phase5l.json    ← 6,310 transactions, four-tier (publication dataset)
│   ├── master_wire_ledger_phase5i.json    ← 481 wires (wire-specific subset)
│   └── entity_classification.json         ← Entity → type mapping (228 entities)
├── visualizations/                        ← Interactive shell network diagram
└── tools/
    ├── narrative_sql_tools.py             ← SQL query functions for all 18 narrative data sources
    ├── linkify_efta.py                    ← Auto-link EFTA IDs → DOJ PDFs in .md files
    ├── convert_links_new_tab.py           ← Convert external links to target="_blank"
    ├── inject_efta_source_table.py        ← Add source document tables to narratives
    └── append_source_appendices.py        ← Append source appendices to narratives
```

### Visual Guides

- **[SCHEMA.md](docs/SCHEMA.md)** — Full database architecture showing how 36 tables, 11.4M entities, and 1.48M files feed into the 6,310-transaction publication ledger
- **[NETWORK.md](docs/NETWORK.md)** — Annotated trust network flow diagram with dollar amounts on every edge

### Forensic Workbook v9

| Tab | Name | Description |
|:---:|------|-------------|
| 1 | Executive Summary | Headline $2.146B, four-tier GAGAS framework, publication ledger |
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

**I didn't read the documents. I audited the money.**

Other projects in this space build search engines, write narrative reports, or create browsable archives. All valuable work. This project applies the same methodology I use in professional public-sector financial auditing — multi-affiliate reconciliation, exception reporting, variance analysis, confidence tiering — to computationally reconstruct the financial infrastructure visible in the EFTA corpus.

The question I set out to answer isn't "what do the documents say?" It's: **"Where did the money go, who moved it, and what did the DOJ redact around it?"**

---

## Why Findings Only — No Source Code or Database

This repository publishes methodology, findings, and summary data. The underlying source code, database, and raw extraction pipeline are not included. This is intentional and consistent with forensic accounting standards:

- **AICPA SSFS No. 1 (Statement on Standards for Forensic Services)** establishes that forensic practitioners maintain control over working papers, proprietary methodologies, and analytical tools. Work product privilege protects the analytical process.
- **AICPA AU-C §230 (Audit Documentation)** provides that audit documentation is the property of the practitioner and should be retained under the practitioner's control. Sufficient documentation is provided for a knowledgeable reviewer to understand the work performed.
- **Chain of custody**: The 8.03GB forensic database represents a consolidated analytical environment. Releasing it in fragments could enable miscontextualization of intermediate results without the full pipeline logic that produced them.
- **Reproducibility through transparency**: The methodology documentation, scoring weights, classification rules, and dedup logic are fully described — enabling independent replication without distributing the tooling itself.
- **Ongoing analysis**: The database and pipeline remain active analytical tools. Premature release could compromise the integrity of forthcoming data narratives and follow-on investigations.

The master wire ledger (481 wires) and entity classification data are published in full in the `data/` directory. These represent the final audited outputs and are sufficient for independent verification of all published findings.

---

## Author

**Randall Scott Taylor**
Director of Finance Administration, large municipal government agency
BS Network & Cyber Security, Wilmington University
MS Applied Data Science, Syracuse University

I built this project — every line of extraction code, every database table, every classification rule, every phase of the pipeline — as a solo effort. AI tools (Claude, Anthropic) were used for development acceleration and quality assurance, the same way a solo practitioner might use a calculator or reference library. The analytical judgments, methodology design, and forensic interpretations are mine.

Professional background: multi-affiliate financial reconciliation, budget auditing, automated classification and exception reporting systems, and large-scale fiscal operations for institutional financial data.

---

## Ethical Standards

- **Victim protection**: No victim names, identifying details, or testimony content is stored, published, or extractable from any output. Victim-adjacent redactions are noted by proximity only.
- **SSFS alignment**: All outputs include frozen Row 1 caveats, (Unverified) column tags, and navigational-tool disclaimers consistent with professional standards.
- **No attribution of guilt**: Financial flows are documented as they appear in DOJ documents. Appearance in this analysis does not imply wrongdoing.
- **Open methodology**: Every extraction rule, scoring weight, and classification threshold is documented and reproducible.

---

## Disclaimer

This analysis does not constitute an audit, examination, or review performed in accordance with GAAS, GAGAS, or AICPA SSFS No. 1. See **[COMPLIANCE.md](docs/COMPLIANCE.md)** for a detailed discussion of applicable professional standards and how this analysis relates to them.

All financial amounts are (Unverified) automated extractions unless explicitly noted otherwise. Entity classifications are based on OCR text extraction with automated normalization and may contain errors. Shell entity designations are analytical classifications, not legal determinations.

---

## Citation

```
Taylor, R.S. (2026). Epstein Financial Forensics: Automated forensic financial
reconstruction from 1.48 million DOJ EFTA documents. GitHub.
https://github.com/randallscott25-star/epstein-forensic-finance#readme
```

---

## License

This work is licensed under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">Creative Commons Attribution 4.0 International</a>.

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
| Feb 25 | Phase 5K–5L: Payment type expansion + publication ledger assembly. 6,310 unique transactions, $2.146B, four-tier GAGAS framework |
| Feb 25 | Workbook v9. Narratives updated to v9 voice. 18 data narratives live. |
| Feb 25 | N19: Blueprint of a Financial Machine — season 1 finale. 123 nodes, 313 edges, full $2.146B corpus mapped. 19 data narratives live. |
| Ongoing | Additional data narratives and follow-on analysis |
