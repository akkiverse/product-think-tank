# Idea: Shikshanama (शिक्षाNama) Official Website & Admin CMS

- **Card:** https://github.com/akkiverse/product-think-tank/issues/7 · **Slug:** `shikshanama` · **Date:** 2026-11-02 · **Author:** strategist

## In one sentence
Shikshanama, a multi-branch coaching institute in West Patel Nagar, New Delhi, gets most enquiries from word of mouth and
Instagram but has no website of its own. We give it a mobile-first website plus an easy admin panel, so parents and students
can see real results and book a free demo in under a minute, and staff can keep everything up to date without a developer.

## Customer
- **Paying customer:** the Shikshanama owners/founders (one client, several branches around West Patel Nagar).
- **People using the site:** students in Class 6–12 (Foundation, Science, Commerce, Humanities) and, more importantly, their
  **parents**, who decide and pay the fees. They live within a few kilometres, find coaching on Google Maps, Instagram and
  through friends, and almost always reach out on WhatsApp or by phone.
- **Admin users:** 1–5 non-technical staff (front desk, counsellors) who post results, batches and banners, and follow up leads.
- **Wider pattern:** about 27% of Indian school students take private coaching (higher in cities) and there are roughly
  68,000+ listed coaching centres, ~89% of them single-owner local setups. Many have the same need, so this build can become
  a reusable template later.

## Problem
- "Parents ask *show me your results* and we send 20 photos on WhatsApp." Results, the strongest reason to join, are scattered
  across Instagram posts and phone galleries.
- Batch timings, branch addresses and seat status change every few weeks; posters and Instagram stories go stale fast.
- Enquiries come by DM, call and walk-in with no single list, so follow-ups get missed during admission season
  (March–July, plus the scholarship-test months). Each missed parent is a lost yearly fee (often ₹20k–₹80k per student, unverified).
- A cheap website built by a freelancer usually needs that freelancer for every change, so it stops being updated.

## Why now
- Admission and board-result season drives a burst of search and Instagram traffic every year; a results-led site turns that
  into leads.
- Parents now expect WhatsApp-first contact; a 1-tap `wa.me` link with a pre-filled message works with no paid API.
- Browsers can crop and convert images to WebP on the phone/laptop itself (canvas + `toBlob("image/webp")`), so staff can
  upload raw phone photos and the site still loads fast on mobile data.
- Free tiers (Vercel, Neon Postgres, Vercel Blob) are enough for a local institute's traffic.

## Competitors and alternatives
| Name | What they do | Price | Gap we fill |
|---|---|---|---|
| Do nothing / Instagram + WhatsApp + Google Business Profile | Posts, DMs, map listing | free | No results showcase with filters, no lead list, no batch schedule, stale info |
| Classplus (branded app + website) | White-label app/website for selling online courses | ~₹29,999/year (listed) | Built for online course selling, not local walk-in leads, results wall, or branch locator; yearly fee |
| Teachmint | Classroom/ERP and smart-board ecosystem | custom quote | Not a marketing website |
| Wix / WordPress + theme | DIY site builder | ~₹0–₹1,000/month + time | Staff must design themselves; no enforced uniform photo crops; lead inbox and WhatsApp follow-up need plugins |
| Local web agency / freelancer | Custom static site | ~₹15k–₹60k one-off (typical, unverified) | Usually no real CMS; every change needs the developer |

## Money
- **Who pays:** Shikshanama, as a client project. Rough market rate for a custom site with CMS: ₹25k–₹60k one-off, plus
  ₹1k–₹3k/month care and hosting (unverified ranges). The actual fee, or whether this is a favour/portfolio piece, is unknown.
- **Why they'd pay:** one extra enrolled student per season likely covers the whole cost.
- **Upside:** once built, the same codebase can be re-skinned for other local coaching centres (template play), only if
  Abhishek wants that later.

