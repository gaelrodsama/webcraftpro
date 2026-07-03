# Stack & Conventions — reglas técnicas no negociables

## 1. Stack
| Layer | Tech | Why |
|---|---|---|
| Markup | HTML5 semantic | Works without JS |
| Style | CSS3 (custom props, clamp, grid, @property) | No preprocessor |
| Behavior | Vanilla JS, classic scripts (NOT modules) | file://, FTP, any env |
| Animation | GSAP 3.13+ + ScrollTrigger | Industry standard |
| Smooth scroll | Lenis 1.1+ (opt-in only) | Replaces Locomotive |
| 3D | Three.js r128 (CDN UMD) | Stable, no modules |
| Fonts | Google Fonts via `<link>` | No self-hosting |
| Images | WebP via `assets/img/` | Universal support |

**Forbidden:** npm, node_modules, build step, Vite/Webpack/Rollup/esbuild/Astro/Next, `<script type="module">` with relative imports, React/Vue/Svelte/Solid/Qwik, TypeScript in deliverable, CSS-in-JS, Tailwind, PostCSS.

**Allowed in lib/:** gsap.min.js (~72 KB) + ScrollTrigger.min.js (~43 KB) = always. Lenis (~13 KB) / Three.js (~600 KB) = only when archetype demands.

## 2. Folder structure
```
project-name/
├── index.html / <other-page>.html / styles.css / main.js
├── lib/ {gsap.min,ScrollTrigger.min,lenis.min,three.min,manifest.js}
├── tools/ (dev-only scripts, NOT shipped)
└── assets/ {img/ (WebP), photos/source/ (originals), credits.json, favicon}
```

## 3. Script load order (end of `<body>` or `<head>` with `defer`)
```html
<script defer src="lib/gsap.min.js"></script>
<script defer src="lib/ScrollTrigger.min.js"></script>
<!-- Lenis/Three only if archetype demands -->
<script defer src="lib/manifest.js"></script>
<script defer src="main.js?v=YYYYMMDD"></script>
```
`?v=YYYYMMDD` mandatory on every deploy. `defer` guarantees parse-order execution, works on file://.

## 4. IIFE pattern
**lib/manifest.js** — brand data only, one global:
```js
(function(){"use strict";window.__BRAND__={name:"Brand",tagline:"..."};})();
```
**main.js** — entry point:
```js
(function(){"use strict";const data=window.__BRAND__||{};
const $=(s,o)=>(o||document).querySelector(s);
const $$=(s,o)=>Array.from((o||document).querySelectorAll(s));
const escHTML=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
function safe(fn,name){try{fn()}catch(e){console.warn("["+name+"]",e)}}
function boot(){
  safe(mountProducts,"mountProducts");
  safe(initSplash,"initSplash"); safe(initNav,"initNav");
  if(window.gsap&&window.ScrollTrigger){try{gsap.registerPlugin(ScrollTrigger)}catch(_){}}
  document.documentElement.classList.add("is-ready");
}
document.readyState==="loading"?document.addEventListener("DOMContentLoaded",boot):boot();
})();
```

## 5. Naming conventions
- HTML/CSS: kebab-case. JS: camelCase. JS constants: UPPER_SNAKE. Images: kebab-case.webp. Data attrs: `data-purpose`.

## 6. CSS organization (single file, sectioned)
1. Tokens (:root) → 2. Reset & base → 3. Utilities → 4. Typography → 5. Components → 6. Sections → 7. Effects → 8. Responsive → 9. Reduced-motion

## 7. Google Fonts
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=…&display=swap">
```
Max 3 families: display serif + body sans + mono/accent (optional).

## 8. Hero priority loading
```html
<link rel="preload" as="image" href="assets/img/hero.webp" fetchpriority="high">
<img src="assets/img/hero.webp" fetchpriority="high" loading="eager">
<!-- Others: loading="lazy" decoding="async" -->
```

## 9. Reset minimum
```css
*,*::before,*::after{box-sizing:border-box;margin:0}
html{-webkit-text-size-adjust:100%;tab-size:2}
body{font-family:var(--sans);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;overflow-x:clip;overscroll-behavior-y:none}
img,svg,video{display:block;max-width:100%}
img{height:auto}
button{font:inherit;color:inherit;cursor:pointer;border:0;background:none}
a{color:inherit;text-decoration:none}
p{text-wrap:pretty}
h1,h2,h3,h4{text-wrap:balance;line-height:1.05;letter-spacing:-0.02em}
::selection{background:var(--accent);color:var(--cream)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:4px}
.skip-link{position:fixed;top:-100px;left:1rem;padding:.6rem 1rem;background:var(--cream);color:var(--bg);z-index:9999;border-radius:8px;font-weight:500}
.skip-link:focus{top:1rem}
```

## 10. Breakpoints (mobile-first)
```css
/* Default: mobile */
@media (min-width:540px){} /* large phone / small tablet */
@media (min-width:720px){} /* tablet portrait */
@media (min-width:960px){} /* tablet landscape / small laptop */
@media (min-width:1280px){} /* laptop / desktop */
@media (min-width:1600px){} /* large desktop */
```
No custom breakpoints. 5 fixed steps.

## 11. Easings
```css
:root{--ease-out:cubic-bezier(0.16,1,0.3,1);--ease-in:cubic-bezier(0.7,0,0.84,0);--ease-soft:cubic-bezier(0.25,0.46,0.45,0.94);--ease-bounce:cubic-bezier(0.34,1.56,0.64,1)}
```
GSAP: `"expo.out"` / `"power3.out"` = match --ease-out.

## 12. HTML must work without JS
Test: disable JS → all content visible, navigable, acceptable layout. Allowed to lose: animations, smooth scroll, 3D, cursor, form submit simulation. NOT allowed to lose: text, images, navigation, structure.

## 13. Page transitions (View Transitions API)
```css
@view-transition{navigation:auto}
::view-transition-old(root),::view-transition-new(root){animation-duration:0.6s;animation-timing-function:cubic-bezier(0.16,1,0.3,1)}
::view-transition-old(root){animation-name:fadeOutUp}
::view-transition-new(root){animation-name:fadeInUp}
```

## 14. Final check
- No `<script type="module">`, no import/export, all scripts defer in order
- manifest.js exposes only `window.__BRAND__`, main.js is IIFE
- Every init* wrapped in safe(), no .jpg/.png refs, skip-link present
- Alt-text on every image, focus-visible styled