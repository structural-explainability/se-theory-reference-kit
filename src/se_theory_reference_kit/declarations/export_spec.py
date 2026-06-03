"""declarations/export_spec.py - Repo-owned generated export specification shape."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Self, cast


@dataclass(frozen=True, slots=True)
class ExportSpec:
    """A generated JSON artifact export specification."""

    source_name: str
    source_table: str
    output_name: str
    schema: str
    payload_key: str

    @classmethod
    def specs_from_toml(cls, data: Mapping[str, object]) -> tuple[Self, ...]:
        """Build export specs by joining [surface_kinds] and [export_map].

        Kit-owned convention for each non-catalog kind present in both maps:
            source_table = kind
            payload_key  = kind
            schema       = f"se-theory-{artifact_slug}-{kind}-registry"
        """
        repository = _section(data, "repository")
        surface_kinds = _string_mapping(data, "surface_kinds")
        export_map = _string_mapping(data, "export_map")

        slug = repository.get("theory")
        if not isinstance(slug, str) or not slug:
            return ()

        specs: list[Self] = []
        for kind, source in surface_kinds.items():
            output = export_map.get(kind)
            if output is None:
                continue

            specs.append(
                cls(
                    source_name=Path(source).name,
                    source_table=kind,
                    output_name=Path(output).name,
                    schema=f"se-theory-{slug}-{kind}-registry",
                    payload_key=kind,
                )
            )

        return tuple(specs)


def _section(data: Mapping[str, object], name: str) -> dict[str, object]:
    """Return a TOML section as a plain string-keyed mapping."""
    value = data.get(name, {})
    if not isinstance(value, Mapping):
        return {}

    section = cast(Mapping[object, object], value)

    result: dict[str, object] = {}
    for key, item in section.items():
        if isinstance(key, str):
            result[key] = item

    return result


def _string_mapping(
    data: Mapping[str, object],
    section_name: str,
) -> dict[str, str]:
    """Return a string-to-string mapping from a TOML table."""
    section = _section(data, section_name)

    result: dict[str, str] = {}
    for raw_key, raw_value in section.items():
        if isinstance(raw_value, str):
            result[raw_key] = raw_value

    return result
