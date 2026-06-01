"""tests/test_declarations.py - Declaration model tests."""

from pathlib import Path

from se_theory_reference_kit.declarations.config import TheoryReferenceConfig
from se_theory_reference_kit.declarations.export_spec import ExportSpec
from se_theory_reference_kit.declarations.surface import SurfaceSymbols


def test_theory_reference_config_accepts_core_values() -> None:
    """Config stores repo-owned declaration values."""
    config = TheoryReferenceConfig(
        repo_slug="se-theory-neutral-substrate",
        artifact_slug="neutral-substrate",
        lean_public_root="SE.NeutralSubstrate",
        generated_data_dir=Path("data/neutral-substrate"),
        strict_warning_exemptions=frozenset({"kind mismatch"}),
    )

    assert config.repo_slug == "se-theory-neutral-substrate"
    assert config.artifact_slug == "neutral-substrate"
    assert config.lean_public_root == "SE.NeutralSubstrate"
    assert config.strict_warning_exemptions == frozenset({"kind mismatch"})


def test_surface_symbols_defaults_missing_kinds_to_empty() -> None:
    """Missing surface kinds behave as empty symbol sets."""
    surface = SurfaceSymbols.from_optional_kinds(
        types=frozenset({"Primitive"}),
        predicates=frozenset({"Neutral"}),
    )

    assert surface.symbols_for_kind("type") == frozenset({"Primitive"})
    assert surface.symbols_for_kind("axiom") == frozenset()
    assert surface.all_symbols == frozenset({"Primitive", "Neutral"})


def test_export_spec_stores_repo_owned_export_shape() -> None:
    """ExportSpec stores one generated artifact declaration."""
    spec = ExportSpec(
        source_name="types.toml",
        source_table="type",
        output_name="type-registry.json",
        schema="se-example-type-registry-1",
        payload_key="types",
    )

    assert spec.source_name == "types.toml"
    assert spec.payload_key == "types"
