"""validation/checks/reference_artifacts.py - Validate declared reference artifacts."""

from collections.abc import Iterable
from pathlib import Path

from se_theory_reference_kit.base.results import CheckResult, failure, ok, partial
from se_theory_reference_kit.reference.artifacts import ArtifactDeclaration
from se_theory_reference_kit.reference.registry import build_reference_registry
from se_theory_reference_kit.reference.validation import (
    validate_reference_artifact_shape,
)
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.registry import Check

__all__ = ["CHECK_ID", "check_reference_artifacts", "CHECK"]

CHECK_ID = "reference.artifacts"


def check_reference_artifacts(context: ReferenceRunContext) -> Iterable[CheckResult]:
    """Verify declared reference artifacts exist, parse, and have generic shape."""
    declarations = _artifact_declarations_from_context(context)
    if not declarations:
        return [partial(CHECK_ID, "no reference artifacts declared")]

    findings: list[CheckResult] = []

    for declaration in declarations:
        raw_rel_path = declaration.get("path")
        raw_artifact_id = declaration.get("id")

        artifact_id = raw_artifact_id if isinstance(raw_artifact_id, str) else None

        if not isinstance(raw_rel_path, str) or not raw_rel_path:
            findings.append(
                failure(
                    CHECK_ID,
                    "artifact declaration path must be a nonempty string",
                    artifact_id=artifact_id,
                )
            )
            continue

        rel_path = raw_rel_path
        path = context.reference_root / rel_path
        if not path.is_file():
            findings.append(
                failure(
                    CHECK_ID,
                    "declared reference artifact does not exist",
                    artifact_id=artifact_id,
                    path=path,
                )
            )

    if findings:
        return findings

    registry = build_reference_registry(
        declarations,
        root=context.repo_root,
        reference_dir_name=context.config.reference_dir_name,
    )

    for artifact in registry.artifacts:
        findings.extend(
            validate_reference_artifact_shape(
                check_id=CHECK_ID,
                artifact=artifact,
            )
        )

    if not findings:
        findings.append(ok(CHECK_ID, "all declared reference artifacts load"))

    return findings


def _artifact_declarations_from_context(
    context: ReferenceRunContext,
) -> list[ArtifactDeclaration]:
    """Build artifact declarations from configured surface-kind sources."""
    declarations: list[ArtifactDeclaration] = []

    for kind, source in context.config.surface_kind_sources.items():
        declarations.append(
            {
                "id": kind,
                "path": Path(source).name,
            }
        )

    return declarations


CHECK = Check(
    check_id=CHECK_ID,
    title="Declared reference artifacts exist and parse",
    run=check_reference_artifacts,
)
