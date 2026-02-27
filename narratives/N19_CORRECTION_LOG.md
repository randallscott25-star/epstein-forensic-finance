# N19 — Data Quality Correction Log

## What Changed

Between initial publication and the current version, 30 entities were removed from the N19 roster. Dollar values were corrected for several others. This document explains why.

## The Problem

The narrative was pulling dollar values from the wrong table.

The database has two financial tables. `fund_flows` is the raw NLP extraction — the parser reads every document in the corpus, and when it sees a name near a dollar amount, it logs a row. That's a proximity score. It does not mean that person sent or received that money. `fund_flows_audited` is the verified version. Every row gets a confidence tier: PROVEN, STRONG, MODERATE, WEAK, or VERY_WEAK.

The original narrative used `fund_flows`. It should have used `fund_flows_audited` filtered to MODERATE confidence and above.

## What That Means in Practice

When a news article about a $10 million art swindler sentencing mentions a public figure in the same article, the parser logs that figure's name with $10 million. A story about a $6 million lobbying case that mentions the same name — another $6 million. A Colonial Pipeline ransom story — another $4.4 million. Stack 130 of those rows and you get $168 million attributed to a name that never sent or received a dime through the Epstein financial network.

That's co-occurrence noise. The NLP saw the name and the number in the same document. It did not verify a sender, a receiver, an account, or a transaction.

## Who Was Removed and Why

Every entity removed had zero verified financial transactions at MODERATE confidence or above. Their names appeared in the document corpus — sometimes extensively — but had no bank statements, no wire records, no trust documents, and no internal emails showing them as sender or receiver of funds.

**30 entities removed (all $0 verified):**

Donald Trump, Bill Clinton, Prince Andrew, Ehud Barak, Larry Summers, Woody Allen, Leon Botstein, Bill Richardson, Bill Gates, Benjamin Netanyahu, Peter Mandelson, Alan Dershowitz, Mark Epstein, Jack Scarola, Reid Weingarten, Laura Menninger, Gerald Lefcourt, Ken Starr, David Boies, Alex Acosta, William F. Sweeney Jr., Geoffrey Berman, Barry Krischer, Jojo Fontanilla, Sultan Bin Sulayem, Cecile De Jongh, Ariane de Rothschild, Scott Denett, Kathy Ruemmler, Audrey Strauss

## Who Stayed and Why

The 39 remaining entities have verified financial activity. Bank statements with their names as account holders. Wire transfer records with sender/receiver/amount/date fields. Trust documents with disbursement schedules. Internal emails discussing specific payments.

Names like Leon Black, Ghislaine Maxwell, Darren Indyke — they stayed because they have real bank data parsed from Deutsche Bank production documents (DB-SDNY series), JPMorgan records, and Citibank statements.

## Dollar Corrections

Several entities that remained had their dollar values adjusted downward after removing WEAK and VERY_WEAK tier entries:

| Entity | Before | After | Reason |
|---|---|---|---|
| Ghislaine Maxwell | $908.2M | $121.2M | 87% was news article co-occurrence |
| Richard Kahn | $360.1M | $132.1M | Removed unverified proximity hits |
| Leon Black | $628.0M | $258.8M | Retained only verified bank data |
| Larry Visoski | $73.3M | $19.3M | Removed unverified proximity hits |
| Noam Chomsky | $6.3M | $2.2M | Single BNY Mellon account statement parsed as 36 separate rows |
| Karyna Shuliak | $3.0M | $2.7M | Removed newspaper article co-occurrence (doorman wages article) |

## The Takeaway

The underlying transaction data is solid. Bank statements, wire records, trust documents — that data didn't change. What changed is which table was used to surface dollar attribution. Proximity is not attribution. A name appearing near a number in a document is not the same as a verified transfer between identified parties.

The pipeline works. The mapping layer had a bug. It was caught, corrected, and the commit history timestamps every change.

## Methodology

All dollar values now derive from `fund_flows_audited` at MODERATE confidence or above. The tier system:

- **PROVEN** — Parsed directly from bank statements with sender, receiver, amount, and date
- **STRONG** — Corroborated across multiple source documents
- **MODERATE** — Real financial context with identifiable parties

WEAK and VERY_WEAK tiers are excluded from all published figures. The global noise rate at MODERATE and above is under 1%.

Full methodology documented in [METHODOLOGY.md](../docs/METHODOLOGY.md).
