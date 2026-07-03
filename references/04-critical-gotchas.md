# ⚠️ Critical Gotchas — leer antes de escribir código

Gotchas = bugs reales de proyectos anteriores. Internalizar y aplicar preventivamente.

## TIER A — Rompe el sitio silenciosamente

### A.1 ❌ `<script type="module">` con imports relativos
`file://` bloquea ES modules. Usar siempre `<script defer>` + IIFE. Nunca import/export.
```html
<!-- ✅ CORRECT --> <script defer src="lib/gsap.min.js"></script>
<!-- ❌ FORBIDDEN --> <script type="module" src="main.js"></script>
```

### A.2 ❌ `prefers-reduced-motion` matando micro-interacciones
Windows lo envía ON por defecto. Taxonomía:
- **Intrusivo:** autoplay video, particles, parallax >40px, loops infinitos, shake/bounce → **deshabilitar**
- **Funcional/micro:** hover tilt 7°, color transitions, scroll fades, mesh gradient, scramble, count-up, marquee → **siempre ejecutar**
```css
@media(prefers-reduced-motion:reduce){.particles{display:none}/* NO: .card{transition:none} */}
```
```js
if(reduced)return; // solo para intrusivos
// tilt, magnetic, scramble: gate por (hover:none), NUNCA por reduced-motion
```

### A.3 ❌ Custom cursor en (0,0) antes del primer mousemove
```css
.cursor{opacity:0;transition:opacity.25s}
.cursor.is-ready{opacity:1}
```
```js
let firstMove=false;
window.addEventListener("mousemove",e=>{
  if(!firstMove){firstMove=true;cursor.classList.add("is-ready");}
});
```

### A.4 ❌ splitWords/splitChars aplana `<br>` y `<em>`
Iterar childNodes, preservar BR y elementos inline. No usar `el.textContent`.

### A.4.5 ❌ `.reveal` + `data-split` juntos → elemento invisible
```css
.reveal[data-split]{opacity:1;transform:none} /* defensivo, siempre */
```

### A.5 ❌ mouseenter/mouseleave no dispatcheables
Usar `mouseover/mouseout` + `relatedTarget` check.

### A.6 ❌ Race condition con async-rendered cards
```js
function bindBilingual(root=document){
  root.querySelectorAll("[data-bilingual]").forEach(el=>{
    if(el.dataset.bilingualBound)return;
    el.dataset.bilingualBound="1";
    // attach listeners
  });
}
```

### A.7 ❌ `gsap.from` dentro de pinned ScrollTrigger
No animar child cards dentro de pinned sections. El scroll horizontal ES la animación.

### A.8 ❌ IntersectionObserver threshold muy alto
```js
const io=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add("is-revealed");io.unobserve(e.target)}});
},{threshold:.01,rootMargin:"0px 0px -2% 0px"});
// Safety: a 6s force-reveal lo que sigue oculto
setTimeout(()=>{document.querySelectorAll("[data-reveal]:not(.is-revealed)").forEach(el=>{if(el.getBoundingClientRect().top<window.innerHeight)el.classList.add("is-revealed")})},6000);
```

### A.9 ❌ Splash stuck si JS falla
```css
.splash{animation:splashSafety.01s 4.5s forwards}
@keyframes splashSafety{to{opacity:0;pointer-events:none;clip-path:inset(0 0 100% 0)}}
```
```js
function initSplash(){const s=document.querySelector("[data-splash]");if(!s)return;const h=()=>s.classList.add("is-out");if(document.readyState==="complete")setTimeout(h,600);else window.addEventListener("load",()=>setTimeout(h,400));setTimeout(h,4000)}
```

### A.10 ❌ Mix .jpg/.png/.webp → 404s
```bash
grep -rn '\.jpg\|\.png' --include="*.html" --include="*.css" --include="*.js" # debe retornar vacío
```

### A.13 ❌ Hostinger/CDN sirve JS/CSS stale por horas
**Fix 1 — .htaccess:** copiar `templates/htaccess.template` al project root.
**Fix 2 — cache-buster:** `?v=YYYYMMDD` en cada `<link>` y `<script>`. Bumpear en cada deploy.
**Fix 3 — IIFE over modules:** cache-buster no propaga a imports internos de ES modules.

### A.14 ❌ ES modules con imports relativos rompen cache-bust + file://
Usar IIFE pattern. `import` no hereda `?v=` del script padre. Ver A.1 + 01-stack-and-conventions.md §4.

## TIER B — UX con bugs

### B.1 ❌ Carousel overflow-x:auto hereda Y clip
```css
.carousel-track{overflow-x:auto;overflow-y:visible;padding-block:2rem 2.5rem}
```

