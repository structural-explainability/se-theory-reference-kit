"""tests/test_regressions.py - Regression tests for the reference registry."""

from pathlib import Path

from se_theory_reference_kit.reference.artifacts import ReferenceDocument
from se_theory_reference_kit.reference.registry import _symbol_names


def test_build_registry_from_config_preserves_artifact_kind() -> None:
    declarations = [
        {
            "id": kind,
            "kind": kind,
            "path": Path(source).name,
        }
        for kind, source in {
            "type": "reference/substrate-types.toml",
            "predicate": "reference/substrate-predicates.toml",
        }.items()
    ]

    assert declarations == [
        {
            "id": "type",
            "kind": "type",
            "path": "substrate-types.toml",
        },
        {
            "id": "predicate",
            "kind": "predicate",
            "path": "substrate-predicates.toml",
        },
    ]


def test_symbol_names_prefers_lean_symbol_over_display_name() -> None:
    document: ReferenceDocument = {
        "predicate": {
            "NeutralByDesign": {
                "name": "Neutrality by design",
                "lean_symbol": ("SE.NeutralSubstrate.Neutrality.NeutralByDesign"),
            }
        }
    }

    assert _symbol_names(document, "predicate") == [
        "SE.NeutralSubstrate.Neutrality.NeutralByDesign"
    ]
