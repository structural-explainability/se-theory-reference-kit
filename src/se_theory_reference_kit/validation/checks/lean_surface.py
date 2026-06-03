"""validation/checks/lean_surface.py - Validate reference coverage of Lean surface."""

from collections.abc import Iterable

from se_theory_reference_kit.base.results import CheckResult, failure, ok, partial
from se_theory_reference_kit.lean.surface import missing_expected_surface_symbols
from se_theory_reference_kit.reference.registry import (
    build_registry_from_config,
    registered_lean_symbols,
)
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.registry import Check

__all__ = ["CHECK_ID", "check_lean_surface", "CHECK"]

CHECK_ID = "lean.surface"


def check_lean_surface(context: ReferenceRunContext) -> Iterable[CheckResult]:
    """Verify expected public Lean symbols appear in reference artifacts."""
    expected = context.surface.all_symbols
    if not expected:
        return [partial(CHECK_ID, "no public surface symbols declared")]

    registry = build_registry_from_config(context.repo_root, context.config)
    registered = registered_lean_symbols(registry)
    missing = missing_expected_surface_symbols(
        surface=context.surface,
        registered=registered,
    )

    if missing:
        return [
            failure(
                CHECK_ID,
                f"expected public Lean symbol is not registered: {symbol}",
                detail={"lean_symbol": symbol},
            )
            for symbol in sorted(missing)
        ]

    return [
        ok(
            CHECK_ID,
            f"all {len(expected)} expected public Lean symbols are registered",
        )
    ]


CHECK = Check(
    check_id=CHECK_ID,
    title="Public Lean surface is covered by reference artifacts",
    run=check_lean_surface,
)
