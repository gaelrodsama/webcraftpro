#!/usr/bin/env python3
"""
WebCraft Pro — design-scorer.py
Evaluates HTML design quality across multiple dimensions: color, typography,
spacing, semantic structure, and responsive readiness.

Usage:
    python scripts/design-scorer.py --input ejemplo.html
    python scripts/design-scorer.py --input ejemplo.html --output report.json
"""

import argparse
import io
import json
import re
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Error: beautifulsoup4 no está instalado. Ejecuta: pip install beautifulsoup4")


def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def score_color(soup):
    """Evalúa uso de color: variables CSS, paleta detectada, contraste percibido."""
    issues = []
    score = 100
    has_variables = False
    has_dark_bg = False
    has_light_text_on_dark = False
    color_count = 0

    for style in soup.find_all("style"):
        text = style.string or ""
        if ":root" in text or "{" in text:
            # Check for CSS custom properties
            vars_found = re.findall(r"--[\w-]+\s*:", text)
            color_count += len(vars_found)
            if vars_found:
                has_variables = True

            # Detect dark backgrounds
            if re.search(r"background[^}]*?(#0[0-9a-f]|#1[0-9a-f]|rgb\(0\s*,0\s*,0)", text, re.I):
                has_dark_bg = True

    if not has_variables:
        issues.append({
            "category": "color",
            "severity": "medium",
            "title": "No CSS custom properties detected",
            "detail": "Colors may be hardcoded without variables",
            "suggestion": "Define colors in :root using --color-* variables for consistency and easy theming"
        })
        score -= 15

    if color_count < 3:
        issues.append({
            "category": "color",
            "severity": "low",
            "title": f"Only {color_count} color variable(s) found",
            "detail": "May indicate minimal color system",
            "suggestion": "Define at least primary, secondary, accent, and neutral colors"
        })
        score -= 5

    # Check body text color presence
    body = soup.find("body")
    if body and body.get("style"):
        if not re.search(r"color\s*:", body["style"], re.I):
            issues.append({
                "category": "color",
                "severity": "low",
                "title": "Body text color not explicitly styled",
                "detail": "May default to browser black",
                "suggestion": "Set explicit color on body (e.g., #1a1a2e instead of pure black)"
            })
            score -= 5

    return issues, score


def score_typography(soup):
    """Evalúa tipografía: familias, Google Fonts, escala, line-height."""
    issues = []
    score = 100

    # Google Fonts
    google_fonts = []
    for link in soup.find_all("link", href=True):
        if "fonts.googleapis.com" in link["href"]:
            families = re.findall(r"family=([^&:]+)", link["href"])
            google_fonts.extend(families)

    if not google_fonts:
        issues.append({
            "category": "typography",
            "severity": "low",
            "title": "No Google Fonts loaded",
            "detail": "Uses only system fonts",
            "suggestion": "Consider adding web fonts (e.g., Inter, Playfair Display) for better typography"
        })
        score -= 5

    # font-family on body
    has_body_font = False
    for style in soup.find_all("style"):
        text = style.string or ""
        if re.search(r"body\s*\{[^}]*font-family", text, re.I):
            has_body_font = True

    if not has_body_font:
        issues.append({
            "category": "typography",
            "severity": "medium",
            "title": "No font-family declared on body",
            "detail": "Typography hierarchy may not be intentional",
            "suggestion": "Set font-family on body with fallback stack (e.g., 'Inter', system-ui, sans-serif)"
        })
        score -= 15

    # font-size clamping / responsiveness
    has_clamp = False
    for style in soup.find_all("style"):
        text = style.string or ""
        if "clamp(" in text:
            has_clamp = True
            break

    # line-height on body
    has_line_height = False
    for style in soup.find_all("style"):
        text = style.string or ""
        if re.search(r"body\s*\{[^}]*line-height", text, re.I):
            has_line_height = True

    if not has_line_height:
        issues.append({
            "category": "typography",
            "severity": "low",
            "title": "No line-height on body",
            "detail": "Readability may be affected",
            "suggestion": "Set line-height: 1.5-1.7 on body for comfortable reading"
        })
        score -= 5

    # Heading font-size variety (signs of a scale)
    h_sizes = set()
    for h_level in range(1, 4):
        for tag in soup.find_all(f"h{h_level}"):
            style = tag.get("style", "")
            m = re.search(r"font-size\s*:\s*([^;]+)", style, re.I)
            if m:
                h_sizes.add(m.group(1).strip())
    if len(h_sizes) < 2:
        issues.append({
            "category": "typography",
            "severity": "medium",
            "title": "No clear typographic scale",
            "detail": "Headings may lack visual hierarchy",
            "suggestion": "Use a modular scale (e.g., 1.25 ratio) for heading sizes"
        })
        score -= 10

    return issues, score


def score_spacing(soup):
    """Evalúa espaciado: padding/margin en secciones, gap en grids."""
    issues = []
    score = 100
    style_text = ""
    for style in soup.find_all("style"):
        style_text += (style.string or "")

    # Section padding
    has_section_padding = False
    for m in re.finditer(r"section\s*\{[^}]*padding[^}]*\}", style_text):
        if re.search(r"padding[^}]*\d", m.group(0)):
            has_section_padding = True
            break

    if not has_section_padding:
        issues.append({
            "category": "spacing",
            "severity": "medium",
            "title": "Sections may lack vertical padding",
            "detail": "No section padding rule found (e.g., section { padding: 5rem 0 })",
            "suggestion": "Add section { padding: 5rem 1.5rem } with mobile reduction via media query"
        })
        score -= 15

    # Gap in grids
    has_gap = False
    if re.search(r"gap\s*:", style_text):
        has_gap = True

    if not has_gap:
        issues.append({
            "category": "spacing",
            "severity": "low",
            "title": "Grid/flex gap not detected",
            "detail": "Elements may lack consistent spacing in layouts",
            "suggestion": "Use gap: 1.5rem-2rem in grid and flex containers for consistent spacing"
        })
        score -= 5

    return issues, score


