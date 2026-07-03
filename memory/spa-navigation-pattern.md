---
name: spa-navigation-pattern
description: Patrón SPA multi-sección en HTML single-file (data-page + showSection)
metadata:
  type: reference
  domain: html-patterns
---
# SPA Navigation Pattern (Single-File HTML)

## Estructura
```html
<section id="inicio" data-page="inicio" class="active">
<section id="servicios" data-page="inicio">  <!-- misma página -->
<section id="propiedades-venta" data-page="propiedades-venta">
```
## CSS
```css
section[data-page] { display: none; }
section[data-page].active { display: block; }
```
## JS
```js
function showSection(pageId) {
  document.querySelectorAll('section[data-page]').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('section[data-page="' + pageId + '"]').forEach(s => s.classList.add('active'));
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
  document.querySelectorAll('.nav-link[onclick*="' + pageId + '"]').forEach(l => l.classList.add('active'));
  // Cerrar mobile nav, scroll to top, re-evaluar scroll reveal
}
```
## Navegación
```html
<a class="nav-link active" onclick="showSection('inicio')">Inicio</a>
<a class="nav-link" onclick="showSection('propiedades-venta')">Comprar</a>
```
**Why:** Reemplaza páginas separadas por un solo HTML SPA. Sin dependencias, carga instantánea.
**How:** Usar en modo CREAR. No usar href en nav links. Scroll reveal debe re-evaluarse tras showSection.