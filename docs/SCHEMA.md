# Database Architecture

**8GB SQLite · 36 Tables · 19 Datasets · 11.4M Entities · 1.48M Files**

> This is not a search index. This is a relational forensic database designed to model financial flows, entity networks, and redaction patterns across the largest public corpus of Epstein-related documents.

---

## Architecture Overview

```
EPSTEIN FORENSIC DATABASE (8GB)
│
├── CORPUS LAYER (1.48M files)
│   ├── files ─────────────────────── 1,476,377 records
│   │   ├── file_id, efta_number
│   │   ├── dataset (DS1-12, DS98-104)
│   │   ├── doc_type, classification
│   │   ├── extracted_text
│   │   └── date_range
│   │
│   ├── dates_found ───────────────── Temporal mapping across corpus
│   │   └── Links files → date references
│   │
│   └── media_evidence ────────────── 503,154 images + 874 videos
│       ├── [DS10](https://www.justice.gov/epstein/doj-disclosures/data-set-10-files) evidence catalog
│       ├── image classification
│       └── metadata extraction
│
├── ENTITY INTELLIGENCE LAYER (11.4M entities)
│   ├── entities ──────────────────── 11,438,106 extracted entities
│   │   ├── name (normalized)
│   │   ├── raw_name (OCR original)
│   │   ├── entity_type (PERSON / ORG / GPE / UNKNOWN)
│   │   ├── mention_count
│   │   └── datasets (comma-separated)
│   │
│   ├── poi_rankings ──────────────── Persons of interest
│   │   ├── Multi-axis corpus frequency scoring
│   │   ├── News-filtered (removes media noise)
│   │   └── Cross-dataset presence weighting
│   │
│   └── evidence_index ────────────── Evidentiary chains
│       └── Document-to-document linking
│
├── FINANCIAL ANALYSIS LAYER (105,000+ records)
│   │
│   ├── RAW EXTRACTION
│   │   ├── financial_hits ────────── 35,375 keyword-flagged records
│   │   │   ├── keyword (wire_transfer, fedwire, SWIFT, routing)
│   │   │   ├── context (±500 chars surrounding text)
│   │   │   ├── extracted_amount
│   │   │   └── source_file → files.file_id
│   │   │
│   │   └── financial_redactions ──── Redacted financial content
│   │       └── Tracks what was hidden near financial data
│   │
│   ├── CLASSIFIED FLOWS
│   │   ├── fund_flows ────────────── 23,832 directional A→B flows
│   │   │   ├── entity_from → entity_to
│   │   │   ├── amount, date
│   │   │   ├── raw_text (original OCR)
│   │   │   └── source_file → files.file_id
│   │   │
│   │   └── fund_flows_audited ────── 7,355 confidence-scored flows
│   │       ├── entity_from → entity_to
│   │       ├── amount, date
│   │       ├── tier (PROVEN / STRONG / MODERATE / WEAK / VERY_WEAK)
│   │       ├── wire_indicator (Fedwire / SWIFT / IMAD / credit_advice)
│   │       ├── 5-axis confidence score
│   │       │   ├── context_language (×3 weight)
│   │       │   ├── amount_specificity (×1)
│   │       │   ├── date_presence (×1)
│   │       │   ├── entity_quality (×2)
│   │       │   └── source_doc_type (×1)
│   │       └── category (wire_transfer / check / ach / balance)
│   │
│   ├── VERIFIED SOURCES
│   │   ├── verified_wires ────────── 185 court-exhibit authenticated
│   │   │   ├── entity_from → entity_to
│   │   │   ├── amount, date
│   │   │   ├── exhibit (A, B, C — Alfano exhibits)
│   │   │   ├── bates_number (DB-SDNY-#######)
│   │   │   └── source_bank
│   │   │
│   │   └── trust_transfers ───────── Trust-to-trust records
│   │       ├── trust_from → trust_to
│   │       ├── amount, date
│   │       └── document_ref
│   │
│   ├── EXTERNAL BENCHMARKS
│   │   ├── fincen_transactions ───── FinCEN SAR cross-reference
│   │   │   └── Bank-reported suspicious activity
│   │   │
│   │   └── fincen_bank_connections ─ Bank relationship mapping
│   │       └── Regulatory filing data
│   │
│   └── MASTER OUTPUT
│       ├── publication_ledger ────── 6,310 Phase 5L transactions ★★
│       │   ├── entity_from → entity_to
│       │   ├── amount, date, payment_type
│       │   ├── tier (T1/T2/T3/T4 — GAGAS-aligned)
│       │   │   └── T1: Epstein-Controlled ($1.61B)
│       │   │   └── T2: Known Associates ($343M)
│       │   │   └── T3: Extended Network ($7.6M)
│       │   │   └── T4: Unclassified ($185M)
│       │   ├── source_exhibit, bates_number
│       │   └── dedup_key (amount + entity_pair + date)
│       │
│       ├── master_wire_ledger ────── 481 Phase 5I-audited wires ★
│       │   ├── entity_from → entity_to
│       │   ├── amount, date
│       │   ├── source (verified_wires / audited_PROVEN / audited_STRONG)
│       │   ├── exhibit (if court-verified)
│       │   ├── from_type → entity classification
│       │   │   └── EPSTEIN_ENTITY / EXTERNAL_PARTY / BANK_CUSTODIAN
│       │   ├── to_type → entity classification
│       │   ├── flow_direction
│       │   │   └── MONEY_IN / INTERNAL_MOVE / MONEY_OUT /
│       │   │       BANK_SHELL / SHELL_BANK / PASS_THROUGH
│       │   ├── is_date_recovery (Phase 23)
│       │   ├── is_above_cap (Phase 24)
│       │   └── is_phase25_recovery (Phase 25 date recovery)
│       │
│       ├── verified_bank_statements ── 1,202 multi-bank transactions
│       │   ├── bank, statement_date, amount
│       │   └── balance_context, source_file
│       │
│       ├── payment_type_registry ──── 10 classified payment types
│       │   └── wire, CHIPS, SWIFT, check, bank_statement, etc.
│       │
│       └── dedup_audit_log ───────── Dedup decision trail
│           └── Publication ledger assembly audit
│
├── REDACTION ANALYSIS LAYER
│   ├── redaction_recovery ────────── Content under redaction overlays
│   │   ├── Recovered text fragments
│   │   └── Interest scoring
│   │
│   ├── redaction_markers ─────────── Position tracking
│   │   ├── Page-level redaction mapping
│   │   └── Proximity to financial data
│   │
│   └── redaction_summary ─────────── Per-document aggregation
│       ├── total_redactions per EFTA number
│       ├── bad_redactions (recoverable)
│       └── proper_redactions (secure)
│
└── EXTERNAL CROSS-REFERENCE LAYER
    ├── FAA AIRCRAFT REGISTRY
    │   ├── faa_master ────────────── Aircraft registrations
    │   ├── faa_engine ────────────── Engine records
    │   └── faa_acftref ──────────── Aircraft reference data
    │       └── Flight tracking cross-reference
    │
    └── ICIJ OFFSHORE LEAKS
        ├── icij_entities ─────────── Offshore entity records
        ├── icij_officers ─────────── Officer/director records
        └── icij_relationships ────── Entity relationship mapping
            └── Shell company cross-referencing
```

