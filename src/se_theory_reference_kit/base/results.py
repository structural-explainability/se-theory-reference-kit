"""validation/results.py - Result vocabulary for theory-reference checks."""

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

type JsonDetail = dict[str, object]

__all__ = [
    "CheckResult",
    "CheckSeverity",
    "CheckStatus",
    "JsonDetail",
    "cannot_verify",
    "failure",
    "ok",
    "partial",
    "warning",
    "worst_status",
]


def empty_detail() -> JsonDetail:
    """Return an empty result detail dictionary."""
    return {}


class CheckStatus(StrEnum):
    """Status vocabulary for one validation finding."""

    OK = "ok"
    PARTIAL = "partial"
    FAIL = "fail"
    CANNOT_VERIFY = "cannot-verify"


class CheckSeverity(StrEnum):
    """Severity vocabulary for one validation finding."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class CheckResult:
    """One validation finding emitted by one check.

    Attributes:
        check_id: Stable id of the check that emitted the finding.
        status: Check status.
        severity: Finding severity.
        message: Human-readable finding message.
        artifact_id: Optional artifact id associated with the finding.
        path: Optional path associated with the finding.
        detail: Optional structured detail for reports or downstream tooling.
    """

    check_id: str
    status: CheckStatus
    severity: CheckSeverity
    message: str
    artifact_id: str | None = None
    path: Path | None = None
    detail: JsonDetail = field(default_factory=empty_detail)


def ok(
    check_id: str,
    message: str,
    *,
    artifact_id: str | None = None,
    path: Path | None = None,
    detail: JsonDetail | None = None,
) -> CheckResult:
    """Create an ok result."""
    return CheckResult(
        check_id=check_id,
        status=CheckStatus.OK,
        severity=CheckSeverity.INFO,
        message=message,
        artifact_id=artifact_id,
        path=path,
        detail={} if detail is None else detail,
    )


def partial(
    check_id: str,
    message: str,
    *,
    artifact_id: str | None = None,
    path: Path | None = None,
    detail: JsonDetail | None = None,
) -> CheckResult:
    """Create a partial result."""
    return CheckResult(
        check_id=check_id,
        status=CheckStatus.PARTIAL,
        severity=CheckSeverity.WARNING,
        message=message,
        artifact_id=artifact_id,
        path=path,
        detail={} if detail is None else detail,
    )


def warning(
    check_id: str,
    message: str,
    *,
    artifact_id: str | None = None,
    path: Path | None = None,
    detail: JsonDetail | None = None,
) -> CheckResult:
    """Create a warning failure result."""
    return CheckResult(
        check_id=check_id,
        status=CheckStatus.FAIL,
        severity=CheckSeverity.WARNING,
        message=message,
        artifact_id=artifact_id,
        path=path,
        detail={} if detail is None else detail,
    )


def failure(
    check_id: str,
    message: str,
    *,
    artifact_id: str | None = None,
    path: Path | None = None,
    detail: JsonDetail | None = None,
) -> CheckResult:
    """Create an error failure result."""
    return CheckResult(
        check_id=check_id,
        status=CheckStatus.FAIL,
        severity=CheckSeverity.ERROR,
        message=message,
        artifact_id=artifact_id,
        path=path,
        detail={} if detail is None else detail,
    )


def cannot_verify(
    check_id: str,
    message: str,
    *,
    artifact_id: str | None = None,
    path: Path | None = None,
    detail: JsonDetail | None = None,
) -> CheckResult:
    """Create a cannot-verify result."""
    return CheckResult(
        check_id=check_id,
        status=CheckStatus.CANNOT_VERIFY,
        severity=CheckSeverity.ERROR,
        message=message,
        artifact_id=artifact_id,
        path=path,
        detail={} if detail is None else detail,
    )


def worst_status(results: Iterable[CheckResult]) -> CheckStatus:
    """Return the worst status across validation results."""
    rank = {
        CheckStatus.OK: 0,
        CheckStatus.PARTIAL: 1,
        CheckStatus.FAIL: 2,
        CheckStatus.CANNOT_VERIFY: 3,
    }

    worst = CheckStatus.OK
    for result in results:
        if rank[result.status] > rank[worst]:
            worst = result.status

    return worst
