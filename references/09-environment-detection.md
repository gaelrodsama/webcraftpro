# Environment Detection & Fallback Strategy

Skill funciona con o sin Python. Bash + curl siempre disponibles (Git Bash en Windows, nativo en macOS/Linux).

## 1. Quick reference

| Step | Python OK | Python missing |
|---|---|---|
| Download libs | `python download_libs.py --target …` | `bash download_libs.sh --target …` |
| Openverse images | `python openverse_fetch.py --inline-queries '…'` | `bash openverse_fetch.sh --id … --query …` (loop) |
| WebP conversion | `python webp_convert.py --src … --dst …` | **Skip.** Usar originales JPG/PNG |
| Verify project | `python verify_project.py --project …` | **grep directo** (ver §5) |

## 2. Detect Python (una vez al inicio)
```bash
PY=""
if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
fi
if [ -n "$PY" ]; then echo "Python OK: $PY"; $PY -c "import urllib.request" || echo "(urllib missing)"; else echo "No Python — using Bash fallbacks"; fi
```

## 3. Bash equivalents

**download_libs.sh:** `--target <path>`, `--three` (Three.js), `--no-skip` (re-download). Bash 3+ compatible.
```bash
bash "<skill-dir>/scripts/download_libs.sh" --target project/lib
```

**openverse_fetch.sh:** 1 query per call. Loop para múltiples:
```bash
QUERIES=("hero|misty mountains forest|wide|" "product-1|coffee macro pour||")
for q in "${QUERIES[@]}"; do IFS='|' read -r id query aspect size <<< "$q"
bash "<skill-dir>/scripts/openverse_fetch.sh" --id "$id" --query "$query" --target project/assets/img --credits project/assets/credits.json
sleep 0.3; done
```
Idempotente en credits.json (appends). Limitaciones vs Python: sin retry automático, parsing JSON grep-based.

## 4. WebP conversion sin Python
```bash
# ffmpeg
if command -v ffmpeg >/dev/null 2>&1; then ffmpeg -y -i "$INPUT" -vf "scale='min(1200,iw)':-2:flags=lanczos,format=yuv420p" -c:v libwebp -quality 80 "$OUTPUT.webp"; fi
# cwebp
if command -v cwebp >/dev/null 2>&1; then cwebp -q 80 "$INPUT" -o "$OUTPUT.webp"; fi
# Skip: cp originals a assets/img/. Referenciar .jpg/.png en HTML. Aceptable — browsers modernos soportan ambos.
```

## 5. Verify sin Python (grep commands)
- Module imports: `grep -rn 'type="module"' --include="*.html" project/`
- Mixed formats: `grep -rnE '"[^"]+\.(jpg|jpeg|png)"' --include="*.html" --include="*.css" --include="*.js" project/`
- Image existence: `grep -rohE 'assets/img/[^"]+\.(webp|jpg|jpeg|png|svg)' --include="*.html" project/ | sort -u | while read p; do if [ ! -f "project/$p" ]; then echo "MISSING: $p"; fi; done`
- One h1: `for h in project/*.html; do c=$(grep -c '<h1' "$h"); if [ "$c" -ne 1 ]; then echo "WARN: $h has $c h1"; fi; done`
- lang attr: `for h in project/*.html; do if ! grep -q '<html[^>]*lang=' "$h"; then echo "WARN: $h missing lang"; fi; done`
- alt on img: `for h in project/*.html; do grep -E '<img\b[^>]*>' "$h" | grep -vE 'alt=' | wc -l; done` (debe ser 0)

## 6. Detection helper (copy-paste)
```bash
PY="";if command -v python3>/dev/null 2>&1;then PY=python3;elif command -v python>/dev/null 2>&1;then PY=python;fi
IMG_TOOL="";if [ -n "$PY" ] && $PY -c "from PIL import Image" 2>/dev/null;then IMG_TOOL="pillow";elif command -v ffmpeg>/dev/null 2>&1;then IMG_TOOL="ffmpeg";elif command -v cwebp>/dev/null 2>&1;then IMG_TOOL="cwebp";fi
echo "Python: ${PY:-(none)}  Img: ${IMG_TOOL:-(none)}  Curl: $(command -v curl>/dev/null 2>&1 && echo OK || echo MISSING)"
```

## 7. Sin curl ni Python (worst case)
Solo en corporate Windows sin Git Bash o Linux containers sin networking. Si curl missing pero wget existe → adaptar scripts. Si ambos faltan → pedir al usuario instalar Git for Windows.

## 8. Strategy summary
```
START → detect Python+curl+img tool
  → curl missing → ask user install Git (rare)
  → Python OK → .py scripts (preferred)
  → Python missing → .sh scripts
  → img tool missing → use originals JPG/PNG, update HTML refs
  → verify with grep checks
```
Nunca pedir "install Python first". Skill se adapta.

## 9. No PowerShell scripts
macOS/Linux no tienen PS. Windows via Claude Code tiene Git Bash. PowerShell triplica script count sin beneficio.