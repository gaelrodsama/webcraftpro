# Sistema de Memoria

> Instrucciones para gestión de memoria entre sesiones. Leer al inicio de modo MEJORAR.

## Componentes
```
memory/
├── memory-system.md           ← este archivo
├── design-decisions.md        ← log cronológico decisiones diseño
├── MEMORY.md                  ← índice de memorias
└── brand-profiles/            ← un archivo por proyecto/cliente
```

## Brand Profiles (`memory/brand-profiles/{kebab-name}.md`)

### Cuándo crear
Tras ejecutar `scripts/extract-brand.py` + `prompts/brand-extractor.md` en modo MEJORAR.

### Formato
```markdown
---
name: kebab-name
cliente: Nombre Empresa
fecha: YYYY-MM-DD
source: URL o "HTML proporcionado"
---
# Perfil: [Nombre]
## Colores
- **Primario**: `#HEX` — uso: [botones, headers]
- **Secundario**: `#HEX` — uso: [fondos, bordes]
- **Acento**: `#HEX` — uso: [CTAs, highlights]
- **Neutro claro/oscuro**: `#HEX` — [fondos/texto]
## Tipografías
- **Principal**: [fuente] — [body/headings]
- **Cargas**: [Google Fonts links / @font-face]
## Logotipo
- Tipo/Dimensión/Posición/Alt text
## Tono: [formal/casual/técnico/emocional/mixto]
## CTAs actuales: [lista texto + sección + tipo + enlace]
## Intocables: [secciones que no modifican]
## Distintivos: [iconos custom, ilustraciones, patrones, gradientes]
```

## Design Decisions Log (`design-decisions.md`)
Añadir entrada al final tras cada mejora/creación:
```markdown
## [YYYY-MM-DD] — [Proyecto]
**Decisión**: ...
**Alternativas**: ...
**Razón**: ...
**Impacto**: ...
```

## Flujo Memoria en MEJORAR
1. Recibir HTML → 2. Buscar perfil en `brand-profiles/` (si existe→cargar, si no→extraer) → 3. Leer `design-decisions.md` → 4. Ejecutar mejora → 5. Guardar/actualizar perfil → 6. Escribir entrada log

> ⚠️ Brand profiles contienen datos reales de clientes. No compartir en repos públicos. `.gitignore` excluye `memory/brand-profiles/*`.