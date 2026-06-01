"""reference/registry.py - Reference artifact registry helpers."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from se_theory_reference_kit.reference.artifacts import (
    ArtifactDeclaration,
    LoadedReferenceArtifact,
    ReferenceDocument,
    load_reference_artifact,
)

type SectionEntries = dict[str, dict[str, Any]]


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
