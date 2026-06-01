"""validation/checks/reference_index.py - Validate the reference index."""

from collections.abc import Iterable

from se_theory_reference_kit.base.io import load_toml
from se_theory_reference_kit.base.results import CheckResult, failure, ok
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.registry import Check

__all__ = ["CHECK_ID", "check_reference_index", "CHECK"]

CHECK_ID = "reference.index"


def check_reference_index(context: ReferenceRunContext) -> Iterable[CheckResult]:
    """Verify the reference index exists and parses."""
    path = context.reference_index_path

    if not path.is_file():
        return [
            failure(
                CHECK_ID,
                "reference index does not exist",
                path=path,
            )
        ]

    load_toml(path)

    return [
        ok(
            CHECK_ID,
            "reference index exists and parses",
            path=path,
        )
    ]


CHECK = Check(
    check_id=CHECK_ID,
    title="Reference index exists and parses",
    run=check_reference_index,
)
