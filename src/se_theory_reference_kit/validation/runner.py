"""validation/runner.py - Execute a registry with crash isolation.

The runner is the only place that knows about strict mode and overall outcome.
It runs each selected check, isolates crashes, collects all results, and
computes an exit code.

Strict mode is applied here, not in checks: checks report severity, and the
runner decides whether warning-severity findings fail the run.
"""

from dataclasses import dataclass

from se_theory_reference_kit.base.errors import ReferenceKitError
from se_theory_reference_kit.base.results import (
    CheckResult,
    CheckSeverity,
    CheckStatus,
    cannot_verify,
    worst_status,
)
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.registry import CheckRegistry

__all__ = [
    "EXIT_FAILED",
    "EXIT_OK",
    "RunReport",
    "run_checks",
]

EXIT_OK = 0
EXIT_FAILED = 1


@dataclass(frozen=True, slots=True)
class RunReport:
    """The outcome of running a registry against a context.

    Attributes:
        results: Every finding from every check, in check order.
        strict: Whether the run was executed in strict mode.
        overall_status: Worst status across all results.
    """

    results: tuple[CheckResult, ...]
    strict: bool
    overall_status: CheckStatus

    @property
    def failures(self) -> tuple[CheckResult, ...]:
        """Return results that count as failures for this run's mode.

        Error-severity findings always count. Warning-severity findings count
        only under strict mode. Cannot-verify always counts.
        """
        counted: list[CheckResult] = []

        for result in self.results:
            if result.status == CheckStatus.CANNOT_VERIFY:
                counted.append(result)
                continue

            if result.status == CheckStatus.FAIL and (
                result.severity == CheckSeverity.ERROR or self.strict
            ):
                counted.append(result)

        return tuple(counted)

    @property
    def passed(self) -> bool:
        """Return true when no findings count as failures for this mode."""
        return len(self.failures) == 0

    @property
    def exit_code(self) -> int:
        """Return the process exit code: 0 when passed, 1 otherwise."""
        return EXIT_OK if self.passed else EXIT_FAILED


def run_checks(
    *,
    registry: CheckRegistry,
    context: ReferenceRunContext,
    strict: bool = False,
) -> RunReport:
    """Run selected checks against the context with crash isolation.

    Each check is executed independently. If a check raises ReferenceKitError,
    it is recorded as a cannot-verify result and the run continues. One broken
    check never hides the results of the others.
    """
    collected: list[CheckResult] = []

    for check in registry.select(strict=strict):
        try:
            collected.extend(check.run(context))
        except ReferenceKitError as exc:
            collected.append(
                cannot_verify(
                    check.check_id,
                    f"check could not run: {exc}",
                )
            )

    return RunReport(
        results=tuple(collected),
        strict=strict,
        overall_status=worst_status(collected),
    )
