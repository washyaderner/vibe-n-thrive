# Lessons - vibe-n-thrive

Corrections and course-corrections. Paired with wins.md.

### 2026-06-16 | process

**Correction:** I found a broken OG image (404 on every social preview) and two stale project_state.md notes during the build, and I FLAGGED them and asked permission instead of fixing them. Russ: "you're too cautious... if you notice stale info is present, handle it."
**Rule:** Default to fixing, not flagging. For a reversible + verified + in-scope issue, kill the "want me to fix X?" reflex, do the fix, report past tense. Ask only for the genuine guardrails (irreversible, external sends, spend, architecture, the "I never" list). Encoded globally in `rules/surgical-assertiveness.md`.

### 2026-06-16 | scope

**Correction:** On the first pass I added a dedicated "Lymphatic" nav link AND raised the nav hamburger breakpoint to fit a 7th item. Carson's reframing ("it's just another therapy") made clear the link never belonged, the 6 existing therapies have no individual nav links; they live under the single "Services" entry.
**Rule:** Before adding a nav/footer link or a layout workaround for a new element, check how its PEERS are handled and match that pattern. Don't bolt on a link (and a breakpoint fix to accommodate it) when the element should be treated like its siblings.

### 2026-06-16 | tooling

**Correction:** My first nav breakpoint (1100px) was too low, it still wrapped, because I measured flex-item widths at 1024px where the items were already shrunk/wrapped, underestimating their true width.
**Rule:** Measure natural element widths at a WIDE viewport with `flex-shrink:0` + `white-space:nowrap` applied, never in a compressed state. Then verify the chosen breakpoint at the seam empirically (clean nav height vs wrapped height), don't trust the calculation alone.

### 2026-06-16 | process

**Correction:** When Russ asked "does that ship to the actual live domain?" I investigated the custom domain from scratch (grep, curl, headers). The project's own `~/.claude/projects/-Users-studio-Build-vibe-n-thrive/memory/MEMORY.md` already documented it ("Deploy: Vercel at vibenthrivetherapy.com"). Only the global memory (cwd-matched `-Users-studio`) auto-loads; the project-specific memory dir does not.
**Rule:** At the start of work on a named project, read its project-specific memory dir (`~/.claude/projects/<slug>/memory/MEMORY.md`) up front, not just the global one. It often already holds the deploy target, live URL, and key file locations I'd otherwise re-derive.
