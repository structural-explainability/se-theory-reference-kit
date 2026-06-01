"""reference/artifacts.py - Reference artifact discovery and loading."""

from dataclasses import dataclass
from pathlib import Path
from typing import cast

from se_theory_reference_kit.base.io import load_toml
from se_theory_reference_kit.base.paths import reference_artifact_path, reference_dir

type ReferenceDocument = dict[str, object]
type ArtifactDeclaration = dict[str, object]


@dataclass(frozen=True, slots=True)
class LoadedReferenceArtifact:
    """Loaded reference artifact.

    Attributes:
        artifact_id: Stable artifact id from the reference index.
        path: Resolved artifact path.
        kind: Artifact kind declared by the owning repository.
        data: Parsed TOML data.
    """

    artifact_id: str
    path: Path
    kind: str
    data: ReferenceDocument


def discover_reference_artifacts(
    *,
    root: Path | None = None,
    reference_dir_name: str = "reference",
) -> tuple[Path, ...]:
    """Discover TOML reference artifacts under the reference directory.

    Args:
        root: Repository root.
        reference_dir_name: Reference directory name.

    Returns:
        Sorted reference TOML paths.
    """
    root_dir = reference_dir(root=root, reference_dir_name=reference_dir_name)

    if not root_dir.exists():
        return ()

    return tuple(
        sorted(
            path
            for path in root_dir.rglob("*.toml")
            if path.is_file() and path.name != "index.toml"
        )
    )


def load_reference_artifact(
    artifact: ArtifactDeclaration,
    *,
    root: Path,
    reference_dir_name: str = "reference",
) -> LoadedReferenceArtifact:
    """Load one reference artifact declared in the reference index.

    Args:
        artifact: Artifact declaration from reference/index.toml.
        root: Repository root.
        reference_dir_name: Reference directory name.

    Returns:
        Loaded reference artifact.

    Raises:
        ValueError: If the declaration lacks a valid path.
    """
    artifact_id = str(artifact.get("id", "<unnamed>"))
    kind = str(artifact.get("kind", ""))

    rel_path = artifact.get("path", "")
    if not isinstance(rel_path, str) or not rel_path:
        msg = f"artifact {artifact_id!r} path must be a nonempty string"
        raise ValueError(msg)

    path = reference_artifact_path(
        rel_path,
        root=root,
        reference_dir_name=reference_dir_name,
    )

    return LoadedReferenceArtifact(
        artifact_id=artifact_id,
        path=path,
        kind=kind,
        data=load_toml(path),
    )


def reference_artifact_meta(document: ReferenceDocument) -> dict[str, object]:
    """Return normalized metadata from a reference artifact.

    Args:
        document: Parsed reference artifact.

    Returns:
        Copy of the [meta] table, or an empty dictionary when absent.

    Raises:
        ValueError: If [meta] is present but not a table.
    """
    meta = document.get("meta", {})
    if not isinstance(meta, dict):
        msg = "Expected [meta] table"
        raise ValueError(msg)

    # WHY: isinstance narrowing drops the parameters; re-assert them for the copy.
    return dict(cast("dict[str, object]", meta))


def ordered_table_values(
    document: ReferenceDocument,
    table_name: str,
) -> list[dict[str, object]]:
    """Return nested table values sorted by order, then id/key.

    Args:
        document: Parsed reference artifact.
        table_name: Top-level table name.

    Returns:
        Ordered table entries. Each entry receives an id if missing.

    Raises:
        ValueError: If the table is not a table of tables.
    """
    table = document.get(table_name, {})
    if not isinstance(table, dict):
        msg = f"Expected [{table_name}.<id>] tables"
        raise ValueError(msg)

    # WHY: isinstance narrowing drops the parameters; re-assert before iterating.
    table_map = cast("dict[str, object]", table)
    entries: list[dict[str, object]] = []

    for key, value in table_map.items():
        if not isinstance(value, dict):
            msg = f"Expected table entry for {table_name}.{key}"
            raise ValueError(msg)

        entry = dict(cast("dict[str, object]", value))
        entry.setdefault("id", str(key))
        entries.append(entry)

    return sorted(
        entries,
        key=lambda item: (
            item.get("order", 999_999),
            str(item.get("id", "")),
        ),
    )
