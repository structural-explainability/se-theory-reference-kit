"""reference/validation.py - Generic reference artifact shape validation."""

from collections.abc import Iterable

from se_theory_reference_kit.base.results import CheckResult, failure, ok
from se_theory_reference_kit.reference.artifacts import LoadedReferenceArtifact
from se_theory_reference_kit.reference.registry import section_entries

REQUIRED_ENTRY_FIELDS: tuple[str, ...] = (
    "lean_symbol",
    "lean_kind",
    "source_module",
)


def validate_required_fields(
    *,
    check_id: str,
    artifact: LoadedReferenceArtifact,
    section: str,
    required_fields: Iterable[str] = REQUIRED_ENTRY_FIELDS,
) -> tuple[CheckResult, ...]:
    """Validate required fields for all entries in one reference section.

    Args:
        check_id: Validation check id.
        artifact: Loaded reference artifact.
        section: Section name.
        required_fields: Required field names.

    Returns:
        Validation findings.
    """
    findings: list[CheckResult] = []
    required = tuple(required_fields)

    for entry_id, entry in section_entries(artifact.data, section).items():
        for field_name in required:
            value = entry.get(field_name)
            if not isinstance(value, str) or not value:
                findings.append(
                    failure(
                        check_id,
                        f"{section}.{entry_id} missing required field {field_name!r}",
                        artifact_id=artifact.artifact_id,
                        path=artifact.path,
                        detail={"section": section, "entry_id": entry_id},
                    )
                )

    return tuple(findings)


def validate_reference_artifact_shape(
    *,
    check_id: str,
    artifact: LoadedReferenceArtifact,
) -> tuple[CheckResult, ...]:
    """Validate generic reference artifact shape.

    Args:
        check_id: Validation check id.
        artifact: Loaded reference artifact.

    Returns:
        Validation findings.
    """
    if not artifact.kind:
        return (
            failure(
                check_id,
                "reference artifact declaration has no kind",
                artifact_id=artifact.artifact_id,
                path=artifact.path,
            ),
        )

    return (
        ok(
            check_id,
            "reference artifact has generic TOML shape",
            artifact_id=artifact.artifact_id,
            path=artifact.path,
        ),
    )
