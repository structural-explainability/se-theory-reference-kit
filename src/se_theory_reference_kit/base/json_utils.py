"""base/json_utils.py - Deterministic JSON helpers."""

import json
from pathlib import Path
from typing import Any

from se_theory_reference_kit.base.io import write_text

JsonObject = dict[str, Any]


def encode_json(payload: JsonObject) -> str:
    """Encode a JSON payload deterministically.

    The payload builder owns ordering. This encoder preserves insertion order
    rather than sorting keys.

    Args:
        payload: JSON-compatible object.

    Returns:
        Encoded JSON text ending with a newline.
    """
    return (
        json.dumps(
            payload,
            indent=2,
            sort_keys=False,
            ensure_ascii=True,
        )
        + "\n"
    )


def write_or_check_text(path: Path, content: str, *, check: bool) -> bool:
    """Write a file or check whether it is current.

    Returns true when the file is current or was written.
    Returns false when check mode finds stale content.

    Args:
        path: Output path.
        content: Expected file content.
        check: If true, check freshness without writing.

    Returns:
        True when current or written, otherwise false.
    """
    if check:
        if not path.exists():
            print(f"[stale] {path.as_posix()} is missing")
            return False

        current = path.read_text(encoding="utf-8")
        if current != content:
            print(f"[stale] {path.as_posix()} is out of date")
            return False

        print(f"[ok   ] {path.as_posix()}")
        return True

    write_text(path, content)
    print(f"[write] {path.as_posix()}")
    return True


def write_or_check_json(path: Path, payload: JsonObject, *, check: bool) -> bool:
    """Write a JSON payload or check whether the file is current.

    Args:
        path: Output path.
        payload: JSON payload.
        check: If true, check freshness without writing.

    Returns:
        True when current or written, otherwise false.
    """
    return write_or_check_text(path, encode_json(payload), check=check)
