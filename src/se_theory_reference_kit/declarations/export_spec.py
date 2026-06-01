"""declarations/export_spec.py - Repo-owned generated export specification shape."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExportSpec:
    """A generated JSON artifact export specification.

    The kit owns this model shape. Each theory repository owns the tuple of
    export specifications.
    """

    source_name: str
    source_table: str
    output_name: str
    schema: str
    payload_key: str
