"""commands/catalog.py - Reference catalog command."""

from argparse import Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from se_theory_reference_kit.base.json_utils import encode_json, write_or_check_text
from se_theory_reference_kit.commands._context import resolve_command_context
from se_theory_reference_kit.declarations.index import reference_artifacts
from se_theory_reference_kit.export.catalog import build_reference_catalog
from se_theory_reference_kit.reference.registry import build_reference_registry


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
    command_context = resolve_command_context(root=root, load_index=True)

    if command_context.reference_index is None:
        msg = "reference index was not loaded"
        raise RuntimeError(msg)

    catalog_schema = command_context.config.catalog_schema
    catalog_artifact_name = command_context.config.catalog_artifact_name
    namespace = (
        command_context.config.reference_namespace
        or f"se.{command_context.config.artifact_slug.replace('-', '_')}"
    )

    if catalog_schema is None:
        msg = "repo-owned config must declare CATALOG_SCHEMA for catalog export"
        raise RuntimeError(msg)

    if catalog_artifact_name is None:
        msg = "repo-owned config must declare CATALOG_ARTIFACT_NAME for catalog export"
        raise RuntimeError(msg)

    artifact_declarations = reference_artifacts(command_context.reference_index)
    registry = build_reference_registry(
        artifact_declarations,
        root=command_context.repo_root,
        reference_dir_name=command_context.config.reference_dir_name,
    )

    payload = build_reference_catalog(
        registry=registry,
        schema=catalog_schema,
        source=command_context.config.repo_slug,
        namespace=namespace,
        artifact=catalog_artifact_name,
    )

    output_path = (
        command_context.repo_root
        / command_context.config.generated_data_dir
        / f"{catalog_artifact_name}.json"
    )

    current = write_or_check_text(
        output_path,
        encode_json(payload),
        check=bool(args.check),
    )

    if current:
        if args.check:
            print("Reference catalog is current.")
        else:
            print("Reference catalog completed.")
        return 0

    print("Reference catalog is stale.")
    return 1
