"""validation/checks/export.py - Validate generated export freshness."""

from collections.abc import Iterable

from se_theory_reference_kit.base.results import CheckResult, failure, ok, partial
from se_theory_reference_kit.export.engine import export_registries
from se_theory_reference_kit.reference.registry import build_registry_from_config
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.registry import Check

__all__ = ["CHECK_ID", "check_exports_current", "CHECK"]

CHECK_ID = "reference.exports"


def check_exports_current(context: ReferenceRunContext) -> Iterable[CheckResult]:
    """Verify generated export artifacts are current."""
    if not context.export_specs:
        return [partial(CHECK_ID, "no export specs declared")]

    registry = build_registry_from_config(context.repo_root, context.config)
    namespace = _reference_namespace(context)

    results = export_registries(
        specs=context.export_specs,
        registry=registry,
        reference_root=context.repo_root / context.config.reference_dir_name,
        output_root=context.repo_root / context.config.generated_data_dir,
        repo_slug=context.config.repo_slug,
        reference_namespace=namespace,
        check=True,
    )

    findings: list[CheckResult] = []
    for result in results:
        if not result.current:
            artifact_id = result.output_path.name

            findings.append(
                failure(
                    CHECK_ID,
                    "generated export artifact is stale",
                    artifact_id=artifact_id,
                    path=result.output_path,
                )
            )

    if findings:
        return findings

    return [ok(CHECK_ID, "generated export artifacts are current")]


def _reference_namespace(context: ReferenceRunContext) -> str:
    """Return configured reference namespace or derived default."""
    if context.config.reference_namespace:
        return context.config.reference_namespace

    return f"se.{context.config.artifact_slug.replace('-', '_')}"


CHECK = Check(
    check_id=CHECK_ID,
    title="Generated export artifacts are current",
    run=check_exports_current,
)
