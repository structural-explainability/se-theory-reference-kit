"""lean/modules.py - Convert between Lean module names and source paths."""

from pathlib import Path

from se_theory_reference_kit.base.errors import PathResolutionError

__all__ = [
    "infer_core_modules",
    "lean_module_to_relative_path",
    "path_to_module",
]


def lean_module_to_relative_path(module: str) -> Path:
    """Convert a Lean module name to a relative Lean source path.

    Args:
        module: Lean module name.

    Returns:
        Relative Lean source path.

    Raises:
        PathResolutionError: If the module name is empty, malformed, or
            path-like.
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

    return Path(*parts).with_suffix(".lean")


def path_to_module(path: Path, lean_root: Path) -> str:
    """Convert a Lean file path to a Lean module name.

    Args:
        path: Lean source file.
        lean_root: Root directory used for module-relative path conversion.

    Returns:
        Dotted Lean module name.
    """
    relative = path.relative_to(lean_root).with_suffix("")
    return ".".join(relative.parts)


def infer_core_modules(surface_module: str, lean_root: Path) -> list[str]:
    """Infer Core modules under a public Surface module namespace.

    Args:
        surface_module: Public surface module, typically ending in ".Surface".
        lean_root: Lean source root.

    Returns:
        Inferred Core module names. Returns an empty list when the surface module
        does not follow the expected Surface naming pattern or no Core files are
        found.
    """
    if not surface_module.endswith(".Surface"):
        return []

    root_module = surface_module.removesuffix(".Surface")
    root_dir = lean_root.joinpath(*root_module.split("."))

    if not root_dir.exists():
        return []

    core_files = sorted(root_dir.rglob("Core.lean"))

    root_core = root_dir / "Core.lean"
    if root_core in core_files:
        core_files.remove(root_core)
        core_files.insert(0, root_core)

    return [path_to_module(path, lean_root) for path in core_files]
