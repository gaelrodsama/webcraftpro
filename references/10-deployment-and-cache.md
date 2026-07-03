# Deployment & Cache Strategy

\#1 source post-launch: "subí el código nuevo y el bug sigue ahí". Casi siempre es cache.

## 1. The problem
Hostinger/Apache/CDNs sirven static files con `Cache-Control: max-age=2592000` (30 días). Subir un archivo NUEVO no invalida cachés. Solución 3-capas — saltar una y el bug vuelve.

## 2. Layer 1 — .htaccess (copia de `templates/htaccess.template`)
```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType text/css "access plus 1 hours"
  ExpiresByType application/javascript "access plus 1 hours"
  ExpiresByType image/webp "access plus 1 month"
  ExpiresByType font/woff2 "access plus 1 month"
</IfModule>
<IfModule mod_headers.c>
  <FilesMatch "\.(html|css|js|json)$">Header set Cache-Control "no-cache, must-revalidate"</FilesMatch>
  <FilesMatch "\.(webp|jpg|jpeg|png|svg|woff2)$">Header set Cache-Control "public, max-age=2592000"</FilesMatch>
</IfModule>
```
HTML revalida cada visita. JS/CSS/JSON revalidan cada visita. Images/fonts cache 1 mes. Funciona en Apache y LiteSpeed. No funciona en Nginx (VPS).

## 3. Layer 2 — Cache-busting query strings
```html
<link rel="stylesheet" href="styles.css?v=20260511">
<script defer src="main.js?v=20260511"></script>
```
Usar `YYYYMMDD`. Bumpear en cada deploy que cambie JS/CSS. Mismo valor en todas las HTML files del proyecto.

## 4. Layer 3 — No ES modules con imports relativos
`?v=` NO propaga a `import './lib/effects.js'`. El browser sirve ese archivo sin cache-buster. Solución: IIFE pattern + `<script defer>` — cada script es entry point con su propio cache-buster. Beneficio extra: funciona en `file://`.

## 5. Deploy checklist
- [ ] `.htaccess` en project root (copiado de template)
- [ ] Todos `<link>` y `<script>` con `?v=YYYYMMDD` (hoy)
- [ ] No `<script type="module">` en deliverable
- [ ] No import/export en JS deliverable
- [ ] Todos `defer` + IIFE pattern
- [ ] En cada cambio a JS/CSS, bumpear `?v=`

## 6. "Subí pero sigo viendo el bug" — diagnóstico
1. **Bumpear `?v=` y re-subir HTML** → 80% casos resuelto
2. **DevTools → Network → reload → styles.css/main.js: ¿200 (fresh) o (disk cache)?** Si stale → Ctrl+Shift+R o cambiar versión
3. **Verificar .htaccess:** abrir `https://sitio.com/.htaccess` → 403 (existe) / 404 (no subió)

## 7. Hostinger-specific
| Plan | Cache behavior |
|---|---|
| Single/Premium/Business shared | Apache + .htaccess funciona |
| Cloud | LiteSpeed, .htaccess funciona (posible LSCache plugin) |
| VPS | Nginx — .htaccess ignorado. Configurar nginx.conf o bumpear `?v=` |

## 8. Alternative hosts
- **Netlify/Cloudflare Pages:** `_headers` file en project root
- **GitHub Pages:** sin server config. Solo cache-busting `?v=`
- **S3+CloudFront:** `Cache-Control` metadata + `create-invalidation`

## 9. 3-question diagnostic
1. "¿Qué URL tienes?" — file:// (no ES modules), localhost (check folder), https:// (cache diagnostic)
2. "DevTools → Network → reload → ¿Status de styles.css/main.js?" — 200=fresh, 304=server dice sin cambios, (disk cache)=browser stale
3. "¿Cache-Control response header?" — `no-cache,must-revalidate`=htaccess funciona, `max-age=2592000`=htaccess no aplicado