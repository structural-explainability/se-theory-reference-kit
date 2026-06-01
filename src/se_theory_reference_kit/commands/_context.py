"""commands/_context.py - Resolve repo-provided declarations for commands."""

from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import cast

from se_theory_reference_kit.base.errors import ConfigurationError
from se_theory_reference_kit.base.paths import find_repository_root
from se_theory_reference_kit.declarations.config import TheoryReferenceConfig
from se_theory_reference_kit.declarations.export_spec import ExportSpec
from se_theory_reference_kit.declarations.index import (
    ReferenceIndex,
    load_reference_index,
)
from se_theory_reference_kit.declarations.surface import SurfaceSymbols

REFERENCE_TOOL_PACKAGE = "reference_tool"


@dataclass(frozen=True, slots=True)
class CommandContext:
    """Resolved command context for one theory repository."""

    repo_root: Path
    config: TheoryReferenceConfig
    surface: SurfaceSymbols
    export_specs: tuple[ExportSpec, ...]
    reference_index: ReferenceIndex | None = None


def resolve_command_context(
    *,
    root: Path | None = None,
    load_index: bool = False,
) -> CommandContext:
    """Resolve repo-owned declarations used by command handlers."""
    repo_root = find_repository_root(root)

    config = _load_config()
    surface = _load_surface()
    export_specs = _load_export_specs()

    reference_index = None
    if load_index:
        reference_index = load_reference_index(
            root=repo_root,
            reference_dir_name=config.reference_dir_name,
            reference_index_name=config.reference_index_name,
        )

    return CommandContext(
        repo_root=repo_root,
        config=config,
        surface=surface,
        export_specs=export_specs,
        reference_index=reference_index,
    )


def _import_reference_tool_module(name: str) -> ModuleType:
    """Import one repo-owned reference_tool module."""
    module_name = f"{REFERENCE_TOOL_PACKAGE}.{name}"

    try:
        return import_module(module_name)
    except ModuleNotFoundError as exc:
        msg = f"required repo-owned module not found: {module_name}"
        raise ConfigurationError(msg) from exc


def _load_config() -> TheoryReferenceConfig:
    """Load repo-owned theory-reference configuration."""
    module = _import_reference_tool_module("config")
    value = getattr(module, "CONFIG", None)

    if not isinstance(value, TheoryReferenceConfig):
        msg = f"{module.__name__}.CONFIG must be a TheoryReferenceConfig"
        raise ConfigurationError(msg)

    return value


def _load_surface() -> SurfaceSymbols:
    """Load repo-owned Lean public surface declaration."""
    module = _import_reference_tool_module("lean_surface")
    value = getattr(module, "SURFACE", None)

    if not isinstance(value, SurfaceSymbols):
        msg = f"{module.__name__}.SURFACE must be a SurfaceSymbols"
        raise ConfigurationError(msg)

    return value


def _load_export_specs() -> tuple[ExportSpec, ...]:
    """Load repo-owned export specifications."""
    module = _import_reference_tool_module("export_spec")
    value: object = getattr(module, "EXPORT_SPECS", None)

    if not isinstance(value, tuple):
        msg = f"{module.__name__}.EXPORT_SPECS must be tuple[ExportSpec, ...]"
        raise ConfigurationError(msg)

    raw_specs = cast(tuple[object, ...], value)

    specs: list[ExportSpec] = []
    for item in raw_specs:
        if not isinstance(item, ExportSpec):
            msg = f"{module.__name__}.EXPORT_SPECS must contain only ExportSpec values"
            raise ConfigurationError(msg)
        specs.append(item)

    return tuple(specs)
