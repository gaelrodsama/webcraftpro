# Windows / Browser Troubleshooting

\#1 source of "looks dead": Windows ships `prefers-reduced-motion: reduce` ON by default.

## 1. `prefers-reduced-motion` on Windows

**What's happening:** Windows 10/11 "Show animations" setting is OFF in many corporate installs, power-saving modes, and manufacturer defaults. Browsers pass this as `prefers-reduced-motion: reduce`. The user didn't request less motion — the OS defaulted to it.

**Why it kills websites:** Gating every animation with reduce produces a flat site. Tilt, scroll-reveal, marquees, fades all die.

### Solution: distinguish intrusive vs functional motion

| Type | Examples | Behavior with reduce |
|---|---|---|
| **Intrusive** | Autoplay video, particles >50 dots, parallax >40px, infinite spinners, shake/bounce, typing loops | **Disable** or strongly reduce |
| **Smooth scroll** | Lenis, native smooth | **Shorten** duration (0.5-0.7s), don't disable |
| **Functional UI** | Hover tilt 7°, button lift, color transitions, fade-in scroll, mesh gradient, scramble, count-up | **Always run** |

### Code pattern
```css
@media (prefers-reduced-motion: reduce) {
  .hero-video{animation-play-state:paused}
  .particles{display:none}
  .live-dot,.bouncy-arrow{animation:none}
  /* DO NOT add: .card{transition:none} or *{animation:none!important} */
}
```
```js
const reduced=matchMedia("(prefers-reduced-motion:reduce)").matches;
// Lenis: shorter, not off
const lenis=new Lenis({duration:reduced?.7:1.15});
// Particles: skip
if(reduced)return;
// Tilt: gate by hover capability ONLY, never by reduced-motion
if(matchMedia("(hover:none)").matches)return;
```

**Verification:** DevTools → Rendering → Emulate `prefers-reduced-motion: reduce`. Reload. Hover, tilt, fade, marquee, count-up still work. Only particle/video/parallax>40px off.

## 2. Windows quirks

### 2.1 High-DPI scaling (125-200%)
```js
const dpr=Math.min(devicePixelRatio||1,2); // cap at 2 always
```
Three.js: `renderer.setPixelRatio(dpr)`. Particles: cap DPR for perf.

### 2.2 Edge Segoe UI font
```css
font-family:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
```

### 2.3 ClearType anti-aliasing
```css
body{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-rendering:optimizeLegibility}
```

### 2.4 Battery saver throttles rAF to 30fps
Design animations that work at 30fps. Test: DevTools → Performance → CPU 4× slowdown.

### 2.5 Edge blocks autoplay
```html
<video autoplay muted loop playsinline preload="metadata" poster="hero-poster.webp">
  <source src="hero.mp4" type="video/mp4">
</video>
```

### 2.6 Font weight 300 on Windows
Variable fonts at wght 300 can render thin/broken. Test at 350/400, pick lowest that renders cleanly.

### 2.7 GPU acceleration disabled (RDP, VMs, bad drivers)
```js
function hasWebGL(){try{const c=document.createElement("canvas");return!!(window.WebGLRenderingContext&&(c.getContext("webgl")||c.getContext("experimental-webgl")))}catch(e){return false}}
if(!hasWebGL())document.querySelector(".hero-3d").style.backgroundImage="url('assets/img/hero-fallback.webp')";
```
Lower `filter:blur()` values when possible.

## 3. macOS quirks
- **Safari 100vh:** use `min-height:100svh` (small viewport) + `100vh` fallback
- **backdrop-filter:** include `-webkit-backdrop-filter` for older Safari
- **Fixed position jump:** `transform:translateZ(0)` on fixed elements

## 4. Mobile / iOS quirks
- Touch action: `.carousel{touch-action:pan-x}`
- Text size: `html{-webkit-text-size-adjust:100%}`
- Hover on touch: always pair with `@media(hover:hover){.card:hover{...}}`
- iOS keyboard: add padding-bottom to form on focus
- Three.js mobile:
```js
const isMobile=window.innerWidth<900||/Mobi|Android/i.test(navigator.userAgent);
renderer.setPixelRatio(Math.min(devicePixelRatio||1,isMobile?1.5:2));
if(isMobile){renderer.shadowMap.enabled=false;renderer.antialias=false}
```

## 5. Feature detection (never UA-sniff)
```js
CSS.supports("backdrop-filter","blur(10px)") // ✅
typeof IntersectionObserver!=="undefined"
matchMedia("(hover:hover)").matches
"startViewTransition"in document
```

## 6. Common errors

| User says | Cause | Fix |
|---|---|---|
| "Nothing moves on Windows" | reduced-motion gating | See §1 |
| "Black square corner at startup" | Cursor before mousemove | Gotcha A.3 |
| "Images don't load" | Mixed format refs | Gotcha A.10, grep |
| "Menu won't appear" | Module imports on file:// | Gotcha A.1 |
| "Spinner stuck" | Splash JS failed | Gotcha A.9 (CSS safety) |
| "Animation choppy" | GPU off / battery save | Reduce particles, blur |
| "Cards don't tilt on Surface" | hover=none on touch | `(hover:hover)&&(pointer:fine)` |

## 7. 3-machine smoke test
1. **Windows reduced-motion:** hover+tilt+fade+marquee work; particle/video off
2. **Mobile/touch:** content readable, no overflow, nav works, forms submittable
3. **JS disabled:** all content visible, nav works, layout intact

## 8. Final checklist
- [ ] No `<script type="module">`, no import/export
- [ ] reduced-motion only gates intrusive (not tilt/hover/fade/scroll)
- [ ] DPR capped at 2, WebGL detected with fallback
- [ ] `backdrop-filter` has solid background fallback
- [ ] `100svh` for heroes, `(hover:hover)` for hover interactions
- [ ] Site works on `file://` and with JS disabled
- [ ] Cursor not at (0,0) at load