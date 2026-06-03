"""reference/registry.py - Reference artifact registry helpers."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from se_theory_reference_kit.base.io import load_toml
from se_theory_reference_kit.declarations.config import TheoryReferenceConfig
from se_theory_reference_kit.declarations.surface import SurfaceSymbols
from se_theory_reference_kit.reference.artifacts import (
    ArtifactDeclaration,
    LoadedReferenceArtifact,
    ReferenceDocument,
    load_reference_artifact,
)

type SectionEntries = dict[str, dict[str, Any]]

SURFACE_KINDS: frozenset[str] = frozenset(
    {"type", "predicate", "axiom", "theorem", "requirement", "vocabulary", "witness"}
)


@dataclass(frozen=True, slots=True)
class ReferenceRegistry:
    """Loaded reference artifact registry.

    Attributes:
        artifacts: Loaded reference artifacts in index order.
    """

    artifacts: tuple[LoadedReferenceArtifact, ...]

    def by_id(self) -> dict[str, LoadedReferenceArtifact]:
        """Return loaded artifacts keyed by artifact id."""
        return {artifact.artifact_id: artifact for artifact in self.artifacts}


def build_reference_registry(
    artifact_declarations: list[ArtifactDeclaration],
    *,
    root: Path,
    reference_dir_name: str = "reference",
) -> ReferenceRegistry:
    """Build a registry from artifact declarations.

    Args:
        artifact_declarations: Artifact declarations from reference/index.toml.
        root: Repository root.
        reference_dir_name: Reference directory name.

    Returns:
        Loaded reference registry.
    """
    loaded = tuple(
        load_reference_artifact(
            artifact,
            root=root,
            reference_dir_name=reference_dir_name,
        )
        for artifact in artifact_declarations
    )

    return ReferenceRegistry(artifacts=loaded)


def build_registry_from_config(
    repo_root: Path, config: TheoryReferenceConfig
) -> ReferenceRegistry:
    """Build the full reference registry from the config artifact sources."""
    declarations: list[ArtifactDeclaration] = [
        {"id": kind, "path": Path(source).name}
        for kind, source in config.surface_kind_sources.items()
    ]
    return build_reference_registry(
        declarations,
        root=repo_root,
        reference_dir_name=config.reference_dir_name,
    )


def build_surface_symbols(
    repo_root: Path, config: TheoryReferenceConfig
) -> SurfaceSymbols:
    """Derive the public surface from the mapped reference artifacts."""
    reference_root = repo_root / config.reference_dir_name
    by_kind: dict[str, frozenset[str]] = {}
    for kind, source in config.surface_kind_sources.items():
        if kind not in SURFACE_KINDS:
            continue
        artifact = load_toml(reference_root / Path(source).name)
        by_kind[kind] = frozenset(_symbol_names(artifact, kind))
    return SurfaceSymbols(by_kind=by_kind)


def section_entries(
    data: ReferenceDocument,
    section: str,
) -> SectionEntries:
    """Return table entries for a reference section.

    Args:
        data: Parsed reference artifact.
        section: Section name.

    Returns:
        Section entries keyed by entry id.
    """
    raw_section = data.get(section, {})

    if not isinstance(raw_section, dict):
        return {}

    # WHY: isinstance narrowing collapses the value to dict[Unknown, Unknown],
    # so re-assert the parameters that pyright strict otherwise reports unknown.
    section_map = cast("dict[str, object]", raw_section)

    entries: SectionEntries = {}

    for key, value in section_map.items():
        if isinstance(value, dict):
            entries[key] = cast("dict[str, Any]", value)

    return entries


def registered_lean_symbols(
    registry: ReferenceRegistry,
    *,
    sections: frozenset[str] | None = None,
) -> set[str]:
    """Return Lean symbols registered in reference artifacts.

    Args:
        registry: Loaded reference registry.
        sections: Optional section filter.

    Returns:
        Registered Lean symbol names.
    """
    symbols: set[str] = set()

    for artifact in registry.artifacts:
        section_names = sections if sections is not None else frozenset(artifact.data)

        for section in section_names:
            for entry in section_entries(artifact.data, section).values():
                symbol = entry.get("lean_symbol")
                if isinstance(symbol, str) and symbol:
                    symbols.add(symbol)

    return symbols


def source_modules_in_registry(data: ReferenceDocument) -> list[str]:
    """Return source modules declared inside a reference artifact.

    Args:
        data: Parsed reference artifact.

    Returns:
        Source module names in first-seen order.
    """
    modules: list[str] = []
    seen: set[str] = set()

    top_level = data.get("source_module")
    if isinstance(top_level, str) and top_level and top_level not in seen:
        modules.append(top_level)
        seen.add(top_level)

    for value in data.values():
        if not isinstance(value, dict):
            continue

        # WHY: re-assert parameters lost by isinstance narrowing before iterating.
        section_map = cast("dict[str, object]", value)

        extract_unique_source_modules(modules, seen, section_map)

    return modules


def extract_unique_source_modules(
    modules: list[str], seen: set[str], section_map: dict[str, object]
) -> None:
    """Extract unique source modules from a section map."""
    for entry in section_map.values():
        if not isinstance(entry, dict):
            continue

        entry_map = cast("dict[str, object]", entry)
        source_module = entry_map.get("source_module")
        if (
            isinstance(source_module, str)
            and source_module
            and source_module not in seen
        ):
            modules.append(source_module)
            seen.add(source_module)


def _symbol_names(data: ReferenceDocument, kind: str) -> list[str]:
    """Return public symbol names from a reference artifact section."""
    entries = section_entries(data, kind)
    names: list[str] = []

    for entry_id, entry in entries.items():
        raw_name = entry.get("name")
        if isinstance(raw_name, str) and raw_name:
            names.append(raw_name)
            continue

        raw_symbol = entry.get("lean_symbol")
        if isinstance(raw_symbol, str) and raw_symbol:
            names.append(raw_symbol)
            continue

        names.append(entry_id)

    return names
