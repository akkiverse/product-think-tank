# Business brief: WealthManager

- **Card:** https://github.com/akkiverse/product-think-tank/issues/2 · **Idea:** [IDEA.md](IDEA.md) · **Date:** 2026-11-01 · **Author:** analyst

## Verdict: GO · Score 74/100
**GO**, scoped strictly as an **unbiased Indian Mutual Fund Basket Explorer, Portfolio Overlap/Fee-Leak X-Ray, and IPO Prospectus (DRHP) Decoder** that works alongside a user's existing broker (Groww, Zerodha, Angel One). The single biggest risk is **SEBI regulatory compliance**: v1 must present objective mathematical metrics and cited DRHP facts with clear educational disclaimers, never unlicensed "Buy / Sell / Hold" stock tips or trade execution.

## Market
- **Total size:** 150M+ demat accounts and 80M+ active mutual fund SIP accounts in India ([SEBI](https://www.sebi.gov.in), [AMFI](https://www.amfiindia.com)).
- **First segment:** ~5M–10M salaried DIY retail investors (ages 24–40) investing ₹10,000–₹50,000/month across 3–8 mutual funds and applying to 4–10 mainboard IPOs per year.
- **How we reach them:**
  1. Free shareable **"Portfolio Overlap & Regular-Plan Fee Leak Report"** card (built for r/IndiaInvestments, X/Twitter fin-tech circles, and WhatsApp groups).
  2. SEO pages for upcoming Indian mainboard IPO DRHP 1-page breakdowns ("<Company> IPO DRHP Red Flags & Peer Valuation").
  3. Estimated organic CAC: ₹0–₹150 via shareable calculator tools.

## Business model
- **Who pays:** DIY Indian retail investors who want unbiased portfolio hygiene without switching brokers or getting spammed with loan/insurance upsells.
- **Pricing:**
  - **Free tier:** Curated Mutual Fund Baskets (Tax Saver ELSS, Low-Cost Index Core, Better-than-FD Liquid/Short Duration, High-Growth Flexi/Midcap), SIP Step-Up & Tax Calculator, and 3 free IPO DRHP breakdowns/month.
  - **Pro tier:** ₹199/month or ₹1,499/year for unlimited Multi-Fund Overlap & Fee-Leak X-Ray, custom DRHP/PDF red-flag analysis, and downloadable portfolio health reports.
- **Revenue projections:**
  - **At 100 paying customers:** ~₹1.5L/year (~₹12,500/month)
  - **At 1,000 paying customers:** ~₹15L/year (~₹1.25L/month)

## Costs
| Item | At launch / month | At 1,000 users / month |
|---|---|---|
| Vercel (Python FastAPI + static UI on team `akkiverse`) | $0 (Hobby / existing plan) | $0–$20 |
| Database / storage (stateless JSON + browser local storage in v1) | $0 | $0 |
| Market data (`api.mfapi.in` public AMFI NAV feed + curated holdings/IPO dataset) | $0 | $0 |
| AI / APIs (optional LLM DRHP text extraction, cached per IPO) | $0 (pre-computed / optional key) | $5–$15 |
| **Total** | **$0 / month** | **$5–$35 / month** |

Build effort: **3–4 days** for a polished, tested FastAPI web app on Vercel.

## Risks
| # | Risk | Likelihood (L/M/H) | Mitigation |
|---|---|---|---|
| 1 | **SEBI RIA/RA boundary:** Giving personalized stock "Buy/Sell" calls without a SEBI license is illegal. | M | Strictly show objective math (expense ratio, rolling return, % overlap, CAGR, cited DRHP numbers) + mandatory SEBI educational disclaimer on every screen. |
| 2 | **High competition from free broker apps** (Groww, INDmoney, Tickertape). | H | Focus on the two things brokers hide: (a) how much overlap & commission drag exists across a user's funds, and (b) plain-English IPO litigation/debt red flags. |
| 3 | **Live stock/MF holding data licensing costs.** | M | Use free official AMFI NAV APIs (`mfapi.in`) + curated top-fund portfolio holdings snapshots; require zero paid exchange feeds. |
| 4 | **Low willingness to pay for subscriptions in India.** | M | Keep running costs near $0 so the free tier builds audience while testing ₹199/mo vs one-time ₹99 "Annual Portfolio Audit" passes. |
| 5 | **Users reluctant to link bank/demat credentials to a new app.** | H | Zero login and zero credential linking in v1: users select funds or paste/upload holdings locally without giving bank/PAN access. |

## Score
| Criterion | 0–20 | Why |
|---|---|---|
| Problem pain | 16 | Almost every Indian SIP investor holds overlapping mutual funds and struggles to read 300-page IPO DRHPs. |
| Market | 17 | 80M+ active SIP accounts and booming retail IPO participation in India. |
| Ability to win | 12 | Crowded category, but "broker-neutral Portfolio Overlap + IPO Red-Flag Decoder" is a sharp, underserved wedge. |
| Money | 13 | Consumer fintech subscriptions in India are price-sensitive, though near-zero server cost makes break-even tiny. |
| Ease / cost to build | 16 | Clean Python FastAPI web app on Vercel with $0 monthly infra cost and no paid API requirement for v1. |
| **Total** | **74/100** | **GO (≥ 70, no blocker when scoped as an analytical companion)** |

Rule: GO ≥ 70 with no blocker · REFINE 45–69 or a fixable blocker · DROP < 45 or a hard blocker.

## Recommendation for Abhishek
**I recommend Option A — Approve build** for the lean, SEBI-safe v1 (`SPEC.md`): a Python FastAPI web app with **Curated Mutual Fund Baskets, Multi-Fund Overlap & Fee-Leak X-Ray, SIP Step-Up Calculator (with Indian LTCG tax), and an IPO DRHP Plain-English Red-Flag Decoder**. It costs $0/month to run, needs no SEBI brokerage license, and lets us test real user demand in days.
