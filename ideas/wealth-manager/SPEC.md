# Spec: WealthManager

- **Card:** https://github.com/akkiverse/product-think-tank/issues/2 · **Brief:** [BRIEF.md](BRIEF.md) · **Version:** 1 · **Date:** 2026-11-01

## Goal
Give Indian retail investors a fast, broker-neutral web app to **(1) explore objective, low-cost Mutual Fund baskets**, **(2) check stock/sector overlap and Regular-vs-Direct fee leaks across their funds**, **(3) simulate SIP wealth creation after inflation and Indian LTCG tax**, and **(4) inspect upcoming Indian IPOs via plain-English DRHP fundamentals and red-flag checklists** — with zero login, zero personal data collection, and $0/month infrastructure cost. Success for v1 = all acceptance criteria tests passing and a live Vercel preview ready for user testing.

## User stories and acceptance criteria

### US-1: Curated Mutual Fund Baskets & Live NAV Lookup
As an Indian retail investor overwhelmed by 1,500+ mutual fund schemes, I want to browse pre-built, rule-based mutual fund baskets ("Top Tax Savers (ELSS)", "High Growth Long Term", "Better than Fixed Deposits", "Low-Cost Index Core") and look up live AMFI NAVs so that I can compare funds by objective metrics (3Y/5Y CAGR, expense ratio, max drawdown, risk grade).
- **AC-1.1** Given the Mutual Fund Baskets view, when a user selects a basket category (`tax-savers`, `high-growth`, `better-than-fd`, `index-core`), then the API returns the curated funds in that basket with scheme code, category, 3Y/5Y CAGR, expense ratio (Direct vs Regular), risk level, and selection rationale.
- **AC-1.2** Given a valid AMFI scheme code, when the live NAV endpoint is called, then it returns the latest NAV and date from the AMFI feed (with graceful fallback to cached NAV data if the upstream API is unreachable).
- **AC-1.3** Given a search or filter by risk level or maximum expense ratio, when the user filters funds, then only schemes matching those objective rules are returned.

### US-2: Portfolio Overlap & Direct-vs-Regular Fee Leak X-Ray
As an investor holding multiple mutual funds, I want to select 2 to 5 funds and enter my current corpus + monthly SIP so that I can see how much my funds overlap in underlying stocks and how much money I lose over 10 years to Regular-plan commissions.
- **AC-2.1** Given 2 to 5 selected mutual fund IDs, when the user runs the Portfolio X-Ray, then the API calculates the pairwise and overall stock overlap percentage, lists the overlapping stocks with combined weights, and shows sector concentration.
- **AC-2.2** Given a portfolio corpus, monthly SIP, and selected funds, when the Fee Leak calculation runs, then it computes the 10-year rupee difference between Direct plan expense ratios and Regular plan expense ratios and assigns a diversification hygiene score (0–100).

### US-3: IPO Intelligence & DRHP Red-Flag Decoder
As a retail investor deciding whether to bid on an Indian IPO, I want a plain-English breakdown of upcoming/recent IPOs (financial health, valuation vs listed peers, promoter holding, issue objective, and red flags) plus the ability to paste any IPO prospectus/note text for instant risk scoring so that I don't rely on social-media hype.
- **AC-3.1** Given the IPO Intelligence screen, when the user views the IPO radar or selects an IPO, then the API returns structured fundamentals: issue size, fresh issue vs Offer-for-Sale (OFS) split, P/E vs peer average, revenue/PAT growth, pros, red flags, and an objective fundamentals score (0–100).
- **AC-3.2** Given custom pasted text from an IPO note or DRHP summary, when the user submits it to the DRHP Decoder endpoint, then it extracts positive signals (e.g., debt reduction, revenue growth, fresh issue) and risk flags (e.g., high OFS %, litigation, promoter pledge, negative cash flow, valuation premium) with a plain-English checklist.

