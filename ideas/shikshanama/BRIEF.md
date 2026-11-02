# Business brief: Shikshanama (शिक्षाNama) Official Website & Admin CMS

- **Card:** https://github.com/akkiverse/product-think-tank/issues/7 · **Idea:** [IDEA.md](IDEA.md) · **Date:** 2026-11-02 (v2) · **Author:** analyst

## Verdict: REFINE (by the scoring rule) · Score 68/100 · Recommendation: approve anyway as a portfolio demo
v1 scored 71 when the fee was unknown. Abhishek has now confirmed it is a **free demo to win Shikshanama** (paid launch only if
they like it), and asked for React + richer motion and a WhatsApp consent flow. That means ₹0 revenue now (Money drops) and more
build work (Ease drops), while the pitch gets stronger. The score falls to 68, just under GO. The product itself needs no
change. The gap is commercial: there's no agreed launch price yet. The biggest product risk is still minors' data, now covered
by the WhatsApp/paper consent flow and fictional demo content.

## Market
- **This build:** one prospect (Shikshanama, West Patel Nagar, New Delhi, several nearby branches). Audience: Class 6–12
  students and parents nearby; traffic peaks around board results (May) and admissions (March–July).
- **Portfolio value:** the demo shows what AkkiVerse can build for local institutes. India has ~68,000+ listed coaching centres,
  ~89% independent (rentechdigital); the coaching market is ~USD 7–8 billion (2025, IMARC).
- **Reach (after launch):** Instagram @shikshanamaofficial bio link, Google Business Profile, WhatsApp status, QR posters per branch.

## Business model
- **Now:** ₹0, an investment in a sales demo.
- **If Shikshanama says yes:** paid launch. Suggested ask (to agree before or at the demo): ₹25k–₹40k setup + ₹1,500–₹3,000/month
  hosting and care, covering the Vercel paid plan (~\$20/month) and optional automatic WhatsApp later. Market ranges are unverified.
- **Later, if wanted:** re-skin for other institutes (~₹15k setup + ₹1,500/month each → 100 institutes ≈ ₹1.5 lakh/month;
  illustrative only, not part of this build).

## Costs
| Item | Demo (now) / month | Paid launch / month |
|---|---|---|
| Vercel (React static build + FastAPI function) | ₹0, Hobby (non-commercial demo is allowed) | Pro ≈ \$20 (~₹1,700), client-paid |
| Database: Neon Postgres free tier (0.5 GB) | ₹0 | ₹0 |
| Images: Vercel Blob (WebP) | ₹0 | ₹0–₹200 |
| WhatsApp (tap-to-send `wa.me` links) | ₹0 | ₹0 (automatic sending later ≈ ₹0.115/message + Meta verification) |
| Domain | none (Vercel URL) | ~₹800/year, client-paid |
| **Total** | **₹0** | **~₹1,700–₹1,900, client-paid** |

Build effort: **9–12 working days** (React public site with motion ~4, admin + cropper ~4, consent link + PDF ~1.5,
tests + preview E2E ~1.5).

## Risks
| # | Risk | Likelihood (L/M/H) | Mitigation |
|---|---|---|---|
| 1 | Real students' photos used in the demo without consent (e.g. copied from Instagram) | M | Demo uses only fictional sample people (AC-18.2); real results need consent status "Given" (US-20/21) |
| 2 | Shikshanama doesn't buy → time spent with no revenue | M | Treat as portfolio; agree a launch price before the demo; keep the code reusable for other institutes |
| 3 | React SPA hurts Google ranking or mobile speed | M | Per-route meta tags, JSON-LD, sitemap; JS budget ≤ 200 KB; admin code split out; Lighthouse ≥ 85 target |
| 4 | Parents ignore the WhatsApp consent link | M | Paper PDF fallback (US-21); dashboard shows pending consents; results simply wait |
| 5 | Demo preview link is blocked by Vercel login for outsiders | M | Use Vercel's shareable preview link or a production deploy of the demo for the pitch (Abhishek's choice) |
| 6 | Scope creep (auto WhatsApp, payments, student login) | H | Explicit out-of-scope list; new asks become new CRs |

## Score
| Criterion | 0–20 | Why |
|---|---|---|
| Problem pain | 16 | Results and batch info drive admissions; today they're scattered over Instagram/WhatsApp and leads get missed |
| Market | 13 | One prospect, but the demo doubles as a portfolio piece for a large pool of similar institutes |
| Ability to win | 17 | Polished React UI, locked crops, WhatsApp-first leads and consent flow make a strong pitch vs Wix/Classplus |
| Money | 9 | ₹0 now; paid only if Shikshanama adopts; no price agreed yet |
| Ease / cost to build | 13 | ₹0 to run, but large surface: React + FastAPI, 9 admin managers, cropper, consent link + bilingual PDF |
| **Total** | **68/100** | REFINE by rule (45–69) |

Rule: GO ≥ 70 with no blocker · REFINE 45–69 or a fixable blocker · DROP < 45 or a hard blocker.

## If REFINE: what must change
- Nothing in the product. To reach GO on paper, agree a launch price with Shikshanama (Money would rise to ~13, total ~72).
- Optional scope trims if speed matters more than polish: drop dark mode (AC-23.5) and the paper PDF (US-21) from v1.

## Recommendation for Abhishek
**Approve the build as a deliberate portfolio demo.** The score is just under 70 only because a free demo earns nothing yet,
and you've already decided it's worth it as a showcase. Merge PR #8 and move card #7 to **Approved: build**. If you can, settle
a launch price with Shikshanama before showing them the demo.
