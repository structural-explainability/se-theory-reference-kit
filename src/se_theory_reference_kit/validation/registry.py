"""validation/registry.py - Check registry and consumer extension hook.

The kit provides a fixed set of default generic checks. Consuming theory
repositories append repo-specific checks to that set without modifying the kit.
The kit's defaults are never edited by a consumer; they are extended.

This is the seam that lets one shared engine serve every theory repository
without forking. Immutability enforces it: extend() returns a new registry with
the added checks appended, so a consumer cannot mutate the kit's defaults in
place.
"""

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Self

from se_theory_reference_kit.base.results import CheckResult
from se_theory_reference_kit.validation.context import ReferenceRunContext

__all__ = [
    "CheckFunc",
    "Check",
    "CheckRegistry",
]

# A check reads the resolved context and yields findings. It never mutates the
# context and never raises for a failed check. Failed checks are CheckResult
# objects. Operational failures are isolated by the runner.
type CheckFunc = Callable[[ReferenceRunContext], Iterable[CheckResult]]


@dataclass(frozen=True, slots=True)
class Check:
    """A registered check: a function plus its catalogue metadata.

    Attributes:
        check_id: Stable, unique id.
        title: Short human-readable description for logs and reports.
        run: The check function.
        strict_only: When true, the check runs only in strict mode.
    """

    check_id: str
    title: str
    run: CheckFunc
    strict_only: bool = False


@dataclass(frozen=True, slots=True)
class CheckRegistry:
    """An immutable, ordered collection of checks.

    Order is preserved so runs are deterministic and the default generic checks
    always precede consumer-appended checks. Ids must be unique across the
    registry.
    """

    checks: tuple[Check, ...] = ()

    def __post_init__(self) -> None:
        """Reject duplicate check ids at construction time."""
        seen: set[str] = set()
        duplicates: list[str] = []

        for check in self.checks:
            if check.check_id in seen:
                duplicates.append(check.check_id)
            seen.add(check.check_id)

        if duplicates:
            joined = ", ".join(sorted(set(duplicates)))
            msg = f"duplicate check ids in registry: {joined}"
            raise ValueError(msg)

    def extend(self, *checks: Check) -> Self:
        """Return a new registry with the given checks appended.

        The kit's defaults are never mutated; a consumer extends them. The
        returned registry preserves order and re-validates id uniqueness, so a
        consumer cannot shadow a default id.
        """
        return type(self)(checks=(*self.checks, *checks))

    def extended_with(self, checks: Iterable[Check]) -> Self:
        """Return a new registry appending an iterable of checks."""
        return self.extend(*tuple(checks))

    def ids(self) -> tuple[str, ...]:
        """Return the check ids in order."""
        return tuple(check.check_id for check in self.checks)

    def select(self, *, strict: bool) -> Sequence[Check]:
        """Return the checks that should run for the given mode.

        In non-strict mode, strict-only checks are skipped. In strict mode, all
        checks run.
        """
        if strict:
            return self.checks

        return tuple(check for check in self.checks if not check.strict_only)
