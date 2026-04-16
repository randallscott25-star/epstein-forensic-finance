# Professional Standards & Compliance

> This document describes the professional standards framework applicable to this analysis, how the work relates to those standards, and the limitations that apply. This is not a legal opinion.

---

## Nature of This Engagement

This project is a **pro bono public interest forensic analysis** of publicly available government documents. It was conducted by a single practitioner as an independent research effort — not under engagement by a client, not as part of litigation support, and not as a commissioned audit.

The analysis applies financial auditing methodology to publicly released DOJ EFTA documents to reconstruct fund flows and entity relationships visible in the corpus. It produces quantitative findings with tier-labeled source strength.

---

## Applicable Professional Standards

### AICPA Statement on Standards for Forensic Services (SSFS) No. 1

**What it governs:** Forensic accounting engagements including litigation support, expert testimony, and investigative accounting.

**How this analysis relates:**

While SSFS No. 1 formally applies to AICPA members performing forensic services under client engagement, I have voluntarily adopted its principles as a quality framework:

| SSFS Principle | How This Analysis Conforms |
|----------------|---------------------------|
| **Professional competence** | Practitioner holds MS Applied Data Science and professional experience in multi-affiliate financial reconciliation and budget auditing |
| **Due professional care** | 12 contamination/integrity issues identified and corrected across the pipeline and post-audit review; four-tier GAGAS-aligned confidence framework; 9 limitations documented |
| **Planning and supervision** | 25+ phase pipeline with quality gates at each stage; dedup evolution across five methodological generations (amount-only → date-aware → verified-tier → context-recovery → cross-layer) |
| **Sufficient relevant data** | 1,476,437 files across 19 datasets; 6,397 publication ledger transactions; 481 wire transfers; 185 court-exhibit verified wires |
| **Documentation** | Complete methodology published; every extraction rule, scoring weight, and classification threshold documented |
| **Communication of results** | All outputs are tier-labeled (T1–T4) for source strength; no attribution of guilt |

**What this analysis is NOT:** This is not a forensic engagement performed under SSFS No. 1. I am not engaged by a client. The analysis does not produce expert testimony or litigation support. It produces research findings for public interest purposes.

---

### Generally Accepted Auditing Standards (GAAS)

**What it governs:** Financial statement audits performed by CPAs.

**How this analysis relates:**

GAAS applies to audits of financial statements by independent auditors. This analysis is not a financial statement audit. However, the following GAAS principles informed the methodological design:

| GAAS Standard | Application in This Analysis |
|---------------|------------------------------|
| **General Standard 1: Training & Proficiency** | Practitioner's professional background in institutional financial data analysis, automated classification systems, and multi-affiliate reconciliation |
| **General Standard 2: Independence** | No financial relationship with any entity in the dataset; no engagement by any party; no compensation received |
| **General Standard 3: Due Care** | Multiple quality gates; contamination bug detection; conservative bias in classification (excluding WEAK/VERY_WEAK tiers worth $991M); April 2026 post-audit integrity review |
| **Fieldwork Standard 1: Planning** | Structured 25+ phase pipeline with defined scope, data sources, and extraction rules at each phase |
| **Fieldwork Standard 2: Internal Control** | Five-stage dedup evolution (amount-only → date-aware → verified-tier → context-recovery → cross-layer); entity classification audit; custodian suffix audit; cross-layer dedup audit |
| **Fieldwork Standard 3: Evidence** | Court-exhibit verified wires (122 entries with bates stamps); 5-axis confidence scoring; cross-table reconciliation |
| **Reporting Standard 1: GAAP Conformity** | N/A — no financial statements are produced |
| **Reporting Standard 2: Consistency** | Consistent methodology applied across all phases; documented deviations (Phase 22 chain-hop removal, Phase 24 cap removal, Phase 25 date recovery, Phase 5L publication ledger assembly, April 2026 integrity audit) |
| **Reporting Standard 3: Disclosure** | 9 limitations documented; tier labels (T1–T4) on all amounts for source-strength disclosure; bug fixes and integrity removals disclosed with impact amounts |
| **Reporting Standard 4: Opinion** | **No opinion is expressed.** This analysis produces findings, not audit opinions. |

**Critical limitation:** This analysis does not conform to GAAS and does not purport to. No audit opinion is expressed. No financial statements are examined. The GAAS framework is referenced solely to demonstrate that recognized auditing principles informed the methodology.

---

### Generally Accepted Government Auditing Standards (GAGAS / Yellow Book)

**What it governs:** Audits of government entities and programs, and audits performed by government auditors.

**How this analysis relates:**

