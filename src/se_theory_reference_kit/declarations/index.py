"""declarations/index.py - Reference index loading and inspection."""

from pathlib import Path
from typing import cast

from se_theory_reference_kit.base.io import load_toml
from se_theory_reference_kit.base.paths import reference_index_path

type ArtifactDeclaration = dict[str, object]
type ReferenceIndex = dict[str, object]


def load_reference_index(
    *,
    root: Path | None = None,
    reference_dir_name: str = "reference",
    reference_index_name: str = "index.toml",
) -> ReferenceIndex:
    """Load reference/index.toml.

    Args:
        root: Repository root.
        reference_dir_name: Reference directory name.
        reference_index_name: Reference index file name.

    Returns:
        Parsed reference index.

    Raises:
        FileNotFoundError: If the index file does not exist.
    """
    path = reference_index_path(
        root=root,
        reference_dir_name=reference_dir_name,
        reference_index_name=reference_index_name,
    )

    if not path.exists():
        msg = f"{reference_dir_name}/{reference_index_name} not found: {path}"
        raise FileNotFoundError(msg)

    return load_toml(path)


def reference_artifacts(index: ReferenceIndex) -> list[ArtifactDeclaration]:
    """Return artifact declarations from reference/index.toml.

    Args:
        index: Parsed reference index.

    Returns:
        Artifact declarations.

    Raises:
        TypeError: If the artifact field is not a list.
    """
    artifacts = index.get("artifact", [])

    if not isinstance(artifacts, list):
        msg = "reference/index.toml field 'artifact' must be a list."
        raise TypeError(msg)

    # WHY: isinstance narrowing drops the element type; re-assert before filtering.
    artifact_list = cast("list[object]", artifacts)
    return [item for item in artifact_list if isinstance(item, dict)]


def surface_module(index: ReferenceIndex) -> str:
    """Return the declared public Lean surface module.

    Args:
        index: Parsed reference index.

    Returns:
        Declared public Lean surface module.

    Raises:
        ValueError: If surface_module is missing or invalid.
    """
    value = index.get("surface_module", "")

    if not isinstance(value, str) or not value:
        msg = "reference/index.toml must declare surface_module."
        raise ValueError(msg)

    return value
