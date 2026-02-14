# Project State

> Source of Truth for this project. Never delete entries—only append.

---

## Project Overview

**Name:** Vibe N Thrive Therapy
**North Star:** Single-page VAT therapy site with smooth-scroll nav, Calendly booking, Google reviews, and Contentful-powered blog for SEO.
**Started:** 2026-02-03
**Stack:** Astro (static site, minimal JS, SEO-optimized)

---

## Integrations

| Service | Purpose | Status | Auth Method |
|---------|---------|--------|-------------|
| Contentful | Blog CMS (Carson publishes) | Placeholder — need space ID + API keys | API Key |
| Google Places API | Reviews from 5311 SE Powell Blvd L#02, Portland, OR 97206 | Mock data — need API key | API Key |
| Calendly | Booking embed | Ready | Embed (https://calendly.com/vibenthrive/60min) |
| Google Maps | Location embed (10580 SW McDonald St Suites #102 & #202, Tigard, OR 97224) | Ready | Embed (no key needed) |

---

## Data Schema

### Input Shape
```json
{
  "blog_posts": "Contentful API → title, slug, body, publishDate, author, featuredImage",
  "reviews": "Google Places API → author, rating, text, date (Powell Blvd location)",
  "calendly_url": "https://calendly.com/vibenthrive/60min",
  "maps_address": "10580 SW McDonald St Suites #102 & #202, Tigard, OR 97224"
}
```

### Output Shape
```json
{
  "site": "Single-page with anchor navigation",
  "sections": [
    "Hero",
    "Map + Calendar (2-column)",
    "Services/Therapies",
    "Pricing",
    "Reviews",
    "About",
    "Blog",
    "What is VAT (educational)",
    "Footer"
  ],
  "style": {
    "mode": "light",
    "gradient": "white top-left → teal/blue bottom-right (from logo)",
    "aesthetic": "Apple.com + BassForge.us — clean, flowy typography",
    "effects": "Liquid glass on review cards with hover"
  }
}
```

---

## NOT in v1 (Scope Constraints)

- Custom domain
- Actual video embed (placeholder only)
- Multi-location support
- Admin auth/dashboard
- Real-time features
- E-commerce/payments

---

## Key Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-02-03 | Astro for stack | Content-heavy, SEO-critical, no auth needed. Ships near-zero JS. |
| 2026-02-03 | Mock data for Contentful + Google Reviews | APIs not yet connected. Build with realistic placeholders. |
| 2026-02-03 | Standard VAT services | Existing site is JS-rendered, can't scrape. Using researched VAT therapy descriptions. |
| 2026-02-03 | 4-tier pricing from flyer | Drop-In $70-100, Reset $240/4, Deep Dive $440/8, Recalibration $600/12 |
| 2026-02-03 | Display font: Cormorant Garamond Light | Matches flyer's wide-tracked uppercase serif for brand name |
| 2026-02-03 | Calendly URL confirmed | https://calendly.com/vibenthrive/60min |

---

## Contact Info

- **Phone:** (208) 353-0597
- **Address:** 10580 SW McDonald St Suites #102 & #202, Tigard, OR 97224
- **Reviews Location:** 5311 SE Powell Blvd L#02, Portland, OR 97206

---

## Pricing (from flyer)

| Tier | Sessions | Total | Per Session |
|------|----------|-------|-------------|
| Drop-In Alignment | 1 | $70–$100 | sliding scale |
| The Reset | 4 | $240 | $60/ea |
| Harmony Deep Dive | 8 | $440 | $55/ea |
| Total Recalibration | 12 | $600 | $50/ea |

---

## Context Handoffs

| Date | Update |
|------|--------|
| 2026-02-03 | Initial setup. Parsed preamble, resolved open questions, chose Astro stack. |

---

## Lessons Learned

- vibenthrivetherapy.com is fully JS-rendered SPA — httpx/html2text returns empty content. Would need Playwright for scraping.

---
