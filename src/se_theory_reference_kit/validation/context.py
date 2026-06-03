"""validation/context.py - Context object for theory-reference validation checks."""

from dataclasses import dataclass
from pathlib import Path

from se_theory_reference_kit.declarations.config import TheoryReferenceConfig
from se_theory_reference_kit.declarations.export_spec import ExportSpec
from se_theory_reference_kit.declarations.surface import SurfaceSymbols

__all__ = ["ReferenceRunContext"]


@dataclass(frozen=True, slots=True)
class ReferenceRunContext:
    """Resolved read-only context for theory-reference validation."""

    repo_root: Path
    config: TheoryReferenceConfig
    surface: SurfaceSymbols
    export_specs: tuple[ExportSpec, ...] = ()

    @property
    def reference_root(self) -> Path:
        """Return the reference artifact directory."""
        return self.repo_root / self.config.reference_dir_name

    @property
    def generated_root(self) -> Path:
        """Return the generated data directory."""
        return self.repo_root / self.config.generated_data_dir
