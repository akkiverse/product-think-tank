# Spec: WealthManager (Private Family & Friends Wealth & News Intelligence Portal)

- **Card:** https://github.com/akkiverse/product-think-tank/issues/2 · **Brief:** [BRIEF.md](BRIEF.md) · **Version:** 2 · **Date:** 2026-11-01

## Goal
Build a private, invite-only, visually striking **Wealth & News Intelligence Portal** for Abhishek (**Admin**), his family, and close friends (**Members**). Each user logs in to see their **Groww / Zerodha / Mutual Fund portfolio report** with live-refreshed valuations, **AI-generated portfolio correction & rebalancing suggestions** (powered by **Google Gemini API** or **local Ollama**), and **personalized notifications** from live business/economic news that affects either **their investments** or **the company/industry they work in** — while the **Admin** can create/manage users, view which news is helpful to which user, and **block or unblock** passing any news insight to a specific person's dashboard.

## User stories and acceptance criteria

### US-1: Invite-Only Authentication & Admin User Management
As the Admin (Abhishek), I want to be the only person who can create and manage user accounts (including their employer company, sector, and risk profile), with zero public self-registration, so that only my family and friends can access the portal.
- **AC-1.1** Given the login page or auth API, when an unauthenticated visitor accesses the app, then no public sign-up/registration endpoint or form is exposed; only valid credentials created by the Admin can log in and receive a session token.
- **AC-1.2** Given an authenticated Admin session, when the Admin creates or updates a user (`username`, `display_name`, `password`, `role`, `employer_company`, `employer_sector`, `risk_profile`, `notes`), then the user account is persisted and that user can immediately log in to their own isolated dashboard.
- **AC-1.3** Given a non-admin Member session, when the Member attempts to call any Admin user-management or news-moderation endpoint, then the API rejects the request with `403 Forbidden`.

