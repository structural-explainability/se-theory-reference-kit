"""tests/test_commands_context.py - Command context loading tests."""

from pathlib import Path
import sys

from se_theory_reference_kit.commands._context import resolve_command_context


def test_resolve_command_context_loads_repo_owned_typed_declarations(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Command context loads typed declarations from repo-owned reference_tool."""
    root = tmp_path / "repo"
    reference_tool = root / "reference_tool"
    reference = root / "reference"
    reference_tool.mkdir(parents=True)
    reference.mkdir()
    (root / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    (reference_tool / "__init__.py").write_text("", encoding="utf-8")
    (reference_tool / "config.py").write_text(
        "from se_theory_reference_kit.declarations.config import "
        "TheoryReferenceConfig\n"
        "CONFIG = TheoryReferenceConfig(\n"
        "    repo_slug='se-example',\n"
        "    artifact_slug='example',\n"
        "    lean_public_root='SE.Example',\n"
        ")\n",
        encoding="utf-8",
    )
    (reference_tool / "lean_surface.py").write_text(
        "from se_theory_reference_kit.declarations.surface import SurfaceSymbols\n"
        "SURFACE = SurfaceSymbols.from_optional_kinds(\n"
        "    types=frozenset({'Primitive'}),\n"
        ")\n",
        encoding="utf-8",
    )
    (reference_tool / "export_spec.py").write_text(
        "from se_theory_reference_kit.declarations.export_spec import ExportSpec\n"
        "EXPORT_SPECS = (\n"
        "    ExportSpec(\n"
        "        source_name='types.toml',\n"
        "        source_table='type',\n"
        "        output_name='type-registry.json',\n"
        "        schema='se-example-type-registry-1',\n"
        "        payload_key='types',\n"
        "    ),\n"
        ")\n",
        encoding="utf-8",
    )
    (reference / "index.toml").write_text(
        'surface_module = "SE.Example.Surface"\n',
        encoding="utf-8",
    )

    monkeypatch.syspath_prepend(str(root))
    sys.modules.pop("reference_tool", None)
    sys.modules.pop("reference_tool.config", None)
    sys.modules.pop("reference_tool.lean_surface", None)
    sys.modules.pop("reference_tool.export_spec", None)

    context = resolve_command_context(root=root, load_index=True)

    assert context.repo_root == root
    assert context.config.repo_slug == "se-example"
    assert context.surface.all_symbols == frozenset({"Primitive"})
    assert len(context.export_specs) == 1
    assert context.reference_index == {"surface_module": "SE.Example.Surface"}
