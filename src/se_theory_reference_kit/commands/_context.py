"""commands/_context.py - Resolve repo-provided declarations for commands."""

from dataclasses import dataclass
from pathlib import Path
import tomllib

from se_theory_reference_kit.base.errors import ConfigurationError
from se_theory_reference_kit.base.paths import find_repository_root
from se_theory_reference_kit.declarations.config import TheoryReferenceConfig
from se_theory_reference_kit.declarations.export_spec import ExportSpec
from se_theory_reference_kit.declarations.surface import SurfaceSymbols
from se_theory_reference_kit.reference.registry import build_surface_symbols

CONFIG_RELPATH = Path("reference") / "theory-reference.toml"
CONFIG_SCHEMA = "se-theory-reference"


@dataclass(frozen=True, slots=True)
class CommandContext:
    """Resolved command context for one theory repository."""

    repo_root: Path
    config: TheoryReferenceConfig
    surface: SurfaceSymbols
    export_specs: tuple[ExportSpec, ...]


def resolve_command_context(*, root: Path | None = None) -> CommandContext:
    """Resolve repo-owned declarations from reference/theory-reference.toml."""
    repo_root = find_repository_root(root)
    data = _load_config_data(repo_root)

    config = TheoryReferenceConfig.from_toml(data)
    export_specs = ExportSpec.specs_from_toml(data)
    surface = build_surface_symbols(repo_root, config)

    return CommandContext(
        repo_root=repo_root,
        config=config,
        surface=surface,
        export_specs=export_specs,
    )


def _find_config(root: Path) -> Path:
    """Locate reference/theory-reference.toml from root upward."""
    root = Path(root).resolve()
    for base in (root, *root.parents):
        candidate = base / CONFIG_RELPATH
        if candidate.is_file():
            return candidate
    msg = f"no {CONFIG_RELPATH.as_posix()} found from {root}"
    raise ConfigurationError(msg)


def _load_config_data(root: Path) -> dict[str, object]:
    """Parse and header-check the theory-reference config."""
    path = _find_config(root)
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        msg = f"{path}: could not read theory-reference config"
        raise ConfigurationError(msg) from exc

    schema = data.get("schema")
    if schema != CONFIG_SCHEMA:
        msg = f"{path}: schema must be {CONFIG_SCHEMA!r}, got {schema!r}"
        raise ConfigurationError(msg)

    return data