GAGAS (issued by the U.S. Government Accountability Office) applies to government audits and attestation engagements. This analysis is not a government audit. However, GAGAS principles relevant to the public interest nature of this work include:

| GAGAS Principle | Application |
|-----------------|-------------|
| **Public interest** | Analysis conducted pro bono to increase public understanding of publicly released government documents |
| **Transparency** | Complete methodology published; classification rules documented; limitations disclosed; integrity audit trail exposed via live API |
| **Independence** | No financial or personal relationship with any entity in the dataset |
| **Professional judgment** | Four-tier GAGAS-aligned confidence framework reflects graduated certainty; T4 (Unclassified, $257M) excluded from SAR comparison |

**Critical limitation:** This analysis does not conform to GAGAS and does not purport to. It is not a government audit.

---

### AU-C §230: Audit Documentation

**What it governs:** Documentation standards for audit engagements.

**Relevance to work product protection:**

AU-C §230 establishes that audit documentation is the **property of the practitioner** and should be retained under the practitioner's control. While this analysis is not an audit, the same principle applies to forensic work product:

- The 8GB forensic database, extraction code, and analytical pipeline constitute **practitioner work product**
- SSFS No. 1 recognizes that forensic practitioners maintain **proprietary methodologies and analytical tools**
- Work product doctrine protects the analytical process that produced the findings

This is why the repository publishes **findings and methodology** but not the underlying database or source code. The published master wire ledger (481 wires), entity classification data, and complete methodology documentation provide sufficient information for a knowledgeable reviewer to understand and evaluate the work performed — consistent with AU-C §230.05's documentation sufficiency standard.

---

### Federal Rules of Evidence — Daubert Standard

**What it governs:** Admissibility of expert testimony in federal court.

**Relevance:**

While this analysis is not prepared for litigation, the methodology was designed to meet the Daubert reliability factors should the findings ever be subject to judicial scrutiny:

| Daubert Factor | How Addressed |
|----------------|---------------|
| **Testable methodology** | Every extraction rule, scoring weight, and classification threshold is documented and reproducible |
| **Peer review** | Methodology published for public review; AI-assisted QA applied throughout |
| **Known error rate** | v6.2 spot-check: 93% PROVEN accuracy (28/30); 0% balance contamination; 12 bugs/integrity issues documented with impact |
| **Standards controlling operation** | 5-axis scoring system with defined weights; four-tier GAGAS-aligned confidence framework; documented dedup rules |
| **General acceptance** | Methodology draws from established forensic accounting, financial auditing, and data science practices |

---

## What This Analysis IS and IS NOT

| This Analysis IS | This Analysis IS NOT |
|------------------|----------------------|
| A forensic financial reconstruction | A financial statement audit |
| Source-strength tier-labeled (T1–T4) | An audit opinion |
| A pro bono public interest research effort | A commissioned or client-engaged service |
| A documented evidence trail from the EFTA corpus | A definitive accounting of all Epstein finances |
| Transparent in methodology and limitations | A basis for legal action without independent verification |
| The work of one practitioner with AI tooling | A team audit with segregated duties |

---

## Limitations Specific to Solo Practice

This analysis was conducted by a single practitioner. In a traditional audit or forensic engagement, certain controls — such as segregation of duties, independent partner review, and multi-person verification — would apply. Those controls are not present here.

Mitigating factors:
- **AI-assisted QA**: Claude (Anthropic) was used for code review, methodology critique, and output verification — providing a form of independent review
- **Self-correcting pipeline**: 9 contamination bugs were caught during the pipeline itself; 3 additional integrity issues were caught in the April 2026 post-audit review, demonstrating active quality monitoring
- **Conservative bias**: The publication ledger ($2.308B) is built on four-tier GAGAS classification; T1–T3 auditable subtotal ($2.038B) covers 122.8% of the SAR benchmark
- **Transparent limitations**: All 9 known limitations are documented; tier labels appear on every financial amount
- **Reproducibility**: The methodology is described in sufficient detail for independent replication
- **Live audit trail**: Every integrity removal is documented and exposed via the public API at `the-projects.org/api/pub/stats#audit_trail`

---

## Applicable Law

The underlying DOJ documents analyzed in this project are **public records** released under the Epstein Files Transparency Act (Public Law 119-38), signed November 19, 2025. Analysis of public government records is protected activity under the First Amendment.

This repository does not reproduce copyrighted source material, store victim-identifying information, or publish material subject to court seal. The analysis constitutes original research and commentary on public records.

---

*This compliance statement was prepared by R.S. Taylor and reflects his understanding of applicable professional standards. It is not a legal opinion and should not be relied upon as such.*
