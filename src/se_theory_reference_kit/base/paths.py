"""base/paths.py - Repository-relative path helpers."""

from pathlib import Path

from se_theory_reference_kit.base.errors import (
    PathResolutionError,
    RepositoryRootError,
)

ROOT_MARKERS: tuple[str, ...] = ("pyproject.toml", "SE_MANIFEST.toml", ".git")


def find_repository_root(start: Path | None = None) -> Path:
    """Find the nearest repository root from a starting path.

    Args:
        start: Starting path. Defaults to the current working directory.

    Returns:
        Resolved repository root path.

    Raises:
        RepositoryRootError: If no repository root marker is found.
    """
    current = (start or Path.cwd()).resolve()

    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if any((candidate / marker).exists() for marker in ROOT_MARKERS):
            return candidate

    msg = f"Could not resolve repository root from {current}"
    raise RepositoryRootError(msg)


def resolve_repo_path(path: str | Path, *, root: Path | None = None) -> Path:
    """Resolve a path as repository-relative and contained within the repository.

    Args:
        path: Repository-relative path.
        root: Repository root. Defaults to nearest detected repository root.

    Returns:
        Resolved absolute path.

    Raises:
        PathResolutionError: If the path escapes the repository root.
    """
    repo_root = find_repository_root(root)
    resolved = (repo_root / path).resolve()

    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        msg = f"Path escapes repository root: {path}"
        raise PathResolutionError(msg) from exc

    return resolved


def reference_dir(
    *,
    root: Path | None = None,
    reference_dir_name: str = "reference",
) -> Path:
    """Return the repository reference directory."""
    return resolve_repo_path(reference_dir_name, root=root)


def reference_artifact_path(
    path: str | Path,
    *,
    root: Path | None = None,
    reference_dir_name: str = "reference",
) -> Path:
    """Resolve a declared reference artifact path.

    The declared path must be repository-relative and under the reference
    directory.

    Args:
        path: Declared repository-relative artifact path.
        root: Repository root.
        reference_dir_name: Name of the reference artifact directory.

    Returns:
        Resolved reference artifact path.

    Raises:
        PathResolutionError: If the path is outside the reference directory.
    """
    resolved = resolve_repo_path(path, root=root)
    reference_root = reference_dir(
        root=root,
        reference_dir_name=reference_dir_name,
    ).resolve()

    try:
        resolved.relative_to(reference_root)
    except ValueError as exc:
        msg = f"Reference artifact path is not under {reference_dir_name}/: {path}"
        raise PathResolutionError(msg) from exc

    return resolved


def lean_module_to_path(
    module: str,
    *,
    root: Path | None = None,
    lean_public_root: str,
) -> Path:
    """Resolve a Lean module name to its repository source path.

    Args:
        module: Lean module name.
        root: Repository root.
        lean_public_root: Expected public Lean root for the owning repository.

    Returns:
        Repository-contained Lean source path.

    Raises:
        PathResolutionError: If the module name is empty, path-like, malformed,
            or outside the declared public Lean root.
    """
    module_name = module.strip()

    if not module_name:
        msg = "Lean module name must be nonempty."
        raise PathResolutionError(msg)

    if "/" in module_name or "\\" in module_name:
        msg = f"Expected Lean module name, got path-like value: {module}"
        raise PathResolutionError(msg)

    parts = module_name.split(".")

    if any(not part for part in parts):
        msg = f"Malformed Lean module name: {module}"
        raise PathResolutionError(msg)

    if module_name != lean_public_root and not module_name.startswith(
        f"{lean_public_root}."
    ):
        msg = f"Expected Lean module under {lean_public_root}, got: {module_name}"
        raise PathResolutionError(msg)

    relative_path = Path(*parts).with_suffix(".lean")
    return resolve_repo_path(relative_path, root=root)
