# Narrative 17: One-Way Money

**I spent 200+ hours pulling wire transfers out of 1.48 million EFTA documents. 481 wires. $973 million. 219 entities across Deutsche Bank, JPMorgan, Citibank, Bank of America, Barclays, and Wells Fargo. When I ran a balance sheet on the nine entities at the center of this network, $221 million went in from the outside. $54 million came out. The other $167 million has no documented exit in any production from any institution.**

---

## The Data

Let me be clear about what I'm working with.

The master wire ledger contains 481 wire transfers totaling $973,392,414 extracted across the Phase 5I entity-resolution pipeline from the EFTA document production. 185 of those wires come from Deutsche Bank's verified court exhibits — specifically the five exhibits (A through E) attached to their Suspicious Activity Report on Epstein's accounts. The remaining 296 wires were extracted from the broader EFTA corpus across multiple banking institution productions including Bank of America, JPMorgan, Citibank, Barclays, and Wells Fargo. This isn't a Deutsche Bank story. This is a multi-institution story. Deutsche Bank's SAR exhibits happen to be the most organized slice of it, so I'll use them as the structural backbone — but the full picture is bigger than one bank.

The entity classification index identifies 228 unique entities: 26 classified as Epstein-controlled, 126 as external parties, and 6 as banks or custodians.

---

## Five Exhibits, Five Functions

Deutsche Bank organized its SAR wire evidence into five exhibits. I did not design this taxonomy. The bank's compliance department chose these groupings. What I did was sort every wire by source and destination and compute what goes in versus what comes out of each exhibit — and what fell out is that their five exhibits map directly to five distinct operational functions.

### Layer 1 — Accumulation (Exhibit A)

**17 wires | $151,499,980**

Every wire in Exhibit A goes in one direction: from an external source into Southern Trust Company Inc. That's it. One destination for all 17 wires. Zero outbound wires.

Southern Trust was incorporated in the U.S. Virgin Islands in 2011 as Financial Informatics Inc. and renamed in September 2012. Three source clusters feed it:

| Source Cluster | Wires | Total | Period |
|---|---|---|---|
| Leon Black / Apollo entities | 14 | $106,500,000 | Oct 2013 – Apr 2017 |
| Edmond de Rothschild (institutional + personal) | 2 | $24,999,980 | Dec 2015 |
| Narrow Holdings LLC c/o Elysium Management | 1 | $20,000,000 | Jul 2014 |
| **Total** | **17** | **$151,499,980** | |

Narrow Holdings is care-of Elysium Management — Leon Black's family office. That brings Black's effective total through this single shell to $126.5 million. One man's entities account for 83.5% of all Exhibit A volume.

### Layer 2 — Distribution (Exhibit B)

**18 wires | $33,139,248**

Exhibit B captures capital moving into and out of investment vehicles. Southern Financial LLC is the hub. Money enters from Tudor Futures Fund ($13,503,941 in two wires, August 2014) and three Blockchain Capital entities ($15,000,000 into The 2017 Caterpillar Trust, all on February 21, 2018). Money exits to venture investments: Joichi Ito ($1,000,001 across three wires), Coatue Enterprises LLC ($2,000,000 across four quarterly payments), and Neoteny 3 LP ($1,000,000).

Where Layer 1 collects capital, Layer 2 deploys it.

### Layer 3 — Operations (Exhibit C)

**64 wires | $89,372,037**

This is the machine's operating system. Twenty-one wires totaling $51,876,640 flow from Jeepers Inc. (a Deutsche Bank brokerage entity) into Jeffrey Epstein's NOW/SuperNow checking account. That's brokerage-to-cash conversion — investment holdings liquidated into spendable money.

