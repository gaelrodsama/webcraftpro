---
name: webcraftpro-premium-generator
description: Generate premium static websites (HTML/CSS/vanilla JS) with GSAP, 3D effects, scroll storytelling. Zero build step. Triggered by user asking for "wow" / "premium" / "increíble" websites.
---

# Premium Static Website Generator — Skill

Generate **drag-and-drop websites** for Hostinger/any static host. Award-winning visual quality (Active Theory, Locomotive, Resn). Zero build step, zero npm, zero frameworks. Pure HTML + CSS + vanilla JS + local libraries (GSAP, Lenis, Three.js when needed).

## When to use

User asks for: new website with visual ambition ("premium", "wow", "increíble"). Non-technical user (no npm, no server config). Spanish or English.

**Do NOT use for:** editing existing complex codebases, web apps with backend/database, documentation-only.

---

## ⚠️ Read-first references (in order)

1. `references/09-environment-detection.md` — detect Python/curl availability
2. `references/04-critical-gotchas.md` — silent-breaking errors (esp. A.13/A.14 cache, B.1.4 Lenis)
3. `references/10-deployment-and-cache.md` — 3-layer cache strategy
4. `references/07-windows-troubleshooting.md` — reduced-motion ON by default on Windows
5. `references/02-archetypes.md` — pick ONE archetype, never combine
6. `references/06-diversity-guardrails.md` — anti-copy rules + rotation

Then:
7. `references/01-stack-and-conventions.md` — file structure, IIFE, script load order
8. `references/03-effects-catalog.md` — effect snippets
9. `references/05-image-and-asset-pipeline.md` — Openverse, WebP, photos
10. `references/08-pre-deploy-checklist.md` — run before declaring done

---

## Conversation flow

User is non-technical. Default: decide silently. Max 4-6 short questions.

### Step 1 — User dump
Let them describe. Capture: business type, brand name, tone, photos, special features. Don't ask follow-ups yet.

### Step 2 — Minimum follow-ups (ONE message, ≤15 words each)
1. Brand name (if not given)
2. Photos: their own in `assets/photos/source/` or Openverse stock? Default = Openverse
3. CTA goal (book/subscribe/contact/buy)
4. Anything MUST include? (optional)
5. Pages: one-page default? Ask only if multi-page implied

**Don't ask about:** color palette, fonts, layout, effects, tech decisions — choose from archetype.

### Step 3 — Silent archetype selection

| Industry | Archetype default |
|---|---|
| Restaurant/hotel/hospitality | Editorial Dark Warm / Light Editorial Cream |
| Travel agency/experiences | Light Editorial Cream / Magazine |
| Newsletter/publication | Cinematic 3D Storytelling / Brutalist Grid |
| Tech/SaaS/startup | Mouse-Reactive Gradient / Glassmorphism |
| Portfolio/studio/creative | 3D Cinematic / Brutalist / Liquid Wave |
| Boutique/luxury | Glassmorphism / Editorial Dark Warm |
| Café/artisan/lifestyle | Light Editorial Cream / Magazine |
| Cultural/gallery/event | Brutalist Grid / Newspaper |

### Step 4 — Silent setup (detect Python first)
```bash
PY=""
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
fi
mkdir -p {project-name}/{assets/img,assets/photos/source,lib,tools}
```
Libraries: prefer Python `download_libs.py`, fallback Bash. Images: Openverse via Python, then WebP conversion. Check actual extensions (`.webp` or `.jpg`/`.png`) before generating HTML.

### Step 5 — Generate code
Follow archetype recipe + gotchas + conventions + deployment strategy.

**Mandatory generation rules:**
- IIFE pattern, not ES modules. No `import`/`export`. Classic `<script defer>` + `window.__BRAND__`
- `?v=YYYYMMDD` cache-buster on every `<link>` and `<script>`
- Native scroll default (`scroll-behavior: smooth`). Lenis opt-in only
- Defensive CSS `.reveal[data-split] { opacity: 1; transform: none; }`
- Copy `templates/htaccess.template` to project root

### Step 6 — Verify
```bash
python "<skill-dir>/scripts/verify_project.py" --project {project-name}
```
Fix reported issues silently, re-run.

### Step 7 — Preview + Hand off
```bash
cd {project-name} && python3 -m http.server 8765
```
Navigate Preview to `http://localhost:8765/`. Tell user: folder path, preview URL, deploy instructions (drag folder to Hostinger). Offer adjustments — don't push.

---

## Hard rules (from 04-critical-gotchas.md — key ones up top)

1. No `<script type="module">` with relative imports — breaks `file://`, breaks cache busting. Use `<script defer>` + IIFE.
2. `.htaccess` in every project root — without it Hostinger serves stale JS/CSS for 30 days.
3. `?v=YYYYMMDD` cache-buster on every `<link>` and `<script>`.
4. Native scroll by default. Lenis opt-in only — fragile across Windows.
5. Defensive CSS for `.reveal[data-split]` — JS-only fix fails if JS cached stale.
6. No npm runtime deps — only `lib/` files. Python only dev-time.
7. Don't gate micro-interactions with `prefers-reduced-motion` — Windows ships it ON.
8. All images WebP. Never mix `.jpg`/`.png`/`.webp`.
9. Hardcode content in HTML. JS only enriches. If JS fails, site still reads.
10. Each `init*` wrapped in `safe(fn, name)` — one failure doesn't break rest.
11. IntersectionObserver threshold ≤ 0.05 + 6s safety timeout.
12. Splash with double safety (CSS animation 4.5s + JS hide).
13. Idempotent mounts — check `if (target.children.length > 0) return;`.

---

## Quality bar

- **First-screen wow**: first viewport must be visually arresting
- **Effects feel intentional**: every animation has a reason, no duplicates
- **Mobile intentional composition**: not squashed desktop
- **Copy editorial**: no buzzwords ("unlock", "transform", "revolutionary")
- **Robustness > spectacularity** when in doubt

## Diversity mandate

Reference projects (Nómada, 911 Restaurante, The Gambit) are EXAMPLES, not templates. If writing code mirrors one too closely → stop, pick different archetype. Read `06-diversity-guardrails.md`.

---

## Skill files index

```
SKILL.md                                ← entry point
intake-template.md                      ← intake questions
references/01 through 10/               ← full reference library
templates/htaccess.template             ← copy to project root
scripts/{openverse_fetch,webp_convert,download_libs,verify_project}.py
```

## Zero-prompt mode

User can copy `recommended-settings.json` patterns into `.claude/settings.json` once. After that, skill runs silently. Patterns scoped to only skill's own scripts + safe helpers (`mkdir`, `ls`, `cp`, `grep`). Nothing destructive pre-authorized.

---

## Final: treat user as non-technical client. Goal: working beautiful website, minimum friction.
- Decide for them. Run silently. Default to robust. Show, don't lecture.