"""commands/validate.py - Repository validation command."""

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
        help="Validate theory-reference artifacts.",
    )
    parser.add_argument("--strict", action="store_true")
    parser.set_defaults(handler=run_validate_command)


def run_validate_command(args: Namespace) -> int:
    """Run theory-reference validation."""
    root = None if args.root is None else Path(args.root)
    command_context = resolve_command_context(root=root, load_index=True)

    validation_context = ReferenceRunContext(
        repo_root=command_context.repo_root,
        config=command_context.config,
        surface=command_context.surface,
        export_specs=command_context.export_specs,
        reference_index=command_context.reference_index,
    )

    report = run_checks(
        registry=default_registry(),
        context=validation_context,
        strict=bool(args.strict),
    )

    for result in report.results:
        artifact = f" [{result.artifact_id}]" if result.artifact_id else ""
        path = f" {result.path.as_posix()}" if result.path else ""
        print(
            f"{result.status.value.upper()} "
            f"{result.check_id}{artifact}{path}: {result.message}"
        )

    return report.exit_code
