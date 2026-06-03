"""tests/test_export.py - Generated export helper tests."""

from pathlib import Path

from se_theory_reference_kit.declarations.export_spec import ExportSpec
from se_theory_reference_kit.export.catalog import build_reference_catalog
from se_theory_reference_kit.export.engine import (
    build_registry_payload,
    export_registries,
)
from se_theory_reference_kit.reference.artifacts import ArtifactDeclaration
from se_theory_reference_kit.reference.registry import build_reference_registry


def make_repo(tmp_path: Path) -> Path:
    """Create a minimal repository with one reference artifact."""
    root = tmp_path / "repo"
    reference = root / "reference"
    reference.mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    (reference / "types.toml").write_text(
        "[meta]\n"
        'artifact = "types"\n'
        "\n"
        "[type.Primitive]\n"
        'lean_symbol = "Primitive"\n'
        'lean_kind = "structure"\n'
        'source_module = "SE.Example.Core"\n'
        "order = 1\n",
        encoding="utf-8",
    )
    return root


def test_build_registry_payload_uses_export_spec(tmp_path: Path) -> None:
    """Registry payload uses repo-owned export spec values."""
    root = make_repo(tmp_path)
    source_path = root / "reference" / "types.toml"
    document: dict[str, object] = {
        "meta": {"artifact": "types"},
        "type": {
            "Primitive": {
                "lean_symbol": "Primitive",
                "lean_kind": "structure",
                "source_module": "SE.Example.Core",
            }
        },
    }
    spec = ExportSpec(
        source_name="types.toml",
        source_table="type",
        output_name="type-registry.json",
        schema="se-example-type-registry-1",
        payload_key="types",
    )

    payload = build_registry_payload(
        spec=spec,
        document=document,
        source_path=source_path,
        repo_slug="se-example",
        reference_namespace="se.example",
    )

    assert payload["schema"] == "se-example-type-registry-1"
    assert payload["artifact"] == "type-registry"
    assert payload["types"] == [
        {
            "id": "Primitive",
            "lean_symbol": "Primitive",
            "lean_kind": "structure",
            "source_module": "SE.Example.Core",
        }
    ]


def test_export_registries_writes_and_checks_generated_json(tmp_path: Path) -> None:
    """Export engine writes generated JSON and check mode verifies freshness."""
    root = make_repo(tmp_path)
    output_root = root / "data" / "example"
    declaration: ArtifactDeclaration = {
        "id": "types",
        "kind": "type",
        "path": "reference/types.toml",
    }
    registry = build_reference_registry([declaration], root=root)
    spec = ExportSpec(
        source_name="types.toml",
        source_table="type",
        output_name="type-registry.json",
        schema="se-example-type-registry-1",
        payload_key="types",
    )

    written = export_registries(
        specs=(spec,),
        registry=registry,
        reference_root=root / "reference",
        output_root=output_root,
        repo_slug="se-example",
        reference_namespace="se.example",
        check=False,
    )
    checked = export_registries(
        specs=(spec,),
        registry=registry,
        reference_root=root / "reference",
        output_root=output_root,
        repo_slug="se-example",
        reference_namespace="se.example",
        check=True,
    )

    assert written[0].wrote
    assert checked[0].current
    assert (output_root / "type-registry.json").is_file()


def test_build_reference_catalog_uses_loaded_registry(tmp_path: Path) -> None:
    """Catalog helper builds a generic reference catalog envelope."""
    root = make_repo(tmp_path)
    declaration: ArtifactDeclaration = {
        "id": "types",
        "kind": "type",
        "path": "reference/types.toml",
    }
    registry = build_reference_registry([declaration], root=root)

    catalog = build_reference_catalog(
        registry=registry,
        schema="se-example-catalog-1",
        source="se-example",
        namespace="se.example",
        artifact="example-catalog",
    )

    assert catalog["schema"] == "se-example-catalog-1"
    assert catalog["reference_paths"] == [
        (root / "reference" / "types.toml").as_posix()
    ]
