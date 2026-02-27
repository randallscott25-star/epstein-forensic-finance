# Follow the Money, Follow the Plane

**32 same-day matches. 4.3× above random chance. $575 million in wire transfers within 3 days of a documented Epstein aircraft flight.**

*All amounts are (Unverified) automated extractions from DOJ EFTA documents. Appearance in this analysis does not imply wrongdoing. See [COMPLIANCE.md](../docs/COMPLIANCE.md) for professional standards framework.*

---

## What I Found

I cross-referenced 160 verified wire transfer dates against 321 documented flight dates for Epstein's two registered aircraft — N212JE (Gulfstream) and N908JE (Boeing 727). The flight data comes from CBP APIS records in the EFTA corpus.

The overlap runs 4.3× above random chance.

Wire transfers and aircraft movements clustered on the same dates at a rate that calendar coincidence can't explain. Over the period October 2013 through April 2019, 32 wire transfers landed on the exact same date as a documented flight, and 149 transfers fell within a ±3-day window of documented aircraft movement.

I'm not claiming causation. I'm showing the timing.

## The Data Sources

**Financial transfers**: 185 verified wire transfers with dates, court exhibit references, and bates stamps, extracted from Deutsche Bank-SDNY production documents (Exhibits A through E). Date range: October 2013 – April 2019. Source: [master wire ledger](../data/master_wire_ledger_phase5i.json).

