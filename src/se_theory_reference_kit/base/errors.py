"""base/errors.py - Exception types for theory-reference tooling."""


class ReferenceKitError(Exception):
    """Base exception for theory-reference-kit failures."""


class RepositoryRootError(ReferenceKitError):
    """Raised when a repository root cannot be resolved."""


class ConfigurationError(ReferenceKitError):
    """Raised when repo-provided reference configuration is invalid."""


class ArtifactLoadError(ReferenceKitError):
    """Raised when a reference artifact cannot be loaded."""


class ArtifactWriteError(ReferenceKitError):
    """Raised when a reference artifact cannot be written."""


class PathResolutionError(ReferenceKitError):
    """Raised when a repository-relative path is invalid."""
