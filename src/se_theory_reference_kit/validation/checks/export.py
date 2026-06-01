"""validation/checks/exports.py - Validate generated export freshness."""

from collections.abc import Iterable

from se_theory_reference_kit.base.results import CheckResult, failure, ok, partial
from se_theory_reference_kit.declarations.index import reference_artifacts
from se_theory_reference_kit.export.engine import export_registries
from se_theory_reference_kit.reference.registry import build_reference_registry
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.registry import Check

__all__ = ["CHECK_ID", "check_exports", "CHECK"]

CHECK_ID = "exports.current"


def check_exports(context: ReferenceRunContext) -> Iterable[CheckResult]:
    """Verify generated exports are current without writing files."""
    if context.reference_index is None:
        return [partial(CHECK_ID, "reference index not loaded")]

    if not context.export_specs:
        return [partial(CHECK_ID, "no export specs declared")]

    namespace = (
        context.config.reference_namespace
        or f"se.{context.config.artifact_slug.replace('-', '_')}"
    )

    declarations = reference_artifacts(context.reference_index)
    registry = build_reference_registry(
        declarations,
        root=context.repo_root,
        reference_dir_name=context.config.reference_dir_name,
    )

    results = export_registries(
        specs=context.export_specs,
        registry=registry,
        reference_root=context.reference_root,
        output_root=context.generated_root,
        repo_slug=context.config.repo_slug,
        reference_namespace=namespace,
        check=True,
    )

    stale = [result for result in results if not result.current]

    if stale:
        return [
            failure(
                CHECK_ID,
                "generated export is stale",
                path=result.output_path,
            )
            for result in stale
        ]

    return [ok(CHECK_ID, "generated exports are current")]


CHECK = Check(
    check_id=CHECK_ID,
    title="Generated exports are current",
    run=check_exports,
)
