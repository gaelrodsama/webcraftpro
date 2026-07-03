# Prompt: SEO Audit

> Auditoría SEO en modo MEJORAR (post seo-analyzer.py, pre improve-web.md).

## 1. Verificar contra `references/seo-checklist.md`
Repasar UNO POR UNO: Meta tags → Open Graph → Twitter Cards → Schema.org → Semántica HTML5 → Core Web Vitals → Accesibilidad → Técnico → Performance.

## 2. Priorizar hallazgos

| Severidad | Criterio |
|-----------|----------|
| **Critical** | Rompe funcionalidad o SEO completamente (falta title, no viewport) |
| **High** | Impacta ranking/usabilidad significativamente (sin OG, Schema, alt) |
| **Medium** | Mejorable (title corto, descripción genérica) |
| **Low** | Nice-to-have (preload fuentes, lazy loading) |

## 3. Output
Lista priorizada de issues SEO. No modificar HTML aún — esperar a `improve-web.md`.
Cada issue: qué se encontró → qué debería ser → severidad.