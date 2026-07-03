# Prompt: Extract Brand Identity from HTML

> Doble verificación manual + automática pre-modificación. Scripts Python = análisis técnico. Este prompt = análisis visual/semántico.

## 1. Escanear HTML
- **Header**: ¿logo? ¿`<img>`/SVG/texto? ¿clase/id?
- **Paleta**: `:root` variables CSS o selectores con colores repetidos (`.btn`, `.hero`, `body`)
- **Tipografía**: Google Fonts `<link>` + `font-family` en body/:root
- **CTAs**: clase `.cta`/`.btn`, links de acción principal

## 2. Documentar Brand Profile (formato: `memory/memory-system.md`)
**Obligatorio:** colores, tipografías, logotipo, tono, CTAs
**Opcional:** secciones intocables, elementos visuales distintivos, favicon

## 3. Identificar intocables
- Formularios (campos, action, method), teléfonos/emails/direcciones
- Texto legal, avisos privacidad, URLs redes sociales exactos

## 4. Determinar tono

| Tono | Señales |
|------|---------|
| Formal | "Le informamos", "nuestros servicios", usted |
| Casual | "Hola", "te ayudamos", "tú", contracciones |
| Técnico | Jerga industria, especificaciones, datos |
| Emocional | Palabras aspiracionales, historias, sentimientos |
| Mixto | Combinación |

## 5. Guardar en `memory/brand-profiles/{kebab-name}.md`
Paso interno. Sin output al usuario.