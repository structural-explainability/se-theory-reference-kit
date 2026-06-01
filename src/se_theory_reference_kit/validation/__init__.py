"""validation/__init__.py - Checks, registry, runner, and default check set.

Public surface:
  - Check, CheckRegistry           the check contract and its catalogue
  - CheckResult, CheckStatus, ...  the result vocabulary
  - RunReport, run_checks          execution with crash isolation
  - default_registry, DEFAULT_CHECKS  the kit's fixed generic check set
"""

from se_theory_reference_kit.base.results import (
    CheckResult,
    CheckSeverity,
    CheckStatus,
)
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.defaults import DEFAULT_CHECKS, default_registry
from se_theory_reference_kit.validation.registry import Check, CheckFunc, CheckRegistry
from se_theory_reference_kit.validation.runner import RunReport, run_checks

__all__ = [
    "Check",
    "CheckFunc",
    "CheckRegistry",
    "CheckResult",
    "CheckSeverity",
    "CheckStatus",
    "ReferenceRunContext",
    "RunReport",
    "run_checks",
    "default_registry",
    "DEFAULT_CHECKS",
]
