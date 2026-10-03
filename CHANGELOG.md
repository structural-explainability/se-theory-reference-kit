# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.4.0] - 2026-10-03

### Added

- Added a shared `repo_relative_path` helper for converting internal filesystem
  paths to repository-relative POSIX paths at generated-artifact boundaries.
- Added regression coverage verifying repository-relative paths in generated
  registry JSON and aggregate reference catalogs.
- Added generated-file regression coverage confirming exported reference paths
  remain portable after serialization.

### Changed

- Updated generated registry exports to receive the repository root explicitly
  and serialize source reference paths relative to that root.
- Updated generated reference catalogs to serialize loaded reference-artifact
  paths relative to the repository root.
- Kept absolute `Path` objects for internal filesystem operations while making
  committed generated metadata repository-relative and platform-independent.
- Updated package metadata and development documentation to match the current
  Python 3.15, `uv`, `prek`, Ruff, `ty`, pytest, and Zensical workflow.
- Updated repository-manifest terminology to describe configuration-driven
  theory-reference loading rather than the removed index-based model.
- Updated manifest validation commands to use the published
  `se-manifest-schema` command surface.
- Simplified release metadata maintenance so package versions remain derived
  from Git tags.
- Added `se-theory-reference-kit` as the primary CLI executable so the
  published package can be run directly with
  `uvx se-theory-reference-kit@latest`.
- Retained `se-theory-reference` as a backward-compatible command alias.

### Removed

- Removed the Hatch VCS fallback version so distribution builds fail rather
  than silently use a stale version when valid Git version metadata is
  unavailable.
- Removed stale project-template configuration that referenced unrelated
  coverage targets, warning filters, and research-project directories.
- Removed stale `pre-commit` and Pyright development instructions in favor of
  `prek` and `ty`.

### Fixed

- Fixed generated registry JSON leaking absolute machine-specific filesystem
  paths through `reference_path`.
- Fixed generated reference catalogs leaking absolute machine-specific
  filesystem paths through `reference_paths` and
  `reference_artifacts[].path`.
- Fixed generated reference metadata so the same committed artifacts are
  reproducible across Windows, Linux, CI, and differently located repository
  clones.
- Fixed tests and command wiring to propagate the repository root through both
  registry-export and catalog-export paths.
- Fixed package test coverage configuration to target
  `src/se_theory_reference_kit/`.

---

## [0.3.1] - 2026-07-29

### Fixed

- Preserved repository-relative reference artifact paths from
  `reference/theory-reference.toml`.
- Fixed reference registry construction so configured artifact paths resolve
  through the shared repository path helpers.
- Fixed reference artifact validation to preserve artifact kinds and configured
  repository-relative paths.
- Fixed strict unfinished-work validation to inspect the configured reference
  artifact paths without reducing them to basenames.
- Fixed public Lean surface extraction to load configured reference artifacts
  through the shared path-resolution layer.
- Added regression tests for artifact kinds, repository-relative paths, public
  Lean symbol extraction, strict validation paths, and export-root-relative
  filenames.

---

## [0.3.0] - 2026-07-29

### Added

- Added Python 3.15 project, typing, testing, and release support.
- Added fail-fast PowerShell release validation through `rel.ps1`.
- Added validation coverage for configuration-derived reference artifact kinds
  and registered Lean symbol names.

### Changed

- Made `rel.ps1` the authoritative local release-validation procedure.
- Updated the release workflow, documentation, package metadata, and lock file
  for the `0.3.0` release.
- Updated reference artifact loading to treat mapped artifact paths consistently
  relative to the configured `reference/` directory.
- Updated Lean public-surface validation to compare registered `lean_symbol`
  values rather than human-readable display names.

### Fixed

- Fixed reference artifact path resolution when configuration-derived
  declarations provide paths relative to the configured reference directory.
- Fixed configuration-derived artifact declarations so the `surface_kinds`
  mapping key is preserved as the loaded artifact `kind`.
- Fixed cascading `reference.artifacts` failures caused by loaded artifacts
  receiving an empty kind.
- Fixed cascading `lean.surface` failures caused by display names such as
  `Neutrality by design` being compared with actual Lean declaration names.
- Fixed reference validation for repositories whose public Lean root is a
  top-level module such as `SE`.
- Fixed native-command error handling in the PowerShell release procedure so
  validation stops immediately when a command exits unsuccessfully.

---

## [0.2.0] - 2026-06-03

