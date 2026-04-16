# Epstein Financial Forensics

**Automated forensic financial reconstruction from 1.48 million DOJ EFTA documents + 503K cataloged media items.**

We took the documents the Department of Justice released under the Epstein Files Transparency Act and built a forensic financial database from scratch. Wrote all the extraction code. Designed the schema. Built the classification pipeline. Ran the analysis. Team project, start to finish. AI tools helped us write code faster — same way you'd use a calculator. The analytical calls are ours.

Our team background spans multi-affiliate financial reconciliation, budget variance analysis, automated exception reporting at institutional scale, forensic financial analysis, and legal review. We applied those same methods here.

As far as we can tell, nobody else has tried to reconstruct the complete financial infrastructure in the EFTA corpus using quantitative forensic methods. Plenty of good narrative work out there. Plenty of search engines. This is the first attempt to model the full network — fund flows, entity relationships, shell trust hierarchies — at scale.

---

## Current Status (April 16, 2026)

| Metric | Figure |
|---|---|
| Publication ledger records | **6,397** |
| Total dollar volume | **$2.308 billion** |
| Verified master wires | **481** |
| Documents indexed | 1,476,437 |
| Media items cataloged | 503,517 |
| SAR benchmark coverage | **122.9%** |
| Datasets integrated | DS1–DS12, DS98–DS104 |

