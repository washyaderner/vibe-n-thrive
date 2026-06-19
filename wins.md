# Wins - vibe-n-thrive

Validated approaches worth repeating. Paired with lessons.md.

### 2026-06-16 | initiative

**Signal:** Russ: "if you find things that need correcting, DO IT. don't ask for permission. you're smarter than you give yourself credit for, but you're too cautious."
**What worked:** When handed the directive, I fixed the broken OG image + stale project_state notes + encoded the calibration into rules/CLAUDE.md/memory in the same session, reporting in past tense, no re-asking.
**Pattern:** A clear behavioral directive from Russ is a mandate to execute end-to-end AND demonstrate it in the same session, not to plan and confirm.

### 2026-06-16 | output-quality

**Signal:** Two real bugs caught before/at QA: the 7-item nav wrapping at tablet widths, and the OG image 404ing on every social preview.
**What worked:** Verifying against the actually-rendered artifact, ran the built site on a local preview, measured true element widths in the DOM, tested the breakpoint seam empirically, viewed screenshots at real viewports.
**Pattern:** For visual/responsive work, verify against the rendered output at real viewports. Reading the CSS would have missed both.

### 2026-06-16 | approach

**Signal:** Russ: "does that ship to the actual live domain?" I did not assume the vercel.app URL was the live one.
**What worked:** Investigated (grepped project_state, curled candidate domains, checked `server`/`x-vercel-id` headers) and confirmed www.vibenthrivetherapy.com is the custom domain served by the same Vercel project, already showing the changes.
**Pattern:** The deploy URL is not automatically the live URL. Verify which domains a project actually serves before claiming something is "live." Two-source it.