Also feeding the operating account: $23,075,000 from Kellerhals Ferguson Kroblin PLLC (Epstein's USVI estate counsel, 2 wires), $3,000,000 from Link Rockenbach P.A., and $2,000,000 from AIC Title Agency.

### Layer 4 — Redistribution (Exhibit D)

**11 wires | $68,760,686**

Exhibit D is internal plumbing. The Haze Trust — which receives art-sale proceeds from Sotheby's ($11,249,417) and Christie's ($7,725,000) — redistributes capital across the shell network. $32,000,000 goes to Southern Financial LLC (Checking) across 5 wires. $10,000,000 goes to Southern Trust Company (Checking). $5,000,000 goes to Southern Financial LLC (DBAGNY).

This is the rebalancing mechanism. Capital repositioned between shells as needed.

### Layer 5 — Legitimization (Exhibit E)

**12 wires | $6,253,493**

Every wire in Exhibit E originates from Gratitude America MMDA, Epstein's charitable vehicle. Funds flow to Gratitude America Ltd. accounts at Morgan Stanley, Citibank, and First Bank of Puerto Rico ($5,800,000), plus direct grants to the Melanoma Research Alliance Foundation ($225,000), the Bruce & Marsha Moskowitz Foundation ($150,000 across 3 wires), and the Cancer Research Wellness Institute ($50,000 across 2 wires).

This is the paper trail of charitable purpose.

---

## The Balance Sheet

Here's the part nobody else has done.

I treated each of the nine entities at the center of this network as its own ledger. Money in from the outside, money in from other shells, money out to other shells, money out to the outside. Then I ran the arithmetic.

| Shell Entity | External In | Shell In | Shell Out | External Out | Net Position |
|---|---|---|---|---|---|
| Southern Trust | $140,396,559 | $30,000,000 | $83,200,000 | $29,765,000 | **+$57,431,559** |
| NOW/SuperNow Account | $32,718,397 | $74,605,287 | $0 | $0 | **+$107,323,684** |
| Southern Financial | $14,039,248 | $82,855,320 | $38,250,000 | $5,613,125 | **+$53,031,443** |
| Caterpillar Trust | $15,000,000 | $0 | $10,000,000 | $0 | **+$5,000,000** |
| Haze Trust | $19,032,745 | $64,503,608 | $167,358,928 | $0 | **−$83,822,575** |
| Jeepers Inc. | $0 | $6,000,000 | $57,876,640 | $0 | **−$51,876,640** |
| Plan D LLC | $1,125 | $30,500,000 | $10,000,000 | $18,000,000 | **+$2,501,125** |
| Gratitude America | $0 | $22,064,876 | $12,064,876 | $453,493 | **+$9,546,507** |
| NES LLC | $0 | $0 | $0 | $553,536 | **−$553,536** |
| **System Total** | **$221,188,074** | | | **$54,385,154** | **+$166,802,920** |

$221 million entered from the outside. $54 million is visible leaving. The remaining **$167 million** has no documented exit in the entire production — not in the SAR exhibits, not in the normalized data, not from any institution.

Three entities eat most of it:

The NOW/SuperNow Account absorbs $107.3 million net. It takes in $32.7 million from external sources and $74.6 million from the Jeepers brokerage pipeline and other internal transfers. Sends zero back out in the wire record. Terminal destination.

Southern Trust Company nets $57.4 million. It takes in $140.4 million from external sources plus $30 million from internal shell transfers, and distributes $83.2 million to other shells and $29.8 million externally.

Southern Financial nets $53 million. Receives $14 million from external sources and $82.9 million from the Haze Trust redistribution pipeline. Distributes $38.3 million internally and $5.6 million out to Ito, Coatue, and other external parties.

This isn't evidence that money was stolen. It's evidence that the production is **asymmetric**. The filings comprehensively document how money entered the shell network and selectively omit where it went. Whether that reflects the limits of what banks tracked, what they chose to include, or what they were willing to hand over is a question I can't answer from wire data. The arithmetic speaks for itself.

---

## The Paired Deposit Pattern

Both of the network's two largest external depositors — Black/Apollo and Rothschild — do the same thing when they wire money to Southern Trust: they split the deposit across two entities.

**Black's Paired Deposits:**

| Date | Personal Entity | Amount | Fund Entity | Amount | Combined |
|---|---|---|---|---|---|
| Apr 25, 2014 | Leon & Debra Black | $5,000,000 | Black Family Partners LP | $5,000,000 | $10,000,000 |
| Oct 16, 2014 | Leon & Debra Black | $7,000,000 | Black Family Partners LP | $13,000,000 | $20,000,000 |
| Oct 22, 2014 | Leon & Debra Black c/o Apollo | $2,000,000 | Black Family Partners LP | $3,000,000 | $5,000,000 |
| Oct 13, 2015 | Leon & Debra Black c/o Apollo | $5,000,000 | Black Family Partners LP | $5,000,000 | $10,000,000 |

Four of ten Black deposit dates are paired — personal account and family fund hitting the same destination on the same day. Split ratios aren't uniform (1:1, 0.54:1, 0.67:1, 1:1). The remaining six dates are single-entity deposits.

**Rothschild's Paired Deposit:**

| Date | Entity | Amount | Type |
|---|---|---|---|
| Dec 17, 2015 | Edmond de Rothschild (Suisse) SA | $10,000,000 | Institutional |
| Dec 21, 2015 | Benjamin Edmond de Rothschild | $14,999,980 | Personal |
| **Combined** | | **$24,999,980** | |

Same pattern. One institutional wire, one personal wire, same shell. The $20 difference between $24,999,980 and $25,000,000 is a standard wire transfer fee. The four-day gap between wires — versus Black's same-day execution — is consistent with international transfer origination from Geneva to St. Thomas.

Two depositors operating from different continents using the same structural method to fund the same entity. That's not coincidence. That's procedure.

---

## The October 15, 2013 Round Trip

The very first Black deposit contains something I didn't expect.

Exhibit A records, on October 15, 2013:

> **Leon & Debra Black → Southern Trust Company Inc. | $8,500,000**

The normalized wire data — extracted from the broader production — records the same date:

> **SOUTHERN_TRUST → DEBRA_BLACK | $8,500,000**

Same amount. Same day. In and out. The money enters under the joint name "Leon & Debra Black" and exits to "DEBRA_BLACK" within the same business day. Different entity designation on each side.

That's a pass-through. Southern Trust serves as a waypoint that changes the name on the paper trail.

A second amount-matched pair exists with a longer gap: $8,000,000 enters from Leon & Debra Black c/o Apollo on April 25, 2017 (Exhibit A) and $8,000,000 exits from SOUTHERN_TRUST to LEON_BLACK on September 5, 2018 (normalized data). Same amount, seventeen months apart, different entity names on each end.

---

## December 2015

The densest cluster in the Exhibit A record. Four wires, $44,999,980, fourteen days:

| Date | Source | Amount |
|---|---|---|
| Dec 17 | Edmond de Rothschild (Suisse) SA | $10,000,000 |
| Dec 18 | Black Family Partners LP | $10,000,000 |
| Dec 21 | Benjamin Edmond de Rothschild | $14,999,980 |
| Dec 30 | Leon & Debra Black c/o Apollo Management | $10,000,000 |

On December 18, 2015 — one day after the first Rothschild wire, three days before the second — the DOJ announced a non-prosecution agreement with Edmond de Rothschild (Suisse) SA under the Swiss Bank Program. The bank admitted helping U.S. clients conceal assets in undeclared accounts: 950 accounts, $2.16 billion, 2008–2013. Penalty: $45,245,000.

EFTA document <a href="https://efts.uscourts.gov/efts-nyed/masterSearch/results?query=EFTA00584904" target="_blank">EFTA00584904</a> contains the consulting contract between Southern Trust Company Inc. and Edmond de Rothschild Holding S.A., dated October 5, 2015. Services: "risk analysis and algorithms." Payout: $25 million if the DOJ penalty fell below $75 million; $10 million if between $75 million and $150 million. Payment due within three business days of EDRH completing payment to U.S. authorities.

The DOJ penalty of $45.2 million fell well below the $75 million threshold. The contract entitled Epstein to the maximum $25 million. Our wire ledger captures $24,999,980 arriving in two wires within four days of the DOJ announcement. The contract terms, the penalty amount, and the wire dates line up without a single inconsistency.

But it's not just Rothschild money in this window. Black Family Partners wired $10 million the day after the Rothschild institutional wire. Leon & Debra Black wired another $10 million twelve days later. Two of the three Exhibit A source clusters deposited into the same shell in the same two-week period around the same DOJ enforcement action.

Q4 2015 — the October and December deposits combined — accounts for 6 wires totaling $54,999,980. That's 36.3% of all Exhibit A value concentrated in a single quarter. No other quarter comes close.

---

## The 260 Wires Nobody Talks About

Here's where I owe you the full picture.

122 wires sit in neat exhibit buckets. The other 260 don't. They were extracted from the broader EFTA production — Deutsche Bank's SDNY document production, supplementary banking records, and cross-institutional transfers spanning JPMorgan ($8.5 million across 16 wires), Bank of America ($10.0 million across 10 wires), Citibank ($6.3 million across 14 wires), and BNY Mellon ($273,230 across 5 wires).

These 260 wires contain 105 entities that never appear in the SAR exhibits. I call them shadow entities — not because they're hiding, but because they exist in a parallel dataset that the formal filing doesn't reference.

The biggest shadow entity is Brad Wechsler. An Apollo Global Management affiliate executive whose name appears in 10 wires totaling $42,942,500 in flow volume.

Here's what Wechsler's sub-ledger looks like:

**Inbound to Wechsler:**

| Source | Amount |
|---|---|
| ALEXANDERSON | $1,600,000 |
| ALEXANDERSON | $3,000,000 |
| **Total In** | **$4,600,000** |

ALEXANDERSON is Eileen Alexanderson, an Elysium Management (Black family office) employee documented across 6 wires and $16.2 million in the production.

**Outbound from Wechsler:**

| Destination | Wire 1 | Wire 2 | Wire 3 | Total |
|---|---|---|---|---|
| HEATHER_GRAY | $8,818,875 | $718,875 | $8,100,000 | $17,637,750 |
| SPINELLA | $8,818,875 | $718,875 | $8,100,000 | $17,637,750 |
| RICHARD_JOSLIN | $3,000,000 | $67,000 | — | $3,067,000 |
| **Total Out** | | | | **$38,342,500** |

Three wires to HEATHER_GRAY. Three wires to SPINELLA. Identical amounts in each pair — $8,818,875, $718,875, $8,100,000. Mirrored to the dollar.

$38.3 million out from $4.6 million in. That's a **$33.7 million gap** in Wechsler's own sub-ledger. The other $33.7 million entered from somewhere not captured in our production.

HEATHER_GRAY and SPINELLA are terminal sinks. They receive $17.6 million each and never appear as a source in any wire.

---

## Terminal Sinks and Ghost Sources

A terminal sink is an entity that receives money and never sends any. A ghost source sends money and never receives any. In a clean financial system, most entities do both. In this network, the separation is stark.

**Terminal sinks absorbing over $1 million:**

| Entity | Wires | Total Received |
|---|---|---|
| Southern Trust Company Inc. | 17 | $151,499,980 |
| Jeffrey Epstein NOW/SuperNow | 61 | $83,372,037 |
| Southern Financial LLC (Checking) | 5 | $32,000,000 |
| The Haze Trust (Checking) | 4 | $21,760,686 |
| HEATHER_GRAY | 3 | $17,637,750 |
| SPINELLA | 3 | $17,637,750 |
| The 2017 Caterpillar Trust | 3 | $15,000,000 |
| ITO | 8 | $11,260,001 |
| BUTTERFLY_TRUST | 4 | $6,350,000 |
| Gratitude America Ltd. | 4 | $5,800,000 |
| RICHARD_JOSLIN | 3 | $3,567,000 |
| Coatue Enterprises LLC | 4 | $2,000,000 |

**Ghost sources sending over $10 million** — entities that appear only as senders:

| Entity | Wires | Total Sent |
|---|---|---|
| The Haze Trust (DBAGNY) | 8 | $49,727,941 |
| Black Family Partners LP c/o Apollo | 5 | $36,000,000 |
| Leon & Debra Black | 4 | $35,500,000 |
| Leon & Debra Black c/o Apollo | 4 | $25,000,000 |
| Kellerhals Ferguson Kroblin PLLC | 2 | $23,075,000 |
| Narrow Holdings LLC c/o Elysium | 1 | $20,000,000 |
| ALEXANDERSON | 6 | $16,167,000 |
| Benjamin Edmond de Rothschild | 1 | $14,999,980 |
| Tudor Futures Fund | 2 | $13,503,941 |
| Sotheby's | 1 | $11,249,417 |
| Blockchain Capital IV LP | 1 | $10,500,000 |
| Black Family Partners LP | 1 | $10,000,000 |
| Edmond de Rothschild (Suisse) SA | 1 | $10,000,000 |

Money enters from ghost sources and lands in terminal sinks. The network is built for one-way flow. Capital comes in from the outside and does not visibly return through the same channels.

---

## What I Can and Cannot Say

I can say this: five exhibits, five functions. Accumulation, distribution, operations, redistribution, legitimization. Deutsche Bank organized it this way. I just ran the numbers.

I can say this: $221 million in, $54 million out. That's not an interpretation. That's arithmetic on 481 wires across multiple banking institutions.

I can say this: two independent depositors from two different continents use the same paired-entity structure to fund the same shell company. The October 2013 round trip moves $8.5 million in and out of Southern Trust on the same day under different names. The Wechsler mirror transactions distribute $35.3 million in identical paired amounts to two terminal sinks. These are patterns. They repeat.

I cannot say where the $167 million went. The production doesn't show me.

I cannot say whether the asymmetry in the filing — comprehensive inflows, selective outflows — was intentional or accidental. Deutsche Bank chose what to put in those five exhibits. Other institutions chose what to include in their productions. I work with what they gave the court.

I cannot say what any of these patterns mean in terms of legal liability. I'm conducting forensic financial analysis, not a prosecution.

I report what the data shows. The data shows an architecture.

---

## Source Data

**Source data:** [Master Wire Ledger](../data/master_wire_ledger_phase5i.json) · <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?usp=sharing&ouid=103970896670138914877&rtpof=true&sd=true" target="_blank">Forensic Workbook</a> · <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/shell_network.html" target="_blank">Interactive Network</a> · <a href="https://randallscott25-star.github.io/epstein-forensic-finance/visualizations/17_one_way_money.html" target="_blank">One-Way Money Visualization</a>

| Dataset | Records | Coverage |
|---|---|---|
| <a href="https://github.com/Tweederrr/epstein-forensic-finance/tree/main/data" target="_blank">Master Wire Ledger (Phase 5I)</a> | 481 wires | $973,392,414 |
| <a href="https://github.com/Tweederrr/epstein-forensic-finance/tree/main/data" target="_blank">Entity Classification Index</a> | 227 entities | 43 EPSTEIN_ENTITY, 151 EXTERNAL_PARTY, 8 BANK/CUSTODIAN |

### EFTA Source Documents

| Document | Reference | Content |
|---|---|---|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | Deutsche Bank SAR | Exhibits A–E: 122 wire transfers, $349M — source for five-layer architecture |
| <a href="https://efts.uscourts.gov/efts-nyed/masterSearch/results?query=EFTA00584904" target="_blank">EFTA00584904</a> | Consulting Agreement | Southern Trust Co. / Edmond de Rothschild Holding S.A., Oct 5 2015 |
| <a href="https://efts.uscourts.gov/efts-nyed/masterSearch/results?query=EFTA00582812" target="_blank">EFTA00582812</a> | Retention Letter | Latham & Watkins / Kathryn Ruemmler engagement, Jul 31 2015 |

### Forensic Workbook Tabs

| Tab | Link |
|---|---|
| Master Wire Ledger — Exhibit A (Black → Southern Trust) | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Entity P&L — Balance Sheet | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1497389416#gid=1497389416" target="_blank">📊 Open Tab</a> |
| Shell Network — Full entity map | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1040516313#gid=1040516313" target="_blank">📊 Open Tab</a> |
| Money Flow Patterns — Entity flows | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2075093083#gid=2075093083" target="_blank">📊 Open Tab</a> |
| Shell Trust Hierarchy | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1943952132#gid=1943952132" target="_blank">📊 Open Tab</a> |
| Executive Summary | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1804001356#gid=1804001356" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### Banking Institutions in Production

| Institution | Wires | Volume |
|---|---|---|
| Deutsche Bank | 70 | $164,397,517 |
| Bank of America | 10 | $9,950,141 |
| JPMorgan | 16 | $8,480,039 |
| Citibank | 14 | $6,336,432 |
| Morgan Stanley | 4 | $6,200,000 |
| BNY Mellon | 5 | $273,230 |
| HSBC | 2 | $116,656 |
| First Bank PR | 2 | $300,000 |

### DOJ Datasets

**All 12 DOJ Datasets:** <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-1-files" target="_blank">1</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-2-files" target="_blank">2</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-3-files" target="_blank">3</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-4-files" target="_blank">4</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-5-files" target="_blank">5</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-6-files" target="_blank">6</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-7-files" target="_blank">7</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">8</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">9</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-10-files" target="_blank">10</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">11</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-12-files" target="_blank">12</a>

All EFTA document IDs are from the public DOJ release under the Epstein Files Transparency Act at <a href="https://efts.gov" target="_blank">efts.gov</a>. Full methodology in [METHODOLOGY.md](../METHODOLOGY.md).
