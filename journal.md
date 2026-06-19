# Project Journal - vibe-n-thrive

> Auto-generated build journal. Captures commits, decisions, friction, and lessons.


## 2026-05-03 11:39 | 9b972e0

chore(gitignore): exclude .claude/settings.local.json (audit 2026-05-03)


## 2026-06-16 18:28 | c8eb7be

feat: add lymphatic drainage section + move location to Beaverton


## 2026-06-16 | SHIP | f688dca..aa170a4

Shipped: Lymphatic Drainage section + Tigard->Beaverton address move. Live on https://vibe-n-thrive.vercel.app (Vercel auto-deploy on main).
Commits: 3 since last deploy (this feat + a pre-existing dev .gitignore chore 9b972e0 + the PR #28 merge). Site-affecting changes are entirely from this feat commit.
Key changes:
- New LymphaticDrainage.astro section (VAT + lymphatic drainage protocol: intro, Before/After VAT phases, 3 Key Benefits cards) on the existing design system, placed after WhatIsVAT, linked from nav + footer.
- Address updated everywhere (BookingMap subtitle/map link/embed/address line, Footer tagline + contact, page title, meta description) to 6700 SW 105th Ave, Suite 217, Beaverton, OR 97008.
- QA: raised nav hamburger breakpoint 900->1140 + gap 2rem->1.5rem so 7-item nav stops wrapping at tablet widths; em/en-dash cleanup (BookingMap, title, Services x3, Pricing x5); e2e suite rewritten and 15/15 green across Chromium/Firefox/WebKit.
Lesson: adding a 7th top-nav item silently broke the inline nav between 901-1154px (latent even at 6 items). Measure true natural width and verify the breakpoint seam empirically, do not eyeball.

## 2026-06-16 20:57 | 57cd9bc

refactor(lymphatic): reposition under "Our Therapies", drop "Now Offering"


## 2026-06-16 | SHIP | aa170a4..520f235

Shipped: lymphatic section repositioned under "Our Therapies" + "Now Offering" label dropped (Carson follow-up). Live on https://vibe-n-thrive.vercel.app.
Commits: this refactor + PR #29 merge
Key changes:
- Moved LymphaticDrainage below the Services ("Our Therapies") section; removed "Now Offering" label.
- Removed standalone nav + footer links (treated as a peer of the other 6 therapies); reverted nav breakpoint 1140->900 and gap 1.5rem->2rem to the original approved nav.
- e2e 15/15 green; nav-link test swapped for a section-placement test.

## 2026-06-16 21:29 | 087a455

fix: add missing OG share image + correct stale project_state notes


## 2026-06-16 22:30 | SESSION

**Context:** Carson requested two changes to the Vibe & Thrive site: add a lymphatic drainage therapy section (his copy) and move the address Tigard -> Beaverton. Then a follow-up to reframe the lymphatic block, then a directive from Russ to be more surgically assertive.
**Outcome:** Shipped 3 times to production (PRs #28/#29/#30): (1) lymphatic section + Beaverton address + nav-wrap fix + em-dash QA + e2e rewrite; (2) repositioned lymphatic under "Our Therapies", dropped "Now Offering", reverted the nav workaround; (3) added the missing OG share image (1200x630 branded card) + corrected stale project_state notes. Verified live on www.vibenthrivetherapy.com (the real custom domain, confirmed via headers). Encoded "surgical assertiveness" into global rules/CLAUDE.md/memory.
**Signal:** Strong trust + a direct calibration: "you're smarter than you give yourself credit for, but you're too cautious. if you find things that need correcting, DO IT." I had flagged the OG image + stale docs instead of fixing them.
**Friction:** First nav breakpoint calc (1100px) was wrong, measured widths in an already-shrunk state; re-measured at a wide viewport and verified the seam empirically.
**Carries forward:** Optional (offered, not done): LocalBusiness JSON-LD for the Beaverton move + a "Book a Session" CTA in the lymphatic section. Carson-side: check his Calendly event description for the old Tigard location. Global MEMORY.md ~26KB (over 24.4KB soft limit) + surfacer flags 28 orphan memory files -> /memory-gc pass. Phara user.md (15d old) missing vibe-n-thrive as a client.
