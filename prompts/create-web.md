# Prompt: Create Web From Scratch

> Modo CREAR. Cargar tras briefing. Seguir orden + referencias indicadas.

## Paso 1: Briefing (mínimo, < 1 min)
1. Tipo web: landing/corporativa/e-commerce/SaaS/blog/portfolio/web app
2. Industria/nicho
3. Objetivo: leads/ventas/portfolio/informar
4. Público objetivo (edad, perfil, sector)
5. Referencias estilo (URLs, opcional)
→ Defaults sensatos si omite. No preguntar de más.

## Paso 2: Diseñar estructura
`references/web-types-guide.md` → tipo solicitado. Definir secciones completas pre-HTML.

## Paso 3: Aplicar diseño
`references/design-principles.md`: escala tipográfica, 60-30-10, sistema 8px, mobile-first, componentes modernos.

## Paso 4: SEO desde inicio
`references/seo-checklist.md`: meta tags, OG, Twitter, Schema, semántica HTML5, Core Web Vitals. Desde la primera línea.

## Paso 5: Template (opcional)
Si el tipo coincide con `templates/base-{tipo}.html` → adaptar colores/contenido/secciones. Si no → construir desde cero con `references/html-patterns.md`.

## Paso 6: Escribir HTML
- Un solo archivo self-contained (CSS interno `<style>`, JS inline/mínimo)
- Comentado con `<!-- ===== SECCIÓN ===== -->`
- Responsive, accesible (alt, aria-label, contraste, headings jerárquicos)
- Funcional: enlaces `#` o reales, formularios funcionales, favicon placeholder

## Paso 7: Auto-verificar
[ ] 1 H1? [ ] Meta tags? [ ] OG? [ ] Schema? [ ] HTML semántico? [ ] Responsive? [ ] Alt? [ ] Contraste? [ ] CTAs claros? [ ] Hover states?

## Paso 8: Entregar
1. HTML completo (ruta o bloque) + resumen (tipo, secciones, decisiones diseño) + opciones personalización + "¿Quieres algún ajuste?"