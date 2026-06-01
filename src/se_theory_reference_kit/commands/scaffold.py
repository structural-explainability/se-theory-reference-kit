"""commands/scaffold.py - Reference scaffold command."""

from argparse import Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from se_theory_reference_kit.commands._context import resolve_command_context


def configure_scaffold_parser(subparsers: _SubParsersAction[Any]) -> None:
    """Configure the scaffold subcommand."""
    parser = subparsers.add_parser(
        "scaffold",
        help="Scaffold missing reference entries from Lean source.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.set_defaults(handler=run_scaffold_command)


def run_scaffold_command(args: Namespace) -> int:
    """Run reference scaffolding."""
    root = None if args.root is None else Path(args.root)
    command_context = resolve_command_context(root=root, load_index=True)

    print(f"repo_root: {command_context.repo_root.as_posix()}")
    print("Reference scaffolding command is wired.")
    print("Scaffold engine extraction is required before entries can be written.")

    if args.dry_run:
        print("mode: dry-run")
    if args.overwrite:
        print("mode: overwrite")

    return 0
