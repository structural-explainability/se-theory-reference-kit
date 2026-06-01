"""export/catalog.py - Generic reference catalog construction."""

from dataclasses import dataclass
from typing import Any

from se_theory_reference_kit.reference.registry import ReferenceRegistry

type JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class CatalogEntry:
    """Generic catalog entry for one loaded reference artifact."""

    artifact_id: str
    kind: str
    path: str


def build_reference_catalog(
    *,
    registry: ReferenceRegistry,
    schema: str,
    source: str,
    namespace: str,
    artifact: str,
) -> JsonObject:
    """Build a generic reference catalog from loaded reference artifacts.

    This function builds the common catalog envelope and reference path list.
    Repo-specific catalog payload sections remain owned by the theory repo.

    Args:
        registry: Loaded reference registry.
        schema: Catalog schema id.
        source: Owning repository slug.
        namespace: Reference namespace.
        artifact: Catalog artifact name.

    Returns:
        JSON-compatible catalog payload.
    """
    entries = [
        CatalogEntry(
            artifact_id=item.artifact_id,
            kind=item.kind,
            path=item.path.as_posix(),
        )
        for item in registry.artifacts
    ]

    return {
        "schema": schema,
        "source": source,
        "namespace": namespace,
        "artifact": artifact,
        "reference_paths": [entry.path for entry in entries],
        "reference_artifacts": [
            {
                "id": entry.artifact_id,
                "kind": entry.kind,
                "path": entry.path,
            }
            for entry in entries
        ],
    }
