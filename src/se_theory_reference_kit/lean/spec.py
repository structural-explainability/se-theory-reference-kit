"""lean/spec.py - Extract stable citation identifiers from Lean spec files."""

from pathlib import Path
import re

from se_theory_reference_kit.base.io import read_text

__all__ = [
    "SPEC_STRING_RE",
    "extract_spec_ids",
    "infer_spec_module",
]

# WHY: SE theory repos commonly define citation ids as Lean string constants in
# Spec modules. This helper extracts the string payloads without interpreting
# theory semantics.
SPEC_STRING_RE = re.compile(
    r"def\s+(?P<name>[A-Za-z_][A-Za-z0-9_'.]*)\s*:\s*String\s*:=\s*"
    r'"(?P<value>[^"]+)"',
    re.MULTILINE,
)


def extract_spec_ids(spec_file: Path) -> set[str]:
    """Extract stable citation ids from a Lean Spec file.

    Args:
        spec_file: Lean Spec source file.

    Returns:
        Citation id string values. Missing files return an empty set.
    """
    if not spec_file.exists():
        return set()

    text = read_text(spec_file)
    return {match.group("value") for match in SPEC_STRING_RE.finditer(text)}


def infer_spec_module(surface_module: str) -> str:
    """Infer the Spec module from the public surface module.

    Args:
        surface_module: Public surface module.

    Returns:
        Inferred Spec module name.
    """
    if surface_module.endswith(".Surface"):
        return surface_module.removesuffix(".Surface") + ".Spec"

    return surface_module + ".Spec"
