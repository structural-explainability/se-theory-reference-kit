"""commands/root.py - Root command dispatcher for se-theory-reference."""

from argparse import ArgumentParser, Namespace
from collections.abc import Callable, Sequence

from se_theory_reference_kit.commands.catalog import configure_catalog_parser
from se_theory_reference_kit.commands.export import configure_export_parser
from se_theory_reference_kit.commands.inspect import configure_inspect_parser
from se_theory_reference_kit.commands.scaffold import configure_scaffold_parser
from se_theory_reference_kit.commands.validate import configure_validate_parser

CommandHandler = Callable[[Namespace], int]


def build_parser() -> ArgumentParser:
    """Build the root argument parser."""
    parser = ArgumentParser(
        prog="se-theory-reference",
        description="Reference tooling for Structural Explainability theory repos.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root or path inside the target repository.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    configure_validate_parser(subparsers)
    configure_scaffold_parser(subparsers)
    configure_export_parser(subparsers)
    configure_catalog_parser(subparsers)
    configure_inspect_parser(subparsers)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the combined command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 2

    return int(handler(args))
