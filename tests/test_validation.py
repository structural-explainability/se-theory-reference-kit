"""tests/test_validation.py - Validation registry and runner tests."""

from collections.abc import Iterable
from pathlib import Path

import pytest

from se_theory_reference_kit.base import (
    CheckResult,
    CheckSeverity,
    CheckStatus,
    failure,
    ok,
)
from se_theory_reference_kit.base.errors import ReferenceKitError
from se_theory_reference_kit.declarations.config import TheoryReferenceConfig
from se_theory_reference_kit.declarations.surface import SurfaceSymbols
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.registry import Check, CheckRegistry
from se_theory_reference_kit.validation.runner import run_checks


def make_context(tmp_path: Path) -> ReferenceRunContext:
    """Create a minimal validation context."""
    root = tmp_path / "repo"
    root.mkdir()
    return ReferenceRunContext(
        repo_root=root,
        config=TheoryReferenceConfig(
            repo_slug="se-example",
            artifact_slug="example",
            lean_public_root="SE.Example",
        ),
        surface=SurfaceSymbols(),
    )


def test_check_registry_rejects_duplicate_ids() -> None:
    """Check registries reject duplicate check ids."""
    check = Check(
        check_id="example",
        title="Example",
        run=lambda _context: (),
    )

    with pytest.raises(ValueError):
        CheckRegistry(checks=(check, check))


def test_check_registry_extend_returns_new_registry() -> None:
    """Extending a registry does not mutate the original."""
    check = Check(
        check_id="example",
        title="Example",
        run=lambda _context: (),
    )
    registry = CheckRegistry()
    extended = registry.extend(check)

    assert registry.ids() == ()
    assert extended.ids() == ("example",)


def test_check_registry_select_skips_strict_checks_when_not_strict() -> None:
    """Strict-only checks run only in strict mode."""
    routine = Check(
        check_id="routine",
        title="Routine",
        run=lambda _context: (),
    )
    strict = Check(
        check_id="strict",
        title="Strict",
        run=lambda _context: (),
        strict_only=True,
    )
    registry = CheckRegistry(checks=(routine, strict))

    assert [check.check_id for check in registry.select(strict=False)] == ["routine"]
    assert [check.check_id for check in registry.select(strict=True)] == [
        "routine",
        "strict",
    ]


def test_run_checks_collects_results(tmp_path: Path) -> None:
    """Runner collects check results and computes pass status."""
    context = make_context(tmp_path)

    def run_ok(_context: ReferenceRunContext) -> Iterable[CheckResult]:
        return (ok("ok-check", "passed"),)

    registry = CheckRegistry(
        checks=(
            Check(
                check_id="ok-check",
                title="OK check",
                run=run_ok,
            ),
        )
    )

    report = run_checks(registry=registry, context=context)

    assert report.passed
    assert report.exit_code == 0
    assert report.overall_status == CheckStatus.OK


def test_run_checks_treats_warnings_as_failures_only_under_strict(
    tmp_path: Path,
) -> None:
    """Warning-severity failures fail only in strict mode."""
    context = make_context(tmp_path)

    def run_warning(_context: ReferenceRunContext) -> Iterable[CheckResult]:
        return (
            CheckResult(
                check_id="warning-check",
                status=CheckStatus.FAIL,
                severity=CheckSeverity.WARNING,
                message="warning",
            ),
        )

    registry = CheckRegistry(
        checks=(
            Check(
                check_id="warning-check",
                title="Warning check",
                run=run_warning,
            ),
        )
    )

    routine = run_checks(registry=registry, context=context, strict=False)
    strict = run_checks(registry=registry, context=context, strict=True)

    assert routine.passed
    assert not strict.passed


def test_run_checks_isolates_reference_kit_errors(tmp_path: Path) -> None:
    """Runner turns operational check failures into cannot-verify results."""
    context = make_context(tmp_path)

    def run_broken(_context: ReferenceRunContext) -> Iterable[CheckResult]:
        msg = "broken input"
        raise ReferenceKitError(msg)

    registry = CheckRegistry(
        checks=(
            Check(
                check_id="broken-check",
                title="Broken check",
                run=run_broken,
            ),
        )
    )

    report = run_checks(registry=registry, context=context)

    assert not report.passed
    assert report.results[0].status == CheckStatus.CANNOT_VERIFY
    assert report.exit_code == 1


def test_failure_helper_uses_typed_detail() -> None:
    """Failure helper stores structured detail."""
    result = failure(
        "example",
        "failed",
        detail={"field": "value"},
    )

    assert result.detail == {"field": "value"}
