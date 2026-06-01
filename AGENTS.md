# AGENTS.md (SE Theory Reference Kit)

## Contract Mode

Work in contract-first mode.

Do not recommend temporary fixes unless explicitly requested.
Do not introduce "for now" architecture.
Do not simplify in ways that create later reversal across repositories.
Build always with the end in mind.

Before recommending a change, identify:

1. the owner of the responsibility,
2. the public contract surface,
3. the dependency direction,
4. the release target,
5. whether the change scales across all theory repositories,
6. whether the change creates future churn.

## Release Target

These repositories target the current SE release train.

Python 3.15 is an accepted release target for the Dec 31 SE release.
Do not downgrade the Python target because current tooling lags.
The canonical Python version is defined in `.python-version`.

If an API, command, dependency, or entry point fails, first determine the intended
durable surface. Then update the implementation to match that surface.

## Scope

Changes must preserve:

- determinism,
- cross-platform compatibility,
- data-driven definitions,
- explicit and inspectable structure.

Do not introduce hidden logic where declarative structure is possible.

## Theory Constraints

This repository provides shared Python tooling for the
formal theory layer of Structural Explainability.

Lean files are the authoritative source of all formal definitions, predicates,
relations, classifications, and theorems.

Do not introduce:

- runtime application behavior,
- operational validation pipelines,
- contract artifact generation,
- semantic validation outside Lean,
- Python command surfaces that define correctness.

## Python Tooling Constraints

Python may provide repository tooling for:

- reference registry scaffolding,
- reference registry validation,
- reference registry export/checking,
- manifest metadata synchronization,
- documentation generation,
- repository hygiene,
- lightweight automation.

Python must not be the authority for formal theory semantics.

Lean remains authoritative for:

- definitions,
- predicates,
- relations,
- classifications,
- theorems,
- proof obligations.

Python tooling may check that declared reference data and repository metadata are
well-formed and synchronized with expected files. It must not introduce a
parallel semantic system or define correctness independently of Lean.

## Lean Public Surface

Each theory repository must expose a stable Lean import root.

The public import root is part of the repository contract.
Internal modules may change only when the public root continues to provide the
declared theory surface.

Use the SE namespace policy consistently:

- generic or collision-prone theory roots use `SE.*`,
- distinctive theory roots may remain bare,
- package names and import roots may differ,
- Lake dependency names must match package names.

Do not rename public imports without treating the change as a public contract
change across dependent repositories.

## Documentation Constraints

Documentation is descriptive only.

Documentation must mirror the Lean module structure and terminology.
Documentation must not:

- redefine formal semantics,
- introduce new definitions,
- encode invariants not present in Lean,
- diverge from Lean naming.

If documentation and Lean differ, Lean is correct.

## Requirements

- Use `uv` for all Python environment and tooling commands.
- Do not recommend or use `pip install ...` as the primary workflow.
- Commands must work on Windows, macOS, and Linux.
- Use Python-native or cross-platform tooling in scripts.
- Avoid shell syntax that only works on one operating system.

## Quickstart

```shell
uv self update
uv python pin 3.15
uv sync --extra dev --extra docs --upgrade
```

## Lint and Format

```shell
uv run python -m ruff format .
uv run python -m ruff check . --fix
```

## Build Documentation

```shell
uv run python -m zensical build
```

## pre-commit

pre-commit runs only on tracked or staged files.
Use `git add -A` before expecting hooks to run on newly created files.

```shell
uvx pre-commit run --all-files
```

## Non-goals

Theory repositories do not define:

- identity-regime execution behavior,
- operational validation pipelines,
- domain mappings,
- runtime systems,
- contract artifact exports,
- interpretation semantics,
- application data models.

Those responsibilities belong to downstream SE repositories.
