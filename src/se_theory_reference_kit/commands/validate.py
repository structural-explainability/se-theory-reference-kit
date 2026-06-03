"""commands/validate.py - Validation command."""

from argparse import Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from se_theory_reference_kit.commands._context import resolve_command_context
from se_theory_reference_kit.validation.context import ReferenceRunContext
from se_theory_reference_kit.validation.defaults import default_registry
from se_theory_reference_kit.validation.runner import run_checks


def configure_validate_parser(subparsers: _SubParsersAction[Any]) -> None:
    """Configure the validate subcommand."""
    parser = subparsers.add_parser(
        "validate",
        help="Validate reference artifacts against declared Lean public surface.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Run strict validation checks.",
    )
    parser.set_defaults(handler=run_validate_command)


def run_validate_command(args: Namespace) -> int:
    """Run validation checks."""
    raw_root = getattr(args, "root", None)
    root = None if raw_root is None else Path(raw_root)

    command_context = resolve_command_context(root=root)

    context = ReferenceRunContext(
        repo_root=command_context.repo_root,
        config=command_context.config,
        surface=command_context.surface,
        export_specs=command_context.export_specs,
    )

    registry = default_registry()
    report = run_checks(
        registry=registry,
        context=context,
        strict=bool(args.strict),
    )

    for result in report.results:
        print(f"[{result.check_id}] {result.status.value}  {result.message}")

    return report.exit_code
