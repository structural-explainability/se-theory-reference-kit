"""declarations/config.py - Repository-specific configuration model."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self, cast

EMPTY_STRING_SET: frozenset[str] = frozenset()
EMPTY_SOURCE_MAP: Mapping[str, str] = {}


@dataclass(frozen=True, slots=True)
class TheoryReferenceConfig:
    """Repository-specific configuration consumed by the generic engine."""

    repo_slug: str
    artifact_slug: str
    lean_public_root: str
    reference_dir_name: str = "reference"
    generated_data_dir: Path | str = "data"
    reference_namespace: str | None = None
    catalog_artifact_name: str | None = None
    catalog_schema: str | None = None
    surface_kind_sources: Mapping[str, str] = field(
        default_factory=lambda: EMPTY_SOURCE_MAP
    )
    strict_warning_exemptions: frozenset[str] = field(
        default_factory=lambda: EMPTY_STRING_SET
    )

    @classmethod
    def from_toml(cls, data: Mapping[str, object]) -> Self:
        """Build configuration from a parsed theory-reference.toml mapping."""
        repository = _section(data, "repository")
        lean = _section(data, "lean")
        reference = _section(data, "reference")
        export = _section(data, "export")
        export_map = _string_mapping(data, "export_map")
        surface_kinds = _string_mapping(data, "surface_kinds")
        strict = _section(data, "strict")

        artifact_slug = _require_str(repository, "theory", "repository.theory")
        catalog_path = export_map.get("catalog")
        catalog_artifact = Path(catalog_path).stem if catalog_path else None
        catalog_schema = _opt_str(export.get("catalog_schema")) or (
            f"se-theory-{artifact_slug}-catalog"
        )

        return cls(
            repo_slug=_require_str(repository, "name", "repository.name"),
            artifact_slug=artifact_slug,
            lean_public_root=_require_str(lean, "root_module", "lean.root_module"),
            reference_dir_name=_str(reference.get("root"), "reference"),
            generated_data_dir=_str(export.get("root"), "data"),
            reference_namespace=_opt_str(lean.get("namespace")),
            catalog_artifact_name=catalog_artifact,
            catalog_schema=catalog_schema,
            surface_kind_sources=surface_kinds,
            strict_warning_exemptions=frozenset(
                _string_list(strict, "warning_exemptions")
            ),
        )


def _section(data: Mapping[str, object], name: str) -> Mapping[str, object]:
    """Return a TOML section as a mapping."""
    value = data.get(name, {})
    if isinstance(value, Mapping):
        return cast(Mapping[str, object], value)
    return {}


def _str(value: object, default: str) -> str:
    """Return value if it is a string, otherwise return default."""
    return value if isinstance(value, str) else default


def _opt_str(value: object) -> str | None:
    """Return value if it is a string, otherwise return None."""
    return value if isinstance(value, str) else None


def _require_str(section: Mapping[str, object], key: str, label: str) -> str:
    """Return a required non-empty string field."""
    value = section.get(key)
    if not isinstance(value, str) or not value:
        msg = f"theory-reference.toml: {label} must be a non-empty string"
        raise ValueError(msg)
    return value


def _string_list(section: Mapping[str, object], key: str) -> list[str]:
    """Return a string list from a TOML section."""
    value = section.get(key, [])
    if not isinstance(value, list):
        msg = f"theory-reference.toml: {key} must be a list of strings"
        raise TypeError(msg)

    result: list[str] = []
    for item in cast(list[object], value):
        if not isinstance(item, str):
            msg = f"theory-reference.toml: {key} must be a list of strings"
            raise TypeError(msg)
        result.append(item)

    return result


def _string_mapping(
    data: Mapping[str, object],
    section_name: str,
) -> dict[str, str]:
    """Return a string-to-string mapping from a TOML table."""
    section = _section(data, section_name)

    result: dict[str, str] = {}
    for raw_key, raw_value in section.items():
        if not isinstance(raw_value, str):
            msg = (
                f"theory-reference.toml: {section_name} must be a table "
                "of string values"
            )
            raise TypeError(msg)
        result[raw_key] = raw_value

    return result
