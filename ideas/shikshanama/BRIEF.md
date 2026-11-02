# Business brief: Shikshanama (शिक्षाNama) Official Website & Admin CMS

- **Card:** https://github.com/akkiverse/product-think-tank/issues/7 · **Idea:** [IDEA.md](IDEA.md) · **Date:** 2026-11-02 · **Author:** analyst

## Verdict: GO · Score 71/100
A known client with a real, seasonal need (results-led admissions and WhatsApp leads), a clear feature list and a stack that
fits free tiers make this worth building. The biggest risk is **publishing minors' photos and marks without recorded parental
consent**; the spec makes a consent tick mandatory before any result goes live. Two items must be settled **before release**
(not before build): which Vercel plan hosts a commercial client site, and the institute's real content (numbers, founders, results).

## Market
- **This build:** one client (Shikshanama, West Patel Nagar, New Delhi, multiple nearby branches). Audience: Class 6–12 students
  and parents within a few kilometres; traffic peaks around board results (May) and admissions (March–July).
- **Wider:** India's coaching/test-prep market is roughly USD 7–8 billion (2025, IMARC) with ~68,000+ listed centres, ~89%
  independent (rentechdigital). Many have no proper website, so a polished, re-skinnable template could be sold later.
- **Reach for the client:** Instagram @shikshanamaofficial bio link, Google Business Profile website field, WhatsApp status,
  QR code on posters at each branch. Cost per visitor: ~₹0 (organic).

## Business model
- **This client:** one-off build fee + optional monthly care/hosting. Market range (unverified): ₹25k–₹60k build,
  ₹1k–₹3k/month care. Actual fee: **unknown, Abhishek to confirm.**
- **If turned into a template later** (not part of this build): ~₹15k setup + ₹1,500/month per institute →
  100 institutes ≈ ₹1.5 lakh/month, 1,000 ≈ ₹15 lakh/month recurring (illustrative only).

## Costs
| Item | At launch / month | At 1,000 visitors/day / month |
|---|---|---|
| Vercel (Python functions) | ₹0 on Hobby, but Hobby is non-commercial; Pro ≈ \$20 (~₹1,700) | same |
| Database: Neon Postgres via Vercel Marketplace (free tier, 0.5 GB) | ₹0 | ₹0 (content + leads ≪ 0.5 GB) |
| Images: Vercel Blob (WebP, ~50–300 KB each) | ₹0 (within included usage) | ₹0–₹200 |
| AI / APIs (WhatsApp `wa.me` links, Google Maps links, no API keys) | ₹0 | ₹0 |
| Domain (institute buys/owns) | ~₹800/year, client-paid | same |
| **Total** | **₹0–₹1,700** | **₹0–₹1,900** |

Build effort: **7–10 working days** (public site ~3, admin + cropper ~4, tests + preview E2E ~2).

## Risks
| # | Risk | Likelihood (L/M/H) | Mitigation |
|---|---|---|---|
| 1 | Minors' photos/marks published without parental consent (DPDP Act 2023) | M | Mandatory "Parent/guardian consent received" tick per result; unticked results never show publicly; delete removes the photo file too |
| 2 | Hobby plan is non-commercial; client site may need a paid plan | M | Abhishek decides the hosting plan before release; build and previews work on the current team |
| 3 | Staff stop updating content → stale site | M | Very simple admin, mobile-friendly; 20-min hand-over on the preview; ticker/batches show "last updated" in admin |
| 4 | Lead form spam or fake numbers | M | Indian mobile format check, honeypot field, per-IP rate limit, admin can delete leads |
| 5 | Scope creep (fully bilingual, online payments, student login) | H | Explicit out-of-scope list in SPEC; new asks become new CRs |

## Score
| Criterion | 0–20 | Why |
|---|---|---|
| Problem pain | 16 | Results and batch info are the main reasons parents choose; today they're scattered over Instagram/WhatsApp and leads get missed in season |
| Market | 12 | One known client now; template upside is real but unproven |
| Ability to win | 16 | Client is already engaged; a custom results wall, locked crops and WhatsApp-first leads beat Wix/Classplus for this use |
| Money | 12 | Fee unknown; low running cost; possible paid-plan cost if hosted commercially |
| Ease / cost to build | 15 | Standard CRUD + server-rendered pages, free tiers fit; but large surface (8 admin managers + cropper) |
| **Total** | **71/100** | GO |

Rule: GO ≥ 70 with no blocker · REFINE 45–69 or a fixable blocker · DROP < 45 or a hard blocker.

## If REFINE: what must change
- n/a (GO). Before **release**: confirm hosting plan, client's domain, and load real content with consent.

## Recommendation for Abhishek
**Approve the build.** Merge PR #8 and move card #7 to **Approved: build**. Please also answer the 3 questions in IDEA.md
(fee, domain/hosting plan, English vs fully bilingual); none of them blocks the build, but they must be settled before release.
