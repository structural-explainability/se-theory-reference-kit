"""commands/export.py - Generated export command."""

from argparse import Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from se_theory_reference_kit.commands._context import resolve_command_context
from se_theory_reference_kit.declarations.index import reference_artifacts
from se_theory_reference_kit.export.engine import export_registries
from se_theory_reference_kit.reference.registry import build_reference_registry


def configure_export_parser(subparsers: _SubParsersAction[Any]) -> None:
    """Configure the export subcommand."""
    parser = subparsers.add_parser(
        "export",
        help="Export generated data artifacts from reference artifacts.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether generated artifacts are current without writing.",
    )
    parser.set_defaults(handler=run_export_command)


def run_export_command(args: Namespace) -> int:
    """Run generated export or export freshness check."""
    root = None if args.root is None else Path(args.root)
    command_context = resolve_command_context(root=root, load_index=True)

    if command_context.reference_index is None:
        msg = "reference index was not loaded"
        raise RuntimeError(msg)

    artifact_declarations = reference_artifacts(command_context.reference_index)
    registry = build_reference_registry(
        artifact_declarations,
        root=command_context.repo_root,
        reference_dir_name=command_context.config.reference_dir_name,
    )

    namespace = (
        command_context.config.reference_namespace
        or f"se.{command_context.config.artifact_slug.replace('-', '_')}"
    )

    results = export_registries(
        specs=command_context.export_specs,
        registry=registry,
        reference_root=command_context.repo_root
        / command_context.config.reference_dir_name,
        output_root=command_context.repo_root
        / command_context.config.generated_data_dir,
        repo_slug=command_context.config.repo_slug,
        reference_namespace=namespace,
        check=bool(args.check),
    )

    if all(result.current for result in results):
        if args.check:
            print("Reference exports are current.")
        else:
            print("Reference export completed.")
        return 0

    print("Reference exports are stale.")
    return 1
