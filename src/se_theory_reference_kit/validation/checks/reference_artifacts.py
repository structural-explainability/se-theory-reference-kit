"""validation/checks/reference_artifacts.py - Validate declared reference artifacts."""

from collections.abc import Iterable

from se_theory_reference_kit.base.results import CheckResult, failure, ok, partial
from se_theory_reference_kit.declarations.index import reference_artifacts
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
    if context.reference_index is None:
        return [partial(CHECK_ID, "reference index not loaded")]

    declarations = reference_artifacts(context.reference_index)
    if not declarations:
        return [partial(CHECK_ID, "no reference artifacts declared")]

    findings: list[CheckResult] = []

    for declaration in declarations:
        rel_path = declaration.get("path")
        artifact_id = str(declaration.get("id", "<unnamed>"))

        if not isinstance(rel_path, str) or not rel_path:
            findings.append(
                failure(
                    CHECK_ID,
                    "artifact declaration path must be a nonempty string",
                    artifact_id=artifact_id,
                )
            )
            continue

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


CHECK = Check(
    check_id=CHECK_ID,
    title="Declared reference artifacts exist and parse",
    run=check_reference_artifacts,
)