### US-4: SIP Step-Up, Inflation & Indian LTCG Tax Simulator + SEBI Compliance
As a long-term investor, I want to simulate a monthly SIP with an annual step-up percentage, expected return, inflation rate, and Indian Equity LTCG tax (12.5% above ₹1.25 lakh exemption) so that I see my real post-tax purchasing power.
- **AC-4.1** Given monthly SIP amount (₹), annual step-up (%), duration (years), expected return (% p.a.), and inflation (% p.a.), when the simulator runs, then it returns total invested, pre-tax corpus, estimated Indian LTCG tax (12.5% on gains above ₹1,25,000), post-tax corpus, inflation-adjusted corpus in today's rupees, and year-by-year breakdown.
- **AC-4.2** Given any page or API summary response, when rendered, then it includes the mandatory SEBI educational/analytical tool disclaimer and contains zero personal contact details.

## Screens
| Screen | Purpose | Stories |
|---|---|---|
| **1. Overview & Curated MF Baskets** | Filterable cards for "Top Tax Savers", "High Growth Long Term", "Better than Fixed Deposits", and "Low-Cost Index Core" with live AMFI NAV lookup. | US-1, US-4 |
| **2. Portfolio Overlap & Fee-Leak X-Ray** | Interactive 2–5 fund comparator showing stock overlap matrix, sector concentration warning, and 10-year Regular-vs-Direct fee leak in ₹. | US-2 |
| **3. IPO Intelligence & DRHP Decoder** | Curated IPO cards (Fresh vs OFS bar, Peer P/E comparison, Red-Flag badges) + interactive text analyzer for any IPO summary. | US-3 |
| **4. SIP Step-Up & Post-Tax Wealth Simulator** | Interactive ₹ calculator with annual step-up, inflation adjustment, and 12.5% LTCG tax breakdown table. | US-4 |

## Data
| Entity | Fields | Stored where | Personal data? |
|---|---|---|---|
| `MutualFundScheme` | `id`, `amfi_code`, `name`, `basket`, `category`, `cagr_3y`, `cagr_5y`, `expense_direct`, `expense_regular`, `risk`, `top_holdings` (stock + weight + sector) | Bundled JSON dataset + live NAV via `api.mfapi.in` | No |
| `IpoProfile` | `slug`, `company`, `sector`, `issue_size_cr`, `fresh_issue_pct`, `ofs_pct`, `pe_ratio`, `peer_pe`, `rev_cagr_3y`, `pat_margin`, `pros`, `red_flags`, `score` | Bundled JSON dataset | No |
| `PortfolioXRayInput` | `fund_ids`, `current_corpus_inr`, `monthly_sip_inr` | Stateless request / browser local state only | No |

## Integrations
- **AMFI Public Mutual Fund NAV API (`https://api.mfapi.in/mf/<scheme_code>`):** Free, unauthenticated public endpoint for latest Indian mutual fund NAVs. Mocked in all automated tests (`pytest`) and wrapped with a local fallback so the app works offline or if `mfapi.in` is slow.

## Non-functional
- **Privacy:** Zero personal data on public pages; no user accounts, phone numbers, emails, or PAN/demat credentials collected.
- **Regulatory safety:** Visible banner & footer disclaimer stating that `WealthManager` is an educational & mathematical analysis tool and not a SEBI-registered Investment Adviser or Stock Broker.
- **Speed:** All endpoints respond in < 300 ms (cached/local calculations).
- **Stack:** Python **FastAPI** backend serving a clean, responsive single-page web UI (`vercel.json` configured for Vercel Python serverless deployment on team `akkiverse`).

## Out of scope (v1)
- Direct stock or mutual fund order execution / brokerage matching.
- UPI mandate creation or live IPO bidding (users click out to their broker).
- Personalized "Buy / Sell / Hold" stock price targets.
- Paid NSE/BSE real-time tick-by-tick feeds.
- User login, database storage of personal portfolios, or Account Aggregator (AA) KYC onboarding.

## Environment variables needed (names only; Abhishek sets them in Vercel)
| Name | What for |
|---|---|
| *(None required for v1)* | All v1 features run on free public data and deterministic financial math with zero secret keys needed. |
