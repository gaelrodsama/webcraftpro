# Prompt: Design Review

> Evaluar diseño visual en modo MEJORAR (post design-scorer.py, pre improve-web.md).

## 1. Evaluar cada dimensión

### Iconografía y Profesionalismo
- [ ] Iconos vectoriales (SVG/Lucide/FA), NUNCA emoji
- [ ] Mismo set, mismo estilo en toda la página
- [ ] Diseño profesional: sin bordes gruesos, sombras excesivas, neón

### Jerarquía Visual
- [ ] Hero es lo primero que ve el usuario
- [ ] CTAs destacan visualmente
- [ ] Progresión lógica: tamaño → peso → color → espaciado

### Color
- [ ] Regla 60-30-10 (neutro/primario/acento)
- [ ] Contraste WCAG AA (4.5:1 texto normal, 3:1 grande)
- [ ] CTAs usan color de mayor contraste
- [ ] Paleta consistente en toda la página

### Tipografía
- [ ] Max 2 familias
- [ ] Escala coherente (sin saltos bruscos)
- [ ] Line-height: 1.5-1.7 cuerpo, 1.1-1.3 headings
- [ ] Párrafos con `max-width: 65ch`

### Espaciado
- [ ] Secciones: min 3rem mobile, 5rem desktop vertical
- [ ] Padding cards/contenedores consistente
- [ ] Gaps grid uniformes

### Responsive
- [ ] Funciona mobile (nav, CTAs, tamaños)
- [ ] Grids colapsan a 1 columna
- [ ] Botones ≥ 44px táctil
- [ ] Menú adaptable (hamburger)

### Consistencia
- [ ] Mismos estilos para mismos componentes
- [ ] Cards uniformes en altura/estilo
- [ ] Iconos mismo estilo (todos outline o todos filled)
- [ ] Bordes, radii, sombras consistentes

### Componentes
- [ ] Cards con hover states
- [ ] Botones con hover/active/focus
- [ ] Formularios con focus/error/success
- [ ] Navegación indica página actual

## 2. Prioridades

| Prioridad | Criterio |
|-----------|----------|
| **P1 Critical** | Funcional/usabilidad grave (CTAs no visibles, texto ilegible) |
| **P2 High** | Impacto calidad significativo (espaciado roto, jerarquía confusa) |
| **P3 Medium** | Mejora estética notable (tipografía, hover states) |
| **P4 Low** | Pulido (animaciones, micro-interacciones, sombras) |

## Output: lista priorizada de mejoras diseño. No modificar HTML aún.