def score_semantic_structure(soup):
    """Evalúa estructura semántica y jerarquía."""
    issues = []
    score = 100

    # Heading hierarchy
    headings = []
    for level in range(1, 7):
        for tag in soup.find_all(f"h{level}"):
            headings.append({"level": level, "text": tag.get_text(strip=True)[:40]})

    h1_count = sum(1 for h in headings if h["level"] == 1)
    if h1_count == 0:
        issues.append({
            "category": "structure",
            "severity": "high",
            "title": "No H1 tag found",
            "detail": "Page lacks a main heading",
            "suggestion": "Add one H1 with the page's main title"
        })
        score -= 20
    elif h1_count > 1:
        issues.append({
            "category": "structure",
            "severity": "medium",
            "title": f"Multiple H1 tags ({h1_count})",
            "detail": "Should have only one H1 per page",
            "suggestion": "Use H2-H6 for subheadings, keep one H1"
        })
        score -= 10

    # Content sections
    sections = soup.find_all("section")
    if len(sections) == 0:
        issues.append({
            "category": "structure",
            "severity": "medium",
            "title": "No <section> elements found",
            "detail": "Content may lack semantic grouping",
            "suggestion": "Wrap each content block in <section> with an id"
        })
        score -= 15
    elif not all(s.get("id") for s in sections):
        issues.append({
            "category": "structure",
            "severity": "low",
            "title": "Some sections missing id attributes",
            "detail": "Sections without ids can't be linked via anchor",
            "suggestion": "Add descriptive id to each section (e.g., id='features')"
        })
        score -= 5

    return issues, score


def score_responsive(soup):
    """Evalúa readiness responsive."""
    issues = []
    score = 100
    style_text = ""
    for style in soup.find_all("style"):
        style_text += (style.string or "")

    # Media queries
    media_queries = re.findall(r"@media\s*(?:only\s+)?(?:screen\s+)?(?:and\s+)?\([^)]+\)\s*\{", style_text)

    if len(media_queries) == 0:
        issues.append({
            "category": "responsive",
            "severity": "high",
            "title": "No media queries found",
            "detail": "Page may not be responsive",
            "suggestion": "Add media queries at 768px (tablet) and 480px (mobile) breakpoints"
        })
        score -= 25
    elif len(media_queries) < 2:
        issues.append({
            "category": "responsive",
            "severity": "medium",
            "title": f"Only {len(media_queries)} media query(ies)",
            "detail": "May miss mobile or tablet breakpoint",
            "suggestion": "Add breakpoints at 768px and 480px for full responsiveness"
        })
        score -= 10

    # Container max-width
    if not re.search(r"max-width\s*:\s*\d", style_text):
        issues.append({
            "category": "responsive",
            "severity": "medium",
            "title": "No container max-width detected",
            "detail": "Content may stretch too wide on large screens",
            "suggestion": "Add .container { max-width: 1200px; margin: 0 auto; padding: 0 1.5rem; }"
        })
        score -= 10

    # Viewport
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if not viewport:
        issues.append({
            "category": "responsive",
            "severity": "critical",
            "title": "No viewport meta tag",
            "detail": "Page won't scale correctly on mobile",
            "suggestion": "Add <meta name='viewport' content='width=device-width, initial-scale=1.0'>"
        })
        score -= 20

    # Fluid typography
    if re.search(r"clamp\(", style_text):
        issues.append({
            "category": "responsive",
            "severity": "info",
            "title": "Fluid typography detected (clamp)",
            "detail": "Good practice for responsive text",
            "suggestion": "OK"
        })
    else:
        score -= 5

    return issues, score


def score_design(html_content):
    """Evalúa el HTML en 5 dimensiones de diseño. Retorna score compuesto + issues."""
    soup = BeautifulSoup(html_content, "lxml")

    color_issues, color_score = score_color(soup)
    typography_issues, typo_score = score_typography(soup)
    spacing_issues, spacing_score = score_spacing(soup)
    structure_issues, struct_score = score_semantic_structure(soup)
    responsive_issues, resp_score = score_responsive(soup)

    all_issues = color_issues + typography_issues + spacing_issues + structure_issues + responsive_issues

    # Calculate composite (weighted average)
    composite = (
        color_score * 0.20 +
        typo_score * 0.25 +
        spacing_score * 0.15 +
        struct_score * 0.20 +
        resp_score * 0.20
    )

    # Count by severity
    severity_map = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for issue in all_issues:
        sev = issue["severity"]
        if sev in severity_map:
            severity_map[sev] += 1

    return {
        "composite_score": round(composite, 1),
        "dimension_scores": {
            "color": max(0, color_score),
            "typography": max(0, typo_score),
            "spacing": max(0, spacing_score),
            "structure": max(0, struct_score),
            "responsive": max(0, resp_score)
        },
        "severity_summary": severity_map,
        "issues": sorted(all_issues, key=lambda x: {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}.get(x["severity"], 5))
    }


def main():
    # Ensure UTF-8 output even on Windows
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description="WebCraft Pro — Design Scorer for HTML")
    parser.add_argument("--input", "-i", required=True, help="Path to input HTML file")
    parser.add_argument("--output", "-o", help="Path to output JSON file (default: stdout)")
    args = parser.parse_args()

    html = read_html(args.input)
    result = score_design(html)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Design report saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
