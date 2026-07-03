# Patrones HTML Modernos — WebCraft Pro

> Catálogo de estructuras HTML por tipo de web. Adaptar, no copiar ciegamente.

## Landing Page
```
header(sticky, logo+nav+CTA) → nav
section.hero(h1+p+CTA+img)
section.features(h2+subtitle+div.grid>article.feature-card*4-6)
section.social-proof(logo-cloud o stats)
section.testimonials(div.grid>article.testimonial-card*3)
section.how-it-works(div.steps>div.step*3)
section.faq(div.faq-list>div.faq-item*4-6)
section.cta-final(h2+p+btn-primary)
footer(div.grid columnas + div.footer-bottom)
```

## SaaS / Web App
```
header(search+notifications+avatar) + sidebar(fixed, nav)
main > section.stats-overview(div.grid>div.stat-card*4)
       section.data-table(div.card-header+div.table-wrap>table)
       section.charts(div.chart-container*2)
       section.recent-activity(div.activity-feed>div.activity-item*5)
```

## E-commerce
```
header(logo+search+categorías+carrito)
section.hero-promo(banner) + section.categories(grid>a.category-card*4-6)
section.featured-products(grid>article.product-card*8: img+badge+h3+price+button)
section.testimonials + section.newsletter + footer
```

## Blog
```
header(logo+nav+search)
section.featured-post(hero) + section.posts-grid(grid>article.blog-card*N: img+meta+h2+excerpt+read-more)
--- Artículo individual ---
article.blog-post: header.post-header(h1+meta+author) + div.post-content + section.author-bio + section.related-posts
```

## Portfolio / Agencia
```
header(logo+nav minimal) → main
section.hero(creativa) → section.showcase(div.masonry-grid>article.project-card*N: img+overlay+link)
section.about + section.services + section.testimonials + section.contact(email+social)
```

## Corporativa
```
header(sticky, logo+nav) → main
section.hero → section.about(historia+stats) → section.services(grid) → section.team(fotos+cargos)
→ section.cta-banner → section.contact(form+info+mapa) → footer(logo+nav+sociales+legal)
```

## Dashboard / Admin
```
header(search+notif+avatar) → div.dashboard-layout
sidebar(iconos+labels+submenús) + main: page-header + stats-row(3-4 KPI cards) + chart-row + table-section + quick-actions
```

## Buenas Prácticas
- IDs semánticos en cada sección (navegación ancla)
- ARIA labels en elementos sin texto visible
- `alt` descriptivo (contenido) / `alt=""` (decorativas)
- `<label>` por cada input
- Skip to content link oculto
- `<button>` acciones, `<a>` navegación
- `:focus-visible` nunca eliminado sin reemplazo
- Preferir `rem` sobre `px`