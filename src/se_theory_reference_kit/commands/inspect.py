"""commands/inspect.py - Inspect resolved theory-reference declarations."""

from argparse import Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from se_theory_reference_kit.commands._context import resolve_command_context
from se_theory_reference_kit.reference.registry import build_registry_from_config


def configure_inspect_parser(subparsers: _SubParsersAction[Any]) -> None:
    """Configure the inspect subcommand."""
    parser = subparsers.add_parser(
        "inspect",
        help="Inspect resolved theory-reference declarations.",
    )
    parser.set_defaults(handler=run_inspect_command)


def run_inspect_command(args: Namespace) -> int:
    """Inspect the resolved command context."""
    raw_root = getattr(args, "root", None)
    root = None if raw_root is None else Path(raw_root)

    command_context = resolve_command_context(root=root)
    config = command_context.config

    print(f"repo_root: {command_context.repo_root.as_posix()}")
    print(f"repo_slug: {config.repo_slug}")
    print(f"artifact_slug: {config.artifact_slug}")
    print(f"lean_public_root: {config.lean_public_root}")
    print(f"reference_dir: {config.reference_dir_name}")
    print(f"generated_data_dir: {config.generated_data_dir}")

    print("surface_kind_sources:")
    for kind, source in sorted(config.surface_kind_sources.items()):
        print(f"  {kind}: {source}")

    registry = build_registry_from_config(
        command_context.repo_root,
        config,
    )
    print(f"loaded_artifacts: {len(registry.artifacts)}")

    print("surface_symbols:")
    for kind, symbols in sorted(command_context.surface.by_kind.items()):
        print(f"  {kind}: {len(symbols)}")

    print(f"export_specs: {len(command_context.export_specs)}")
    for spec in command_context.export_specs:
        print(f"  {spec.source_name} -> {spec.output_name}")

    return 0
