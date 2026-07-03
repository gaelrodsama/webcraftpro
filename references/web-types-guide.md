# Guía por Tipo de Web

> Secciones esenciales + consideraciones por tipo. Consultar al iniciar modo CREAR.

## Landing Page
**Propósito:** Conversión. Tono: persuasivo, 2ª persona. 1 página, 5-8 secciones.
**Secciones:** Hero (título+CTA+imagen) → Features/Benefits (3-6 cards) → Social Proof → How It Works (3 pasos) → Testimonios (3) → FAQ (4-6) → CTA Final → Footer minimal
**Schema:** `Product` o `Service` + `FAQPage` para rich snippets

## Corporativa / Institucional
**Propósito:** Credibilidad. Tono: profesional, formal-accesible. 1 página o multi.
**Secciones:** Hero → Nosotros (historia+stats) → Servicios (grid) → Equipo → Casos de éxito/Clientes → Blog (opcional) → Contacto (form+mapa) → Footer completo
**Schema:** `Organization` + `sameAs` + `contactPoint` + BreadcrumbList

## E-commerce
**Propósito:** Venta directa. Tono: descriptivo, persuasivo. Multi-página.
**Secciones Home:** Hero promocional → Categorías → Productos destacados (4-8 cards) → Testimonios → Newsletter
**Página producto:** Galería → Info (nombre, precio, variantes) → Descripción (bullets+beneficios) → Reviews → Related products
**Schema:** `Product` + `offers` + `aggregateRating` + `BreadcrumbList` + OG product

## SaaS / Web App
**Propósito:** Conversión a suscripción. Tono: beneficio-driven. 1 página scroll o multi.
**Secciones:** Hero (demo producto) → Problema-Solución → Features (con demo visual) → Pricing (3 planes) → Integraciones → Testimonios → CTA Final (prueba gratis)
**Schema:** `SoftwareApplication` + `Product` para planes

## Blog / Magacín
**Propósito:** Tráfico orgánico + autoridad. Tono: autoral. Multi-página.
**Home:** Featured post → Categorías → Posts grid (cards thumbnail+título+excerpt+fecha) → Sidebar → Pagination
**Artículo:** Header (título+autor+fecha+lectura+categoría) → Featured image → Content → Author bio → Related posts → Comments
**Schema:** `BlogPosting`/`Article` + OG article + BreadcrumbList + hreflang multi-idioma

## Portfolio / Agencia Creativa
**Propósito:** Mostrar trabajo. Tono: creativo, visual primero. 1 página scroll.
**Secciones:** Hero impactante (video/animación) → Showcase (grid masonry, hover overlay) → About → Services → Clients (logos) → Testimonios → Contact
**Schema:** `Organization` + `knowsAbout`

## Web App / Dashboard
**Propósito:** Herramienta funcional. Tono: neutral, minimalista. Multi-página con sidebar.
**Secciones:** Login → Dashboard (KPIs+gráfica+tabla) → CRUD tables → Detalle → Perfil/Settings → Ayuda/Docs
**Técnico:** Noindex, sin Schema, sesión simulada, responsive priorizando desktop