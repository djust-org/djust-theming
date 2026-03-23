"""
Component contracts define the structural requirements for each theme component.

Each contract specifies:
- Required context variables (name, type, default value)
- Required HTML elements that must appear in rendered output
- Required accessibility attributes
- Available slot variables for composability

These contracts are used by the test harness to validate that component templates
(both default and theme-overridden) meet structural and accessibility requirements.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class ContextVar:
    """A context variable expected by a component template."""

    name: str
    type: str  # e.g. "str", "bool", "Optional[str]"
    default: Any = None
    required: bool = False


@dataclass(frozen=True)
class RequiredElement:
    """An HTML element that must exist in the rendered output."""

    tag: str
    attrs: dict = field(default_factory=dict)


@dataclass(frozen=True)
class AccessibilityRequirement:
    """An accessibility attribute that must exist in the rendered output."""

    description: str
    # CSS-like selector hint (for documentation), e.g. "button", "[role=alert]"
    selector_hint: str
    attr: str
    # If value is None, the attr just needs to be present.
    value: Optional[str] = None


@dataclass(frozen=True)
class ComponentContract:
    """Full contract for a single component."""

    name: str
    required_context: tuple[ContextVar, ...] = ()
    optional_context: tuple[ContextVar, ...] = ()
    required_elements: tuple[RequiredElement, ...] = ()
    accessibility: tuple[AccessibilityRequirement, ...] = ()
    available_slots: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Contract definitions
# ---------------------------------------------------------------------------

BUTTON_CONTRACT = ComponentContract(
    name="button",
    required_context=(
        ContextVar(name="text", type="str", required=True),
    ),
    optional_context=(
        ContextVar(name="variant", type="str", default="primary"),
        ContextVar(name="size", type="str", default="md"),
        ContextVar(name="css_prefix", type="str", default=""),
        ContextVar(name="attrs", type="dict", default=None),
        ContextVar(name="slot_icon", type="str", default=None),
        ContextVar(name="slot_content", type="str", default=None),
        ContextVar(name="slot_loading", type="str", default=None),
    ),
    required_elements=(
        RequiredElement(tag="button"),
    ),
    accessibility=(),
    available_slots=("slot_icon", "slot_content", "slot_loading"),
)

CARD_CONTRACT = ComponentContract(
    name="card",
    required_context=(),
    optional_context=(
        ContextVar(name="title", type="Optional[str]", default=None),
        ContextVar(name="content", type="str", default=""),
        ContextVar(name="footer", type="Optional[str]", default=None),
        ContextVar(name="css_prefix", type="str", default=""),
        ContextVar(name="attrs", type="dict", default=None),
        ContextVar(name="slot_header", type="str", default=None),
        ContextVar(name="slot_body", type="str", default=None),
        ContextVar(name="slot_footer", type="str", default=None),
    ),
    required_elements=(
        RequiredElement(tag="div"),
    ),
    accessibility=(),
    available_slots=("slot_header", "slot_body", "slot_footer"),
)

ALERT_CONTRACT = ComponentContract(
    name="alert",
    required_context=(
        ContextVar(name="message", type="str", required=True),
    ),
    optional_context=(
        ContextVar(name="title", type="Optional[str]", default=None),
        ContextVar(name="variant", type="str", default="default"),
        ContextVar(name="dismissible", type="bool", default=False),
        ContextVar(name="css_prefix", type="str", default=""),
        ContextVar(name="attrs", type="dict", default=None),
        ContextVar(name="slot_icon", type="str", default=None),
        ContextVar(name="slot_message", type="str", default=None),
        ContextVar(name="slot_actions", type="str", default=None),
        ContextVar(name="slot_dismiss", type="str", default=None),
    ),
    required_elements=(
        RequiredElement(tag="div", attrs={"role": "alert"}),
    ),
    accessibility=(
        AccessibilityRequirement(
            description="Alert container must have role=alert",
            selector_hint="div",
            attr="role",
            value="alert",
        ),
    ),
    available_slots=("slot_icon", "slot_message", "slot_actions", "slot_dismiss"),
)

BADGE_CONTRACT = ComponentContract(
    name="badge",
    required_context=(
        ContextVar(name="text", type="str", required=True),
    ),
    optional_context=(
        ContextVar(name="variant", type="str", default="default"),
        ContextVar(name="css_prefix", type="str", default=""),
        ContextVar(name="attrs", type="dict", default=None),
        ContextVar(name="slot_content", type="str", default=None),
    ),
    required_elements=(
        RequiredElement(tag="span"),
    ),
    accessibility=(),
    available_slots=("slot_content",),
)

INPUT_CONTRACT = ComponentContract(
    name="input",
    required_context=(
        ContextVar(name="name", type="str", required=True),
    ),
    optional_context=(
        ContextVar(name="label", type="Optional[str]", default=None),
        ContextVar(name="placeholder", type="str", default=""),
        ContextVar(name="type", type="str", default="text"),
        ContextVar(name="css_prefix", type="str", default=""),
        ContextVar(name="attrs", type="dict", default=None),
        ContextVar(name="slot_label", type="str", default=None),
        ContextVar(name="slot_input", type="str", default=None),
        ContextVar(name="slot_help_text", type="str", default=None),
        ContextVar(name="slot_error", type="str", default=None),
    ),
    required_elements=(
        RequiredElement(tag="div"),
    ),
    accessibility=(
        AccessibilityRequirement(
            description="Label must reference input via for attribute",
            selector_hint="label",
            attr="for",
        ),
    ),
    available_slots=("slot_label", "slot_input", "slot_help_text", "slot_error"),
)


COMPONENT_CONTRACTS: dict[str, ComponentContract] = {
    "button": BUTTON_CONTRACT,
    "card": CARD_CONTRACT,
    "alert": ALERT_CONTRACT,
    "badge": BADGE_CONTRACT,
    "input": INPUT_CONTRACT,
}


def get_contract(component_name: str) -> ComponentContract:
    """Return the contract for a component, or raise KeyError."""
    return COMPONENT_CONTRACTS[component_name]
