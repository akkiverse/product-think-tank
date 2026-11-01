# Business brief: WealthManager (Private Family & Friends Edition)

- **Card:** https://github.com/akkiverse/product-think-tank/issues/2 · **Idea:** [IDEA.md](IDEA.md) · **Date:** 2026-11-01 · **Author:** analyst (updated for Private Family & Friends Portal)

## Verdict: GO · Score 88/100
**Strong GO.** Because this is a **private, invite-only portal for Abhishek, his family, and close friends** (not a public commercial product), public customer-acquisition costs and commercial licensing hurdles disappear. Combining **Groww/Zerodha portfolio import + live market price/NAV sync + Google Gemini / Local Ollama analysis + Employer/Business News matching + Admin Block/Unblock moderation** delivers massive personal value at **$0/month** operating cost.

## Target Users & Scope
- **Users:** Abhishek (**Admin**) + 5 to 25 invited family members and close friends (**Members**).
- **Access:** Strictly **invite-only login**. No public registration form exists anywhere in the app.
- **Core Value:**
  1. Every user logs in and sees an **attractive, professional wealth report** of their Groww/Zerodha stocks and mutual funds with **AI-generated portfolio correction suggestions**.
  2. Every user sees **analyzed notifications** when business/economic news impacts either **their investments** OR **the company/industry they work in**.
  3. **Admin (Abhishek)** creates users, sees which news is matched to which user across the whole circle, and can **Block or Unblock** any news insight from appearing on a specific person's dashboard.

## How Groww & Zerodha Fetching Works Best
| Portal | Reality of Official APIs | How WealthManager Fetches & Keeps It Live |
|---|---|---|
| **Zerodha** | Has **Kite Connect API** (token-based holdings fetch) + 1-click Console CSV export | Supports **both** direct Zerodha Kite API token fetch AND 1-click Zerodha Holdings CSV import. |
| **Groww & Other Portals** | Groww has **no public retail API** for personal accounts, but provides 1-click Holdings Export (CSV/Excel) & CAMS/CAS statements | Users (or Admin) upload their **Groww Holdings file** (or add tickers/MF schemes once). Thereafter, **WealthManager automatically fetches live NSE/BSE stock prices and live AMFI Mutual Fund NAVs** on every refresh! |

## Costs
| Item | At launch / month | For 20 Family & Friends / month |
|---|---|---|
| Hosting (Vercel team `akkiverse` or local Mac) | $0 | $0 |
| AI Engine: **Local Ollama** (`http://localhost:11434`) | $0 | $0 |
| AI Engine: **Google Gemini API** (`GEMINI_API_KEY` free tier / flash) | $0 | $0–$2 |
| Live Market Prices (AMFI NAV API + Yahoo/NSE public quote feed) | $0 | $0 |
| Live Business & Economic News (ET, Moneycontrol, Mint, Google News RSS) | $0 | $0 |
| **Total** | **$0 / month** | **$0–$2 / month** |

Build effort: **1 focused build cycle** (Python FastAPI backend + luxury executive fintech UI).

## Risks & Mitigations
| # | Risk | Likelihood (L/M/H) | Mitigation |
|---|---|---|---|
| 1 | **Groww doesn't offer a direct OAuth API** | H | Built-in **Groww & Zerodha CSV parser + Smart Live Quote/NAV Engine**: import holdings once, and the app fetches live stock prices & MF NAVs automatically. |
| 2 | **Local Ollama isn't reachable when viewing the Vercel cloud URL** | M | **Dual AI Switcher**: Admin can choose `Google Gemini API`, `Local Ollama`, or `Auto (try Gemini/Ollama, fallback to built-in analytical engine)`. |
| 3 | **Noisy or alarming news reaching a family member's dashboard** | M | **Admin Moderation Matrix**: Admin sees all user-matched news items and can toggle **Block / Unblock** per user at any time. |
| 4 | **Vercel serverless filesystem resets between deploys** | M | Support external DB/KV URL if provided, plus 1-click Admin JSON backup/restore & pre-seeded family/demo accounts so state is never lost. |

## Score
| Criterion | 0–20 | Why |
|---|---|---|
| Problem pain | 19 | High personal value for family & friends who hold scattered Groww/Zerodha portfolios and miss actionable corrections or employer/sector news. |
| Fit for audience | 19 | Tailor-made for a private 5–25 person circle with Admin gatekeeping and employer-aware intelligence. |
| Technical feasibility | 16 | Groww/Zerodha import + live quote/NAV enrichment + RSS news + Gemini/Ollama works cleanly without paid institutional feeds. |
| Cost efficiency | 18 | Virtually $0/month using local Ollama and Google Gemini API. |
| Ease to build & maintain | 16 | Self-contained Python FastAPI app with an executive web UI and full test suite. |
| **Total** | **88/100** | **Strong GO** |

## Recommendation for Abhishek
**Approve build (Option A).** The updated `SPEC.md` now includes every single feature you asked for: invite-only login, Admin user creation, Groww/Zerodha portfolio ingestion + live price/NAV refresh, Google Gemini + local Ollama analysis, employer-company & economic news matching, Admin Block/Unblock controls per user, and a sleek, professional UI.
