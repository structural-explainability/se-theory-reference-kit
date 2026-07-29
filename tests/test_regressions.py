"""tests/test_regressions.py - Regression tests for the reference registry."""

from pathlib import Path

from se_theory_reference_kit.declarations.config import TheoryReferenceConfig
from se_theory_reference_kit.reference.artifacts import ReferenceDocument
from se_theory_reference_kit.reference.registry import (
    _symbol_names,
    build_registry_from_config,
)


def test_config_artifact_declarations_preserve_kind_and_path() -> None:
    declarations = [
        {
            "id": kind,
            "kind": kind,
            "path": source,
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
            "path": "reference/substrate-types.toml",
        },
        {
            "id": "predicate",
            "kind": "predicate",
            "path": "reference/substrate-predicates.toml",
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


def test_build_registry_from_config_preserves_repository_relative_paths(
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "se-theory-neutral-substrate"\nversion = "0.0.0"\n',
        encoding="utf-8",
    )

    reference_root = tmp_path / "reference"
    reference_root.mkdir()

    artifact_path = reference_root / "substrate-axioms.toml"
    artifact_path.write_text(
        'schema = "se-substrate-axiom-registry-1"\nkind = "axiom"\n',
        encoding="utf-8",
    )

    config = TheoryReferenceConfig(
        repo_slug="se-theory-neutral-substrate",
        artifact_slug="neutral-substrate",
        lean_public_root="SE",
        surface_kind_sources={
            "axiom": "reference/substrate-axioms.toml",
        },
    )

    registry = build_registry_from_config(tmp_path, config)

    assert len(registry.artifacts) == 1
    assert registry.artifacts[0].artifact_id == "axiom"
    assert registry.artifacts[0].kind == "axiom"
    assert registry.artifacts[0].path == artifact_path.resolve()