## Risks (and cheapest test)
| Risk | Type | How to test cheaply |
|---|---|---|
| Student photos/names of minors published without consent (India DPDP Act 2023 needs parental consent for children's data) | Legal/privacy | Add a "consent received" tick to every result; ask the institute how they collect consent today |
| Vercel Hobby (free) plan is for non-commercial use; a paid client site may need Pro (~\$20/month) | Cost/legal | Abhishek confirms which Vercel plan the live site will sit on before release |
| Staff don't actually update the CMS, site goes stale | Adoption | 20-minute hand-over with a staff member doing one real result + one batch on the preview |
| Lead form spam | Build | Honeypot field + simple rate limit; review inbox after first week |
| Scope is large (public site + 8 admin managers + cropper) | Build | Build in one PR but ordered: public read pages → lead form → admin; cut nice-to-haves first |

## Smallest useful version
*(Updated in SPEC v2: React + Vite front end with motion, FastAPI JSON API, consent flow, sample demo content.)*
A FastAPI app with server-rendered, mobile-first pages (Tailwind-style CSS, a little vanilla JS) on Vercel, Neon Postgres for
content and leads, Vercel Blob for images. Public: ticker, hero with counters and CTAs, filterable Hall of Fame, courses with
upcoming batches, founders, branch locator, testimonials/gallery/Instagram callout, floating WhatsApp/Call, demo form. Admin at
`/admin`: login, managers for results, founders, hero/ticker, courses/batches, branches/contacts, testimonials/gallery, and a
leads inbox with status, CSV export and WhatsApp button. Every image upload goes through a locked-ratio cropper (1:1, 4:5, 16:9)
that saves WebP. Pre-filled with Shikshanama's brand, Instagram handle and flagship address. Realistically 7–10 working days,
not one week.

## Open questions for Abhishek (answered 2026-11-02)
1. ~~Paid job or favour?~~ **Free demo** to show Shikshanama what AkkiVerse can do; paid launch only if they like it.
2. ~~Domain and Vercel plan?~~ **Non-commercial demo on the current Vercel (Hobby) plan**; domain and paid plan come with a paid launch.
3. ~~English only or bilingual?~~ **A mix of English and Hindi that looks good** (Hinglish headings, Hindi accent lines, matched fonts).

Also from Abhishek: use **React + Vite** for a more attractive, dynamic UI with hover effects; for consent, offer a
**downloadable consent form** and/or a **WhatsApp message to the parent from Shikshanama's number**. See SPEC v2.

## Sources
- India coaching market and student share: IMARC Group coaching market report; vacademy.io summary of NSS data (27% of students take coaching).
- Number of coaching centres (~68,180 listed, ~89% independent): rentechdigital.com coaching centre dataset.
- Classplus pricing (~₹29,999/year): classplusapp.com pricing page.
- Teachmint positioning (custom quote, smart classrooms): teachmint.com.
- WhatsApp click-to-chat links: https://faq.whatsapp.com/5913398998672934
- India Digital Personal Data Protection Act 2023 (parental consent for children): https://www.meity.gov.in/data-protection-framework

## Founder's words
> Project Brief: Shikshanama (शिक्षाNama) Official Website & Admin CMS Build a modern, aesthetic, mobile-first website and full-featured Admin Panel (CMS) for Shikshanama (शिक्षाNama), a multi-branch coaching institute based in West Patel Nagar, New Delhi. The platform must combine a clean, Gen-Z-friendly EdTech aesthetic (bento-grid layouts, high-contrast typography supporting English and Devanagari script "शिक्षाNama", smooth animations) with high-conversion local lead generation for students and parents. 1. Core Institute Details (Pre-Populate as Defaults) Brand Name: Shikshanama (शिक्षाNama) Instagram Handle: @shikshanamaofficial (link to [https://instagram.com/shikshanamaofficial](https://instagram.com/shikshanamaofficial)) Main Flagship Branch Address: Ground Floor, E-42, Street Number 2, near Government School, Block E, West Patel Nagar, Patel Nagar, New Delhi, Delhi, 110008 (with support for adding multiple nearby branches). 2. Public Website Modules (All Dynamically Controlled via Admin Panel) Top Announcement Ticker & Sticky Navbar: A toggleable top marquee banner for urgent updates (e.g., Admissions Open, Scholarship Test dates, Board Crash Courses) and a sticky navbar with quick jump links and a "Book Free Demo" CTA. Hero Section: Bold शिक्षाNama branding, dynamic trust counters (e.g., Total Toppers, Years of Excellence, Active Branches), and two primary CTAs: "Book a Free Demo Class" and "Chat on WhatsApp". Hall of Fame (Student Results Showcase): An interactive, filterable showcase where visitors can filter achievers by Class (e.g., 10th, 12th), Stream (Science, Commerce, Humanities, Foundation), and Academic Year. Each card displays a uniformly cropped student photo, Student Name, Class, Stream, Marks/Percentage badge, and Rank/Distinction (e.g., Subject Topper, 98.4%). Courses & Live Upcoming Batches: Categorized stream tabs (Foundation, Science, Commerce, Humanities) showing subjects offered, key highlights, and an "Upcoming Batches" schedule displaying Branch, Start Date, Timings, and Seat Status (Open / Filling Fast) with a 1-click WhatsApp enrollment button. Founders & Leadership Section/Page: A dedicated layout displaying each founder's uniformly cropped portrait, Name, Credentials/Subject Expertise, and their personal vision message to students and parents. Multi-Branch Locator: A clean grid showcasing the West Patel Nagar flagship center and nearby branches. Each branch card must include the full address, branch phone number, a direct "Get Directions" Google Maps link, and a branch-specific WhatsApp button. Campus Life, Testimonials & Instagram Hub: A section featuring student testimonials, classroom/event gallery photos, and a prominent callout to @shikshanamaofficial. Direct Connect & Lead Capture: Persistent floating WhatsApp (with a pre-filled inquiry template) and Direct Call buttons across all pages. A "Book a Free Demo / Counseling" lead form capturing Student Name, Mobile Number, Class, Stream, and Preferred Branch. 3. Admin Panel (CMS) & Built-in Image Cropper Requirements Provide a secure, authenticated Admin Dashboard (/admin) where non-technical staff can manage 100% of the website content without touching code: Mandatory Interactive Image Cropper & Optimizer: Every image upload flow in the Admin Panel MUST enforce an interactive client-side image cropper before saving: Student Result Photos: Locked to a 1:1 (square/circle) aspect ratio so all student faces align uniformly in the grid. Founder Portraits: Locked to a 4:5 vertical portrait aspect ratio for a cohesive leadership section. Gallery / Banner Images: Locked to a 16:9 aspect ratio. Automatically compress and convert all cropped images to .webp format upon upload for instant mobile page loads. Results Manager (CRUD): Add, edit, delete, reorder, or pin student results to the homepage (Photo, Name, Class, Stream, Marks/Percentage, Rank/Badge, Year). Founders Manager (CRUD): Add, edit, reorder, or delete founder profiles (Photo, Name, Designation/Subject, Vision Message). Homepage & Batch Controller: Edit hero statistics, toggle and update the top announcement banner, and manage Courses and "Upcoming Batch" cards (Class, Stream, Branch, Start Date, Status badge). Branch & Contact Manager: Add or edit multiple branch locations (Branch Name, Address, Google Maps URL, Phone Number, WhatsApp Number) and update global contact numbers and social links. Testimonials & Gallery Manager: Upload cropped classroom photos and add student/parent reviews. Student Leads Inbox: A table logging all "Book a Free Demo" form submissions with timestamps, status tags (New, Contacted, Enrolled), CSV export, and a 1-click button to open a WhatsApp chat with that lead.