---

## Data Flow: From Raw Files to Master Ledger

```
1.48M DOJ FILES
     │
     ▼
┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│   OCR Text   │───▶│  Keyword     │───▶│  financial    │
│  Extraction  │    │  Matching    │    │  _hits        │
│  (Tesseract) │    │  (regex)     │    │  35,375 rows  │
└─────────────┘    └──────────────┘    └───────┬───────┘
                                               │
     ┌─────────────┐                           ▼
     │   spaCy NLP  │    ┌──────────────────────────────┐
     │  11.4M       │───▶│        fund_flows             │
     │  entities    │    │     23,832 directional A→B    │
     └─────────────┘    └──────────────┬───────────────┘
                                       │
                                       ▼  5-Axis Scoring
                              ┌────────────────────┐
                              │  fund_flows_audited │
                              │  7,355 classified   │
                              │  PROVEN: 322        │
                              │  STRONG: 2,851      │
                              │  MODERATE: 4,182    │
                              └────────┬───────────┘
                                       │
     ┌─────────────┐                   │
     │  verified    │                  │
     │  _wires      │─────────────┐    │
     │  185 court-  │             │    │
     │  exhibit     │             ▼    ▼
     └─────────────┘    ┌────────────────────────┐
                        │   24-PHASE EXTRACTION   │
     ┌─────────────┐    │   PIPELINE              │
     │  trust      │───▶│                         │
     │  _transfers │    │   Amount dedup          │
     └─────────────┘    │   Entity classification │
                        │   Chain-hop removal     │
                        │   Date-aware census     │
                        │   Custodian audit       │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │   MASTER WIRE LEDGER   │
                        │   481 audited wires    │
                        │   $973,392,414       │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │   PUBLICATION LEDGER   │
                        │   6,310 transactions   │
                        │   $2,308,000,502     │
                        │   122.8% SAR (T1-T3)   │
                        └────────────────────────┘
```

---

## Table Counts Summary

| Layer | Tables | Total Records |
|-------|-------:|-------------:|
| Corpus Infrastructure | 3 | 1,980,405 |
| Entity Intelligence | 3 | 11,438,000+ |
| Financial Analysis — Raw | 2 | 35,375+ |
| Financial Analysis — Classified | 2 | 31,187 |
| Financial Analysis — Verified | 2 | 1,387 |
| Financial Analysis — Benchmarks | 2 | Variable |
| Financial Analysis — Output | 5 | 8,000+ |
| Redaction Analysis | 3 | Variable |
| External Cross-Reference | 14 | Variable |
| **Total** | **36** | **13,000,000+** |
