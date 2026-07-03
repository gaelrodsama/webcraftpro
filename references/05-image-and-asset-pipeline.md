# Image & Asset Pipeline

3 modos: (1) usuario tiene fotos → `webp_convert.py` (2) quiere stock → `openverse_fetch.py` (3) mix. Usuario nunca instala nada manualmente.

## 1. Pipeline
```
[User photos OR Openverse] → assets/photos/source/ → webp_convert.py → assets/img/ (WebP final) → credits.json
```

## 2. Cuándo Openverse vs preguntar

| Usar Openverse (silencioso) | Preguntar al usuario |
|---|---|
| "No tengo fotos", "use stock", "use whatever" | Restaurante/producto/portfolio (fotos SON el producto) |
| Brief genérico/aspirational (hotel, agencia, magazine) | Mencionó Instagram/Drive/Dropbox |
| Necesita >6 imágenes, proveyó 1-2 | Sitio hiper-personal (wedding planner, personal brand) |

Si no responde → default Openverse.

## 3. Openverse fetch (sin API key)
API: `https://api.openverse.org/v1/images/`. No registro, sin rate limit.
- **Licencias permitidas:** cc0, pdm, by, by-sa. NO by-nc-* (comercial).
- **Filtro renderizable:** solo `.jp(e)g|png|webp|gif|avif`
- **Size cap:** saltar >5 MB (salvo que sea único resultado)
- **Attribution metadata:** guardar en `assets/credits.json` (id, src, title, creator, creator_url, license, license_url, source)
- Footer con link visible "Créditos fotográficos →" y página `creditos.html` auto-generada.

## 4. WebP conversion
**Por qué:** 30% menor que JPEG, soporte universal (Chrome, Edge, Firefox, Safari 14+), single format sin `<picture>`.

**Sizes por categoría:**
| Category | Max width | Quality | Target |
|---|---|---|---|
| Hero panoramic | 2000px | 78 | <250 KB |
| Hero portrait | 1400px | 80 | <200 KB |
| Product/card full | 1100-1200px | 80 | <200 KB |
| Product thumb | 480-560px | 75 | <50 KB |
| Background ambient | 1600px | 78 | <180 KB |
| Logo/icon (alpha) | 600px | 80 | <60 KB |
| Avatar | 600px | 78 | <80 KB |

Reducir dimensión primero, luego calidad. < quality 70 produce artefactos.

**Tools:** Pillow (preferido) → ffmpeg → cwebp → copy originals. Nunca bloquear. Si falla, copiar originales + warn.

**Filename:** kebab-case.webp. Categorizar con prefix cuando hay variaciones (hero.webp, hero-mobile.webp, product-tataki.webp, thumb-product-tataki.webp).

## 5. Hero priority loading
```html
<link rel="preload" as="image" href="assets/img/hero.webp" fetchpriority="high">
<img src="assets/img/hero.webp" fetchpriority="high" loading="eager" decoding="sync">
<!-- others: loading="lazy" decoding="async" -->
```

## 6. Mobile alt-image (solo cuando framing importa)
```html
<picture>
  <source media="(max-width:640px)" srcset="hero-mobile.webp">
  <img src="hero.webp" alt="...">
</picture>
```

## 7. User photos
**Folder:** `assets/photos/source/` (originals, ignored at deploy).
**Auto-categorization:** hero* → hero treatment, logo* → alpha-preserved, *-thumb* → thumbnail, others → standard.
**.HEIC support:** intenta pillow-heif, si falla log warning y skips.

## 8. Asset checklist pre-entrega
- [ ] assets/img/: solo WebP. No .jpg/.png/.heic en HTML/CSS/JS.
- [ ] Hero preloaded, todas con alt, lazy loading en no-hero
- [ ] Openverse: credits.json + creditos.html + footer link visible
- [ ] Total assets/img/ < 4 MB. Ninguna >250 KB (except hero)

## Common bugs
- Mixed format refs → grep pre-deploy (gotcha A.10)
- Hero loaded after content → preload + fetchpriority high
- Missing alt → fails accessibility
- Credits page broken if credits.json malformed → verify_project.py checks