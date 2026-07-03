#!/usr/bin/env python3
"""
WebCraft Pro — extract-brand.py
Extrae identidad de marca de un HTML: colores, tipografías, logo, CTAs y tono.
Output: JSON estructurado a stdout.

Uso:
    python scripts/extract-brand.py --input ejemplo.html
    python scripts/extract-brand.py --input ejemplo.html --output brand-profile.json
"""

import argparse
import io
import json
import re
import sys
from collections import OrderedDict

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Error: beautifulsoup4 no está instalado. Ejecuta: pip install beautifulsoup4")


def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_colors(soup):
    """Extrae colores del HTML: CSS variables, reglas en <style>, colores inline."""
    colors = {
        "variables": {},
        "classes": [],
        "primitives": [],
        "summary": {}
    }
    seen = OrderedDict()

    # 1. CSS variables from :root or *
    for tag in soup.find_all("style"):
        text = tag.string or ""
        # :root variables
        for m in re.finditer(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\))", text):
            colors["variables"][m.group(1)] = m.group(2)
            seen[m.group(2).lower()] = True
        # Named classes with colors
        for m in re.finditer(r"\.(\w[\w-]*)\s*\{[^}]*?(color|background|background-color)\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\))", text, re.IGNORECASE):
            colors["classes"].append({"selector": m.group(1), "property": m.group(2), "value": m.group(3)})
            seen[m.group(3).lower()] = True

    # 2. Inline styles
    for tag in soup.find_all(style=True):
        style = tag.get("style", "")
        for m in re.finditer(r"(?:color|background|background-color)\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\))", style, re.IGNORECASE):
            val = m.group(1).lower()
            if val not in seen:
                colors["primitives"].append({"tag": tag.name, "value": val})
                seen[val] = True

    # 3. Compute summary: most used non-neutral colors
    all_colors = list(colors["variables"].values()) + [c["value"] for c in colors["classes"]]
    freq = OrderedDict()
    for c in all_colors:
        c_lower = c.lower()
        freq[c_lower] = freq.get(c_lower, 0) + 1
    # Top 5 most frequent
    top5 = sorted(freq.items(), key=lambda x: -x[1])[:5]
    colors["summary"]["top_colors"] = [{"color": c, "frequency": f} for c, f in top5]

    # Detect primary color (most used non-neutral, non-grey)
    neutral_patterns = re.compile(r"#([fF]{3,6}|[0-9a-fA-F]{2,}(?:2|4|6|8|a|c|e|f){2,}|fff$|000$|f[0-9a-f]{2,}|[0-9a-f]{2,}f{2,})", re.IGNORECASE)
    for c, f in top5:
        if not neutral_patterns.match(c) and not c.startswith("#f") and c != "#ffffff" and c != "#000000":
            colors["summary"]["primary_candidate"] = c
            break

    return colors


def extract_fonts(soup):
    """Extrae tipografías del HTML."""
    fonts = {
        "google_fonts": [],
        "font_family_declarations": [],
        "system_fonts": []
    }

    # Google Fonts links
    for link in soup.find_all("link", href=True):
        href = link["href"]
        if "fonts.googleapis.com" in href:
            # Extract family names
            families = re.findall(r"family=([^&:]+)", href)
            fonts["google_fonts"].extend([f.replace("+", " ") for f in families])

    # font-family declarations in <style>
    for tag in soup.find_all("style"):
        text = tag.string or ""
        for m in re.finditer(r"font-family\s*:\s*['\"]?([^;'\"]+)['\"]?", text):
            fonts["font_family_declarations"].append(m.group(1).strip())

    # Inline font-family
    for tag in soup.find_all(style=True):
        style = tag.get("style", "")
        for m in re.finditer(r"font-family\s*:\s*['\"]?([^;'\"]+)['\"]?", style):
            fonts["font_family_declarations"].append(m.group(1).strip())

    # Deduplicate
    fonts["font_family_declarations"] = list(OrderedDict.fromkeys(fonts["font_family_declarations"]))
    fonts["google_fonts"] = list(OrderedDict.fromkeys(fonts["google_fonts"]))

    return fonts


