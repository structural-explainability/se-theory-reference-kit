"""tests/test_paths.py - Repository path helper tests."""

from pathlib import Path

import pytest

from se_theory_reference_kit.base.errors import PathResolutionError
from se_theory_reference_kit.base.paths import (
    find_repository_root,
    lean_module_to_path,
    reference_artifact_path,
    reference_dir,
    resolve_repo_path,
)


def make_repo(tmp_path: Path) -> Path:
    """Create a minimal repository root."""
    root = tmp_path / "repo"
    root.mkdir()
    (root / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    return root


def test_find_repository_root_uses_markers(tmp_path: Path) -> None:
    """Repository root is resolved from a nested path."""
    root = make_repo(tmp_path)
    nested = root / "a" / "b"
    nested.mkdir(parents=True)

    assert find_repository_root(nested) == root


def test_resolve_repo_path_rejects_escape(tmp_path: Path) -> None:
    """Repository-relative paths may not escape the root."""
    root = make_repo(tmp_path)

    with pytest.raises(PathResolutionError):
        resolve_repo_path("../outside.txt", root=root)


def test_reference_paths_are_repository_relative(tmp_path: Path) -> None:
    """Reference path helpers use standard repository layout."""
    root = make_repo(tmp_path)

    assert reference_dir(root=root) == root / "reference"


def test_reference_artifact_path_requires_reference_directory(tmp_path: Path) -> None:
    """Reference artifacts must be under reference/."""
    root = make_repo(tmp_path)

    assert (
        reference_artifact_path("reference/types.toml", root=root)
        == root / "reference" / "types.toml"
    )

    with pytest.raises(PathResolutionError):
        reference_artifact_path("data/types.toml", root=root)


def test_lean_module_to_path_requires_public_root(tmp_path: Path) -> None:
    """Lean module paths must stay under the repo-declared public root."""
    root = make_repo(tmp_path)

    path = lean_module_to_path(
        "SE.NeutralSubstrate.Surface",
        root=root,
        lean_public_root="SE.NeutralSubstrate",
    )
    assert path == root / "SE" / "NeutralSubstrate" / "Surface.lean"

    with pytest.raises(PathResolutionError):
        lean_module_to_path(
            "Other.Surface",
            root=root,
            lean_public_root="SE.NeutralSubstrate",
        )