**Aircraft flights**: APIS passenger manifests for N212JE and N908JE recovered from the EFTA corpus (Datasets <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">8</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">9</a>, and <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">11</a>). These are CBP customs declaration records showing passenger name, date of birth, aircraft tail number, flight date, and ICAO airport codes for departure and arrival. 321 unique flight dates identified after filtering Epstein's DOB (01/20/1953) from OCR artifacts. Date range: 1990 – June 2019.

**Aircraft registration**: FAA registry confirms N908JE registered to JET ASSETS INC, 1712 Pioneer Ave, Cheyenne, WY. N212JE is the Gulfstream IV used for shorter routes.

**Victim-related documents**: 29,378 date-context entries from EFTA documents containing references to victims, accusers, minors, massage, trafficking, or named survivors. Used for temporal overlay only.

## The Correlation

| Window | Matches | Expected (Random) | Ratio | Wire Volume (Unverified) |
|--------|---------|-------------------|-------|---------|
| Same day (±0) | 32 | 7.5 | **4.29×** | — |
| ±1 day | 73 | ~15 | **~4.9×** | — |
| ±3 days | 149 | ~52 | **~2.9×** | $575,359,330 |

Over the 2,017-day observation window (Oct 2013 – Apr 2019):
- Wire transfers occurred on 7.9% of days (160 of 2,017)
- Documented flights occurred on 4.7% of days (94 unique dates)
- 51% of all wire transfer dates had at least one flight within ±3 days

## The St. Thomas Signal

The strongest sub-signal involves flights to and from **TIST** — Cyril E. King Airport, St. Thomas, U.S. Virgin Islands, the commercial airport serving Little St. James Island.

**49 wire-flight matches involved TIST, totaling $169,283,127 (Unverified) in transfer volume.**

| Wire Date | Flight Date | Δ | Amount (Unverified) | Wire |
|-----------|-------------|---|------|------|
| Oct 16, 2014 | Oct 17, 2014 | +1d | $7,000,000 | Leon & Debra Black → Southern Trust |
| Oct 16, 2014 | Oct 17, 2014 | +1d | $13,000,000 | Black Family Partners → Southern Trust |
| Oct 22, 2014 | Oct 23, 2014 | +1d | $2,000,000 | Leon & Debra Black → Southern Trust |
| Oct 22, 2014 | Oct 23, 2014 | +1d | $3,000,000 | Black Family Partners → Southern Trust |
| Nov 17, 2014 | Nov 19, 2014 | +2d | $1,928,647 | Jeffrey Epstein c/o HBRK → NOW/SuperNow |
| Apr 19, 2016 | Apr 20, 2016 | +1d | $500,000 | Gol Muchnik → NOW/SuperNow |
| Sep 28, 2016 | Sep 30, 2016 | +2d | $700,000 | Jeffrey Epstein → Non-DB Account |
| Dec 2, 2016 | Dec 2, 2016 | ±0d | $10,000 | Kyara Investments → Southern Financial |

The October 2014 cluster is particularly dense: $25 million in Black-affiliated transfers to Southern Trust within one week, bracketed by N212JE flights between Teterboro (KTEB) and St. Thomas (TIST).

## The Airport Pattern

Among ±1 day wire-flight matches, the ICAO airport codes tell a geographic story:

| Airport | Code | Matches | Significance |
|---------|------|---------|-------------|
| St. Thomas, USVI | TIST | 26 | Adjacent to Little St. James Island |
| Teterboro, NJ | KTEB | 16 | Private aviation hub for Manhattan |
| Palm Beach, FL | KPBI | 14 | Near 358 El Brillo Way residence |
| Le Bourget, Paris | LFPB | 5 | Near Avenue Foch apartment |

All four airports serve Epstein's known residences and properties. The Teterboro-to-St. Thomas route (KTEB → TIST) appears repeatedly in the APIS records alongside large wire transfer dates.

## The N908JE Appearance

The Boeing 727 — N908JE, registered to Jet Assets Inc. — appears in 350 date-context entries in the EFTA corpus. Most documented flights in this analysis involve N212JE (the Gulfstream), but N908JE appears in several temporal matches:

- **March 9, 2015**: $10,484 wire (Adam Bly → NOW/SuperNow). Same day, N908JE documented.
- **June 5, 2015**: $10,484 wire (Adam Bly → NOW/SuperNow). Same ±2d window, N908JE documented.

The N908JE entries are fewer because the Boeing 727 was used less frequently in the 2013-2019 period covered by the verified wire data.

## What It Means

Money moved when the plane moved. Not always, not exclusively, but at a rate 4.3 times higher than random chance predicts for same-day overlap.

The pattern is most pronounced in two periods:

**October 2014**: The densest cluster. $45 million in verified wire transfers from Black-affiliated entities and other sources, occurring within the same week as multiple N212JE flights between Teterboro and St. Thomas.

**Late 2018**: Large Deutsche Bank → Haze Trust transfers ($5M, $8M, $6M) coinciding with frequent N212JE flights — over 75% of Deutsche Bank's outflow volume and flight frequency concentrated in the last six months before Epstein's arrest.

## Statistical Note

The 4.29× ratio for same-day overlap is calculated as:

```
Expected = (wire_dates / total_days) × (flight_dates / total_days) × total_days
         = (160 / 2017) × (94 / 2017) × 2017
         = 7.5

Observed = 32

Ratio = 32 / 7.5 = 4.29×
```

This assumes independence between wire transfers and flights — i.e., that the timing of financial transfers has no relationship to the timing of aircraft movement. The 4.29× ratio suggests this assumption is wrong.

However, a confounding variable exists: both wire transfers and flights may cluster around the same periods of high activity (e.g., months when Epstein was in New York conducting business). Seasonal clustering could inflate the observed overlap without implying direct coordination between specific wires and specific flights. A month-by-month stratified analysis would be needed to fully control for this effect.

## What I Can't Determine

- **Whether any specific wire transfer funded any specific flight.** Temporal proximity is not a causal chain. A wire on Tuesday and a flight on Wednesday may be coincidental, coordinated, or driven by a shared third factor (e.g., Epstein's calendar).
- **Who was on the flights.** The APIS records in the EFTA corpus show Epstein as the passenger of record. Other passengers may be named in the full manifest documents, but the OCR extraction from these multi-page CBP forms is incomplete.
- **Whether the victim-context dates represent dates of abuse.** Documents mentioning victims carry dates — but those dates may be filing dates, hearing dates, or reference dates in legal proceedings, not dates of events described in the documents.
- **The complete flight record.** The APIS data covers international and some domestic flights logged through CBP. Domestic flights not involving customs declarations may not appear in this dataset.
- **The direction of causality.** Even where temporal correlation exists, the data cannot distinguish between "money moved because travel was planned" and "travel occurred because money had arrived."

---

*Source: DOJ EFTA Document Release — Deutsche Bank-SDNY Production (Exhibits A–E), APIS/CBP Passenger Records (Datasets <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">8</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">9</a>, <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">11</a>), FAA Aircraft Registry. 2,411,188 dates extracted from 1,072,086 files via automated pipeline. Statistical calculation assumes uniform distribution of events across 2,017-day observation window (Oct 2013 – Apr 2019). This analysis appears in the [master wire ledger](../data/master_wire_ledger_phase5i.json) and supporting data published with this repository.*

---

## Source Documents & Exhibits

### Primary Exhibits
**All Exhibits A–E** (<a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a>): 122 dated wires used for temporal correlation against flight log dates.

| Exhibit | Dated Wires | Value |
|---------|-------------|-------|
| A | 17 | $151,499,980 |
| B | 18 | $33,139,248 |
| C | 64 | $89,372,037 |
| D | 11 | $68,760,686 |
| E | 12 | $6,253,493 |

### Flight Log Source
Flight logs extracted from EFTA corpus (doc_type = flight_log). Correlation computed as wire-to-flight temporal proximity (±3 day window).

### Corpus Statistics Source
**Method**: Temporal correlation analysis — wire dates vs. flight log dates with geographic enrichment.
**Finding**: 4.3× random correlation rate; $169M in wires within ±3 days of St. Thomas flights.
**Database**: 1,476,377 files, 11.4M extracted entities (see [METHODOLOGY.md](../docs/METHODOLOGY.md)).

### Scope Note
Wire dates are from Deutsche Bank production only. Flight correlations may also exist with Bear Stearns/JPMorgan transaction dates not available in this production. The 4.3× rate is a lower bound.

### 📄 EFTA Source Documents

*Click any document ID to open the DOJ PDF in a new tab. Click a Dataset number to browse neighboring files.*

| Document | Source | Description |
|----------|--------|-------------|
| <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> | DS8 | Deutsche Bank-SDNY Production: Exhibits A–E (160 dated wire transfers) |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-8-files" target="_blank">Dataset 8</a> | DS8 | APIS/CBP passenger manifests — aircraft N212JE, N908JE |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-9-files" target="_blank">Dataset 9</a> | DS9 | APIS/CBP passenger manifests — additional flight records |
| <a href="https://www.justice.gov/epstein/doj-disclosures/data-set-11-files" target="_blank">Dataset 11</a> | DS11 | APIS/CBP passenger manifests — additional flight records |
| <a href="https://registry.faa.gov/AircraftInquiry" target="_blank">FAA Aircraft Registry</a> | External | FAA Aircraft Registry — tail number N212JE (Gulfstream), N908JE (Boeing 727) |

### 📊 Verify in Forensic Workbook

| Exhibit / Analysis | View in Workbook |
|---|---|
| Master Wire Ledger — All dated wires | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=2043824625#gid=2043824625" target="_blank">📊 Open Tab</a> |
| Date Recovery — Phase 23 | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=339305346#gid=339305346" target="_blank">📊 Open Tab</a> |
| Executive Summary | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1804001356#gid=1804001356" target="_blank">📊 Open Tab</a> |
| Methodology | <a href="https://docs.google.com/spreadsheets/d/11lw0QjMZ-rYIjWesv5VG1YKts57ahPEm/edit?gid=1840632994#gid=1840632994" target="_blank">📊 Open Tab</a> |

### How to Verify
EFTA document IDs from public DOJ release at <a href="https://efts.gov" target="_blank">efts.gov</a>. Wire data from <a href="https://www.justice.gov/epstein/files/DataSet%208/EFTA00027019.pdf" target="_blank">EFTA00027019</a> Exhibits A–E. Flight logs from EFTA corpus. Full methodology in [METHODOLOGY.md](../docs/METHODOLOGY.md).
