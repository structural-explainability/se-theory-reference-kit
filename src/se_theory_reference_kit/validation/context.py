"""validation/context.py - Context object for theory-reference validation checks.

The context is the read-only input shared by generic validation checks.

It contains repository paths, repo-provided configuration, repo-provided surface
declarations, and repo-provided export specifications. It does not define Lean
semantics and does not own repo-specific public symbol lists.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from se_theory_reference_kit.declarations.config import TheoryReferenceConfig
from se_theory_reference_kit.declarations.export_spec import ExportSpec
from se_theory_reference_kit.declarations.surface import SurfaceSymbols

ReferenceIndex = dict[str, Any]

__all__ = ["ReferenceIndex", "ReferenceRunContext"]


@dataclass(frozen=True, slots=True)
class ReferenceRunContext:
    """Resolved read-only context for theory-reference validation.

    Attributes:
        repo_root: Repository root.
        config: Repo-provided reference configuration.
        surface: Repo-provided public Lean surface declaration.
        export_specs: Repo-provided generated export specifications.
        reference_index: Parsed reference index, when already loaded.
    """

    repo_root: Path
    config: TheoryReferenceConfig
    surface: SurfaceSymbols
    export_specs: tuple[ExportSpec, ...] = ()
    reference_index: ReferenceIndex | None = None

    @property
    def reference_root(self) -> Path:
        """Return the reference artifact directory."""
        return self.repo_root / self.config.reference_dir_name

    @property
    def reference_index_path(self) -> Path:
        """Return the reference index path."""
        return self.reference_root / self.config.reference_index_name

    @property
    def generated_root(self) -> Path:
        """Return the generated data directory."""
        return self.repo_root / self.config.generated_data_dir
