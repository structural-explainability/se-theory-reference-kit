"""reference/stubs.py - Generic reference stub construction."""

from typing import Any

from se_theory_reference_kit.lean.declarations import LeanDecl

type ReferenceEntry = dict[str, Any]


def reference_stub_key(declaration: LeanDecl) -> str:
    """Return the default reference stub key for a Lean declaration.

    Args:
        declaration: Lean declaration.

    Returns:
        Stub key.
    """
    return declaration.name


def make_stub(
    declaration: LeanDecl,
    source_module: str,
) -> ReferenceEntry:
    """Create a generic reference entry stub for a Lean declaration.

    Args:
        declaration: Lean declaration.
        source_module: Source module for the declaration.

    Returns:
        Reference entry stub.
    """
    return {
        "lean_symbol": declaration.name,
        "lean_kind": declaration.kind,
        "source_module": source_module,
    }


def merge_entry(
    existing: ReferenceEntry,
    generated: ReferenceEntry,
    *,
    overwrite: bool,
) -> ReferenceEntry:
    """Merge an existing hand-authored entry with generated fields.

    Args:
        existing: Existing entry.
        generated: Generated stub fields.
        overwrite: If true, generated values replace existing values.

    Returns:
        Merged entry.
    """
    if overwrite:
        return {**existing, **generated}

    merged = dict(generated)
    merged.update(existing)
    return merged
