# Idea: WealthManager

- **Card:** https://github.com/akkiverse/product-think-tank/issues/2 · **Slug:** `wealth-manager` · **Date:** 2026-11-01 · **Author:** strategist

## In one sentence
Indian retail investors overwhelmed by 1,500+ mutual funds, 5,000+ stocks, and noisy IPO hype get a calm, plain-English research and portfolio companion that explains mutual fund baskets, IPO fundamentals, and portfolio overlap without pushing high-commission trades.

## Customer
- **Who:** Salaried Indian retail investors (ages 24–42) who already hold a discount brokerage account (Groww, Zerodha, Angel One, Upstox) and invest ₹5,000–₹50,000/month via SIPs and occasional stocks/IPOs, but do not have the time or training to read 300-page DRHP IPO filings or compare mutual fund rolling returns and portfolio overlap.
- **How many:** India has 150M+ demat accounts (CDSL + NSDL) and 80M+ active mutual fund SIP accounts as of 2025–2026 ([SEBI](https://www.sebi.gov.in), [AMFI](https://www.amfiindia.com)). Even 0.01% of active DIY investors represents ~8,000–15,000 users.
- **How they cope today:** They switch between Groww/Zerodha for execution, Value Research/Tickertape for screening, YouTube/Telegram "finfluencers" for IPO verdicts, and Excel spreadsheets to check if their mutual funds hold the same stocks.

## Problem
- **"I own 6 mutual funds, am I actually diversified?"** Most DIY investors buy "top-rated" funds that hold the exact same top-20 nifty stocks, paying multiple expense ratios for closet indexing.
- **"Should I apply for this IPO or is it just hype?"** Mainboard and SME IPOs launch every week; reading a Red Herring Prospectus takes hours, while social media tips are biased or unverified.
- **"Brokers make money when I trade, not when I sit tight."** Full-service brokerage apps nudge frequent buying/selling or push regular (commission-bearing) plans instead of unbiased portfolio hygiene.
- **Cost of the pain:** 1%–2% annual drag from high-expense/overlapping funds, bad IPO allocations, and hours of weekend research anxiety.

## Why now
1. **SEBI crackdown on unregistered finfluencers & unverified tips (2024–2026):** Investors are actively looking for transparent, data-backed, rule-based research tools rather than social-media stock tips.
2. **Account Aggregator (AA) & CAS (Consolidated Account Statement) adoption:** Investors can export a single NSDL/CDSL/CAMS PDF statement of their holdings in 60 seconds, making broker-agnostic portfolio analysis possible without building a brokerage from scratch.
3. **LLMs for financial filing summarization:** Summarizing a 400-page SEBI DRHP (IPO prospectus) into structured strengths, red flags, valuation multiples, and peer comparisons now costs pennies per filing.

## Competitors and alternatives
| Name | What they do | Price | Gap we fill |
|---|---|---|---|
| **Groww / Upstox / Paytm Money** | Execution-first discount brokers with basic fund lists and 1-click UPI IPO bidding | ₹0–₹20/order | Great for buying, weak on deep portfolio overlap, unbiased IPO red-flag extraction, and cross-broker advice |
| **Angel One (ARQ Prime)** | Full-service broker with rule-based stock scores and research | Brokerage + add-ons | Tied to an Angel One brokerage account; built to drive trading volume |
| **INDmoney** | Net-worth tracker (Indian + US stocks, MFs) via Account Aggregator | Free + commission/premium tiers | Cluttered UI with heavy upselling of credit/insurance/loans |
| **Tickertape / Value Research** | Stock & MF screeners and ratings | Free – ₹2,500/yr | Data-heavy tables for enthusiasts; doesn't turn a user's actual portfolio + upcoming IPOs into a plain-English action checklist |
| **Do nothing / spreadsheet + YouTube** | Manual tracking in Google Sheets + finfluencer videos | Free | High effort, stale data, and unverified hype |

## Money
- **Important regulatory distinction:** Actually executing trades (brokerage) or giving personalized "buy/sell/hold" stock tips requires heavy **SEBI Stock Broker / Registered Investment Adviser (RIA) / Research Analyst (RA)** licenses and net-worth deposits. However, **software tools for educational screening, public-data IPO prospectus breakdowns, and mathematical mutual-fund overlap/cost calculators** can launch as a pure SaaS information tool (with clear SEBI disclaimers: educational/analytical tool, not personalized investment advice).
- **Model:** Freemium SaaS subscription paid by the investor (no commissions, no ads, no data selling):
  - **Free tier:** Live IPO Prospectus Explainer (plain-English summary of business, financials, promoter pledges, litigation red flags from official DRHP) + Curated MF Category Explorer (objective metrics: rolling returns, expense ratio, drawdown).
  - **Pro tier (₹299/month or ₹1,999/year):** Unlimited CAMS/CAS Portfolio X-Ray (stock-level overlap across funds, expense-ratio leak calculator, asset-allocation drift alert) + Watchlist alerts.

## Risks (and cheapest test)
| Risk | Type | How to test cheaply |
|---|---|---|
| **SEBI RIA/RA regulatory boundary:** Crossing from "analytical data tool" into unlicensed "personalized buy/sell advice" is illegal in India. | Legal / Regulatory | Keep v1 strictly to objective metrics (expense ratio, historical rolling return, % portfolio overlap, and cited DRHP prospectus extracts) with zero "Buy/Sell/Hold" verdicts unless partnered with a SEBI-registered RA/RIA. |
| **Building a full brokerage is impossible for a 1-week MVP:** UPI IPO bidding and stock execution require exchange memberships. | Build / Scope | Don't build a brokerage; build the **decision companion** that links out to the user's existing broker (Groww/Zerodha/Angel One) once they decide. |
| **Free data availability:** Real-time NSE/BSE tick data is expensive to license for redistribution. | Cost / Data | Use free end-of-day AMFI mutual fund NAV/scheme data (`api.mfapi.in` / AMFI text feed) and official public SEBI IPO filings. |
| **Crowded space:** Every broker has a free mutual fund page. | Market / Distribution | Differentiate on **Portfolio X-Ray (overlap + fee leak)** and **1-page DRHP Red-Flag Extractor**, which brokers rarely highlight because they want users to buy more funds/IPOs. |

## Smallest useful version
A 1-week **FastAPI + Streamlit (or lightweight React) web app on Vercel** with three focused screens using free public Indian market data (no SEBI license or brokerage backend required):
1. **MF Basket & Overlap Analyzer:** Pick 2–5 Indian mutual funds (via free AMFI data) or paste holdings to see: (a) stock/sector overlap, (b) fee drag (Regular vs Direct plan 10-year cost), and (c) objective category leaders ("Tax Savers / ELSS", "Low-Volatility Debt/Liquid", "Index Core") ranked purely by rolling return consistency and expense ratio.
2. **IPO DRHP Plain-English Decoder:** Upload or select an upcoming Indian IPO prospectus summary to see a structured breakdown: business model in 3 bullets, revenue/profit trend, valuation vs listed peers, and a "Red Flags & Risks" checklist (litigation, debt repayment vs fresh issue).
3. **SIP Goal & Step-Up Simulator:** Interactive calculator showing how a monthly SIP + annual step-up reaches a target corpus after inflation and LTCG tax.

## Open questions for Abhishek (max 3)
1. **Positioning:** Since becoming a SEBI-licensed broker (like Groww/Angel One) takes crores in capital and years of compliance, should we focus `WealthManager` v1 as an **unbiased Portfolio X-Ray & IPO Research Companion** that works alongside any broker the user already has?
2. **Market:** Should v1 focus exclusively on **Indian markets** (NSE/BSE IPOs + AMFI Mutual Funds in ₹), or do you want a global/US market angle?
3. **First feature to lead with:** Which hook do you like best for v1 — **(A) Mutual Fund Portfolio X-Ray + Curated Baskets**, **(B) AI IPO Prospectus Red-Flag Decoder**, or **(C) Both in one clean dashboard**?

## Sources
- [SEBI Master Circulars for Investment Advisers & Research Analysts](https://www.sebi.gov.in)
- [AMFI India Mutual Fund & SIP Data](https://www.amfiindia.com)
- [MFAPI.in — Open Indian Mutual Fund NAV API](https://www.mfapi.in)

## Founder's words
> An app that helps you make investment decisions and gives suggestions is typically known as a Wealth Management or Full-Service Brokerage App. Unlike basic budget trackers, these act like a digital stockbroker and financial advisor rolled into one. Here is exactly how they help you navigate stocks, mutual funds, and IPOs: Stock Market Suggestions: Instead of just giving you a search bar to buy and sell, many of these apps feature AI-powered advisory engines or in-house research teams. They provide "buy, sell, or hold" recommendations, stock screeners to help you find undervalued companies, and daily market insights so you do not have to do all the heavy technical analysis yourself. Curated Mutual Funds: Trying to pick from thousands of mutual funds can be overwhelming. These apps analyze past performance, expense ratios, and risks, then categorize them into easy, pre-made baskets—like "Top Tax Savers," "High Growth for Long Term," or "Better than Fixed Deposits." They also allow you to automate your investments through a monthly SIP (Systematic Investment Plan). IPO Intelligence: When a new company goes public (IPO), these apps provide simplified expert reviews. They break down the company's financial health, explain the pros and cons of the business, and highlight expected listing gains. Applying is generally as simple as entering your UPI ID and approving a payment mandate on your phone. Popular Apps That Fit This Description: Angel One: This is a strong choice if you want active guidance. It features an AI-driven engine called ARQ Prime that provides rule-based stock recommendations, alongside detailed research reports and advisory services.    Rupeezy Groww: Highly rated for beginners. While it is more hands-off with direct stock tips, it excels at helping you discover top-performing mutual funds through easy-to-read charts and offers a frictionless, one-click process for IPO applications.    Decentro INDmoney: Excellent if you want an AI-driven overview of your entire financial life. It tracks your existing investments, suggests ways to diversify your portfolio, and lets you invest seamlessly in Indian stocks, mutual funds, and even US stocks.    BlinkMoney Upstox & Paytm Money: Both offer fast, uncluttered platforms with smart watchlists, curated mutual fund ideas, and deep company analytics to help you make informed decisions before you bid on an IPO. These platforms are heavily regulated (by SEBI) and link securely to your bank, making it safe and easy to build a diversified portfolio directly from your smartphone.
