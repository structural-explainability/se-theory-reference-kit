"""commands/export.py - Generated export command."""

from argparse import Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from se_theory_reference_kit.commands._context import resolve_command_context
from se_theory_reference_kit.export.engine import export_registries
from se_theory_reference_kit.reference.registry import build_registry_from_config


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
    raw_root = getattr(args, "root", None)
    root = None if raw_root is None else Path(raw_root)

    command_context = resolve_command_context(root=root)

    registry = build_registry_from_config(
        command_context.repo_root,
        command_context.config,
    )

    namespace = _reference_namespace(command_context.config)

    reference_root = (
        command_context.repo_root / command_context.config.reference_dir_name
    )
    output_root = command_context.repo_root / command_context.config.generated_data_dir

    results = export_registries(
        specs=command_context.export_specs,
        registry=registry,
        reference_root=reference_root,
        output_root=output_root,
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


def _reference_namespace(config: Any) -> str:
    """Return configured reference namespace or derived default."""
    namespace = getattr(config, "reference_namespace", None)
    if isinstance(namespace, str) and namespace:
        return namespace

    artifact_slug = getattr(config, "artifact_slug", "theory")
    if not isinstance(artifact_slug, str) or not artifact_slug:
        artifact_slug = "theory"

    return f"se.{artifact_slug.replace('-', '_')}"