### US-2: Groww & Zerodha Portfolio Import + Live Market Price / NAV Sync
As a logged-in user (or Admin managing a family member's account), I want to import holdings from **Groww**, **Zerodha** (via CSV export, JSON, quick entry, or Zerodha Kite Connect API token), and refresh live stock prices and AMFI Mutual Fund NAVs so that my portfolio report shows accurate current value, P&L, and asset/sector allocation.
- **AC-2.1** Given a Groww or Zerodha holdings CSV upload (or manual holding entry with symbol/scheme code, broker tag `Groww`/`Zerodha`/`Other`, asset type `STOCK`/`MUTUAL_FUND`/`GOLD`/`FD`, quantity, and average buy price), when imported for a user, then the holdings are normalized and saved to that user's portfolio.
- **AC-2.2** Given a user's saved portfolio containing NSE/BSE stocks and AMFI mutual fund scheme codes, when the portfolio report or live-sync endpoint is requested, then it fetches latest stock prices and AMFI NAVs (with graceful offline/cached fallback) and computes total invested, current value, overall P&L (₹ and %), asset-class split, and sector weights.
- **AC-2.3** Given a Zerodha Kite Connect API token & key configured for a user, when the Zerodha live-fetch endpoint is triggered, then it fetches and updates holdings from Zerodha's `/portfolio/holdings` API (or reports a clear connection status if token is expired).

### US-3: AI Portfolio Correction & Actionable Suggestions Engine (Google Gemini + Local Ollama)
As a logged-in user, I want the app to analyze my portfolio using **Google Gemini API** or **local Ollama** (plus financial hygiene rules) and tell me concrete corrections I should make (e.g., sector over-concentration, high-fee Regular mutual funds vs Direct plans, overlapping funds, single-stock risk, loser/winner rebalancing, and curated MF baskets / IPO radar).
- **AC-3.1** Given a user's portfolio, when the Portfolio Analysis engine runs, then it generates structured **Correction Recommendations** (`severity`: High/Medium/Low, `category`: Concentration / Fee Leak / Overlap / Rebalance / Tax / Opportunity, `title`, `explanation`, `suggested_action`, `quantified_impact_inr`) and an overall **Portfolio Health Score (0–100)**.
- **AC-3.2** Given the AI Provider configuration (`gemini`, `ollama`, or `auto`), when an analysis or news-interpretation request runs, then the backend routes to Google Gemini (`GEMINI_API_KEY`), local Ollama (`OLLAMA_BASE_URL` / model name), or the deterministic financial analyzer fallback without failing if a service is unreachable.

### US-4: Live Business/Economic News + Employer Company Intelligence + Admin Block/Unblock Moderation
As a logged-in user, I want notifications and deep analysis when latest business/economic news affects **my portfolio holdings** OR **the company/industry I work in**; and as **Admin**, I want to see which news is matched to which user across all users and **block or unblock** passing specific news insights to any user's dashboard.
- **AC-4.1** Given live business & economic news items (fetched from financial RSS feeds or custom news refresh) and the list of users, when the News Intelligence analyzer runs, then it matches news items to each user based on **(a) their stock/MF holdings & sectors** and **(b) their `employer_company` and `employer_sector`**, generating a plain-English impact explanation (`why_it_matters`, `action_suggestion`, `match_type`: `PORTFOLIO` | `EMPLOYER` | `MACRO`, `sentiment`: `POSITIVE` | `WATCH` | `RISK`).
- **AC-4.2** Given the Admin News Moderation Matrix, when the Admin views all user-matched news insights and toggles `blocked = true` (or `false`) for a specific `(news_id, user_id)` pair, then that news notification and suggestion is immediately hidden from (or restored to) that user's dashboard and notification feed.
- **AC-4.3** Given a logged-in Member viewing their dashboard and notification drawer, when their feed is loaded, then they see **only unblocked** news insights relevant to their portfolio, their employer company, or key macro events, clearly tagged with `"Employer Impact (<Company>)"` or `"Portfolio Impact (<Ticker/Sector>)"`.

### US-5: Attractive, Professional Executive Wealth UI
As Abhishek and his family/friends, we want a modern, polished, attractive UI that feels like a private wealth management suite on desktop and mobile.
- **AC-5.1** Given the web interface, when rendered, then it provides a cohesive executive theme (deep navy/emerald/gold glassmorphism aesthetic, interactive allocation & sector visual charts, broker badges for Groww/Zerodha, AI correction cards, an Employer & Market Intelligence notification feed, Curated MF/IPO Explorer, and a dedicated Admin Control Center for user & news moderation) with zero personal contact data and **zero pre-filled credentials or quick-login bypass buttons** on the login page.

### US-6: Normalized Relational Database (`users`, `user_employers`, `broker_accounts`, `portfolio_holdings`, `news_articles`, `user_news_insights`) & Daily News Dates
As Abhishek, I want a clean, normalized relational database where `users` stores only core identity and maps via `user_id` to separate `user_employers` (multiple companies/ESOPs) and `broker_accounts` (multiple Zerodha/Groww/family accounts per user), and where every news article displays its exact publication date (`published_at` / `published_date`).
- **AC-6.1** Given the database layer (`PostgreSQL` via `DATABASE_URL` or local `SQLite`), when initialized, then it creates the 7 normalized tables defined in [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) (`users`, `user_employers`, `broker_accounts`, `portfolio_holdings`, `news_articles`, `user_news_insights`, `system_settings`) with `user_id` foreign-key relationships.
- **AC-6.2** Given a logged-in user, when they add or manage multiple broker accounts (e.g., `"My Zerodha"`, `"Mom's Zerodha"`, `"My Groww"`) and multiple employer profiles, then holdings and Zerodha API tokens are stored against the specific `broker_account_id` and `user_id`, not inside the `users` table.
- **AC-6.3** Given any news item in the user feed or Admin Moderation Matrix, when returned by the API and rendered in the UI, then it includes `published_at` and formatted `published_date` (`YYYY-MM-DD`) sorted newest-first.
- **AC-6.4** Given the public login page (`GET /`), when rendered, then the username and password inputs have no pre-filled `value` attributes and no quick-login credential buttons are present.

## Screens
| Screen | Who | Purpose | Stories |
|---|---|---|---|
| **1. Private Invite-Only Login** | All | Clean sign-in screen with empty Username & Password fields (no registration form, no pre-filled credentials). | US-1, US-5, US-6 |
| **2. My Wealth Report & Corrections Dashboard** | Member & Admin | Net worth KPI cards, filter by Broker Account (e.g., *All Accounts*, *My Zerodha*, *Mom's Zerodha*, *Groww*), Asset & Sector allocation charts, Holdings table with live P&L, and **AI Portfolio Correction & Rebalancing Cards**. | US-2, US-3, US-5, US-6 |
| **3. Personalized News & Employer Intelligence Feed** | Member & Admin | Notification bell + dedicated intelligence cards showing **publication date (`published_date`)**, analyzed business/economic news matched to the user's **Employer Companies** (`user_employers`) and **Portfolio Holdings**, with AI action notes. | US-3, US-4, US-5, US-6 |
| **4. Broker Accounts & Portfolio Sync Studio** | Member & Admin | Manage multiple **Broker Accounts** per user (add *My Zerodha*, *Spouse/Parent Zerodha*, *Groww*), one-click **Groww/Zerodha CSV Upload** per account, **Zerodha Kite API Connector** per account, and **Curated MF Baskets & IPO Radar**. | US-2, US-3, US-6 |
| **5. Admin Control Center (Users + Employers + News Gatekeeper + AI Settings)** | Admin only | (a) Create/Edit Family & Friend users + map their **Employer Profiles (`user_employers`)**, (b) **User-News Relevance Matrix** (with publication date) and 1-click **Block / Unblock** toggle per user, and (c) **AI Engine & DB Status** (Google Gemini API vs Local Ollama + live Database status badge). | US-1, US-3, US-4, US-5, US-6 |

## Data (Normalized Relational Schema — Full DDL in [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md))
| Table | Primary Key / Foreign Keys | Key Columns |
|---|---|---|
| `users` | `id` (PK) | `username` (UNIQUE), `display_name`, `password_hash`, `role` (`admin`\|`member`), `risk_profile`, `is_active`, `created_at` |
| `user_employers` | `id` (PK), `user_id` (FK → `users.id`) | `company_name`, `stock_symbol`, `sector`, `relationship_type` (`PRIMARY_EMPLOYER`\|`PREVIOUS_ESOP`\|`FAMILY_EMPLOYER`), `holds_esop`, `is_primary` |
| `broker_accounts` | `id` (PK), `user_id` (FK → `users.id`) | `broker_name` (`Zerodha`\|`Groww`\|`Other`), `account_label`, `account_holder_name`, `client_id`, `sync_mode`, `api_key`, `access_token`, `last_synced_at` |
| `portfolio_holdings` | `id` (PK), `user_id` (FK → `users.id`), `broker_account_id` (FK → `broker_accounts.id`) | `asset_type`, `symbol`, `name`, `sector`, `quantity`, `avg_price`, `live_price`, `plan_type`, `expense_ratio_regular`, `expense_ratio_direct`, `price_updated_at` |
| `news_articles` | `id` (PK) | `title`, `source`, `url`, `published_at` (TIMESTAMPTZ), `published_date` (DATE), `summary`, `companies_json`, `sectors_json`, `sentiment` |
| `user_news_insights` | `id` (PK), `news_id` (FK → `news_articles.id`), `user_id` (FK → `users.id`) | `match_type`, `matched_on`, `ai_analysis`, `suggested_action`, `blocked_by_admin`, `moderated_by`, `moderated_at`, `is_read` |
| `system_settings` | `setting_key` (PK) | `setting_value_json`, `updated_at` |

## Integrations
1. **Google Gemini API (`https://generativelanguage.googleapis.com`):** Used for deep portfolio correction advice and news-to-user/employer analysis when `GEMINI_API_KEY` is configured.
2. **Local Ollama API (`http://localhost:11434/api/generate` or custom `OLLAMA_BASE_URL`):** Used when running locally or connected via tunnel.
3. **Live Market Quotes & AMFI NAVs:** `https://api.mfapi.in/mf/<code >` for mutual funds and public NSE/Yahoo quote endpoints for Indian stocks (with deterministic fallback prices so offline/test runs never fail).
4. **Live Business & Economic News RSS:** Economic Times Markets/Economy, Moneycontrol, LiveMint, and Google News India Business RSS feeds.
5. **Zerodha Kite Connect API (`https://api.kite.trade/portfolio/holdings`):** Optional direct holdings pull when a user enters their Kite API key & access token, alongside native **Groww & Zerodha CSV import**.
*(All external HTTP calls are mocked in `pytest` unit tests per `AGENTS.md`.)*

## Non-functional
- **Security & Privacy:** Invite-only login; password hashing; role-based access control (`admin` vs `member`); no personal phone/email/address hardcoded in public repo files.
- **Resilience:** If Gemini, Ollama, RSS, or upstream quote APIs are offline, the app falls back cleanly to built-in analytical intelligence and cached quotes.
- **Stack:** Python **FastAPI** backend + modern Executive Wealth Single-Page UI (`Tailwind` + `Lucide` icons + interactive SVG charts), deployable to Vercel (`akkiverse`) and runnable locally alongside Ollama.

## Out of scope (v1)
- Public self-registration or commercial billing/subscriptions.
- Automated order placement / trade execution (the app advises on corrections; users execute trades in Groww/Zerodha).

## Environment variables needed (names only; Abhishek sets them in Vercel or `.env`)
| Name | What for |
|---|---|
| `GEMINI_API_KEY` | Optional: Google Gemini API key for cloud AI portfolio & news analysis |
| `OLLAMA_BASE_URL` | Optional: URL for local Ollama (defaults to `http://localhost:11434`) |
| `OLLAMA_MODEL` | Optional: Ollama model name (defaults to `llama3.2` or `gemma2`) |
| `ADMIN_DEFAULT_PASSWORD` | Optional: Initial password for the `admin` account (defaults to a safe local bootstrap password changeable in UI) |
| `APP_SECRET_KEY` | Session signing key |
