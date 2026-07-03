# Prompt: Improve Existing HTML

> CÁRGALO en modo MEJORAR tras extraer marca + auditar SEO + evaluar diseño.
> El flujo previo (pasos 1-5) está en CLAUDE.md §4.

---

## ⚠️ Antes de modificar: confirmar que se ejecutaron
- [ ] Brand Profile extraído (script + manual)
- [ ] `references/brand-preservation.md` leído
- [ ] `python scripts/seo-analyzer.py` + `prompts/seo-audit.md`
- [ ] `python scripts/design-scorer.py` + `prompts/design-reviewer.md`
- [ ] Intocables identificados (logo, color, CTAs, formularios)
- Si falta algo → DETENERSE y ejecutarlo.

---

## Mejorar el HTML

### DEBE
- Arreglar SEO: meta tags, OG, Twitter, Schema, semántica, lazy loading
- Mejorar diseño: tipografía, espaciado, jerarquía, responsive, componentes
- Preservar marca: cada elemento intocable en su lugar exacto
- Documentar cada cambio: `<!-- WebCraft: [qué] — [por qué] -->`
- Aplicar `references/design-principles.md`: escala tipográfica, 60-30-10, sistema 8px
- Mantener funcionalidad: formularios preservan campos+action, links funcionan

### NUNCA
- ❌ Eliminar/cambiar logo (src, alt, posición)
- ❌ Cambiar color primario de marca (solo refinarlo por contraste)
- ❌ Eliminar CTAs existentes
- ❌ Cambiar formularios (name, id, action)
- ❌ Modificar nombre comercial, tagline, contenido core
- ❌ Cambiar URLs redes sociales o datos de contacto
- ❌ Usar emoji como iconos UI (💬 ▶ 📷 ❌ ✅) — usar SVG, Lucide, FA, Heroicons
- ❌ Mezclar estilos de iconos (outline + filled + emoji)
- ❌ Dejar iconos redes sociales sin marca visual clara

---

## Reporte de Cambios (estructura obligatoria)

```
## 📋 Reporte de Mejoras — WebCraft Pro
### SEO (X cambios)
- [Critical/High/Medium/Low] [cambio]
### Diseño (X cambios)
- [P1/P2/P3/P4] [cambio]
### Marca Preservada ✓
- Logo, Color primario, CTAs, Formularios: [estado]
```

## Guardar en Memoria
1. Guardar/actualizar Brand Profile en `memory/brand-profiles/`
2. Escribir entrada en `memory/design-decisions.md`

## Entrega
1. Ruta del HTML mejorado + reporte + "¿Quieres algún ajuste adicional?"
