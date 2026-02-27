# Data Narrative 18 — Offshore Architecture: The Brunel–BVI–ICIJ Bridge

> *DOJ subpoena names a BVI shell. ICIJ Offshore Leaks confirms it. $10M+ flowed through the same trust network. 8,526 pages scanned, 172 documents, one offshore map no one had connected.*

⚠️ **All findings are navigational tools derived from automated extraction. They have not been independently verified and should not be treated as established fact. See [COMPLIANCE.md](/COMPLIANCE.md) for full professional standards disclaimers.**

---

## What I Found

I cross-referenced the DOJ EFTA corpus against the ICIJ Offshore Leaks database and FinCEN transaction records. What came back: the complete offshore-to-domestic financial architecture of the Brunel/MC2 modeling network. One BVI shell company — **Scouting International Investment Co., Ltd.** — appears in exactly one DOJ document and is independently confirmed in the ICIJ Offshore Leaks database as a Brunel-controlled entity incorporated through two offshore intermediaries in Tortola. That entity sits next to a domestic trust pipeline that moved $10M+ through a single JPMorgan account, with outflows to Ghislaine Maxwell totaling $648K+ across 8 STRONG-tier transfers.

No individual data point here is new. The connected map is.

---

## The Source Document

**[EFTA00809672.pdf](https://www.justice.gov/epstein/media/EFTA00809672.pdf)** (5 pages)

| Field | Value |
|-------|-------|
| **Type** | Subpoena Duces Tecum for Videotaped Deposition |
| **Case** | *Epstein v. Rothstein*, No. 50-2009CA040800XXXXMBAG |
| **Date** | April 4, 2019 |
| **Bates Range** | EFTA00809672 – EFTA00809676 |

Page 3, Exhibit A, Section C defines "entities owned or controlled by" Brunel:

> *"MC2 Models Management, LLC, MC2 Models Miami, LLC, Scouting International Investment Co., Ltd., Scouting I International Co., L'eclair au Café Limited Liability Company and Karin Models Agency"*

Six entities. One of them — **Scouting International Investment Co., Ltd.** — appears in the ICIJ Offshore Leaks database.

---

## The ICIJ Match

**Source:** [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org/) — `icij_entities`, `icij_officers`, `icij_relationships`, `icij_intermediaries`, `icij_addresses`

### Scouting International Investment Co., Ltd.

| Field | Value |
|-------|-------|
| **ICIJ Node** | 140553 (Entity) |
| **Officer** | Jean-Luc Brunel (node 93239) |
| **Jurisdiction** | British Virgin Islands |
| **Incorporated** | 10-NOV-2003 |
| **Status** | Struck / Defunct / Deregistered |
| **Type** | Standard International Company |
| **Registered Address** | Portcullis TrustNet Chambers, P.O. Box 3444, Road Town, Tortola, BVI |

### Two Intermediaries

| Intermediary | ICIJ Node | Connected Entities |
|-------------|-----------|-------------------|
| **Portcullis TrustNet (BVI) Limited** | 54662 | 436 entities across ICIJ |
| **NetIncorp.com Corporation** | 290197 | 689 entities across ICIJ |

Both intermediaries are BVI-registered corporate formation agents. Portcullis TrustNet was named in the original 2013 Offshore Leaks investigation. NetIncorp.com's 689 client entities were exhaustively cross-referenced against the EFTA corpus — all 11 name matches were verified as false positives (see [NetIncorp Investigation](#netincorp-investigation) below).

### ICIJ Cross-Reference of All Six Brunel Entities

| Entity | Found in ICIJ? | Details |
|--------|:-:|---------|
| Scouting International Investment Co., Ltd. | ✅ | BVI, Portcullis TrustNet, Inc. 10-NOV-2003, Struck/Defunct |
| L'eclair au Café Limited Liability Company | ❌ | "Leclair" hits 3 unrelated offshore shells |
| MC2 Models Management, LLC | ❌ | Domestic LLC |
| MC2 Models Miami, LLC | ❌ | Domestic LLC |
| Scouting I International Co. | ❌ | Possibly successor/variant entity |
| Karin Models Agency | ❌ | Domestic (deposition confirms: "our company MC2, formerly Karin Models") |

---

## The Money Pipeline

Scouting International shows no direct financial flows in the released documents. Either it was a holding vehicle, or the records got destroyed or withheld. But the domestic side of the Brunel network moved real money through a single trust account.

### The Butterfly Trust — Account #44130552, JPMorgan Chase

**Source Documents:**
- **[EFTA00092643.pdf](https://www.justice.gov/epstein/media/EFTA00092643.pdf)** — "Timeline of Payments to (or on Behalf of) Potential Co-Conspirators"
- **[EFTA00105307.pdf](https://www.justice.gov/epstein/media/EFTA00105307.pdf)** — Wire details with account numbers and beneficiary banks

#### Inflows (Unverified)

| Source | Amount | Confidence | FinCEN Match |
|--------|--------|:----------:|:--------:|
| Deutsche Bank → Butterfly Trust | $2,650,000 (120+ wires) | STRONG | ✅ |
| Deutsche Bank → Butterfly Trust | $7,000,000 (settlements) | MODERATE | ✅ |
| Deutsche Bank → Butterfly Trust | $300,000 | PROVEN | ✅ |
| Deutsche Bank → Butterfly Trust | $30,000 | PROVEN | ✅ |
| Deutsche Bank → Butterfly Trust | $20,000 | PROVEN | ✅ |
| MC2 Model Management → Butterfly Trust | $50,000 | MODERATE | — |
| **Total Inflows** | **$10,050,000+** | | |

#### Outflows to Maxwell (Unverified)

| Transfer | Amount | Confidence |
|----------|--------|:----------:|
| Butterfly Trust → Maxwell | $150,000 | STRONG |
| Butterfly Trust → Maxwell | $100,000 | STRONG |
| Butterfly Trust → Maxwell | $50,000 | STRONG |
| Butterfly Trust → Maxwell | $30,000 | STRONG |
| Butterfly Trust → Maxwell | $21,379 | STRONG |
| Butterfly Trust → Maxwell | $12,500 | STRONG |
| Indyke → Maxwell (via Butterfly Trust) | $175,000 | STRONG |
| Indyke → Maxwell (via Butterfly Trust) | $110,000 | STRONG |
| **Total Outflows to Maxwell** | **$648,879** | |

65 "Butterfly" entities exist in ICIJ. None match "The Butterfly Trust." This was a domestic Epstein vehicle, not an offshore shell.

### MC2 Models Financial Trail (Unverified)

| Flow | Amount | Confidence |
|------|--------|:----------:|
| MC2 → JPMorgan | $800,000 | STRONG |
| MC2 → Butterfly Trust | $50,000 | MODERATE |
| Epstein → Brunel | $1,000,000 | Fund flow reference (see [$1M Offshore Wire](#the-1m-offshore-wire) below) |
| Visoski → Brunel | $182,219 | PROVEN |
| Visoski → Brunel | $10,000 | PROVEN |

---

## The Offshore Evidence

### Deposition Testimony — BVI Money Transfers

**Found in 3 documents:**
- [EFTA00181297.pdf](https://www.justice.gov/epstein/media/EFTA00181297.pdf)
- [EFTA01111413.pdf](https://www.justice.gov/epstein/media/EFTA01111413.pdf)
- [EFTA01248647.pdf](https://www.justice.gov/epstein/media/EFTA01248647.pdf)

Deposition testimony describes money transferred to the British Virgin Islands — the same jurisdiction where Scouting International was incorporated in November 2003.

### The $1M Offshore Wire

**Found in 3 documents:**
- [EFTA00589437.pdf](https://www.justice.gov/epstein/media/EFTA00589437.pdf)
- [EFTA00599855.pdf](https://www.justice.gov/epstein/media/EFTA00599855.pdf)
- [EFTA01122242.pdf](https://www.justice.gov/epstein/media/EFTA01122242.pdf)

A $1 million wire transfer from Epstein to Brunel's offshore account is referenced in the context of MC2 being described as a recruitment pipeline. The destination of this wire is unspecified in the released documents, but the offshore infrastructure — Scouting International, BVI, incorporated November 2003, now defunct — is sitting in the same network.

### Epstein Funding Brunel's Legal Defense

**Source:** Link & Rockenbach PA billing records — matter: "Jean-Luc Brunel, MC2 Model & Talent Miami, LLC, Tyler MacDonald"

| Invoice | Amount | Period |
|---------|--------|--------|
| #817 | $2,917.50 | July 2018 |
| #1032 | $4,657.50 | August 2018 |
| #1826 | $13,816.63 → $24,391.65 (with past due) | January 2019 |
| #2383 | $3,135.00 | March 2019 |

---

## Network Architecture

```
EPSTEIN FINANCIAL NETWORK — BRUNEL OFFSHORE BRANCH

     ┌─── ICIJ Offshore Leaks ───┐
     │                            │
     │  Scouting International    │
     │  Investment Co., Ltd.      │
     │  BVI (Inc. Nov 2003)       │
     │  Status: DEFUNCT           │
     │                            │
     │  Intermediaries:           │
     │  ├── Portcullis TrustNet   │
     │  └── NetIncorp.com Corp    │
     │                            │
     └────────────┬───────────────┘
                  │
     DOJ Subpoena (EFTA00809672)
     names as Brunel-controlled
                  │
     ┌────────────┴────────────┐
     │                         │
  MC2 Models Mgmt       Karin Models Agency
  MC2 Models Miami      (predecessor to MC2)
     │
     │ $50,000
     ▼
  ┌── Butterfly Trust ──┐
  │  Acct #44130552     │
  │  JPMorgan Chase     │
  └──┬──────────────┬───┘
     │              │
  Deutsche Bank   Butterfly Trust
  → $10M+         → Maxwell $648K+
  (FinCEN ✅)     (8 STRONG-tier transfers)

  ┌─── Deposition Testimony ───┐
  │ "monies transferred to the │
  │ British Virgin Islands"    │
  │ (3 documents)              │
  └────────────────────────────┘

  ┌─── Court Filings ─────────┐
  │ "$1M wire transfer to      │
  │ Brunel's offshore account" │
  │ (3 documents)              │
  └────────────────────────────┘
```

---

## NetIncorp Investigation

NetIncorp.com Corporation (ICIJ node 290197), the second intermediary that incorporated Scouting International, has **689 connected entities** in the ICIJ Offshore Leaks database. Eleven of those entity names appeared in the EFTA document corpus. All 11 were investigated and determined to be **false positives** from entity recognition artifacts:

| NetIncorp Client | BVI | Mentions | Verdict | Actual Content |
|-----------------|:---:|:--------:|---------|---------------|
| eMedia Technologies Ltd | ✓ | 43 | ❌ FALSE POSITIVE | OCR fragments: "Remedial," "CTVglobemedia" |
| Nepal Pacific Group Inc. | ✓ | 14 | ❌ FALSE POSITIVE | Carpet salesman named Tenzing Nepali; $31K broadloom invoices |
| NACAR Group, Inc. | ✓ | 8 | ❌ FALSE POSITIVE | NASCAR sponsorship docs, NACARA immigration legislation |
| Inversiones EM 88, Inc. | ✓ | 7 | ❌ FALSE POSITIVE | "Inversiones Trento Spa" — Costa Rica energy press release |
| INVERSIONES PLUS CORP. | ✓ | 7 | ❌ FALSE POSITIVE | Same Costa Rica press release as above |
| 22/11 Corporation | ✓ | 7 | ❌ FALSE POSITIVE | Date formats in legal billing: "08/22/11" |
| Poseidon Research Corp. | ✓ | 6 | ❌ FALSE POSITIVE | P-8 Poseidon military aircraft news, Greek shipping address |
| Tanglewood Offshore Tech | ✓ | 3 | ❌ FALSE POSITIVE | Tanglewood Music Center (Boston) references |
| SOBOL MARINE LTD. | ✓ | 3 | ❌ FALSE POSITIVE | Lyubov Sobol (Russian opposition figure) in news clippings |
| TAKEDA PROPERTIES LTD | ✓ | 3 | ❌ FALSE POSITIVE | Takeda Pharmaceuticals training venue |
| Radiance Generation, Inc. | ✓ | 2 | ❌ FALSE POSITIVE | Frederic Fekkai salon: "Color Radiance Treatment" ($65 hair service) |

**Result:** NetIncorp.com's 689 BVI client entities share **zero** actual connections to the Epstein financial network beyond Scouting International. The Brunel link is precise and isolated — not ambient noise from a broader intermediary relationship.

---

## Methodology

### Databases Cross-Referenced

| Source | Records | Purpose |
|--------|---------|---------|
| DOJ EFTA Corpus | 1,476,377 files | Source documents, entity extraction, financial flows |
| ICIJ Offshore Leaks | 814K entities, 771K officers, 3.3M relationships | Offshore shell identification |
| FinCEN SAR Data | Cross-reference | Transaction verification |
| Fund Flows (5C) | 23,832 directional flows | A→B money movement |
| Fund Flows Audited (5B) | 81,451 classified transactions | 5-tier confidence scoring |
| Verified Wires | Court-exhibit authenticated | Exhibit-authenticated transfers |

### Scripts Executed

| Script | Purpose | Output |
|--------|---------|--------|
| `icij_crossref.py` | Initial ICIJ fuzzy matching | 745 entity, 63 officer, 25 intermediary matches |
| `icij_deep_dive.py` | Relationship graph extraction | Full node trees for 5 targets |
| `icij_crossref_final.py` | Financial table cross-reference | Person ↔ shell ↔ fund flow mapping |
| `brunel_exhaustive.py` | 7-part exhaustive network dig | Portcullis/NetIncorp intermediary graphs |
| `brunel_full_dig.py` | 172-document, 8,526-page corpus scan | Shell entity hit map, wire references |
| `netincorp_deep.py` | 11-entity deep verification scan | All false positives confirmed |

### Other ICIJ-Confirmed Epstein Network Entities

The initial cross-reference identified four additional high-confidence ICIJ matches beyond Brunel:

| Person | ICIJ Source | Offshore Entity | Epstein Financial Link |
|--------|-----------|-----------------|----------------------|
| Jes Staley | Paradise Papers – Barbados | WAGGONER (BARBADOS) LTD | JPMorgan → Staley $1.38M, FinCEN confirmed |
| Michael Dubin | Paradise Papers – Appleby | Powers & Dubin Asset Mgmt (Bermuda), CPD Asset Mgmt (Bermuda) | Financial Trust → Dubin $10M ("Jeepers"), $5M JFK/Harvard |
| Epstein Family Trust | Offshore Leaks – Cook Islands | Node 169778 | Robert J Mintz intermediary, Trustcorp Limited officer |
| Ghislaine Investments | Bahamas Leaks | GHISLAINE INVESTMENTS LTD (node 20161231) | NES LLC → Maxwell $7.66M, 2,725 fund flow records |

These entities are noted for completeness. Each warrants independent narrative treatment.

---

## What's Original, What's Not

### Original
1. **The connected map** — Computational cross-reference linking ICIJ Offshore Leaks ↔ DOJ subpoena ↔ Butterfly Trust wire flows ↔ FinCEN data ↔ BVI deposition testimony in a single analytical framework
2. **The methodology** — Programmatic cross-referencing of three massive databases at scale (1.48M files × 814K ICIJ entities × FinCEN records)
3. **The NetIncorp verification** — Exhaustive 689-entity scan proving the Brunel connection is isolated, not ambient
4. **The completeness** — 8,526 pages across 172 Brunel-related documents, every financial table queried

### Not Original
- Brunel's name is searchable on [offshoreleaks.icij.org](https://offshoreleaks.icij.org/) today
- The subpoena ([EFTA00809672](https://www.justice.gov/epstein/media/EFTA00809672.pdf)) is a publicly released DOJ document
- Butterfly Trust flows were covered in 2023 JPMorgan/Deutsche Bank lawsuit reporting
- The $1M offshore wire was reported by the Daily Beast
- BVI transfer testimony exists in previously available deposition transcripts

### Honest Characterization

Rigorous forensic synthesis of public data. The individual nodes existed in separate databases. The connected map — linking an ICIJ-confirmed offshore shell to a DOJ subpoena to a $10M+ domestic trust pipeline to deposition testimony about BVI money transfers — is the original contribution. That's what forensic accounting does: it connects things that are individually known into a picture that wasn't previously visible.

---

## Appendix: Document Corpus

172 documents across the EFTA corpus contain Brunel-related financial or legal content. Key term frequency across 8,526 pages:

| Term | Hits | Files | Significance |
|------|:----:|:-----:|-------------|
| MC2 Model | 94 | 36 | Widespread — core entity |
| BVI | 362 | 77 | Mostly abbreviation noise; 3 files contain deposition testimony |
| Scouting International | 1 | 1 | ONLY in EFTA00809672 — the subpoena |
| Butterfly Trust | 15 | 5 | Court filings + financial exhibits |
| offshore | 6 | 4 | Includes "$1M wire transfer to Brunel's offshore account" |
| wire transfer | 16 | 7 | Financial documents with transaction details |
| British Virgin | 3 | 3 | Deposition testimony about BVI transfers |
| Karin Models | 14 | 10 | Depositions confirming MC2 predecessor |
| L'eclair | 1 | 1 | ONLY in EFTA00809672 — dead end |
| shell | 23 | 12 | References to shell companies in Epstein enterprise |

---

*Narrative 18 of the Epstein Financial Forensics project. Published February 23, 2026.*
*Every claim is anchored to specific bates stamps and court exhibits. Verify any finding at [justice.gov/epstein](https://www.justice.gov/epstein).*
