"""declarations/config.py - Repository-specific configuration model."""

from dataclasses import dataclass, field
from pathlib import Path

EMPTY_STRING_SET: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class TheoryReferenceConfig:
    """Repository-specific configuration consumed by the generic engine."""

    repo_slug: str
    artifact_slug: str
    lean_public_root: str
    reference_dir_name: str = "reference"
    reference_index_name: str = "index.toml"
    generated_data_dir: Path | str = "data"
    reference_namespace: str | None = None
    catalog_artifact_name: str | None = None
    catalog_schema: str | None = None
    strict_warning_exemptions: frozenset[str] = field(
        default_factory=lambda: EMPTY_STRING_SET
    )
