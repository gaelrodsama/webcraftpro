# SEO Checklist — WebCraft Pro

> Obligatorio aplicar en TODA web generada o mejorada. Verificar cada punto.

## 1. Meta Tags
- `<title>` 45-60 chars, keyword principal, único por página
- `<meta name="description">` 120-160 chars, con CTA
- `<meta name="robots">`: `index, follow` (públicas) / `noindex, nofollow` (internas)
- `<meta charset="UTF-8">` en primeros 1024 bytes
- `<meta name="viewport">`: `width=device-width, initial-scale=1.0`

## 2. Open Graph
- `og:title` (40-60), `og:description` (60-160), `og:image` (≥1200×630, ruta absoluta)
- `og:url` (canónica), `og:type` (website/article/product), `og:locale` (ej. es_MX)

## 3. Twitter Cards
- `twitter:card: summary_large_image`, title/description/image = OG

## 4. Schema.org JSON-LD
- Tipo correcto: Organization/Product/Service/LocalBusiness/FAQPage/BreadcrumbList
- Validar con https://validator.schema.org/

## 5. Semántica HTML5
- 1 único `<h1>`, jerarquía h1→h2→h3 sin saltos
- `<header>`, `<nav>`, `<main>`, `<section>`(con id), `<article>`, `<footer>`, `<aside>`

## 6. Core Web Vitals
- Lazy loading (`loading="lazy"`) en todas excepto hero (eager)
- `width`+`height` en todas las imágenes (evitar CLS)
- Fuentes críticas con preload, `display=swap` siempre
- Scripts con `defer` o al final del `<body>`

## 7. Accesibilidad
- `alt` descriptivo en imágenes (vacíos solo decorativas → `alt=""`)
- `aria-label` en elementos interactivos sin texto visible
- Contraste WCAG AA: texto normal ≥4.5:1, grande ≥3:1
- `<label>` o `aria-label` en todos los inputs
- Skip to content link oculto

## 8. Técnico
- `<link rel="canonical">` self-referencing
- `<html lang="es">` correcto
- Favicon (`<link rel="icon">`) + Apple Touch Icon
- Viewport sin `user-scalable=no`
- Hreflang si multi-idioma

## 9. Performance
- Gzip/Brotli (anotar), minificar CSS/JS, WebP/AVIF con fallback
- Fuentes con `display=swap`, CSS crítico inline