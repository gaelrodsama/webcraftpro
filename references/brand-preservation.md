# Brand Preservation — Identidad de Marca

> Aplicar en modo MEJORAR. Reglas para que la marca sobreviva intacta.

---

## 1. Categorías

| Categoría | Elementos | Acción |
|-----------|-----------|--------|
| **Intocable** | Logo (src, alt, posición), nombre comercial, tagline, colores primarios, teléfono/email/dirección, CTAs principales | NUNCA cambiar, eliminar ni mover |
| **Refinable** | Colores secundarios, tipografías (añadir Google Fonts similares), layout (conservar orden secciones), tono de voz | Mejorar manteniendo esencia |
| **Mejorable** | SEO, performance, accesibilidad, responsive, CSS (variables, animaciones), imágenes (optimizar, lazy loading) | Libertad total |

---

## 2. Identificar Elementos de Marca

1. Logotipo → primer `<img>` en `<header>` o clase `.logo`/`.brand`
2. Paleta → `:root` variables, clases CSS, inline styles recurrentes
3. Tipografías → `font-family` body, Google Fonts `<link>`, `@font-face`
4. CTAs → elementos con clase `.cta`/`.btn`/`.button`, links de acción principal
5. Tono → titulares y cuerpo: formal/casual/técnico/emocional
6. Secciones → mapear cada sección (hero, features, testimonios...) y función

---

## 3. Elementos No Obvios

- Favicon personalizado, imágenes de fondo recurrentes, iconografía SVG inline
- Mascota/personaje de marca, video/sonido embebido, disclaimer legal
- Certificaciones, sellos, badges, acreditaciones

---

## 4. Documentación de Cambios a Marca

Cada modificación a elemento de marca documentar con:
```html
<!-- WebCraft: color primario refinado de #1a3a5c a #1e3f64 para WCAG AA (4.7:1) -->
<!-- WebCraft: CTA preservado en hero, diseño visual mejorado con sombra + hover -->
```
