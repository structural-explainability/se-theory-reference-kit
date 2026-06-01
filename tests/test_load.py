"""tests/test_load.py - Tests for load.py."""

from pathlib import Path

from se_theory_reference_kit.load import (
    load_toml,
)


def test_load_toml(tmp_path: Path) -> None:
    """load_toml reads a valid TOML file."""
    path = tmp_path / "test.toml"
    path.write_text('[section]\nkey = "value"\n', encoding="utf-8")

    result = load_toml(path)

    assert result["section"]["key"] == "value"