### B.1.4 ❌ Lenis frágil en Windows — preferir native scroll
Lenis tiene problemas con drivers trackpad Windows, high-DPI, Edge throttle, battery saver.
**Default:** `scroll-behavior:smooth` + anchor handling nativo. Lenis solo si (a) marca premium extrema + (b) pruebas multi-OS. Config: `lerp:.12 wheelMultiplier:1.2`.
Si usas Lenis: `body{overflow-x:clip}` (no hidden), `lerp:.1`, no `duration` en constructor.

### B.2 ❌ Sticky falla por ancestor con overflow:hidden
```css
body{overflow-x:clip} /* ✅ clip preserva sticky. hidden NO */
```

### B.3 ❌ Sticky figure deja hueco si más corto que contenido
Convertir a single-column editorial o quitar sticky.

### B.4 ❌ Hero title clamp agresivo corta letras
```css
.hero-title{font-size:clamp(2.4rem,7vw,6.4rem);line-height:.98;text-wrap:balance;max-width:18ch;margin-inline:auto}
```

### B.5 ❌ Strip de cards wrappean a 2 líneas
```css
.strip-row{display:flex;flex-wrap:nowrap;gap:.6rem}
.strip-card{flex:1 1 0;min-width:0;max-width:130px}
@media(max-width:1023px){.strip-card:nth-child(n+10){display:none}}
@media(max-width:767px){.strip-card:nth-child(n+8){display:none}}
@media(max-width:539px){.strip-card:nth-child(n+6){display:none}}
```

### B.6 ❌ Halo con overflow:hidden corta abruptamente
```css
.section-halo{position:absolute;inset:-80%-10%-50%-10%;background:radial-gradient(45%35%at 50%50%,rgba(196,154,91,.5),transparent 75%);filter:blur(120px);pointer-events:none}
```

### B.7 ❌ Scramble flickers en hover rápido
```js
let animating=false;
el.addEventListener("mouseenter",()=>{if(animating)return;animating=true;/* scramble RAF, completion: animating=false*/});
// NO mouseleave handler
```

### B.8 ❌ Hardcoded BG color rompe theme switcher
```css
:root{--bg:#0e0b09;--text:#f2ebda}
[data-theme="light"]{--bg:#faf7f0;--text:#1a1714}
section{background:var(--bg);color:var(--text)}
```

### B.9-B.12 — Three.js: evitar UV flip (B.9), setPixelRatio antes de setSize (B.10), single rAF loop (B.11), backdrop-filter con solid fallback (B.12)

## TIER C — Raros pero reales

### C.1 ❌ 100vh jump iOS Safari → usar `100svh`
### C.2 ❌ Form submit con magnetic effect → deshabilitar magnetic durante is-sending
### C.3 ❌ position:fixed dentro de parent con transform → fixed se vuelve relativo al parent
### C.4 ❌ Three.js outputEncoding no seteado → colores washed. `renderer.outputEncoding=THREE.sRGBEncoding`
### C.5 ❌ Three.js cargado después del setup script
### C.6 ❌ Conic-gradient border con seam visible → gradient termina con mismo color que empieza
### C.7 ❌ Sticky section labels under nav → `top:80px`
### C.8 ❌ text-wrap:balance salta en JS-modified → usar `text-wrap:pretty` si split text
### C.9 ❌ Form validation no trigger en `requestSubmit` → llamar `reportValidity()` primero
### C.10 ❌ `<dialog>` no abre/cierra → usar `showModal()` no `.show()`
### C.11 ❌ .heic photos iPhone → script intenta pillow-heif, si falla log warning
### C.11.5 ❌ Cursor trail (thumbnails following mouse) → suele leerse como bug. NO incluir por defecto.
### C.12 ❌ Lenis breaks scrollIntoView → interceptar anchor clicks con `lenis.scrollTo()`

## TIER D — Calidad/mantenibilidad

### D.1 Wrap cada `init*` en `safe(fn, name)` — un failure no rompe el resto
### D.2 Mounts idempotentes: `if(target.children.length>0)return;`
### D.3 Hardcodear contenido crítico en HTML. JS solo enriquece.

## Quick reference — 12 commandments
1. No `<script type="module">` con imports relativos
2. No gatear micro-interacciones con prefers-reduced-motion
3. Cursor opacity:0 hasta primer mousemove
4. Split-text itera childNodes (preserva `<br>`)
5. mouseover/mouseout + relatedTarget, no mouseenter/mouseleave
6. Bind listeners per-element on render
7. No gsap.from children inside pinned ScrollTrigger
8. IntersectionObserver threshold ≤ 0.05 + 6s safety
9. Splash con doble safety (CSS + JS)
10. Todas las imágenes WebP. Grep pre-entrega
11. Cada init* en safe() try/catch
12. Hardcodear contenido en HTML, JS solo enriquece