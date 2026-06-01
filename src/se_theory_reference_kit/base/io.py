"""base/io.py - UTF-8 text and TOML loading helpers."""

from pathlib import Path
import tomllib

from se_theory_reference_kit.base.errors import ArtifactLoadError, ArtifactWriteError

TomlDocument = dict[str, object]


def read_text(path: Path) -> str:
    """Read a UTF-8 text file.

    Args:
        path: File path.

    Returns:
        File contents.

    Raises:
        ArtifactLoadError: If the file cannot be read.
    """
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        msg = f"Unable to read text file: {path}"
        raise ArtifactLoadError(msg) from exc


def write_text(path: Path, content: str) -> None:
    """Write a UTF-8 text file, creating parent directories if needed.

    Args:
        path: Output path.
        content: Text content.

    Raises:
        ArtifactWriteError: If the file cannot be written.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        msg = f"Unable to write text file: {path}"
        raise ArtifactWriteError(msg) from exc


def load_toml(path: Path) -> TomlDocument:
    """Load a TOML file.

    Args:
        path: TOML file path.

    Returns:
        Parsed TOML document.

    Raises:
        ArtifactLoadError: If the file cannot be read or parsed.
    """
    try:
        with path.open("rb") as file_obj:
            data = tomllib.load(file_obj)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        msg = f"Unable to read TOML file: {path}"
        raise ArtifactLoadError(msg) from exc

    return data