def extract_logo(soup):
    """Busca pistas del logotipo en el HTML."""
    logo = {"found": False, "type": None, "selector": None, "src": None, "alt": None, "position": None}

    # Search in header for first img with logo-like classes
    header = soup.find("header") or soup.find(class_=re.compile(r"header|nav", re.I))
    if header:
        # Look for img with logo-related classes
        for img in header.find_all("img"):
            classes = " ".join(img.get("class", []))
            if any(kw in classes.lower() for kw in ["logo", "brand", "site-logo"]):
                logo["found"] = True
                logo["type"] = "img"
                logo["selector"] = f"header img.{'.'.join(img.get('class', []))}" if img.get("class") else "header img"
                logo["src"] = img.get("src", "")
                logo["alt"] = img.get("alt", "")
                logo["position"] = "header"
                break

        # If no img logo, look for SVG in header
        if not logo["found"]:
            svg = header.find("svg")
            if svg:
                logo["found"] = True
                logo["type"] = "svg"
                logo["selector"] = "header svg"
                logo["position"] = "header"

    # If still not found, look for text logo (a with class logo)
    if not logo["found"]:
        logo_link = soup.find(class_=re.compile(r"logo|brand", re.I))
        if logo_link:
            img_inside = logo_link.find("img")
            if img_inside:
                logo["found"] = True
                logo["type"] = "img"
                logo["selector"] = f".{'.'.join(logo_link.get('class', []))} img"
                logo["src"] = img_inside.get("src", "")
                logo["alt"] = img_inside.get("alt", "")
                logo["position"] = "unknown"
            else:
                logo["found"] = True
                logo["type"] = "text"
                logo["selector"] = f".{'.'.join(logo_link.get('class', []))}"
                logo["text"] = logo_link.get_text(strip=True)[:80]
                logo["position"] = "unknown"

    return logo


def extract_ctas(soup):
    """Extrae CTAs: botones y links con apariencia de CTA."""
    ctas = []
    seen_texts = set()

    cta_classes = re.compile(r"(cta|btn|button|action|primary|hero-cta|wp-block-button)", re.I)

    for tag in soup.find_all(["a", "button"]):
        classes = " ".join(tag.get("class", []))
        text = tag.get_text(strip=True)[:80]

        # Skip if no text or too short
        if not text or len(text) < 3:
            continue

        # Check if it looks like a CTA
        is_cta = bool(cta_classes.search(classes))
        is_cta = is_cta or (tag.name == "button")
        is_cta = is_cta or (tag.name == "a" and tag.find_parent(class_=cta_classes))

        if is_cta and text.lower() not in seen_texts:
            seen_texts.add(text.lower())
            ctas.append({
                "text": text,
                "tag": tag.name,
                "classes": classes,
                "href": tag.get("href", "") if tag.name == "a" else "",
                "position": _get_section_context(tag)
            })

    return ctas


def _get_section_context(tag):
    """Determina en qué sección del HTML está un elemento."""
    parent = tag.find_parent(["section", "header", "footer", "div"])
    if parent:
        parent_id = parent.get("id", "")
        parent_class = " ".join(parent.get("class", []))
        if parent_id:
            return f"#{parent_id}"
        if parent_class:
            return f".{parent_class.split()[0]}"
    return "unknown"


def estimate_tone(soup):
    """Estima el tono de voz basado en el texto visible."""
    # Extract text from visible elements
    texts = []
    for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
        t = tag.get_text(strip=True)
        if len(t) > 20:
            texts.append(t)

    full_text = " ".join(texts).lower()

    # Tone signals
    signals = {
        "formal": ["le informamos", "usted", "les", "nuestros servicios", "solicitamos", "cordiales",
                    "atentamente", "damos a conocer"],
        "casual": ["hola", "hey", "tú", "te", "amigo", "fácil", "rápido", "genial"],
        "technical": ["api", "integración", "backend", "frontend", "framework", "cloud", "server",
                      "database", "algorithm", "scalable", "infraestructura"],
        "emotional": ["transforma", "sueña", "cambia tu vida", "libera", "descubre tu",
                      "imagina", "mereces", "feliz", "confianza"]
    }

    scores = {}
    for tone, keywords in signals.items():
        scores[tone] = sum(1 for kw in keywords if kw in full_text)

    total = sum(scores.values()) or 1
    normalized = {t: round(s / total * 100) for t, s in scores.items()}

    dominant = max(scores, key=scores.get) if max(scores.values()) > 0 else "neutral"

    return {
        "dominant_tone": dominant,
        "scores": normalized,
        "sample_texts": texts[:3]
    }


def extract_brand(html_content):
    """Función principal de extracción de marca."""
    soup = BeautifulSoup(html_content, "lxml")

    brand = {
        "colors": extract_colors(soup),
        "fonts": extract_fonts(soup),
        "logo": extract_logo(soup),
        "ctas": extract_ctas(soup),
        "tone": estimate_tone(soup)
    }

    return brand


def main():
    # Ensure UTF-8 output even on Windows
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description="WebCraft Pro — Extract brand identity from HTML")
    parser.add_argument("--input", "-i", required=True, help="Path to input HTML file")
    parser.add_argument("--output", "-o", help="Path to output JSON file (default: stdout)")
    args = parser.parse_args()

    html = read_html(args.input)
    brand = extract_brand(html)

    output = json.dumps(brand, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Brand profile saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
