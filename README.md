# SE Theory: Reference Kit

[![PyPI](https://img.shields.io/pypi/v/se-theory-reference-kit?logo=pypi&label=pypi)](https://pypi.org/project/se-theory-reference-kit/)
[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://structural-explainability.github.io/se-theory-reference-kit/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/structural-explainability/se-theory-reference-kit)
[![Python 3.15](https://img.shields.io/badge/python-3.15%2B-blue?logo=python)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

[![CI-Lean](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/ci-lean.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-theory-reference-kit/actions/workflows/ci-lean.yml)
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

## Package Interface

- The Python import package is `se_theory_reference_kit`.
- The Python distribution package is `se-theory-reference-kit`.
- The public command is `se-theory-reference`.

## Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal

Open a machine terminal where you want the project:

```shell
git clone https://github.com/structural-explainability/se-theory-reference-kit

cd se-theory-reference-kit
code .
```

### In a VS Code terminal

Use VS Code Menu:
View / Command Palette / `Developer: Reload Window` to refresh.

```shell
uv self update
uv python pin 3.15
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install

uv run se-theory-reference --help
uv run se-theory-reference validate --help
uv run se-theory-reference scaffold --help
uv run se-theory-reference export --help
uv run se-theory-reference catalog --help
uv run se-theory-reference inspect --help

# validate manifest file
uvx se-manifest-schema validate-manifest --path SE_MANIFEST.toml --strict

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

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Authority Manifest

[.accountability/surfaces.toml](./.accountability/surfaces.toml)

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)

## Repository Manifest

[SE_MANIFEST.toml](./SE_MANIFEST.toml)
