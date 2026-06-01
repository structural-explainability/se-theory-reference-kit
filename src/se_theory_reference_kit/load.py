"""load.py - Loading and parsing for se-theory-neutral-substrate.

Owns:
  - load_toml()             - read any TOML file
  - load_manifest_schema()  - read manifest-schema.toml

Does not own validation logic.
Validation belongs in orchestrate.py and validate_reference.py.
"""

from pathlib import Path
import tomllib
from typing import Any


def load_toml(path: Path) -> dict[str, Any]:
    """Load and return TOML data from the specified path."""
    return tomllib.loads(path.read_text(encoding="utf-8"))
