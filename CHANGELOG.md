# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.1.0] - 2026-06-01

### Added

- Initial `se-theory-reference-kit` Python package.
- Shared declaration models for theory-reference configuration, public Lean
  surface declarations, and generated export specifications.
- Generic repository path, TOML loading, JSON encoding, and reference artifact
  helpers.
- Generic Lean source inspection helpers for module paths, declarations, spec
  identifiers, and public-surface coverage comparison.
- Generic reference registry, stub, validation, export, and catalog helpers.
- Immutable validation check registry and runner for generic theory-reference
  checks.
- Namespaced public command surface through `se-theory-reference`.
- Generated Python API documentation support.
- Release validation procedure for package, documentation, manifest, import
  boundary, complexity, and distribution checks.

---

## Notes on versioning and releases

- We use **SemVer**:
  - **MAJOR** - breaking changes
  - **MINOR** - backward-compatible changes
  - **PATCH** - fixes, documentation, tooling
- Versions are driven by git tags. Tag `vX.Y.Z` to release.
- Docs are deployed per version tag and aliased to **latest**.

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. CITATION.cff: update version and date-released
1.2. CHANGELOG.md: add section, move unreleased entries, update links
1.3. pyproject.toml: update build fallback-version (near end of the file)

### Task 2. Validate

```shell
uv sync --extra dev --extra docs --upgrade

uv run se-theory-reference --help
uv run se-theory-reference validate --help
uv run se-theory-reference scaffold --help
uv run se-theory-reference export --help
uv run se-theory-reference catalog --help
uv run se-theory-reference inspect --help

uvx --from se-manifest-schema se-manifest validate-manifest --path SE_MANIFEST.toml --strict

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
uvx pre-commit run --all-files

uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# check import layers
uvx --python 3.13 --from import-linter lint-imports --config .github/.importlinter

# check complexity; no output is good (all A or B)
uvx radon cc src/se_theory_reference_kit -s -a -n C

uv build
uvx twine check dist/*
```

### Task 3. Commit, push, and tag

```shell
git add -A
git commit -m "Prep X.Y.Z"
git push -u origin main
```

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

### Task 4. After tagging, verify tag consistency

```shell
uvx --from se-manifest-schema se-manifest check-version --require-tag
```

Confirms CITATION.cff version matches the pushed git tag.
Run this after `git push origin vX.Y.Z`; it will fail before that point.

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/structural-explainability/se-theory-reference-kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/structural-explainability/se-theory-reference-kit/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->
