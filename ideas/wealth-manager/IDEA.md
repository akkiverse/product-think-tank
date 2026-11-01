# Idea: WealthManager (Private Family & Friends Wealth & News Intelligence Portal)

- **Card:** https://github.com/akkiverse/product-think-tank/issues/2 · **Slug:** `wealth-manager` · **Date:** 2026-11-01 · **Author:** strategist (updated with Founder's private-portal requirements)

## In one sentence
A private, invite-only wealth and intelligence portal for Abhishek, his family, and close friends that imports portfolios from Groww, Zerodha, and other Indian portals, refreshes live stock/MF prices, analyzes holdings + live business/employer news using Google Gemini or local Ollama, and gives the Admin full control to create users and block/unblock which news insights reach each person's dashboard.

## Customer
- **Who:** Strictly private — Abhishek (Admin), his family members, and close friends. **Not a commercial public SaaS.**
- **How many:** ~5 to 25 trusted users (invite-only; **no public self-registration**).
- **How they cope today:** Each family member or friend has investments scattered across Groww, Zerodha, or mutual funds, misses important economic/company news (including news about the company they work for), or gets confused by noisy market headlines without someone filtering and explaining what correction they actually need to make.

## Problem
- **"My family and friends hold stocks and mutual funds on Groww/Zerodha, but don't know what corrections to make."** Over-concentration in one sector, overlapping mutual funds, or holding lagging assets goes unnoticed for months.
- **"Important business, economic, or employer-company news gets missed — or noisy news causes panic."** If a user works at a specific company (or holds stocks in a sector hit by policy/economic shifts), they need analyzed, relevant alerts — while the Admin needs a way to **block/unblock** specific news items from reaching a family member's dashboard if it's unhelpful or alarming.
- **"How do we pull Groww & Zerodha portfolios into one place and keep values live?"**
  - **Zerodha** provides the Kite Connect API + Console CSV export.
  - **Groww** does not provide a public retail API, but provides 1-click Holdings CSV/XLSX exports (and CAMS/CAS statements).
  - By combining **1-click Groww/Zerodha Holdings Import + optional Zerodha Kite API token sync + automatic live NSE/BSE stock price & AMFI Mutual Fund NAV refresh**, every user gets live portfolio tracking without paying broker data fees.

## Why now
1. **Dual AI availability (Google Gemini API + Local Ollama):** We can run deep portfolio health diagnostics and news-to-user relevance matching using either **Google Gemini API** (cloud/Vercel) or **local Ollama** (`http://localhost:11434` on Abhishek's Mac) at zero cost.
2. **Private family office portal in a box:** Modern FastAPI + executive fintech UI on Vercel lets a founder give family & friends a private-bank-grade dashboard with Admin oversight in days.

## Competitors and alternatives
| Name | What they do | Price | Why they don't fit our private circle |
|---|---|---|---|
| **Groww / Zerodha / Angel One** | Individual broker apps | Free / Brokerage | Siloed per broker; no Admin family oversight; no employer-company intelligence; no Admin news moderation |
| **INDmoney / MProfit** | Public portfolio trackers | Free – ₹5,000/yr | Public commercial apps with ads/upsells; no Admin ability to create private accounts or filter/block news per family member |
| **WhatsApp family group + Excel** | Manual sharing of news links and spreadsheets | Free | Unstructured, no live NAV/price refresh, no automated AI portfolio correction engine |

## Money (Private Utility — Not for Commercial Sale)
- **Revenue model:** None needed (private internal tool for Abhishek, family, and friends).
- **Running cost:** **$0/month** using Vercel (`akkiverse` team), free AMFI/Yahoo Finance public market feeds, live financial RSS feeds, local **Ollama** (free on Mac), and free-tier **Google Gemini API**.

## Risks (and cheapest test)
| Risk | Type | How we solve it |
|---|---|---|
| **Groww has no public retail OAuth API** | Technical | Support **Groww & Zerodha CSV/JSON 1-click upload + quick ticker entry**, and once tickers/MF codes are stored, automatically fetch **live stock prices & live AMFI NAVs** on login. Also include a **Zerodha Kite Connect API token** connector for direct Zerodha sync. |
| **Local Ollama is not reachable from public Vercel cloud unless tunneled** | Architecture | Build a **Dual AI Router**: uses **Google Gemini API** (`GEMINI_API_KEY`) in the cloud or locally, switches to **Local Ollama** (`OLLAMA_BASE_URL`) when running locally or via tunnel, and includes a built-in deterministic analyzer fallback so it never errors out. |
| **Unhelpful or panic-inducing news reaching a family member** | UX / Governance | **Admin News Gatekeeper:** Admin sees every news item matched to each user (portfolio match + employer match) and can toggle **Block / Unblock** per user in one click. |
| **Unauthorized strangers trying to sign up** | Security | **Zero public registration.** Only Admin can create users, assign passwords, and activate/deactivate accounts. |

## Smallest useful version (v1 Complete Feature Set)
A sleek, professional **Executive Dark/Light Fintech Web App** (Python FastAPI backend + rich interactive dashboard UI) with:
1. **Invite-Only Auth & Admin User Management:** Login screen (no sign-up button). Admin can create/edit family & friend accounts, set their **Employer Company & Industry/Sector**, and manage credentials.
2. **Groww & Zerodha Portfolio Sync + Live Price/NAV Engine:** Import holdings from **Groww CSV**, **Zerodha Console CSV**, **Zerodha Kite API token**, or quick-add stocks/mutual funds/IPO bids, with live price & AMFI NAV refresh.
3. **AI Portfolio Correction & Rebalancing Engine (Gemini + Ollama):** Analyzes each user's holdings and generates actionable correction cards (sector over-concentration, Direct-vs-Regular MF fee drag, underperforming holdings, overlapping funds, risk balance, and curated MF/IPO opportunities).
4. **Live Business/Economic News + Employer Company Intelligence:** Pulls live Indian business/economic news feeds, runs AI impact analysis against both the user's **investments** and their **employer company/industry**, and creates personalized notification alerts.
5. **Admin Intelligence & News Moderation Center:** Shows Admin all users, which news/suggestion is matched to which user and why, with 1-click **Block / Unblock** controls to control what appears on each user's dashboard.

## Founder's words
> An app that helps you make investment decisions and gives suggestions is typically known as a Wealth Management or Full-Service Brokerage App...
>
> basically it is not for business it would be just for me, my family and friends.
> I have ollama running locally and even Google ’s API.
> what I want is we can fetch our investment report from Groww, Zerodha or some other portals and this app should analyse and suggest what correction we can do.
> I want separate user have their own login, with a admin who can create the user and maintain the required dash board and app. No one can register of their own.
> I am not sure but looking for API or some way to fetch live details from Groww or Zerodha of the portfolio.
> Not only that, the app can fetch latest news related to business and economics from news sources (Required analysis) and based on that provide suggestions on Dashboard.
> Basically, what I want is when I login to app I can see the report, and notifications if some news is helpful for me. It should be properly analysed. For example I am working in a certain company so if something I can get from there all those information should be provided.
> Admin will get information for all users like which news is helpful to which user. he will have access to block or unblock passing that info to that person’s dashboard.
> Also, do work on UI it should look attractive and professional
