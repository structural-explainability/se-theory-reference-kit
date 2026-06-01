# Architecture

`se-theory-reference-kit` is a shared engine for theory-reference workflows in
Structural Explainability theory repositories.

The package is designed around a strict ownership boundary:

```text
theory repository owns theory declarations
shared kit owns generic repository mechanics
```

## Architectural boundary

The kit is not a theory repository.
It does not define Lean semantics and does
not decide whether a formal statement is correct.

The kit provides reusable Python infrastructure that can inspect repository
state, compare declarations, validate synchronization, generate derived
artifacts, and expose those operations through a stable command surface.

## Repo-provided declarations

A theory repository provides typed declarations that describe its local
reference-tooling contract.

Those declarations identify the repository, its public Lean root, its public
surface symbols, and its generated export specifications.

The kit loads those declarations, validates their shape, and uses them to drive
generic operations.
The declarations remain owned by the theory repository.

## Reference workflow

The reference workflow has this general shape:

```text
repo-owned Lean source
  -> repo-owned public surface declaration
  -> repo-owned reference artifacts
  -> shared validation and inspection
  -> generated exports and catalogs
```

The generated artifacts are derived from repo-owned inputs.
They are not an independent semantic authority.

## Validation model

Validation is organized around an immutable check registry.

The kit provides generic checks that apply across supported theory repositories.
A consuming repository may extend the default registry with repo-specific
checks, but it does not mutate the kit's defaults.

Validation checks synchronization, structure, freshness, and coverage.
It does not establish formal truth or semantic correctness.

## Command layer

The command layer owns argument parsing and orchestration.

Command modules delegate to engine modules.
They do not own validation logic, export construction,
reference artifact semantics, or Lean declaration semantics.

## Documentation model

Human-authored documentation describes architecture, workflow, and ownership
boundaries.

Generated API documentation mirrors the Python source tree during documentation
builds.
Generated API pages are not hand-maintained.

## Dependency direction

The dependency direction should remain one-way:

```text
commands
  -> declarations
  -> lean
  -> reference
  -> export
  -> validation
  -> base
```

Engine modules should not import command modules.

Repo-specific theory declarations should not be moved into the shared kit.
