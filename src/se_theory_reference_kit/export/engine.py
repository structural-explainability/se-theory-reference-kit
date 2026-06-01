"""export/engine.py - Generic generated JSON export engine."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from se_theory_reference_kit.base.json_utils import encode_json, write_or_check_text
from se_theory_reference_kit.declarations.export_spec import ExportSpec
from se_theory_reference_kit.reference.artifacts import (
    ReferenceDocument,
    ordered_table_values,
    reference_artifact_meta,
)
from se_theory_reference_kit.reference.registry import ReferenceRegistry

type JsonObject = dict[str, Any]


@dataclass(frozen=True, slots=True)
class ExportResult:
    """Result of one generated export operation.

    Attributes:
        output_path: Generated output path.
        current: True when output is current or was written.
        wrote: True when output was written.
        checked: True when the operation ran in check mode.
    """

    output_path: Path
    current: bool
    wrote: bool
    checked: bool


def build_registry_payload(
    *,
    spec: ExportSpec,
    document: ReferenceDocument,
    source_path: Path,
    repo_slug: str,
    reference_namespace: str,
) -> JsonObject:
    """Build one generated registry payload from one reference artifact.

    Args:
        spec: Repo-owned export specification.
        document: Parsed reference artifact.
        source_path: Source reference artifact path.
        repo_slug: Owning repository slug.
        reference_namespace: Reference namespace for generated payloads.

    Returns:
        JSON-compatible generated registry payload.
    """
    meta = reference_artifact_meta(document)
    entries = ordered_table_values(document, spec.source_table)

    return {
        "schema": spec.schema,
        "source": meta.get("source", repo_slug),
        "namespace": meta.get("namespace", reference_namespace),
        "artifact": spec.output_name.removesuffix(".json"),
        "reference_artifact": meta.get(
            "artifact",
            spec.source_name.removesuffix(".toml"),
        ),
        "reference_path": source_path.as_posix(),
        spec.payload_key: entries,
    }


def export_registry(
    *,
    spec: ExportSpec,
    registry: ReferenceRegistry,
    reference_root: Path,
    output_root: Path,
    repo_slug: str,
    reference_namespace: str,
    check: bool,
) -> ExportResult:
    """Export one registry JSON artifact.

    Args:
        spec: Repo-owned export specification.
        registry: Loaded reference registry.
        reference_root: Reference artifact root.
        output_root: Generated output root.
        repo_slug: Owning repository slug.
        reference_namespace: Reference namespace.
        check: If true, check freshness without writing.

    Returns:
        Export result.

    Raises:
        FileNotFoundError: If the source artifact is not loaded in the registry.
    """
    source_path = reference_root / spec.source_name

    source_artifact = next(
        (
            artifact
            for artifact in registry.artifacts
            if artifact.path.resolve() == source_path.resolve()
        ),
        None,
    )

    if source_artifact is None:
        msg = f"export source artifact not loaded: {source_path}"
        raise FileNotFoundError(msg)

    payload = build_registry_payload(
        spec=spec,
        document=source_artifact.data,
        source_path=source_path,
        repo_slug=repo_slug,
        reference_namespace=reference_namespace,
    )

    output_path = output_root / spec.output_name
    content = encode_json(payload)
    current = write_or_check_text(output_path, content, check=check)

    return ExportResult(
        output_path=output_path,
        current=current,
        wrote=current and not check,
        checked=check,
    )


def export_registries(
    *,
    specs: tuple[ExportSpec, ...],
    registry: ReferenceRegistry,
    reference_root: Path,
    output_root: Path,
    repo_slug: str,
    reference_namespace: str,
    check: bool,
) -> tuple[ExportResult, ...]:
    """Export generated registry JSON artifacts.

    Args:
        specs: Repo-owned export specifications.
        registry: Loaded reference registry.
        reference_root: Reference artifact root.
        output_root: Generated output root.
        repo_slug: Owning repository slug.
        reference_namespace: Reference namespace.
        check: If true, check freshness without writing.

    Returns:
        Export results.
    """
    return tuple(
        export_registry(
            spec=spec,
            registry=registry,
            reference_root=reference_root,
            output_root=output_root,
            repo_slug=repo_slug,
            reference_namespace=reference_namespace,
            check=check,
        )
        for spec in specs
    )
