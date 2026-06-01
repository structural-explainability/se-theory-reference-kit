"""lean/__init__.py - Generic Lean source inspection helpers."""

from se_theory_reference_kit.lean.declarations import (
    LEAN_DECL_TO_SECTION,
    SECTION_LEAN_KINDS,
    LeanDecl,
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

__all__ = [
    "LEAN_DECL_TO_SECTION",
    "SECTION_LEAN_KINDS",
    "LeanDecl",
    "extract_decls",
    "extract_for_section",
    "extract_spec_ids",
    "expected_symbols_for_kind",
    "infer_core_modules",
    "infer_spec_module",
    "lean_module_to_relative_path",
    "missing_expected_surface_symbols",
    "path_to_module",
]
