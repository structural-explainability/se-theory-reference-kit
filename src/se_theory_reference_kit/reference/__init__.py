"""reference/__init__.py - Generic reference artifact tooling."""

from se_theory_reference_kit.reference.artifacts import (
    ArtifactDeclaration,
    LoadedReferenceArtifact,
    ReferenceDocument,
    discover_reference_artifacts,
    load_reference_artifact,
    ordered_table_values,
    reference_artifact_meta,
)
from se_theory_reference_kit.reference.registry import (
    ReferenceRegistry,
    build_reference_registry,
    registered_lean_symbols,
    section_entries,
    source_modules_in_registry,
)
from se_theory_reference_kit.reference.stubs import (
    make_stub,
    merge_entry,
    reference_stub_key,
)
from se_theory_reference_kit.reference.validation import (
    validate_reference_artifact_shape,
    validate_required_fields,
)

__all__ = [
    "ArtifactDeclaration",
    "LoadedReferenceArtifact",
    "ReferenceDocument",
    "ReferenceRegistry",
    "build_reference_registry",
    "discover_reference_artifacts",
    "load_reference_artifact",
    "make_stub",
    "merge_entry",
    "ordered_table_values",
    "reference_artifact_meta",
    "reference_stub_key",
    "registered_lean_symbols",
    "section_entries",
    "source_modules_in_registry",
    "validate_reference_artifact_shape",
    "validate_required_fields",
]
