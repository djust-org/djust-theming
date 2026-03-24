"""
Theme manifest parsing, validation, and serialization.

Handles theme.toml files that define user-created themes with references
to color presets and design systems.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# tomllib is stdlib in 3.11+; fall back to tomli for 3.10
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ImportError:
        raise ImportError(
            "Python 3.10 requires the 'tomli' package for TOML parsing. "
            "Install it with: pip install tomli"
        )

# Regex: only lowercase ASCII letters, digits, and hyphens
_VALID_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass
class ThemeManifest:
    """Parsed and validated theme.toml manifest."""

    # [theme] section
    name: str
    version: str
    description: str = ""
    author: str = ""
    license: str = ""

    # [extends] section
    base: Optional[str] = None

    # [tokens] section
    preset: str = "default"
    design_system: str = "material"
    overrides: dict[str, str] = field(default_factory=dict)

    # [static] section
    css: list[str] = field(default_factory=list)
    fonts: list[str] = field(default_factory=list)

    # Internal (not from TOML)
    path: Optional[Path] = None
    templates_dir: Optional[Path] = None

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    @classmethod
    def from_toml(cls, toml_path: Path) -> ThemeManifest:
        """Parse and validate a theme.toml file.

        Args:
            toml_path: Path to the theme.toml file.

        Returns:
            A populated ThemeManifest instance.

        Raises:
            FileNotFoundError: If toml_path does not exist.
            ValueError: If the TOML is invalid or required fields are missing.
        """
        toml_path = Path(toml_path)
        if not toml_path.is_file():
            raise FileNotFoundError(f"Theme manifest not found: {toml_path}")

        try:
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
        except Exception as exc:
            raise ValueError(f"Invalid TOML in {toml_path}: {exc}") from exc

        # --- [theme] section (required) ---
        theme_section = data.get("theme")
        if not theme_section or not isinstance(theme_section, dict):
            raise ValueError(
                f"Missing required [theme] section in {toml_path}"
            )

        name = theme_section.get("name")
        if not name:
            raise ValueError(
                f"Missing required 'name' field in [theme] section of {toml_path}"
            )

        version = theme_section.get("version")
        if not version:
            raise ValueError(
                f"Missing required 'version' field in [theme] section of {toml_path}"
            )

        # --- [extends] section (optional) ---
        extends_section = data.get("extends", {})
        base = extends_section.get("base")

        # --- [tokens] section (optional) ---
        tokens_section = data.get("tokens", {})
        preset = tokens_section.get("preset", "default")
        design_system = tokens_section.get("design_system", "material")
        overrides = tokens_section.get("overrides", {})

        # --- [static] section (optional) ---
        static_section = data.get("static", {})
        css_files = static_section.get("css", [])
        font_files = static_section.get("fonts", [])

        return cls(
            name=name,
            version=version,
            description=theme_section.get("description", ""),
            author=theme_section.get("author", ""),
            license=theme_section.get("license", ""),
            base=base,
            preset=preset,
            design_system=design_system,
            overrides=dict(overrides),
            css=list(css_files),
            fonts=list(font_files),
            path=toml_path.parent,
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Return a list of validation error messages. Empty list means valid."""
        from .registry import get_registry

        registry = get_registry()
        errors: list[str] = []

        # Name validation: only [a-z0-9-], must start with alphanumeric
        if not self.name or not _VALID_NAME_RE.match(self.name):
            errors.append(
                f"Invalid theme name '{self.name}': must contain only "
                f"lowercase letters, digits, and hyphens (pattern: [a-z0-9-])."
            )

        # Preset validation
        if not registry.has_preset(self.preset):
            valid = ", ".join(sorted(registry.list_presets().keys()))
            errors.append(
                f"Unknown preset '{self.preset}'. Valid presets: {valid}"
            )

        # Design system validation
        if not registry.has_theme(self.design_system):
            valid = ", ".join(sorted(registry.list_themes().keys()))
            errors.append(
                f"Unknown design_system '{self.design_system}'. "
                f"Valid design systems: {valid}"
            )

        return errors

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_toml(self) -> str:
        """Serialize this manifest to a TOML string."""
        lines: list[str] = []

        # [theme]
        lines.append("[theme]")
        lines.append(f'name = "{self.name}"')
        lines.append(f'version = "{self.version}"')
        if self.description:
            lines.append(f'description = "{self.description}"')
        if self.author:
            lines.append(f'author = "{self.author}"')
        if self.license:
            lines.append(f'license = "{self.license}"')

        # [extends]
        if self.base:
            lines.append("")
            lines.append("[extends]")
            lines.append(f'base = "{self.base}"')

        # [tokens] — always include so the manifest is self-documenting
        lines.append("")
        lines.append("[tokens]")
        lines.append(f'preset = "{self.preset}"')
        lines.append(f'design_system = "{self.design_system}"')

        if self.overrides:
            lines.append("")
            lines.append("[tokens.overrides]")
            for key, value in self.overrides.items():
                lines.append(f'{key} = "{value}"')

        # [static]
        if self.css or self.fonts:
            lines.append("")
            lines.append("[static]")
            if self.css:
                items = ", ".join(f'"{f}"' for f in self.css)
                lines.append(f"css = [{items}]")
            if self.fonts:
                items = ", ".join(f'"{f}"' for f in self.fonts)
                lines.append(f"fonts = [{items}]")

        lines.append("")  # trailing newline
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def load_theme_manifests(themes_dir: Path) -> list[ThemeManifest]:
    """Discover and load all theme.toml files under *themes_dir*.

    Each immediate subdirectory of *themes_dir* is checked for a
    ``theme.toml`` file.  Directories without one are silently skipped.

    Args:
        themes_dir: Root directory containing theme subdirectories.

    Returns:
        List of parsed ThemeManifest instances (may be empty).
    """
    themes_dir = Path(themes_dir)
    if not themes_dir.is_dir():
        return []

    manifests: list[ThemeManifest] = []
    for child in sorted(themes_dir.iterdir()):
        if not child.is_dir():
            continue
        toml_path = child / "theme.toml"
        if toml_path.is_file():
            manifests.append(ThemeManifest.from_toml(toml_path))

    return manifests
