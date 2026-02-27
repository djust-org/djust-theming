"""
Tests to verify GitHub Actions workflow files use actions/setup-python@v6.
Run with: python -m pytest scratch/test_workflow_versions.py -v
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"

WORKFLOW_FILES = [
    WORKFLOWS_DIR / "test.yml",
    WORKFLOWS_DIR / "publish.yml",
    WORKFLOWS_DIR / "release.yml",
]

EXPECTED_VERSION = "actions/setup-python@v6"
OLD_VERSION = "actions/setup-python@v5"


def test_all_workflow_files_exist():
    for path in WORKFLOW_FILES:
        assert path.exists(), f"Workflow file not found: {path}"


def test_test_yml_uses_setup_python_v6():
    content = (WORKFLOWS_DIR / "test.yml").read_text()
    assert EXPECTED_VERSION in content, (
        f"test.yml should use {EXPECTED_VERSION} but does not"
    )


def test_test_yml_does_not_use_setup_python_v5():
    content = (WORKFLOWS_DIR / "test.yml").read_text()
    assert OLD_VERSION not in content, (
        f"test.yml still references outdated {OLD_VERSION}"
    )


def test_publish_yml_uses_setup_python_v6():
    content = (WORKFLOWS_DIR / "publish.yml").read_text()
    assert EXPECTED_VERSION in content, (
        f"publish.yml should use {EXPECTED_VERSION} but does not"
    )


def test_publish_yml_does_not_use_setup_python_v5():
    content = (WORKFLOWS_DIR / "publish.yml").read_text()
    assert OLD_VERSION not in content, (
        f"publish.yml still references outdated {OLD_VERSION}"
    )


def test_release_yml_uses_setup_python_v6():
    content = (WORKFLOWS_DIR / "release.yml").read_text()
    assert EXPECTED_VERSION in content, (
        f"release.yml should use {EXPECTED_VERSION} but does not"
    )


def test_release_yml_does_not_use_setup_python_v5():
    content = (WORKFLOWS_DIR / "release.yml").read_text()
    assert OLD_VERSION not in content, (
        f"release.yml still references outdated {OLD_VERSION}"
    )


def test_no_workflow_uses_setup_python_v5():
    """Aggregate check: no workflow file anywhere references v5."""
    for path in WORKFLOWS_DIR.glob("*.yml"):
        content = path.read_text()
        matches = re.findall(r"actions/setup-python@v\d+", content)
        for match in matches:
            assert match == EXPECTED_VERSION, (
                f"{path.name}: found '{match}', expected '{EXPECTED_VERSION}'"
            )