### Added

- Added data-driven theory-reference configuration through
  `reference/theory-reference.toml`.
- Added typed declaration loading for repository identity, Lean public surface
  mapping, reference artifact layout, export targets, and validation commands.
- Added config-driven reference registry construction from mapped reference
  artifacts.
- Added artifact-derived public surface construction so public symbols are read
  from reference artifacts rather than duplicated in Python constants.
- Added stable shared command surface for:
  - `se-theory-reference validate`
  - `se-theory-reference validate --strict`
  - `se-theory-reference scaffold`
  - `se-theory-reference scaffold --dry-run`
  - `se-theory-reference scaffold --overwrite`
  - `se-theory-reference export`
  - `se-theory-reference export --check`
  - `se-theory-reference catalog`
  - `se-theory-reference catalog --check`
  - `se-theory-reference inspect`

### Changed

- Reworked validation commands to use the shared `RunReport` returned by the
  validation runner.
- Reworked export, inspect, validation, and reference-artifact checks to use the
  config-driven model instead of `reference/index.toml`.
- Replaced index-based reference discovery with `surface_kinds` and `export_map`
  declarations from `reference/theory-reference.toml`.
- Clarified that Lean source remains authoritative for formal declarations,
  while reference artifacts are authoritative for repo-owned classification,
  traceability, and export intent.
- Simplified theory repository integration so client theory repos can run
  `uv run se-theory-reference ...` directly without repo-local Python wrappers.

### Removed

- Removed dependence on the old `reference/index.toml` model.
- Removed stale imports and command paths that referenced
  `se_theory_reference_kit.declarations.index`.
- Removed hard-coded repo-specific public symbol sets from the shared kit design.
- Removed old `load_index` command-context behavior.

### Fixed

- Fixed Pyright and Ruff issues caused by stale index-based architecture.
- Fixed command help import failures caused by removed declaration modules.
- Fixed validation result handling so command exit status is delegated to the
  validation runner.
- Fixed type narrowing in TOML configuration and export-spec loading.
- Fixed reference, strict, Lean-surface, export, and inspect checks to consume
  typed config and registry boundaries.

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
  - \*_MAJOR_- - breaking changes
  - \*_MINOR_- - backward-compatible changes
  - \*_PATCH_- - fixes, documentation, tooling
- Versions are driven by git tags. Tag `vX.Y.Z` to release.
- Docs are deployed per version tag and aliased to **latest**.

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. CITATION.cff: update version and date-released
1.2. CHANGELOG.md: add section, move unreleased entries, update links

### Task 2. Validate

From PowerShell at the repository root:

```pwsh
# set up or update Python environment
.\sit.ps1

# Update GitHub Actions and pin all action references to immutable SHAs.
uvx gha-tools autoupdate --pin=all --write .github/workflows

# Audit the resulting GitHub configuration for security findings.
uvx zizmor@latest .github/

# Validate.
uvx cffconvert --validate
uvx se-manifest-schema validate-manifest --strict

# check complexity; no output is good (all A or B)
uvx radon cc src/se_theory_reference_kit -s -a -n C

# Check local command surface.
uv run se-theory-reference-kit --help
uv run se-theory-reference-kit validate --help
uv run se-theory-reference-kit scaffold --help
uv run se-theory-reference-kit export --help
uv run se-theory-reference-kit catalog --help
uv run se-theory-reference-kit inspect --help

uv build
uvx twine check dist/*
```

Proceed when the script completes successfully.

### Task 3. Commit, push, and tag

```shell
git add -A
git commit -m "Prepare X.Y.Z"
git push -u origin main
```

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

### Task 4. After tagging, verify tag consistency

```shell
uvx se-manifest-schema check-version --require-tag
```

Confirms CITATION.cff version matches the pushed git tag.
Run this after `git push origin vX.Y.Z`; it will fail before that point.

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/structural-explainability/se-theory-reference-kit/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/structural-explainability/se-theory-reference-kit/releases/tag/v0.4.0
[0.3.1]: https://github.com/structural-explainability/se-theory-reference-kit/releases/tag/v0.3.1
[0.3.0]: https://github.com/structural-explainability/se-theory-reference-kit/releases/tag/v0.3.0
[0.2.0]: https://github.com/structural-explainability/se-theory-reference-kit/releases/tag/v0.2.0
[0.1.0]: https://github.com/structural-explainability/se-theory-reference-kit/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->
