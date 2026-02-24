# Data Narratives

**The financial data tells stories that numbers alone cannot convey.**

These narratives trace fund flow patterns, entity relationships, temporal correlations, and forensic accounting anomalies identified across the 1.48 million documents in the DOJ EFTA release. Early narratives are grounded in wire-level data from the [master wire ledger](../data/master_wire_ledger_phase5i.json). Later narratives draw on the full corpus: 11.4 million entity extractions, 734,122 unique persons, 2.4 million dates, and 321 aircraft flight records. Each finding is extracted through the [Phase 5I pipeline](../docs/METHODOLOGY.md) and cross-referenced against court exhibits where available.

All amounts are **(Unverified)** automated extractions. These are not audit findings — they are data observations. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for the professional standards framework governing this analysis.

---

## Published Narratives

### 🔺 Original Finding

| # | Title | Key Finding | Data Scope |
|---|-------|-------------|------------|
| 17 | [One-Way Money](17_the_architecture.md) | The banks documented every dollar going in and almost none of it coming out. $221M entered nine shells across multiple banking institutions. $54M is visible leaving. The other $167M has no documented exit in any production from any institution. | 481 wires · 219 entities · $973M |

This is the first complete balance sheet ever run on the Epstein shell network — not institution by institution, but across the full multi-bank production. Nobody else has published one.

---

### Deep Dives

| # | Title | Key Finding | Data Scope |
|---|-------|-------------|------------|
| 1 | [The Jeepers Pipeline](01_jeepers_pipeline.md) | $57.9M brokerage shell → personal checking, all dated, all on Exhibit C | 24 wires · $57,876,640 |
| 2 | [Art Market as Liquidity Channel](02_art_market.md) | Sotheby's + Christie's proceeds entered the shell network through Haze Trust | 20 wires · $103,786,473 |
| 3 | [The Plan D Question](03_plan_d_question.md) | $18M out to Leon Black, near-zero inflow — where did Plan D get its money? | 34 wires · $163,097,604 |
| 4 | [Chain-Hop Anatomy](04_chain_hop_anatomy.md) | 4-tier shell network mapped — and $311M in double-counting removed | 67 wires · $312,796,381 |
| 5 | [Deutsche Bank's Role](05_deutsche_bank.md) | 38 wires across every major Epstein entity, 75% of volume in last 6 months | 38 wires · $56,792,936 |
| 6 | [Gratitude America](06_gratitude_america.md) | 88% of outflows to investment accounts, 7% to charitable purposes | 20 wires · $13,080,518 |
| 7 | [Follow the Money, Follow the Plane](07_follow_the_money_follow_the_plane.md) | Wire-flight temporal correlation at 4.3× random chance; $169M near St. Thomas flights | 185 wires · 321 flights · $575M |
| 8 | [The Infrastructure of Access](08_infrastructure_of_access.md) | The people who moved the money are the same people victims named — Maxwell in 204 financial docs and 1,312 victim docs | 11.4M entities · 1.48M files |
| 9 | [734,122 Names](09_734122_names.md) | Asked every person in 1.48M files who bridges financial and victim docs. 57 real names. 10 operational staff. No one hiding who hasn't been found | 734,122 persons · 57 bridgers |
| 10 | [The Round Number Problem](10_the_round_number_problem.md) | Benford's Law fails: digits 2 and 5 at 29.7% and 18.4%. 84.3% of wires are exact round numbers. One decision-maker, not a market | 185 wires · $557M |
| 11 | [The Shell Map](11_the_shell_map.md) | Wire ledger captured 7 entities. The corpus contains 14 — with 178,000 money references. Four shells with 23,922 money mentions never appeared in a single wire | 14 shells · 178K money refs |
| 12 | [The Bank Nobody Prosecuted](12_the_bank_nobody_prosecuted.md) | Bear Stearns banked Epstein 1986–2008, JPMorgan 1998–2013, Deutsche Bank 2013–2018. The enforcement void during the Bear Stearns years has never been examined | 3 banks · 25 years |
| 13 | [Seven Banks, One Trust](13_seven_banks_one_trust.md) | Financial Trust Company touched seven banking institutions simultaneously. The trust structure created jurisdictional fragmentation by design | 7 banks · 1 trust · 325 records |
| 14 | [Where Leon Black's Money Went](14_where_leon_blacks_money_went.md) | Black's entities paid Epstein $158–170M. Our wire ledger verified $60.5M. Downstream flow traced through every shell in the network | 1,600 files · $60.5M verified |
| 15 | [Gratitude America (Expanded)](15_gratitude_america.md) | Karyna Shuliak biographical corrections. Estate bequest $50–100M. Charitable entity as beneficiary designation vehicle | 20 wires · estate records |
| 16 | [The Accountant](16_the_accountant.md) | The financial professionals who maintained the architecture — trustees, estate counsel, and compliance gatekeepers | 29 corpus appearances · 5 key figures |
| 17 | [One-Way Money](17_the_architecture.md) | $221M in. $54M out. $167M gap. First multi-institution balance sheet across 9 shell entities | 481 wires · 219 entities · $973M |
| 18 | [Offshore Architecture: The Brunel–BVI–ICIJ Bridge](18_offshore_architecture.md) | DOJ subpoena names a BVI shell. ICIJ Offshore Leaks confirms it. Scouting International BVI. $10M+ Butterfly Trust pipeline. 3 databases cross-referenced | 3 databases · 172 docs · 689 NetIncorp entities scanned |

---


## Interactive Visualizations

| Visualization | Description |
|--------------|-------------|
| <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/shell_network.html" target="_blank">Shell Network — Full Architecture</a> | Interactive map of all 14 shell entities and 12 banking institutions. Click nodes for detail. Filter by co-occurrence, bank relationships, or wire ledger. |
| <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/17_one_way_money.html" target="_blank">One-Way Money — Five-Layer System</a> | Interactive breakdown of the five exhibit layers, the $167M balance-sheet gap, and the December 2015 convergence timeline. |

---

## How to Read These

Each narrative follows the same structure:

- **Summary** — what I found, in plain language
- **The Data** — tables, counts, and measurements drawn from the source material
- **What the Pattern Shows** — the story the data tells
- **What I Cannot Determine** — the limits of what this analysis can prove

The first six narratives trace wire transfer patterns through Epstein's shell network. Narratives 7–10 expand the aperture: flight correlations, entity co-occurrence across 11.4 million records, full-corpus person scans, and forensic accounting tests. The methodology scales with the questions.

The source workbook containing all exhibits referenced in these narratives is available here: **<a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook (Google Sheets)</a>** (view-only).

I report what the data shows. Interpretation of intent, legality, or business purpose is left to qualified investigators, regulators, and readers.

---

*Randall Scott Taylor — Director of Finance Administration, BS Network & Cyber Security (Wilmington University), MS Applied Data Science (Syracuse University). February 2026.*
