"""
Component storybook -- auto-generated documentation for each theme component.

Reads component contracts, template source, and CSS variable usage to build
rich per-component detail pages.
"""

import re
from pathlib import Path

from djust_theming.contracts import COMPONENT_CONTRACTS, ComponentContract

# Path to the default component templates shipped with the package.
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "djust_theming"
_COMPONENTS_DIR = _TEMPLATES_DIR / "components"

# CSS files that define component styles.
_STATIC_DIR = Path(__file__).resolve().parent.parent / "static" / "djust_theming" / "css"

# Pattern to extract CSS custom property references: var(--name, ...)
_CSS_VAR_RE = re.compile(r"var\(\s*(--[a-zA-Z0-9_-]+)")


def get_component_template_source(component_name: str) -> str:
    """Read and return the raw HTML source of a default component template.

    Args:
        component_name: Component name, e.g. "button", "card".

    Returns:
        Template source as a string, or empty string if not found.
    """
    template_path = _COMPONENTS_DIR / f"{component_name}.html"
    if not template_path.is_file():
        return ""
    return template_path.read_text()


def extract_css_variables(source: str) -> list[str]:
    """Extract unique CSS custom property names from a source string.

    Searches for ``var(--name)`` patterns and returns a deduplicated,
    sorted list of variable names.

    Args:
        source: CSS or HTML source text.

    Returns:
        Sorted list of unique CSS variable names, e.g. ["--background", "--primary"].
    """
    matches = _CSS_VAR_RE.findall(source)
    return sorted(set(matches))


def _get_component_css_variables(component_name: str) -> list[str]:
    """Extract CSS variables used by a component from the CSS files.

    Searches ``components.css`` and ``base.css`` for class selectors that
    match the component name and returns all ``var(--name)`` references
    found in matching rule blocks.
    """
    # Map component names to CSS class prefixes
    class_prefix_map = {
        "button": "btn",
        "card": "card",
        "alert": "alert",
        "badge": "badge",
        "input": "input",
        "modal": "modal",
        "dropdown": "dropdown",
        "tabs": "tab",
        "table": "table",
        "pagination": "pagination",
        "select": "select",
        "textarea": "textarea",
        "checkbox": "checkbox",
        "radio": "radio",
        "breadcrumb": "breadcrumb",
        "avatar": "avatar",
        "toast": "toast",
        "progress": "progress",
        "skeleton": "skeleton",
        "tooltip": "tooltip",
        "nav_item": "nav-link",
        "nav_group": "sidebar",
        "nav": "navbar",
        "sidebar_nav": "sidebar",
    }

    css_prefix = class_prefix_map.get(component_name, component_name)
    all_vars: set[str] = set()

    for css_file in ("components.css", "base.css"):
        css_path = _STATIC_DIR / css_file
        if not css_path.is_file():
            continue
        content = css_path.read_text()
        # Find all rule blocks that contain the component's class prefix
        # Simple approach: scan whole file for var() refs in lines near the class
        in_matching_block = False
        brace_depth = 0
        for line in content.splitlines():
            if f".{css_prefix}" in line and "{" in line:
                in_matching_block = True
                brace_depth = 0
            if in_matching_block:
                brace_depth += line.count("{") - line.count("}")
                all_vars.update(_CSS_VAR_RE.findall(line))
                if brace_depth <= 0:
                    in_matching_block = False

    # Also check the template source for inline var() references
    template_source = get_component_template_source(component_name)
    if template_source:
        all_vars.update(_CSS_VAR_RE.findall(template_source))

    return sorted(all_vars)


def build_storybook_index_context() -> dict:
    """Build context data for the storybook index page.

    Returns:
        Dict with key ``components``: list of dicts with component metadata.
    """
    components = []
    for name, contract in COMPONENT_CONTRACTS.items():
        components.append({
            "name": name,
            "display_name": name.replace("_", " ").title(),
            "required_count": len(contract.required_context),
            "optional_count": len(contract.optional_context),
            "slot_count": len(contract.available_slots),
            "a11y_count": len(contract.accessibility),
        })
    return {"components": components}


def build_storybook_detail_context(component_name: str) -> dict:
    """Build context data for a single component's storybook detail page.

    Args:
        component_name: Component name, e.g. "button".

    Returns:
        Dict with contract info, template source, CSS variables, examples.

    Raises:
        KeyError: If component_name is not in COMPONENT_CONTRACTS.
    """
    contract = COMPONENT_CONTRACTS[component_name]  # raises KeyError
    template_source = get_component_template_source(component_name)
    css_variables = _get_component_css_variables(component_name)

    # Get examples from gallery context builders
    from .context import _EXAMPLE_BUILDERS

    builder = _EXAMPLE_BUILDERS.get(component_name)
    examples = builder() if builder else []

    return {
        "name": component_name,
        "display_name": component_name.replace("_", " ").title(),
        "required_context": [
            {"name": v.name, "type": v.type, "default": v.default, "required": v.required}
            for v in contract.required_context
        ],
        "optional_context": [
            {"name": v.name, "type": v.type, "default": v.default, "required": v.required}
            for v in contract.optional_context
        ],
        "required_elements": [
            {"tag": e.tag, "attrs": e.attrs}
            for e in contract.required_elements
        ],
        "accessibility": [
            {
                "description": a.description,
                "selector_hint": a.selector_hint,
                "attr": a.attr,
                "value": a.value,
            }
            for a in contract.accessibility
        ],
        "available_slots": list(contract.available_slots),
        "template_source": template_source,
        "css_variables": css_variables,
        "examples": examples,
    }


def get_component_coverage(theme_name: str, themes_dir: Path) -> dict:
    """Compute component coverage for a theme.

    Scans the theme's ``components/`` directory for template overrides and
    compares against ``COMPONENT_CONTRACTS``.

    Args:
        theme_name: Theme directory name.
        themes_dir: Root directory containing theme subdirectories.

    Returns:
        Dict with keys: ``overridden`` (list), ``inherited`` (list),
        ``coverage_pct`` (float).

    Raises:
        FileNotFoundError: If the theme directory does not exist.
    """
    theme_dir = Path(themes_dir) / theme_name
    if not theme_dir.is_dir():
        raise FileNotFoundError(f"Theme directory not found: {theme_dir}")

    comp_dir = theme_dir / "components"
    all_names = list(COMPONENT_CONTRACTS.keys())

    overridden = []
    if comp_dir.is_dir():
        for f in comp_dir.iterdir():
            if f.suffix == ".html":
                name = f.stem
                if name in COMPONENT_CONTRACTS:
                    overridden.append(name)

    overridden.sort()
    inherited = sorted(n for n in all_names if n not in overridden)
    total = len(all_names)
    coverage_pct = round(len(overridden) / total * 100, 1) if total > 0 else 0.0

    return {
        "overridden": overridden,
        "inherited": inherited,
        "coverage_pct": coverage_pct,
    }
