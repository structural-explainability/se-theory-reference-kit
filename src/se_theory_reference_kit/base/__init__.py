"""base/__init__.py - Shared base utilities for theory-reference tooling."""

from se_theory_reference_kit.base.errors import (
    ArtifactLoadError,
    ConfigurationError,
    ReferenceKitError,
    RepositoryRootError,
)
from se_theory_reference_kit.base.paths import (
    find_repository_root,
    lean_module_to_path,
    reference_artifact_path,
    reference_dir,
    reference_index_path,
    resolve_repo_path,
)
from se_theory_reference_kit.base.results import (
    CheckResult,
    CheckSeverity,
    CheckStatus,
    JsonDetail,
    cannot_verify,
    failure,
    ok,
    partial,
    warning,
    worst_status,
)

__all__ = [
    "ArtifactLoadError",
    "ConfigurationError",
    "ReferenceKitError",
    "RepositoryRootError",
    "find_repository_root",
    "lean_module_to_path",
    "reference_artifact_path",
    "reference_dir",
    "reference_index_path",
    "resolve_repo_path",
    "CheckResult",
    "CheckSeverity",
    "CheckStatus",
    "JsonDetail",
    "cannot_verify",
    "failure",
    "ok",
    "partial",
    "warning",
    "worst_status",
]
