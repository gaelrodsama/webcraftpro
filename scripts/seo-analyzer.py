#!/usr/bin/env python3
"""
WebCraft Pro — seo-analyzer.py
Analyzes HTML against 25+ SEO checkpoints. Outputs a score (0-100) and a
prioritized list of issues with severities and fix suggestions.

Usage:
    python scripts/seo-analyzer.py --input ejemplo.html
    python scripts/seo-analyzer.py --input ejemplo.html --output report.json
"""

import argparse
import io
import json
import re
import sys
from urllib.parse import urlparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Error: beautifulsoup4 no está instalado. Ejecuta: pip install beautifulsoup4")


def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class SEOIssue:
    def __init__(self, category, severity, title, detail, suggestion, exists=True):
        self.category = category
        self.severity = severity  # "critical", "high", "medium", "low"
        self.title = title
        self.detail = detail
        self.suggestion = suggestion
        self.exists = exists  # True = found (good), False = missing (issue)

    def to_dict(self):
        return {
            "category": self.category,
            "severity": self.severity,
            "title": self.title,
            "detail": self.detail,
            "suggestion": self.suggestion,
            "issue": not self.exists
        }


def analyze_seo(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    issues = []
    score = 100
    deductions = []

    # --- 1. Meta tags ---
    title_tag = soup.find("title")
    if title_tag and title_tag.get_text(strip=True):
        title = title_tag.get_text(strip=True)
        title_len = len(title)
        if title_len < 10:
            issues.append(SEOIssue("meta", "high", "Title too short",
                                   f"Current: {title_len} chars", "Write a title of 45-60 chars", False))
            deductions.append(5)
        elif title_len > 70:
            issues.append(SEOIssue("meta", "medium", "Title too long",
                                   f"Current: {title_len} chars", "Shorten to 45-60 chars", False))
            deductions.append(3)
        else:
            issues.append(SEOIssue("meta", "info", "Title present",
                                   f"'{title}' ({title_len} chars)", "OK", True))
    else:
        issues.append(SEOIssue("meta", "critical", "Missing <title> tag",
                               "No title tag found", "Add a descriptive title (45-60 chars)", False))
        deductions.append(15)

    # Meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content", "").strip():
        desc = meta_desc["content"].strip()
        desc_len = len(desc)
        if desc_len < 50:
            issues.append(SEOIssue("meta", "high", "Meta description too short",
                                   f"Current: {desc_len} chars", "Write 120-160 chars", False))
            deductions.append(5)
        elif desc_len > 170:
            issues.append(SEOIssue("meta", "medium", "Meta description too long",
                                   f"Current: {desc_len} chars", "Shorten to 120-160 chars", False))
            deductions.append(3)
        else:
            issues.append(SEOIssue("meta", "info", "Meta description present",
                                   f"'{desc[:80]}...' ({desc_len} chars)", "OK", True))
    else:
        issues.append(SEOIssue("meta", "critical", "Missing meta description",
                               "No description meta tag found", "Add a compelling 120-160 char description", False))
        deductions.append(12)

    # Charset
    charset = soup.find("meta", attrs={"charset": True})
    if charset and charset.get("charset", "").lower() == "utf-8":
        issues.append(SEOIssue("meta", "info", "UTF-8 charset present", "OK", "OK", True))
    else:
        issues.append(SEOIssue("meta", "high", "Missing UTF-8 charset",
                               "No <meta charset='UTF-8'> found", "Add as first child of <head>", False))
        deductions.append(5)

    # Viewport
    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport and "width=device-width" in viewport.get("content", ""):
        issues.append(SEOIssue("meta", "info", "Viewport meta present", "OK", "OK", True))
    else:
        issues.append(SEOIssue("meta", "critical", "Missing or incorrect viewport",
                               "No width=device-width found", "Add <meta name='viewport' content='width=device-width, initial-scale=1.0'>", False))
        deductions.append(10)

    # Robots
    robots = soup.find("meta", attrs={"name": "robots"})
    if robots and robots.get("content", ""):
        issues.append(SEOIssue("meta", "info", "Robots meta present",
                               f"Content: {robots['content']}", "OK", True))
    else:
        issues.append(SEOIssue("meta", "low", "Missing robots meta",
                               "Default: index, follow", "Add <meta name='robots' content='index, follow'>", False))
        deductions.append(2)

    # Canonical
    canonical = soup.find("link", attrs={"rel": "canonical"})
    if canonical and canonical.get("href"):
        issues.append(SEOIssue("meta", "info", "Canonical URL present",
                               canonical["href"], "OK", True))
    else:
        issues.append(SEOIssue("meta", "medium", "Missing canonical URL",
                               "No <link rel='canonical'> found", "Add with the preferred URL of this page", False))
        deductions.append(4)

    # --- 2. Open Graph ---
    og_tags = ["og:title", "og:description", "og:image", "og:url", "og:type"]
    og_found = 0
    for og in og_tags:
        tag = soup.find("meta", attrs={"property": og})
        if tag and tag.get("content", "").strip():
            og_found += 1
            issues.append(SEOIssue("opengraph", "info", f"{og} present", tag["content"][:60], "OK", True))
        else:
            issues.append(SEOIssue("opengraph", "high", f"Missing {og}",
                                   "Not found in <head>", f"Add <meta property='{og}' content='...'>", False))
            deductions.append(4)

    # --- 3. Twitter Cards ---
    twitter_tags = ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]
    tw_found = 0
    for tw in twitter_tags:
        tag = soup.find("meta", attrs={"name": tw})
        if tag and tag.get("content", "").strip():
            tw_found += 1
            issues.append(SEOIssue("twitter", "info", f"{tw} present", tag["content"][:60], "OK", True))
        else:
            issues.append(SEOIssue("twitter", "medium", f"Missing {tw}",
                                   "Not found", f"Add <meta name='{tw}' content='...'>", False))
            deductions.append(3)

    # --- 4. Schema.org ---
    schema = soup.find("script", attrs={"type": "application/ld+json"})
    if schema and schema.string and len(schema.string.strip()) > 20:
        try:
            schema_data = json.loads(schema.string)
            schema_type = schema_data.get("@type", "unknown")
            issues.append(SEOIssue("schema", "info", f"Schema.org present (@type: {schema_type})",
                                   json.dumps(schema_data, ensure_ascii=False)[:80], "OK", True))
        except json.JSONDecodeError:
            issues.append(SEOIssue("schema", "medium", "Schema.org present but invalid JSON",
                                   "JSON-LD could not be parsed", "Fix the JSON syntax", False))
            deductions.append(3)
    else:
        issues.append(SEOIssue("schema", "high", "Missing Schema.org structured data",
                               "No JSON-LD found", "Add <script type='application/ld+json'> with appropriate @type", False))
        deductions.append(8)

    # --- 5. HTML5 semantics ---
    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 1:
        h1_text = h1_tags[0].get_text(strip=True)[:60]
        issues.append(SEOIssue("semantics", "info", "Single <h1> present",
                               f"'{h1_text}'", "OK", True))
    elif len(h1_tags) == 0:
        issues.append(SEOIssue("semantics", "critical", "Missing <h1> tag",
                               "No h1 found", "Add exactly one h1 with the main page title", False))
        deductions.append(10)
    else:
        issues.append(SEOIssue("semantics", "high", f"Multiple <h1> tags ({len(h1_tags)})",
                               "More than one h1 found", "Keep only one h1, use h2-h6 for subsections", False))
        deductions.append(6)

    # Check headings hierarchy
    heading_levels = []
    for level in range(1, 7):
        for tag in soup.find_all(f"h{level}"):
            heading_levels.append(level)
    hierarchy_issue = False
    for i in range(1, len(heading_levels)):
        if heading_levels[i] > heading_levels[i-1] + 1:
            hierarchy_issue = True
            break
    if hierarchy_issue:
        issues.append(SEOIssue("semantics", "medium", "Heading hierarchy skipped",
                               "Headings jump levels (e.g., h1→h3 without h2)", "Ensure headings don't skip levels", False))
        deductions.append(3)

    # HTML5 semantic tags
    semantic_tags = ["header", "main", "nav", "footer"]
    for tag_name in semantic_tags:
        if soup.find(tag_name):
            issues.append(SEOIssue("semantics", "info", f"<{tag_name}> present", "OK", "OK", True))
        else:
            issues.append(SEOIssue("semantics", "medium", f"Missing <{tag_name}>",
                                   f"No {tag_name} tag found", f"Use <{tag_name}> for semantic HTML5", False))
            deductions.append(3)

    # --- 6. Images ---
    images = soup.find_all("img")
    imgs_no_alt = 0
    imgs_no_dim = 0
    imgs_no_lazy = 0
    hero_imgs = 0
    for img in images:
        src = img.get("src", "")
        if not img.get("alt", "").strip() and "placehold" not in src and "data:" not in src:
            imgs_no_alt += 1
        if not img.get("width") or not img.get("height"):
            imgs_no_dim += 1
        if img.get("loading") != "lazy":
            # Only count if not the first img (hero)
            pass

    if imgs_no_alt > 0:
        issues.append(SEOIssue("accessibility", "high", f"{imgs_no_alt} image(s) missing alt text",
                               "Alt attribute empty or missing", "Add descriptive alt text to each image", False))
        deductions.append(min(6, imgs_no_alt * 2))
    else:
        issues.append(SEOIssue("accessibility", "info", "All images have alt text", "OK", "OK", True))

    if imgs_no_dim > 0:
        issues.append(SEOIssue("performance", "medium", f"{imgs_no_dim} image(s) missing width/height",
                               "Can cause Cumulative Layout Shift", "Add width and height attributes to images", False))
        deductions.append(min(4, imgs_no_dim))

    # Lazy loading check
    imgs_below_fold = images[1:] if len(images) > 1 else []
    no_lazy = sum(1 for img in imgs_below_fold if img.get("loading") != "lazy")
    if no_lazy > 0 and len(imgs_below_fold) > 0:
        issues.append(SEOIssue("performance", "medium", f"{no_lazy} image(s) without lazy loading",
                               "Below-fold images should use loading='lazy'", "Add loading='lazy' to non-hero images", False))
        deductions.append(3)
    else:
        issues.append(SEOIssue("performance", "info", "Lazy loading used correctly", "OK", "OK", True))

    # --- 7. Language ---
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        issues.append(SEOIssue("technical", "info", f"Language declared: {html_tag['lang']}", "OK", "OK", True))
    else:
        issues.append(SEOIssue("technical", "medium", "Missing lang attribute on <html>",
                               "No language declaration", "Add <html lang='es'> or the appropriate language", False))
        deductions.append(3)

    # --- 8. Scripts ---
    head_scripts = soup.find_all("script")
    blocking_scripts = [s for s in head_scripts if not s.get("defer") and not s.get("async") and s.get("src")]
    if blocking_scripts:
        issues.append(SEOIssue("performance", "low", f"{len(blocking_scripts)} render-blocking script(s)",
                               "Scripts in head without defer/async", "Add defer attribute to non-critical scripts", False))
        deductions.append(2)

    # --- 9. Favicon ---
    favicon = soup.find("link", attrs={"rel": re.compile(r"icon", re.I)})
    if favicon:
        issues.append(SEOIssue("technical", "info", "Favicon present", favicon.get("href", ""), "OK", True))
    else:
        issues.append(SEOIssue("technical", "low", "Missing favicon",
                               "No <link rel='icon'> found", "Add a favicon link", False))
        deductions.append(1)

    # --- 10. Form labels ---
    forms = soup.find_all("form")
    inputs_without_labels = 0
    for form in forms:
        inputs = form.find_all(["input", "textarea", "select"])
        for inp in inputs:
            if inp.get("type") in ("hidden", "submit", "button", "image"):
                continue
            inp_id = inp.get("id", "")
            if not inp_id or not form.find("label", attrs={"for": inp_id}):
                if not inp.get("aria-label"):
                    inputs_without_labels += 1
    if inputs_without_labels > 0:
        issues.append(SEOIssue("accessibility", "medium", f"{inputs_without_labels} form input(s) without labels",
                               "Missing <label> or aria-label", "Associate labels with inputs using for=id or aria-label", False))
        deductions.append(min(4, inputs_without_labels * 2))

    # --- Calculate final score ---
    score = max(0, 100 - sum(deductions))

    # Count severity categories
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for issue in issues:
        if issue.severity in severity_counts:
            severity_counts[issue.severity] += 1

    return {
        "score": score,
        "deductions": sum(deductions),
        "severity_summary": severity_counts,
        "issues": [i.to_dict() for i in issues]
    }


def main():
    # Ensure UTF-8 output even on Windows
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser(description="WebCraft Pro — SEO Analyzer for HTML")
    parser.add_argument("--input", "-i", required=True, help="Path to input HTML file")
    parser.add_argument("--output", "-o", help="Path to output JSON file (default: stdout)")
    args = parser.parse_args()

    html = read_html(args.input)
    result = analyze_seo(html)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"SEO report saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
