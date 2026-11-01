# Product profile: WealthManager

- **Repo:** https://github.com/akkiverse/wealth-manager · **Live:** https://wealth-manager-akkiverse.vercel.app (local: `http://127.0.0.1:8088`) · **Version:** `1.0.0`
- **Status:** Release v1.0.0 Ready (awaiting PR #1 merge) · **Last inspected:** 2026-11-01 · **Card:** https://github.com/akkiverse/product-think-tank/issues/2

## What it is and who it's for
A private, invite-only wealth and career-aware news intelligence portal for Abhishek (Admin), his family, and close friends. It consolidates holdings from Groww and Zerodha, refreshes live NSE stock prices and AMFI Mutual Fund NAVs, generates portfolio correction recommendations via Google Gemini API or Local Ollama, and matches live business/economic news against each user's holdings and employer company — with Admin gatekeeping to block or unblock news per user.

## Stack
- **Backend:** Python 3.12+, FastAPI, Pydantic, HTTPX, Uvicorn
- **Frontend:** Executive Dark/Emerald/Gold Single-Page Web Suite (Tailwind CSS)
- **AI Engine:** Dual AI Router supporting Google Gemini API (`GEMINI_API_KEY`), Local Ollama (`OLLAMA_BASE_URL`), and deterministic financial hygiene rules
- **Hosting:** Vercel Python Serverless (`vercel.json`)

## How to run, test and deploy
```bash
# run locally
uv run --with fastapi --with httpx --with uvicorn uvicorn api.index:app --reload --port 8088

# run full test suite (12/12 AC tests, outside APIs mocked)
uv run --with pytest --with fastapi --with httpx pytest -v
```
Deploy: Connected to Vercel (`akkiverse/wealth-manager`); deploys production on merge to `main`.

## Features (from the spec)
| Feature | Spec IDs | Notes |
|---|---|---|
| Invite-only login & Admin user management (with Employer Company & Sector) | `AC-1.1`, `AC-1.2`, `AC-1.3` | Zero public sign-up; strict RBAC |
| Groww & Zerodha CSV import, manual holdings, and Zerodha Kite Connect API sync | `AC-2.1`, `AC-2.2`, `AC-2.3` | Live NSE stock & AMFI NAV enrichment |
| Dual AI Portfolio Correction Engine (Gemini + Local Ollama) | `AC-3.1`, `AC-3.2` | Employer + Portfolio double-risk, Regular-vs-Direct MF fee leak, stock/MF overlap |
| Personalized Business & Employer News Radar + Admin Block/Unblock Gatekeeper | `AC-4.1`, `AC-4.2`, `AC-4.3` | Per-user moderation matrix |
| Executive Private-Wealth UI | `AC-5.1` | Responsive dashboard, sync studio, Admin Control Center |

## Docs map
| Doc | What's in it |
|---|---|
| [README.md](https://github.com/akkiverse/wealth-manager/blob/main/README.md) | Overview, local run, test, and env vars |
| [docs/SPEC.md](https://github.com/akkiverse/wealth-manager/blob/main/docs/SPEC.md) | Full user stories (`US-1`–`US-5`) and acceptance criteria (`AC-1.1`–`AC-5.1`) |
| [docs/changes/CR-0001-initial-build.md](https://github.com/akkiverse/wealth-manager/blob/main/docs/changes/CR-0001-initial-build.md) | Change request for initial `v1.0.0` release |
| [docs/adr/ADR-0001-architecture-and-dual-ai-engine.md](https://github.com/akkiverse/wealth-manager/blob/main/docs/adr/ADR-0001-architecture-and-dual-ai-engine.md) | Architecture & Dual AI Router decision |
| [docs/test-reports/CR-0001.md](https://github.com/akkiverse/wealth-manager/blob/main/docs/test-reports/CR-0001.md) | 12/12 passing AC test report |
| [docs/releases/v1.0.0.md](https://github.com/akkiverse/wealth-manager/blob/main/docs/releases/v1.0.0.md) | Release notes for `v1.0.0` |

## Open work
- PRs: [akkiverse/wealth-manager#1](https://github.com/akkiverse/wealth-manager/pull/1) (`CR-0001` / `v1.0.0`, ready for founder merge)
- Issues: None

## Risks and gaps
| Gap | Where | Why it matters |
|---|---|---|
| Serverless state resets on redeploy unless backed by external DB/KV | `app/store.py` | On Vercel serverless, in-memory changes reset across cold starts; connecting a lightweight cloud DB/KV (Neon/Upstash) makes Admin-created users & CSV imports permanent in the cloud. |

## Suggested next ideas
1. **Cloud Postgres/KV persistence for Vercel:** Persist Admin-created users, imported Groww/Zerodha holdings, and news block rules across serverless cold starts.
2. **CAMS / NSDL Consolidated Account Statement (CAS) PDF parser:** Let family members drop their password-protected CAMS PDF statement directly for automatic mutual fund + demat import.
3. **Weekly Family Wealth Digest (Email / Telegram):** Optional Admin-approved weekly summary of portfolio P&L and unblocked employer/market news.
