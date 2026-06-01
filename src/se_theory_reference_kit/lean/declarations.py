"""lean/declarations.py - Extract generic Lean declarations from source files."""

from dataclasses import dataclass
from pathlib import Path
import re

from se_theory_reference_kit.base.io import read_text

__all__ = [
    "LEAN_DECL_TO_SECTION",
    "SECTION_LEAN_KINDS",
    "DECL_RE",
    "LeanDecl",
    "extract_decls",
    "extract_for_section",
]

# WHY: Reference artifacts group Lean declarations by reference section. This
# mapping is generic across the SE theory repositories; repo-specific symbol
# lists remain in the owning repository.
LEAN_DECL_TO_SECTION: dict[str, str] = {
    "inductive": "type",
    "structure": "type",
    "class": "type",
    "theorem": "theorem",
    "lemma": "theorem",
    "axiom": "axiom",
    "def": "predicate",
    "abbrev": "predicate",
    "instance": "witness",
}

SECTION_LEAN_KINDS: dict[str, frozenset[str]] = {
    "type": frozenset({"inductive", "structure", "class"}),
    "predicate": frozenset({"def", "abbrev"}),
    "theorem": frozenset({"theorem", "lemma"}),
    "axiom": frozenset({"axiom"}),
    "requirement": frozenset({"def"}),
    "vocabulary": frozenset({"def", "abbrev"}),
    "witness": frozenset({"def", "abbrev", "instance"}),
}

# WHY: This is intentionally lightweight source inspection, not a Lean parser.
# It finds ordinary top-level declarations used by reference registries.
DECL_RE = re.compile(
    r"^(?:private\s+|protected\s+)?(?:noncomputable\s+)?"
    r"(?P<kind>theorem|lemma|def|abbrev|inductive|structure|axiom|class|instance)"
    r"\s+(?P<name>[A-Za-z_][A-Za-z0-9_'.]*)",
    re.MULTILINE,
)


@dataclass(frozen=True, slots=True)
class LeanDecl:
    """Lean declaration with name, kind, and reference section."""

    name: str
    kind: str
    section: str


def extract_decls(lean_file: Path) -> list[LeanDecl]:
    """Extract top-level Lean declarations from a Lean file.

    Args:
        lean_file: Lean source file.

    Returns:
        Extracted declarations. Missing files return an empty list.
    """
    if not lean_file.exists():
        return []

    text = read_text(lean_file)
    return [
        LeanDecl(
            name=match.group("name"),
            kind=match.group("kind"),
            section=LEAN_DECL_TO_SECTION.get(match.group("kind"), "unknown"),
        )
        for match in DECL_RE.finditer(text)
    ]


def extract_for_section(lean_file: Path, target_section: str) -> list[LeanDecl]:
    """Extract Lean declarations matching a reference section.

    Args:
        lean_file: Lean source file.
        target_section: Reference section name.

    Returns:
        Declarations whose Lean kind belongs to the requested section.
    """
    wanted = SECTION_LEAN_KINDS.get(target_section)
    if wanted is None:
        return []

    return [decl for decl in extract_decls(lean_file) if decl.kind in wanted]