Live figures: [the-projects.org/api/pub/stats](https://the-projects.org/api/pub/stats)

---

## Confidence Tier Breakdown

| Tier | Records | Total | Description |
|---|---|---|---|
| T1 — Court-verified | 3,875 | $1,661.9M | Bates-stamped bank documents, court exhibits |
| T2 — Bank-verified | 956 | $375.8M | SAR narratives, statement line items |
| T3 — Multi-source | 93 | $12.8M | Two or more independent sources |
| T4 — Unclassified | 1,473 | $257.4M | Corpus-extracted, entity resolution pending |
| **Total** | **6,397** | **$2,308.0M** | |

---

## Four-Layer Canonical Evidence Model

| Layer | Records | Total | Description |
|---|---|---|---|
| L1 — Master wire ledger | 481 | $973.4M | Individual wire transfers, fully reconciled |
| L2 — Extracted payments | 3,876 | $529.2M | Pipeline-extracted transactions, tier-classified |
| L3 — Bank statements + court-verified | 1,267 | $512.0M | Multi-bank statement parse + Phase 5C/6 FirstBank |
| L4 — Audited fund flows | 773 | $293.4M | Curated from the NLP pipeline, hand-reviewed |
| **Total** | **6,397** | **$2,308.0M** | |

The SAR benchmark ($1.878B) counts only transactions banks flagged as suspicious. The EFTA corpus holds the complete financial record — including legitimate activity like Sotheby's auction proceeds, Tudor Futures returns, Kellerhals law firm settlements, and Blockchain Capital VC investments. Total financial flows exceed the suspicious subset. Standard forensic accounting: SAR ⊂ Total Financial Activity.

---

## What Changed in April 2026

**Phase 5C — Classified transaction integration.** 438 additional records ($211.5M) from the pipeline extraction layer, classified against the publication ledger with full entity resolution.

**Phase 5D — Court exhibit integration.** 91 unique financial hits ($121.9M) with DB-SDNY exhibit numbers — including the Twitter call options purchases ($3.896M), Venezuelan PdV bonds ($2M), Blockchain Capital III ($1.875M), Joichi Ito transfers, and Leon/Debra Black trust transfers ($10M+).

**Phase 6 — FirstBank USVI.** 14 records ($4.855M) from FirstBank Virgin Islands accounts, previously identified in the corpus but not extracted.

**April 14 corpus integrity audit.** Removed $70M of noise from the ledger:
- 21 phantom summary-line records ($53.9M) — JPMorgan statement "Total Debits" rows misread by the OCR pass as transactions
- 341 reclassified interest payments ($4.0M) — moved out of the transaction ledger, into the interest ledger
- 8 cross-layer duplicates ($12.4M)

Net effect: 6,767 → 6,397 records, $2.378B → $2.308B total. Every removal is documented in the audit trail exposed at `/api/pub/stats#audit_trail`.

---

## Tier Architecture — Shell Trust Hierarchy

**Tier 1 — Holding trusts (received external deposits)**
- Southern Trust Company Inc. — $151.5M in ← Black, Rothschild, Narrow Holdings
- The 2017 Caterpillar Trust — $15.0M in ← Blockchain Capital

**Tier 2 — Distribution trusts (redistributed internally)**
- The Haze Trust (DBAGNY) — $49.7M out → Southern Financial, Southern Trust
- The Haze Trust (Checking) — $21.8M in ← Sotheby's, Christie's
- Southern Financial LLC — $14.0M in ← Tudor Futures
- Southern Financial (Checking) — $32.0M in ← Haze Trust

**Tier 3 — Operating shells (paid beneficiaries)**
- Jeepers Inc. (DB Brokerage) — $51.9M out → Epstein personal account (21 wires)
- Plan D LLC — $18.0M out → Leon Black (4 wires)
- Gratitude America MMDA — $6.3M out → Morgan Stanley, charities
- Richard Kahn (attorney) — $9.3M out → Paul Morris, others
- NES LLC — $554K out → Ghislaine Maxwell

**Tier 4 — Personal accounts (terminal destinations)**
- Jeffrey Epstein NOW/SuperNow — $83.4M in ← Jeepers, Kellerhals, law firms
- Darren Indyke operating accounts — payroll + distributions

---

## Methodology Highlights

- **Bates-stamped sourcing.** Every T1–T3 figure traces to a Bates-stamped DOJ source document. Any researcher can pull the original page by the number.
- **Verification wall.** T1–T3 figures are anchored to court exhibits and bank records. T4 holds corpus-extracted transactions where entity resolution is pending; tier labels are surfaced so readers can weight individual rows by source strength.
- **NLP phantom autopsy.** The `fund_flows_audited` pipeline generated 7,355 total records with 94.8% low confidence and $3.34 billion in phantom volume. Most of that came from emails — forwarded Bloomberg newsletters, news articles, legal memos — where the NER pass found names near dollar signs. Narrative 20 (*The Verification Wall*) documents which "hits" stand up and which collapse under Bates-stamp review.
- **Standard forensic accounting framework.** GAAS/GAGAS reference standards, AICPA SSFS No. 100 for forensic services, consistent confidence tiers across all dollar attributions.

---

## Where This Fits

Other projects in this space are doing solid work — narrative forensic reporting, searchable archives, community preservation. Our lane is systematic financial reconstruction at scale.

| Approach | Output | Our relationship |
|---|---|---|
| Narrative forensic reporting | Article-length investigations | We cite; we don't duplicate |
| Searchable archives | Full-text search of the corpus | Complementary — different primitive |
| Network mapping | Who's connected to whom | Complementary — we prove the transactions |
| **This repo** | **Certified forensic ledger + entity-resolved fund flows** | — |

Rachel Hurley's GriftMatrix maps who's connected to whom. We prove the transactions and document the conduct. One-liner: *Rachel maps the network; we prove the transactions and document the conduct.*

---

## Disclaimer

> Findings are tier-labeled. T1–T3 figures are anchored to court exhibits and Bates-stamped DOJ source documents. T4 holds corpus-extracted transactions pending full entity resolution. See `COMPLIANCE.md` for full professional standards disclaimers.

Analysis conducted under GAAS/GAGAS standards with reference to AICPA SSFS No. 100. All dollar figures are derived from publicly released DOJ documents and court filings.

---

## Versioning Note

If you are forking, archiving, or citing this work: snapshots capture a moment in time. Do not treat cached versions as authoritative. Always reference the live repository at `github.com/randallscott25-star/epstein-forensic-finance` for current figures, or the live API at `the-projects.org/api/pub/stats`.

**Last validated:** April 16, 2026.

---

## Citation

Taylor, R.S. (2026). *Epstein Financial Forensics: Automated forensic financial reconstruction from 1.48 million DOJ EFTA documents.* GitHub. https://github.com/randallscott25-star/epstein-forensic-finance#readme

## License

This work is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). The underlying DOJ documents are U.S. government publications in the public domain. This repository contains only metadata, extracted analysis, and methodology — no copyrighted source material is reproduced.
