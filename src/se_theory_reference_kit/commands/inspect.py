"""commands/inspect.py - Inspect resolved theory-reference declarations."""

from argparse import Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from se_theory_reference_kit.commands._context import resolve_command_context
from se_theory_reference_kit.declarations.index import (
    reference_artifacts,
    surface_module,
)
from se_theory_reference_kit.reference.registry import build_reference_registry


def configure_inspect_parser(subparsers: _SubParsersAction[Any]) -> None:
    """Configure the inspect subcommand."""
    parser = subparsers.add_parser(
        "inspect",
        help="Inspect resolved reference-tool declarations.",
    )
    parser.set_defaults(handler=run_inspect_command)


def run_inspect_command(args: Namespace) -> int:
    """Inspect the resolved command context."""
    root = None if args.root is None else Path(args.root)
    command_context = resolve_command_context(root=root, load_index=True)

    print(f"repo_root: {command_context.repo_root.as_posix()}")
    print(f"repo_slug: {command_context.config.repo_slug}")
    print(f"artifact_slug: {command_context.config.artifact_slug}")
    print(f"lean_public_root: {command_context.config.lean_public_root}")
    print(f"reference_dir: {command_context.config.reference_dir_name}")
    print(f"generated_data_dir: {command_context.config.generated_data_dir}")

    if command_context.reference_index is None:
        return 0

    print(f"surface_module: {surface_module(command_context.reference_index)}")

    artifact_declarations = reference_artifacts(command_context.reference_index)
    print(f"reference_artifacts: {len(artifact_declarations)}")
    for artifact in artifact_declarations:
        print(
            "  "
            f"{artifact.get('id', '<unnamed>')} "
            f"{artifact.get('kind', '<unknown-kind>')} "
            f"{artifact.get('path', '<no-path>')}"
        )

    registry = build_reference_registry(
        artifact_declarations,
        root=command_context.repo_root,
        reference_dir_name=command_context.config.reference_dir_name,
    )
    print(f"loaded_artifacts: {len(registry.artifacts)}")

    print("surface_symbols:")
    for kind, symbols in sorted(command_context.surface.by_kind.items()):
        print(f"  {kind}: {len(symbols)}")

    print(f"export_specs: {len(command_context.export_specs)}")
    for spec in command_context.export_specs:
        print(f"  {spec.source_name} -> {spec.output_name}")

    return 0
