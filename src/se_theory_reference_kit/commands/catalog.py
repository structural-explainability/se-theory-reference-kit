"""commands/catalog.py - Reference catalog command."""

from argparse import Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from se_theory_reference_kit.base.json_utils import encode_json, write_or_check_text
from se_theory_reference_kit.commands._context import resolve_command_context
from se_theory_reference_kit.export.catalog import build_reference_catalog
from se_theory_reference_kit.reference.registry import build_registry_from_config


def configure_catalog_parser(subparsers: _SubParsersAction[Any]) -> None:
    """Configure the catalog subcommand."""
    parser = subparsers.add_parser(
        "catalog",
        help="Build the generated reference catalog.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether the generated catalog is current without writing.",
    )
    parser.set_defaults(handler=run_catalog_command)


def run_catalog_command(args: Namespace) -> int:
    """Run generated catalog export or freshness check."""
    root = None if args.root is None else Path(args.root)
    command_context = resolve_command_context(root=root)
    config = command_context.config

    if config.catalog_artifact_name is None:
        msg = (
            "theory-reference.toml must declare [export_map].catalog for catalog export"
        )
        raise RuntimeError(msg)
    if config.catalog_schema is None:
        msg = "theory-reference.toml must resolve a catalog schema for catalog export"
        raise RuntimeError(msg)

    namespace = (
        config.reference_namespace or f"se.{config.artifact_slug.replace('-', '_')}"
    )

    registry = build_registry_from_config(command_context.repo_root, config)

    payload = build_reference_catalog(
        registry=registry,
        schema=config.catalog_schema,
        source=config.repo_slug,
        namespace=namespace,
        artifact=config.catalog_artifact_name,
    )

    output_path = (
        command_context.repo_root
        / config.generated_data_dir
        / f"{config.catalog_artifact_name}.json"
    )

    current = write_or_check_text(
        output_path,
        encode_json(payload),
        check=bool(args.check),
    )

    if current:
        print(
            "Reference catalog is current."
            if args.check
            else "Reference catalog completed."
        )
        return 0

    print("Reference catalog is stale.")
    return 1
