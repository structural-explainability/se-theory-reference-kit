"""docs/tools/generate_api.py - Generate API reference pages for mkdocstrings."""

from pathlib import Path

import mkdocs_gen_files

PACKAGE_NAME = "se_theory_reference_kit"

ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = ROOT / "src"
PACKAGE_ROOT = SRC_ROOT / PACKAGE_NAME

print(f"Generating API reference pages for package '{PACKAGE_NAME}'...")

for source_path in sorted(PACKAGE_ROOT.rglob("*.py")):
    module_path = source_path.relative_to(SRC_ROOT).with_suffix("")
    parts = tuple(module_path.parts)

    if parts[-1] == "__main__":
        continue

    if parts[-1] == "__init__":
        doc_parts = parts[:-1]
        if not doc_parts:
            continue
        doc_path = Path("en/api/reference", *doc_parts, "index.md")
        identifier = ".".join(doc_parts)
    else:
        doc_path = Path("en/api/reference", *parts).with_suffix(".md")
        identifier = ".".join(parts)

    with mkdocs_gen_files.open(doc_path, "w") as file_obj:
        print(f"# `{identifier}`", file=file_obj)
        print(file=file_obj)
        print(f"::: {identifier}", file=file_obj)

    mkdocs_gen_files.set_edit_path(doc_path, source_path.relative_to(ROOT))
    print(f"Generated {doc_path} for {source_path}")
