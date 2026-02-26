# Methodology & Standards

## What I Am and What I'm Not

I'm a data scientist. MS in Applied Data Science. My day job is multi-affiliate financial reconciliation at institutional scale — budget variance, exception reporting, automated payroll systems across hospital networks.

I am not a forensic accountant. I am not a prosecutor. I am not a journalist. I don't hold a CPA or a CFE.

What I did here is apply data science methods within a forensic accounting framework. There's a difference. A forensic accountant renders opinions and testifies. I build pipelines, enforce data integrity, and publish verified findings. The analytical framework keeps the work honest. The conclusions are yours to draw.

## What This Project Does

- Extracts financial transactions from 1.48 million DOJ-released documents
- Reconciles dollar amounts across multiple bank productions
- Maps entity relationships, shell structures, and fund flows
- Publishes verified data with bates stamp citations to source documents
- Maintains a reproducible pipeline from raw document to final ledger

## What This Project Does Not Do

- Assign criminal intent to any transaction
- Classify payments as "bribes," "money laundering," or "trafficking"
- Render legal opinions or conclusions of law
- Accuse any individual of criminal conduct
- Speculate on motive behind any financial movement

I trace money. I don't tell you why it moved. I show you that it moved, how much, when, between whom, and through what vehicle. That's it.

## Why This Matters

The EFTA corpus is public record. Anyone can download it. But raw documents aren't evidence — organized, verified, source-cited data is. The goal is to produce work product that could theoretically support a chain of custody if any investigative body ever needed it.

That means:

**Source fidelity.** Every transaction traces back to a specific bates-stamped document in the DOJ production. No transaction enters the ledger without a source citation. If I can't cite it, it doesn't exist in my data.

**No editorial overlay.** The ledger records what the documents say. It does not interpret, classify by motive, or assign guilt. A wire transfer from Entity A to Entity B is recorded as exactly that — a wire transfer from Entity A to Entity B. What that transfer *means* is not my call.

**Reproducibility.** The extraction code, schema design, and classification logic are documented. Another analyst with access to the same EFTA corpus should be able to verify my work. That's the standard I hold myself to.

**Inflation removal.** Duplicate records across overlapping bank productions get flagged and removed through an 11-layer deduplication system. The published totals reflect verified unique transactions, not raw record counts.

**Confidence tiers.** Not all data is equal. Tier 1 transactions have direct dollar amounts and bates citations. Tier 4 estimates carry explicit uncertainty flags. The ledger tells you which is which.

## On Requests to Classify Intent

People ask me to label transactions — call this one a bribe, call that one trafficking, classify these as money laundering. I understand why. The data makes you angry. It should.

But the second I start assigning motive based on who received money or where they live, I've left data science and entered speculation. That's exactly how forensic work gets discredited. A defense attorney would shred it. A judge would exclude it. And then the actual evidence — the verified transactions, the shell structures, the fund flows — gets thrown out with it.

I'd rather give you clean data you can trust than dirty conclusions that feel satisfying.

## Standards I Follow

- **GAAS-adjacent methodology.** I'm not conducting a formal audit under Generally Accepted Auditing Standards, but the principles of evidence gathering, documentation, and independent verification inform the work.
- **FinCEN SAR benchmarking.** Published totals are cross-referenced against known Suspicious Activity Report thresholds. Current coverage: 104.4% of SAR benchmarks across T1-T3 tiers.
- **Three-tier confidence framework.** Every finding is tagged by confidence level. High-confidence claims have multiple independent source documents. Lower-confidence findings are flagged as such.
- **Full corpus analysis.** No sampling. Every document in the production gets processed through the same pipeline. Equal coverage across all bank productions.

## Tools

Python extraction pipeline. SQLite database (8GB). Custom NER for entity extraction. All analysis code is original. AI tools assisted with code generation — same way you'd use a calculator. Every analytical decision is mine.

## How to Help

The most useful thing you can send me is a specific bates number or document reference with a note about what you found in it. That's data I can verify and potentially incorporate.

What I can't use: classification schemes that assign criminal intent, speculation about motive, or requests to label people as guilty of specific crimes. That's not what this project is for.

This project is a flashlight. I point it at the money and show you where it went. What you see is up to you.

---

*Randall Scott Taylor*
*MS Applied Data Science, Syracuse University*

For questions, corrections, or document references — [submit an issue on GitHub](https://github.com/randallscott25-star/epstein-forensic-finance/issues).
