# SE Theory: Reference Kit

[![PyPI](https://img.shields.io/pypi/v/se-theory-reference-kit?logo=pypi&label=pypi)](https://pypi.org/project/se-theory-reference-kit/)
[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://structural-explainability.github.io/se-theory-reference-kit/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/structural-explainability/se-theory-reference-kit)
[![Python 3.15](https://img.shields.io/badge/python-3.15%2B-blue?logo=python)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

[![CI](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/ci-python-zensical.yml)
[![Docs-Deploy](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/deploy-zensical.yml)
[![Pre-Release](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/pre-release.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/pre-release.yml)
[![Release](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/release-pypi.yml/badge.svg)](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/release-pypi.yml)
[![Links](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/links.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/links.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://github.com/structural-explainability/se-theory-reference-kit/security)

> Shared Python engine for validating, scaffolding, and exporting
> Structural Explainability theory-reference artifacts
> that mirror Lean public surfaces.

For the full documentation, see [`docs/en/index.md`](./docs/en/index.md).

## Overview

This project provides the shared Python infrastructure used by
Structural Explainability theory repositories
to maintain reference artifacts aligned with their Lean public surfaces.

The kit owns generic loading, validation, scaffolding, and export machinery.
Each theory repository owns its own public Lean surface
declarations and export specifications.

## Install

```shell
uv add se-theory-reference-kit
uv sync
```

## Usage

```shell
uvx se-theory-reference-kit@latest export
uvx se-theory-reference-kit@latest export --check
uvx se-theory-reference-kit@latest catalog
uvx se-theory-reference-kit@latest catalog --check
uvx se-theory-reference-kit@latest inspect
uvx se-theory-reference-kit@latest validate
uvx se-theory-reference-kit@latest validate --strict
```

## Developer

### Clone Project Repository and Open in VS Code

Open a machine terminal where you want the project:

```shell
git clone https://github.com/structural-explainability/se-theory-reference-kit

cd se-theory-reference-kit
code .
```

### Manage Environment

Use VS Code Menu:
View / Command Palette / `Developer: Reload Window` to refresh.

```shell
# set up or update Python environment
# uvx pup-clean --delete
uv self update
uv python install
uv lock --upgrade
uv sync
uv audit

# set up and run git hooks
uv run prek install --force
uv run prek update
git add -A
uv run prek run --all-files
# repeat if changes were made
uv run prek run --all-files

# Check
uv run se-theory-reference-kit@latest export --help
uv run se-theory-reference-kit@latest catalog --help
uv run se-theory-reference-kit@latest inspect --help
uv run se-theory-reference-kit@latest validate --help

# run common chores
uv run ruff format .
uv run ruff check . --fix
uv run ty check
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

## Authority Manifest

[.accountability/surfaces.toml](./.accountability/surfaces.toml)

## Changelog

[CHANGELOG.md](./CHANGELOG.md)

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)

## Repository Manifest

[SE_MANIFEST.toml](./SE_MANIFEST.toml)
