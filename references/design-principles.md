# Diseño Web — Principios

> Aplicar en TODA web generada o mejorada. No son sugerencias — son criterios.

## 1. Tipografía
- Escala modular: 1rem→1.125→1.424→1.802→2.027rem (mín H1). Hero hasta 3.5rem
- Line-height: 1.5-1.7 cuerpo, 1.1-1.3 headings
- Letter-spacing: -0.02em headings grandes
- `max-width: 65ch` párrafos
- Max 2 familias. Google Fonts: preconnect + preload + `display=swap`

## 2. Color
- Regla 60-30-10: 60% neutro, 30% primario, 10% acento
- WCAG AA: texto normal 4.5:1, grande 3:1, componentes activos 3:1
- Nunca #000 sobre #fff — usar #1a1a2e sobre #f8f8fa
- CSS custom properties en `:root`

## 3. Espaciado (sistema 8px)
- Jerarquía: 0.25→0.5→1→1.5→2→3→4→5→6rem
- Padding min 1.5rem contenedores, secciones 5rem vertical (3rem mobile)
- `max-width: 1200px` desktop, `padding: 0 1.5rem`
- Gap cards: 1.5-2rem

## 4. Jerarquía Visual
- Guiar ojo: tamaño → peso → color → espaciado
- Un solo elemento hero, CTAs con máximo contraste
- Puntos de entrada escaneables (patrón F/Z)

## 5. Responsive (mobile-first)
- Breakpoints: 768px / 1024px / 1280px
- Grid: `repeat(auto-fit, minmax(280px, 1fr))`
- Imágenes: `max-width: 100%; height: auto`
- Tipografía fluida: `clamp(1rem, 2.5vw, 1.5rem)`

## 6. Performance
- CSS crítico inline en `<head>`
- Imágenes con `width`+`height` (anti-CLS)
- Lazy loading debajo del fold
- Scripts con defer o al final de body
- Preload recursos críticos

## 7. Componentes
- **Cards**: border-radius 12-16px, sombra sutil, hover translateY(-4px)
- **Botones**: min 44px altura, border-radius 6-12px, transiciones 0.15-0.2s, estados default→hover→active→focus
- **Nav**: 64-80px desktop / 56-64px mobile, sticky con `backdrop-filter: blur(12px)`, active link destacado
- **Forms**: input height 44-48px, border-radius 6-10px, focus con borde primario, labels visibles

## 8. Iconografía Profesional (OBLIGATORIO)
- **NUNCA emoji como iconos** en UI (💬 ▶ 📷 ❌ ✅) — aspecto amateur, inconsistentes entre OS
- Usar SVG inline / Lucide / Font Awesome / Heroicons. Mismo set y estilo en toda la página
- Tamaño: 18-24px inline, 24-32px redes sociales, 32-48px decorativos
- `aria-hidden="true"` decorativos, `aria-label` interactivos
- Redes sociales: SVGs oficiales o Font Awesome Brands

## 9. Diseño Profesional Moderno
- Minimalismo funcional, espacio negativo, tipografía de calidad (Inter, Plus Jakarta Sans, Playfair, DM Serif)
- Micro-interacciones sutiles (0.15-0.2s), gradientes suaves en fondos (no botones/textos)
- Sin bordes gruesos, sombras múltiples, neón, layouts anticuados

## 10. Animaciones
- Propósito: guiar, no distraer. Duración 0.15-0.3s micro, 0.3-0.6s transiciones
- GPU-accelerated: solo `transform` y `opacity`
- Respetar `prefers-reduced-motion: no-preference`
- IntersectionObserver para fade-in scroll (threshold 0.1-0.2)
- Tipos: FadeInUp, ScaleIn, GradientShift