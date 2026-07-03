
---
name: data-scraping-js-sites
description: Técnica para extraer datos reales de sitios JS-heavy (EasyBroker, Turbo/Stimulus, React)
metadata:
  type: reference
  domain: scraping
---

# Data Extraction from JS-Heavy Sites

## Problema
Sitios como EasyBroker usan Turbo/Stimulus (JS) para cargar propiedades. WebFetch falla porque el HTML servido contiene solo JS, no datos renderizados.

## Solución: curl + sitemap + regex

### Paso 1: Obtener sitemap
```powershell
curl.exe -s -L "https://sitio.com/sitemap.xml"
```
Los sitemaps de EasyBroker listan **todas** las propiedades como URLs individuales.

### Paso 2: Extraer datos de cada página via curl
Las páginas individuales de EasyBroker tienen meta tags OG + HTML estático con specs:

| Dato | Patrón |
|------|--------|
| Precio | `<span class="listing-type-price">` o `og:description` |
| Recámaras | `<li><span>Recámaras:</span> <strong>2 recámaras</strong>` |
| Baños | `<li><span>Baños:</span> <strong>1</strong>` |
| Superficie | `<span>## m²</span>` |
| Imagen | `og:image` → `assets.easybroker.com/property_images/ID/HASH.jpg` |
| Agente | `<li class="agent"><span>Asesor:</span> <strong>NOMBRE</strong>` |

### Paso 3: Comando típico
```powershell
curl.exe -s -L "URL" | Select-String -Pattern '(og:title|og:description|og:image|listing-type-price|listing-type">|li><span>Recámaras|li><span>Baños|<span>\d+ m²)' -CaseSensitive:$false
```

**Why:** WebFetch es inconsistente para sitios JS-heavy. curl accede al HTML server-side que siempre tiene meta tags OG y estructura HTML básica incluso cuando el contenido principal carga via JS.

**How to apply:** Siempre intentar curl primero. Solo usar WebFetch si curl no da resultado.