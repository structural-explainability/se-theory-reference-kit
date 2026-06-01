"""validation/checks/strict.py - Strict-only unfinished-work marker check."""

from collections.abc import Iterable

from se_theory_reference_kit.base.io import read_text
from se_theory_reference_kit.base.results import CheckResult, failure, ok, partial
from se_theory_reference_kit.declarations.index import reference_artifacts
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.registry import Check

__all__ = ["CHECK_ID", "TODO_MARKERS", "check_strict_no_todo", "CHECK"]

CHECK_ID = "structural.strict.no-todo"

TODO_MARKERS: tuple[str, ...] = ("TODO", "FIXME", "XXX")


def _markers_in_text(text: str) -> list[str]:
    """Return unfinished-work markers present as standalone tokens."""
    upper = text.upper()
    found: list[str] = []

    for marker in TODO_MARKERS:
        index = upper.find(marker)
        while index != -1:
            before = upper[index - 1] if index > 0 else ""
            after_index = index + len(marker)
            after = upper[after_index] if after_index < len(upper) else ""

            if not before.isalnum() and not after.isalnum():
                found.append(marker)
                break

            index = upper.find(marker, index + 1)

    return found


def check_strict_no_todo(context: ReferenceRunContext) -> Iterable[CheckResult]:
    """Verify reference artifacts contain no unfinished-work markers."""
    if context.reference_index is None:
        return [partial(CHECK_ID, "reference index not loaded")]

    findings: list[CheckResult] = []

    for declaration in reference_artifacts(context.reference_index):
        artifact_id = str(declaration.get("id", "<unnamed>"))
        rel_path = declaration.get("path")

        if not isinstance(rel_path, str) or not rel_path:
            continue

        path = context.reference_root / rel_path
        if path.suffix.lower() not in {".toml", ".json", ".md"}:
            continue

        if not path.is_file():
            continue

        markers = _markers_in_text(read_text(path))
        if markers:
            findings.append(
                failure(
                    CHECK_ID,
                    "reference artifact contains unfinished-work marker(s): "
                    + ", ".join(sorted(set(markers))),
                    artifact_id=artifact_id,
                    path=path,
                )
            )

    if not findings:
        findings.append(
            ok(CHECK_ID, "no unfinished-work markers in reference artifacts")
        )

    return findings


CHECK = Check(
    check_id=CHECK_ID,
    title="No TODO/FIXME markers in reference artifacts",
    run=check_strict_no_todo,
    strict_only=True,
)
