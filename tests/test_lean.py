"""tests/test_lean.py - Generic Lean inspection tests."""

from pathlib import Path

from se_theory_reference_kit.declarations.surface import SurfaceSymbols
from se_theory_reference_kit.lean.declarations import (
    extract_decls,
    extract_for_section,
)
from se_theory_reference_kit.lean.modules import (
    infer_core_modules,
    lean_module_to_relative_path,
    path_to_module,
)
from se_theory_reference_kit.lean.spec import extract_spec_ids, infer_spec_module
from se_theory_reference_kit.lean.surface import (
    expected_symbols_for_kind,
    missing_expected_surface_symbols,
)


def test_extract_decls_reads_top_level_lean_declarations(tmp_path: Path) -> None:
    """Lean declarations are extracted by name, kind, and section."""
    lean_file = tmp_path / "Core.lean"
    lean_file.write_text(
        "\n".join(
            [
                "inductive PrimitiveKind where",
                "def Neutral : Prop := True",
                "axiom framework_relativity : True",
                "theorem neutrality_theorem : True := by trivial",
            ]
        ),
        encoding="utf-8",
    )

    declarations = extract_decls(lean_file)

    assert [item.name for item in declarations] == [
        "PrimitiveKind",
        "Neutral",
        "framework_relativity",
        "neutrality_theorem",
    ]
    assert [item.section for item in declarations] == [
        "type",
        "predicate",
        "axiom",
        "theorem",
    ]


def test_extract_for_section_filters_by_reference_section(tmp_path: Path) -> None:
    """Section extraction filters declarations by generic section mapping."""
    lean_file = tmp_path / "Core.lean"
    lean_file.write_text(
        "def Neutral : Prop := True\n"
        "theorem neutral_if_only_neutral : True := by trivial\n",
        encoding="utf-8",
    )

    theorem_decls = extract_for_section(lean_file, "theorem")

    assert [item.name for item in theorem_decls] == ["neutral_if_only_neutral"]


def test_module_path_conversions() -> None:
    """Lean module names convert to relative paths and back."""
    relative = lean_module_to_relative_path("SE.NeutralSubstrate.Surface")

    assert relative == Path("SE") / "NeutralSubstrate" / "Surface.lean"
    assert path_to_module(relative, Path()) == "SE.NeutralSubstrate.Surface"


def test_infer_core_modules_prefers_root_core(tmp_path: Path) -> None:
    """Core module inference returns root Core.lean first."""
    root = tmp_path
    ns_root = root / "SE" / "NeutralSubstrate"
    nested = ns_root / "Layer"
    nested.mkdir(parents=True)
    (ns_root / "Core.lean").write_text("", encoding="utf-8")
    (nested / "Core.lean").write_text("", encoding="utf-8")

    modules = infer_core_modules("SE.NeutralSubstrate.Surface", root)

    assert modules[0] == "SE.NeutralSubstrate.Core"
    assert "SE.NeutralSubstrate.Layer.Core" in modules


def test_spec_helpers_extract_ids_and_infer_module(tmp_path: Path) -> None:
    """Spec helpers extract string constants and infer Spec module names."""
    spec_file = tmp_path / "Spec.lean"
    spec_file.write_text(
        'def NS001 : String := "NS-001"\ndef NS002 : String := "NS-002"\n',
        encoding="utf-8",
    )

    assert extract_spec_ids(spec_file) == {"NS-001", "NS-002"}
    assert infer_spec_module("SE.NeutralSubstrate.Surface") == (
        "SE.NeutralSubstrate.Spec"
    )


def test_surface_helpers_use_repo_owned_symbols() -> None:
    """Surface helpers compare against repo-owned symbol declarations."""
    surface = SurfaceSymbols.from_optional_kinds(
        types=frozenset({"Primitive"}),
        predicates=frozenset({"Neutral"}),
    )

    assert expected_symbols_for_kind(surface, "type") == frozenset({"Primitive"})
    assert missing_expected_surface_symbols(
        surface=surface,
        registered={"Primitive"},
    ) == {"Neutral"}
