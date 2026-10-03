# Architecture

`se-theory-reference-kit` is a shared engine for theory-reference workflows in
Structural Explainability theory repositories.

The package is designed around a strict ownership boundary:

```text
theory repository owns theory declarations
shared kit owns generic repository mechanics
```

## Architectural Boundary

The kit is not a theory repository.
It does not define Lean semantics and does
not decide whether a formal statement is correct.

The kit provides reusable Python infrastructure that can inspect repository
state, compare declarations, validate synchronization, generate derived
artifacts, and expose those operations through a stable command surface.

## Repo-Provided Configuration

A theory repository provides `reference/theory-reference.toml` and its
repo-owned reference artifacts.

Those files describe repository identity, the public Lean root, mapped
reference surfaces, and generated export specifications.

The kit loads repository-provided configuration and reference artifacts into
typed internal objects and uses them to drive generic operations.

The configuration and reference artifacts remain owned by the theory
repository.

## Reference Workflow

The reference workflow has this general shape:

```text
repo-owned Lean source
  -> repo-owned theory-reference configuration
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

## Command Layer

The command layer owns argument parsing and orchestration.

Command modules delegate to engine modules.
They do not own validation logic, export construction,
reference artifact semantics, or Lean declaration semantics.

## Documentation Model

Human-authored documentation describes architecture, workflow, and ownership
boundaries.

Generated API documentation mirrors the Python source tree during documentation
builds.
Generated API pages are not hand-maintained.

## Dependency Direction

Dependency direction should remain inward from orchestration toward reusable
engine modules.

Engine modules must not import command modules.

Repo-specific theory configuration and reference content must not be moved into
the shared kit.
