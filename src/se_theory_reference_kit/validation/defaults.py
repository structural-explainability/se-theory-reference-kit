"""validation/defaults.py - The kit's fixed set of generic checks.

This is the single place that knows which checks the kit ships. registry.py is
pure machinery and imports nothing from checks; individual checks import Check
from registry. defaults.py sits above both, importing the machinery and checks
to assemble the default registry. The dependency arrow is one-way:

    registry  <-  checks  <-  defaults

so there is no cycle, and registry/checks can be reasoned about without knowing
the default set.

Consuming repos build their own registry by extending this one:

    from se_theory_reference_kit.validation.defaults import default_registry

    registry = default_registry().extend(repo_specific_check)

The defaults are never edited by a consumer; extend() returns a new registry.

Default order:
  1. reference.index              reference/index.toml exists and parses
  2. reference.artifacts          declared reference artifacts exist and parse
  3. lean.surface                 declared public surface is covered
  4. exports.current             generated exports are current
  5. structural.strict.no-todo    no unfinished-work markers (strict-only)
"""

from se_theory_reference_kit.validation.checks.export import CHECK as EXPORT_CHECK
from se_theory_reference_kit.validation.checks.lean_surface import (
    CHECK as LEAN_SURFACE_CHECK,
)
from se_theory_reference_kit.validation.checks.reference_artifacts import (
    CHECK as REFERENCE_ARTIFACTS_CHECK,
)
from se_theory_reference_kit.validation.checks.strict import (
    CHECK as STRICT_CHECK,
)
from se_theory_reference_kit.validation.registry import Check, CheckRegistry

__all__ = ["DEFAULT_CHECKS", "default_registry"]

# WHY: ordered foundational-first. reference.index runs first because later
# checks depend on the reference index. strict runs last because it is
# strict-only and least likely to gate routine validation.
DEFAULT_CHECKS: tuple[Check, ...] = (
    REFERENCE_ARTIFACTS_CHECK,
    LEAN_SURFACE_CHECK,
    EXPORT_CHECK,
    STRICT_CHECK,
)


def default_registry() -> CheckRegistry:
    """Return the kit's default registry of generic checks.

    Returns a fresh CheckRegistry each call. Consumers extend it to add
    repo-specific checks; the kit's defaults are never mutated.
    """
    return CheckRegistry(checks=DEFAULT_CHECKS)
