"""tests/test_reference.py - Reference artifact tests."""

from pathlib import Path

import pytest

from se_theory_reference_kit.reference.artifacts import (
    load_reference_artifact,
    ordered_table_values,
    reference_artifact_meta,
)
from se_theory_reference_kit.reference.registry import (
    build_reference_registry,
    registered_lean_symbols,
    section_entries,
    source_modules_in_registry,
)


def make_repo(tmp_path: Path) -> Path:
    """Create a minimal repository with reference artifacts."""
    root = tmp_path / "repo"
    reference = root / "reference"
    reference.mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    return root


def test_load_reference_artifact_and_registry(tmp_path: Path) -> None:
    """Reference artifacts load into a registry."""
    root = make_repo(tmp_path)
    artifact_path = root / "reference" / "types.toml"
    artifact_path.write_text(
        "[meta]\n"
        'artifact = "types"\n'
        "\n"
        "[type.Primitive]\n"
        'lean_symbol = "Primitive"\n'
        'lean_kind = "structure"\n'
        'source_module = "SE.Example.Core"\n',
        encoding="utf-8",
    )

    declaration: dict[str, object] = {
        "id": "types",
        "kind": "type",
        "path": "reference/types.toml",
    }
    artifact = load_reference_artifact(declaration, root=root)
    registry = build_reference_registry([declaration], root=root)

    assert artifact.artifact_id == "types"
    assert registry.by_id()["types"].path == artifact_path
    assert registered_lean_symbols(registry) == {"Primitive"}


def test_reference_artifact_meta_requires_table() -> None:
    """Metadata must be a table when present."""
    assert reference_artifact_meta({"meta": {"artifact": "types"}}) == {
        "artifact": "types"
    }

    with pytest.raises(ValueError):
        reference_artifact_meta({"meta": "bad"})


def test_ordered_table_values_sort_by_order_then_id() -> None:
    """Nested table entries are sorted deterministically."""
    document: dict[str, object] = {
        "type": {
            "B": {"order": 2, "label": "b"},
            "A": {"order": 1, "label": "a"},
            "C": {"label": "c"},
        }
    }

    entries = ordered_table_values(document, "type")

    assert [entry["id"] for entry in entries] == ["A", "B", "C"]


def test_section_entries_and_source_modules() -> None:
    """Registry helpers inspect section entries and source modules."""
    document: dict[str, object] = {
        "source_module": "SE.Example.Surface",
        "type": {
            "Primitive": {
                "lean_symbol": "Primitive",
                "source_module": "SE.Example.Core",
            }
        },
    }

    assert section_entries(document, "type") == {
        "Primitive": {
            "lean_symbol": "Primitive",
            "source_module": "SE.Example.Core",
        }
    }
    assert source_modules_in_registry(document) == [
        "SE.Example.Surface",
        "SE.Example.Core",
    ]
