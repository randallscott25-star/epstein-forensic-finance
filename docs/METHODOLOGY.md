# Methodology

> This document describes the forensic extraction pipeline used to reconstruct Epstein-related financial activity from the DOJ EFTA corpus. See [COMPLIANCE.md](COMPLIANCE.md) for applicable professional standards.

## Overview

This document describes the extraction pipeline I built to identify and quantify financial transactions from 1,476,437 files across 19 DOJ EFTA datasets. The pipeline produced a publication ledger of **6,397 unique transactions** totaling **$2,308,000,502** across 10 payment types. The auditable subtotal (Tiers 1–3) reaches **$2,037,759,306** — 122.8% of the $1.878 billion FinCEN SAR benchmark.

I wrote all extraction code, designed the database schema, and performed the forensic analysis as a solo effort, with AI assistance (Claude, Anthropic) for development acceleration and quality assurance. The full database architecture is documented in **[SCHEMA.md](SCHEMA.md)**.

---

## Data Sources

### DOJ EFTA Corpus

| Metric | Value |
|--------|------:|
| Total files indexed | 1,476,437 + 503,154 media |
| Datasets | 19 (<a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">DS1</a>-12 + DS98-104) |
| Extracted text records | 1.48M+ |
| Entity extraction (spaCy NLP) | 11,438,106 entities |
| Unique persons identified | 734,122 |
| Database size | 8GB SQLite |
| Relational tables | 36 |

### Structured Database Tables Used in Wire Extraction

| Table | Rows | Description | Quality |
|-------|-----:|-------------|---------|
| `verified_wires` | 185 | Court-exhibit authenticated wire transfers (Alfano exhibits, DB-SDNY) | Gold standard — dates, bates numbers, exhibits |
| `fund_flows_audited` | 7,355 | 5-tier classified financial flows (PROVEN/STRONG/MODERATE/WEAK/VERY_WEAK) | Audited — entity-pair matching, context scoring |
| `fund_flows` | 16,677 | Raw financial flows before classification | Unfiltered — contains balances, noise |
| `financial_hits` | 35,375 | Keyword-flagged financial references | Mixed — wire_transfer category filtered |
| `trust_transfers` | Variable | Trust-to-trust transfer records | Structured — trust administration records |

### FinCEN SAR Benchmark

| Bank | SAR Amount | Source |
|------|----------:|--------|
| JPMorgan Chase | $1,100,000,000 | U.S. Senate Permanent Subcommittee on Investigations |
| Deutsche Bank | $400,000,000 | FinCEN SAR filings |
| BNY Mellon | $378,000,000 | FinCEN SAR filings |
| **Combined** | **$1,878,000,000** | |

*Sources: NYDFS Consent Order (2020); JPMorgan USVI Settlement (2023)*

---

## 5-Axis Forensic Scoring

Every financial record extracted from the EFTA corpus is independently scored across five axes before entering the wire extraction pipeline:

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

## Extraction Pipeline

### Phase-by-Phase Log

| Phase | Description | Amount | Running Total | % SAR | Quality Gate |
|-------|-------------|-------:|--------------:|------:|-------------|
| v2 | Core OCR Extraction | +$1,204,000,000 | $1,204,000,000 | 64.1% | Amount-unique dedup |
| BF adj | Butterfly Trust Correction | -$63,000,000 | $1,141,000,000 | 60.8% | Manual review |
| v3.2 | 7-Layer Wire Expansion | +$237,452,186 | $1,378,452,186 | 73.4% | 7-layer proximity filter |
| 14.5 | Known Entity Fund Flows | +$90,936,712 | $1,469,388,898 | 78.2% | Entity name match |
| **14.5B** | **Balance Contamination Fix** | **-$53,766,217** | $1,415,622,681 | 75.4% | **BUG FIX** |
| 15E | Fund Flows Real Wires | +$14,000,000 | $1,429,622,681 | 76.1% | Wire keyword required |
| 15F | Redaction Recovery | +$368,170 | $1,429,990,851 | 76.1% | Proximity scan |
| 16.1 | Transaction-Line Parser | +$78,547,827 | $1,508,538,678 | 80.3% | Format validation |
| 16.2 | Round-Wire Extractor | +$4,975,350 | $1,513,514,028 | 80.6% | Round-amount + context |
| 17 | Trust Transfers + <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">DS8</a> | +$12,720,752 | $1,526,234,780 | 81.3% | Table structure |
| 18 | Full Category Sweep | +$3,854,313 | $1,530,089,093 | 81.5% | Category filter |
| **19** | **Audited PROVEN Fix** | **+$59,524,629** | $1,589,613,722 | 84.6% | **BUG FIX** |
| 20A | Verified Wires (amount-new) | +$53,093,926 | $1,642,707,648 | 87.5% | Court-exhibit verified |
| 21A/B | STRONG/MODERATE New Amounts | +$9,641,465 | $1,652,349,113 | 88.0% | Wire indicator + tier |
| **23** | **Date-Aware Wire Census** | **+$191,304,691** | $1,843,653,804 | 98.2% | **Date dedup** |
| **24** | **Above-Cap Verified Wires** | **+$120,575,938** | $1,964,229,742 | 104.6% | **Court-exhibit verified** |
| **25** | **Date Recovery from Context** | **+75 dates, $0 Δ** | $1,964,229,742 | 104.6% | **Source context parsing, 0 collisions** |
| **5I** | **Entity Resolution & Bank Expansion** | **481 wires, 228 entities, 14 banks** | $973,392,414 (entity-resolved) | — | **Entity classification + custodian audit** |
| **5J** | **Multi-Bank Statement Parser** | **+1,202 transactions from 13 banks** | +$430K verified statements | — | **Statement-level verification** |
| **5K** | **Payment Type Expansion** | **CHIPS, SWIFT, checks, bank statements** | 10 payment types | — | **Beyond wire transfers** |
| **5L** | **Publication Ledger Assembly** | **6,310 unique → 6,397 post-audit** | $2.146B → **$2.308B** | 122.9% | **T1–T3 GAGAS tiering** |
| **5C (April)** | **Classified transaction integration** | **+438 records** | +$211.5M | — | **Pipeline extraction, tier-classified** |
| **5D (April)** | **Court exhibit integration** | **+91 records** | +$121.9M | — | **DB-SDNY exhibit numbers** |
| **6 (April)** | **FirstBank USVI integration** | **+14 records** | +$4.9M | — | **Virgin Islands accounts** |
| **Audit (April 14)** | **Corpus integrity audit** | **-370 records, -$70M** | **$2.308B / 6,397** | 122.9% | **Phantom removal + reclassification** |

### April 2026 Audit

The April 14 corpus integrity audit removed $70M of noise from the ledger after Phase 5C/5D/6 were applied:

- **21 phantom summary-line records** (-$53.9M) — JPMorgan statement "Total Debits" rows misread by the OCR pass as transactions
- **341 reclassified interest payments** (-$4.0M) — moved out of the transaction ledger, into a separate interest ledger
- **8 cross-layer duplicates** (-$12.4M) — same transaction appearing in both L2 and L3

Net effect: 6,767 → 6,397 records, $2.378B → $2.308B total. Every removal is documented in the audit trail exposed at `/api/pub/stats#audit_trail`.

---

## Four-Layer Canonical Evidence Model (Post-April 2026)

Post-audit, the 6,397-record ledger is organized into four canonical evidence layers:

| Layer | Records | Total | Source |
|-------|--------:|------:|--------|
| L1 — Master wire ledger | 481 | $973.4M | Individual wire transfers, fully reconciled (Phase v2-24) |
| L2 — Extracted payments | 3,876 | $529.2M | Pipeline-extracted transactions, tier-classified (Phase 5I) |
| L3 — Bank statements + court-verified | 1,267 | $512.0M | Multi-bank statement parse + Phase 5C/6 FirstBank |
| L4 — Audited fund flows | 773 | $293.4M | Curated from the NLP pipeline, hand-reviewed |
| **Total** | **6,397** | **$2,308.0M** | |

---

## Deduplication Strategy

### Dedup Evolution

**Stage 1 (Phases v2-20): Amount-Only Dedup**
Each unique dollar amount was counted once, regardless of entity pairs or dates. Maximally conservative but destroyed legitimate repeat wires.

**Stage 2 (Phase 23): Date-Aware Census**
I added date as a dedup dimension: `(amount, entity_from, entity_to, date)`. This recovered 95 same-amount different-date wires worth $189M.

**Stage 3 (Phase 24): Verified-Tier Cap Removal**
I removed the $10M safety cap for court-exhibit verified wires. All 8 above-cap entries had exhibit numbers, bates stamps, dates, and named counterparties.

**Stage 4 (Phase 25): Date Recovery from Source Context**
I queried source database tables (`fund_flows_audited.date_ref`, `fund_flows_audited.context_snippet`, `verified_wires.date`, `fund_flows.context`) to recover dates for 75 previously undated wires — improving date coverage from 31.9% to 51.6%. Zero collisions with existing dated entries confirmed that all undated wires were genuinely unique, validating the earlier dedup methodology. Credit: u/miraculum_one (Reddit) identified that dates were present in context fields.

**Stage 5 (April 2026 audit): Cross-Layer Duplicate Removal**
The April 14 integrity audit identified 8 cross-layer duplicates — transactions appearing in both L2 (extracted payments) and L3 (bank statements) that represented the same underlying wire. These were resolved to the higher-confidence L3 record.

### Entity Classification

| Type | Description | Examples |
|------|-------------|---------|
| **EPSTEIN ENTITY** | Controlled trusts, shells, personal accounts | Southern Trust, Jeepers Inc., Plan D LLC |
| **EXTERNAL PARTY** | Investors, beneficiaries, counterparties | Leon Black, Sotheby's, Tudor Futures |
| **BANK/CUSTODIAN** | Financial institutions intermediating transfers | Deutsche Bank, JPMorgan, HSBC |
| **UNKNOWN** | Unclassifiable short strings or OCR artifacts | — |

Entity normalization handled 178+ OCR variants (e.g., "JJEFFREY EPSTEIN" → "Jeffrey Epstein", "GHISLA1NE MAXWELL" → "Ghislaine Maxwell").

---

## Contamination Bugs Found & Fixed

Nine data quality issues were identified and corrected during the pipeline:

| # | Phase | Bug | Impact | What Went Wrong | How Fixed |
|---|-------|-----|--------|-----------------|-----------|
| 1 | 14.5B | Balance Contamination | -$53.8M | Running statement balances extracted as wire amounts | `is_balance` flag; excluded from subsequent phases |
| 2 | 16.1 | Brokerage Noise | -$155M | Securities language mixed with wire data | BROKERAGE_NOISE regex filter |
| 3 | 19 | Self-Dedup Bug | +$59.5M | Table checking new entries against itself | Fixed dedup reference to prior-phase JSON only |
| 4 | 20D | Amount-Only Dedup | +$115M | Same amount, different entity pairs collapsed | Entity-pair aware dedup (created Bug 5) |
| 5 | 22 | Chain-Hop Inflation | -$311M | $10M through 4 entities counted as $40M | INTERNAL entity taxonomy; excluded internal hops |
| 6 | 22 | Cross-Table Name Duplication | Risk flagged | Same wire as "Leon & Debra Black" and "LEON_BLACK" | Three-tier confidence framework |
| 7 | 22 | Statement Noise as Entities | -$59M | "Balance Transfers", "Gift Cards" as wire entities | STATEMENT_NOISE filter; 188 entries removed |
| 8 | 23 | Date-Blind Dedup | +$189M | Four $10M wires on different dates counted as one | Date-aware master ledger composite key |
| 9 | 24 | Arbitrary Cap + Custodian | +$120.6M / -$113.4M | $10M cap excluded verified wires; "(DBAGNY)" misclassified | Cap removed for verified tier; custodian audit |

### Post-Phase-24 Audit Findings (April 2026)

| # | Issue | Impact | Resolution |
|---|-------|--------|-----------|
| 10 | Phantom summary lines | -$53.9M | 21 JPMorgan "Total Debits" rows misread as transactions; removed |
| 11 | Interest misclassification | -$4.0M | 341 interest payments reclassified out of the transaction ledger |
| 12 | Cross-layer duplicates | -$12.4M | 8 transactions appearing in both L2 and L3; consolidated to higher-confidence record |

---

## Limitations

1. **Solo practitioner**: No segregation of duties or independent partner review. AI-assisted QA provides partial mitigation.
2. **OCR quality varies**: Some amounts may be misread from scan artifacts (e.g., $1M vs $10M) — detected and corrected when flagged.
3. **Entity normalization is imperfect**: Some entities may be misidentified or incorrectly merged across OCR variants.
4. **Sealed documents are inaccessible**: Court-sealed records cannot be extracted. The dollar value of sealed financial activity is unknown.
5. **SAR vs. completed transactions**: The SAR benchmark counts **attempted** suspicious transactions; I extract **completed** wire transfers.
6. **Destroyed records**: Pre-retention period records may have been destroyed. The dollar value is unquantifiable from the EFTA corpus.
7. **Cross-table name overlap**: Same wire may appear with different entity formatting across database tables — resolved at ledger assembly via the dedup rules.
8. **Chain-hop filtering trade-offs**: Some legitimate multi-step transactions may have been excluded by the internal entity filter.
9. **Date coverage**: 350 of 481 master ledger entries have dates (72.8%) after Phase 5I entity resolution. The remaining 131 undated entries carry higher duplication risk, though zero-collision validation confirmed all undated wires were genuinely unique.

---

## Tools & Infrastructure

- **Language**: Python 3.12
- **Database**: SQLite (8GB, 36 tables, 19 datasets)
- **NLP**: spaCy entity extraction (11.4M entities, 734K persons)
- **OCR Processing**: Tesseract-based text extraction with custom noise filters
- **Analysis**: pandas, openpyxl, json
- **Scoring**: 5-axis forensic confidence scoring (v6.2, 93% PROVEN accuracy)
- **AI Assistance**: Claude (Anthropic) — development acceleration and quality assurance
- **Version Control**: Git/GitHub
- **Total effort**: ~300+ hours across 100+ sessions (February 7 – April 16, 2026), solo practitioner
