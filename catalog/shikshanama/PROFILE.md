# Shikshanama (शिक्षाNama) · Product Profile

- **Live URL:** [https://shikshanama.vercel.app](https://shikshanama.vercel.app)
- **Repository:** [https://github.com/akkiverse/shikshanama](https://github.com/akkiverse/shikshanama)
- **Board Card:** [#7 Shikshanama (शिक्षाNama) Official Website & Admin CMS](https://github.com/akkiverse/product-think-tank/issues/7)
- **Current Version:** `v0.1.0` (CR-0001, CR-0002, CR-0003)
- **Target Audience:** Students in Classes 6–12 and parents seeking premier coaching in West Patel Nagar, New Delhi.

---

## Capabilities & Architecture

1. **Public Gen-Z Coaching Platform:**
   - **Hero & Branding:** Bold Hindi brand script (`शिक्षाNama`), count-up trust counters, top announcement ticker, and light/dark theme switch.
   - **Filterable Hall of Fame:** Instant client-side and server-side filtering by Class (10, 11, 12), Stream (Science, Commerce, Humanities, Foundation), and Academic Year.
   - **Courses & Live Batches:** Stream tabs with subject highlights, live batch schedules, and 1-click WhatsApp enrollment.
   - **Multi-Branch Locator:** Pre-configured with the flagship West Patel Nagar center (Ground Floor, E-42, Street Number 2) plus direct Google Maps directions and branch-specific WhatsApp chats.
   - **High-Conversion Lead Capture:** Free Demo Class booking form with Indian phone number normalization (`+91`), honeypot spam protection, and counsellor follow-up dispatch.

2. **Admin CMS (`/admin`):**
   - **Built-in Image Cropper:** Mandatory client-side cropper enforcing `1:1` for student results, `4:5` for founder portraits, and `16:9` for campus gallery/banners with automatic WebP compression.
   - **Parent Consent Workflow (DPDP Act 2023):** 14-day signed WhatsApp consent links (`/consent/<token>`) and downloadable A4 printable bilingual PDF forms. Unconsented results remain strictly hidden from public pages.
   - **Full Inline Edit & Reorder:** Instant inline editing and reordering (`↑`/`↓`) across Hero stats, Branches, Courses, Batches, Results, Founders, Testimonials, and Gallery.
   - **Sample Content Management & Export:** Seamless toggle between demo preview data and real data via `DEMO_MODE=false`, one-click sample purge, and UTF-8 BOM CSV export with formula-injection escaping.

---

## Tech Stack

- **Frontend:** React 18, TypeScript, Vite, custom responsive CSS with glassmorphism and reduced-motion compliance.
- **Backend:** FastAPI (Python 3.13), stateless HMAC-SHA256 session tokens, CSRF protection, and lockout protection.
- **Data & Storage:** Neon Postgres in production (SQLite fallback in local/tests) and Vercel Blob storage with fallback blob table.
- **Hosting:** Vercel team `akkiverse`.
