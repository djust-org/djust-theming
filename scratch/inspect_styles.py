"""Inspect computed styles on the landing page with djust pack."""
import json
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8000/landing/"

SELECTORS = {
    "body": "body",
    "nav": "nav",
    "hero_section": "main > section:nth-child(1)",
    "hero_h1": "main > section:nth-child(1) h1",
    "hero_subtitle": "main > section:nth-child(1) h1 + p",
    "hero_badge": "main > section:nth-child(1) a.badge",
    "cta_primary": "main > section:nth-child(1) a.landing-btn-primary",
    "cta_pip": "main > section:nth-child(1) .bg-s2",
    "features_section": "main > section:nth-child(2)",
    "features_h2": "main > section:nth-child(2) h2",
    "feature_card": "main > section:nth-child(2) .landing-card",
    "component_section": "main > section:nth-child(3)",
    "component_h2": "main > section:nth-child(3) h2",
    "code_panel": "main > section:nth-child(3) .code-panel",
    "n1_section": "main > section:nth-child(4)",
    "realtime_section": "main > section:nth-child(5)",
    "realtime_card": "main > section:nth-child(5) .landing-card",
    "footer": "footer",
}

PROPS = [
    "background-color", "color", "font-size", "font-weight", "font-family",
    "line-height", "letter-spacing", "padding-top", "padding-bottom",
    "padding-left", "padding-right", "margin-bottom", "border-radius",
    "border-width", "border-color", "border-style", "box-shadow",
    "gap", "max-width", "backdrop-filter",
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(color_scheme="dark")
    page = ctx.new_page()

    # Set djust pack cookie
    ctx.add_cookies([{
        "name": "djust_theme_pack",
        "value": "djust",
        "domain": "127.0.0.1",
        "path": "/",
    }])
    page.goto(URL, wait_until="networkidle")

    # Also set localStorage for theme mode
    page.evaluate("localStorage.setItem('djust-theme-pack', 'djust')")
    page.evaluate("localStorage.setItem('djust-theme-mode', 'dark')")
    page.reload(wait_until="networkidle")

    results = {}
    for name, sel in SELECTORS.items():
        el = page.query_selector(sel)
        if not el:
            results[name] = {"ERROR": f"selector not found: {sel}"}
            continue
        styles = {}
        for prop in PROPS:
            val = el.evaluate(f"el => getComputedStyle(el).getPropertyValue('{prop}')", el)
            if val:
                styles[prop] = val
        results[name] = styles

    browser.close()

print(json.dumps(results, indent=2))
