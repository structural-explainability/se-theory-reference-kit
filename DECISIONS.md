# DECISIONS

<!-- markdownlint-disable MD024 -->

Architectural decisions for `se-theory-reference-kit`.

This document records current load-bearing decisions, rationale, and consequences.

---

## TRK-D-0001: The kit owns the generic theory-reference engine only

### Date recorded

2026-06-01

### Decision

`se-theory-reference-kit` owns reusable Python machinery and model contracts
for loading, scaffolding, validating, inspecting, cataloging, and exporting
theory-reference artifacts that mirror Lean public surfaces.

### Rationale

The five Structural Explainability theory repositories need shared tooling, but
their public Lean surfaces and export specifications remain repo-specific
contract material.

Moving repo-specific declarations into the kit would make the generic engine own
theory content and would create cross-repository churn whenever a theory surface
changes.

### Consequences

- The kit provides generic models, loaders, validators, scaffolders, exporters,
  and command plumbing.
- Theory repositories provide a declarative `reference/theory-reference.toml`
  and their reference artifacts.
- The kit loads repo-provided declarations but must not hard-code symbols from
  neutral substrate, transformation, identity regimes, persistence, or
  structural explainability.

---

## TRK-D-0002: Repo-specific declarations remain in each theory repository

### Date recorded

2026-06-01

### Decision

Each theory repository owns its own public Lean surface, reference layout, and
export specifications.

Lean source is the source of truth for formal declarations.
`reference/*.toml` is the source of truth for repo-owned classification,
traceability, and export intent.
Generated JSON is an output, not an authority source.

The shared kit consumes those declarations through stable, typed declaration
models loaded from repository data.

### Rationale

A public Lean surface is part of the theory repository's public contract.
The export specifications are also repo-specific because they name the artifacts
that a particular theory repository chooses to publish.

Centralizing those declarations in the kit would make the kit a hidden authority
over theory-repository public surfaces.

### Consequences

- Public symbol sets and export specifications do not live in
  `se-theory-reference-kit`.
- They live in each theory repository, in its reference artifacts and its
  `reference/theory-reference.toml`.
- Adding or removing theory symbols is a change in the owning theory repository,
  not in the kit.

---

## TRK-D-0003: Python 3.15 is the v1 release target

### Date recorded

2026-06-01

### Decision

`se-theory-reference-kit` targets Python 3.15 for the December 2026 v1 release
train.

The canonical version is owned by `.python-version` and `pyproject.toml`.

### Rationale

The v1 release follows Python 3.15 final. This greenfield package should target
the intended release runtime rather than an older compatibility baseline.

### Consequences

- Tooling must align with the canonical Python version.
- Tooling parser lag may be handled in tool configuration without changing the
  package runtime contract.

---

## TRK-D-0004: The public command surface is one namespaced command

### Date recorded

2026-06-01

### Decision

The package exposes one public command:

```shell
se-theory-reference
```

Repository-specific theory packages may delegate to this command, but they should
not reimplement reference validation, scaffolding, export, catalog, or inspection
logic.

The shared command surface includes:

```shell
se-theory-reference validate
se-theory-reference validate --strict

se-theory-reference scaffold
se-theory-reference scaffold --dry-run
se-theory-reference scaffold --overwrite

se-theory-reference export
se-theory-reference export --check

se-theory-reference catalog
se-theory-reference catalog --check

se-theory-reference inspect
```

### Rationale

A single namespaced command gives all theory repositories the same operational
surface while keeping repo-specific declarations in data.

Duplicating commands in each theory repository would recreate the local-tooling
drift that the kit exists to eliminate.

### Consequences

- Theory repositories may expose thin compatibility wrappers, but wrappers must
  delegate to `se-theory-reference-kit`.
- New reference operations are added to the kit command surface first.
- Repository-specific Python command logic is avoided unless it addresses a
  genuinely repo-specific concern outside the generic reference workflow.

---

## TRK-D-0005: Reference validation is synchronization validation, not semantic validation

### Date recorded

2026-06-01

### Decision

The kit validates that reference artifacts are well-formed, discoverable,
exportable, and synchronized with declared Lean public surfaces.

It does not validate formal meaning, truth, correctness, legitimacy,
obligation, or enforcement.

### Rationale

Lean is authoritative for formal definitions, predicates, relations,
classifications, and theorems.

Python reference tooling may inspect shape and synchronization, but it must not
become a parallel semantic authority.

### Consequences

- Validation diagnostics report missing files, malformed artifacts, stale
  exports, and missing declared symbols.
- Diagnostics do not claim that a theorem, definition, or theory statement is
  semantically correct.
- Documentation generated by this kit is descriptive and reference-oriented.

---

## TRK-D-0006: Runtime dependencies remain empty until required by the generic engine

### Date recorded

2026-06-01

### Decision

The package starts with no runtime dependencies.

Development and documentation dependencies are kept in optional dependency
groups.

### Rationale

The generic engine uses the Python standard library for paths, TOML reading,
JSON writing, command parsing, and dataclasses.

Keeping runtime dependencies empty prevents tooling dependencies from becoming
implicit public contract dependencies.

### Consequences

- `dependencies = []`.
- Configuration and artifact reading use `tomllib` from the standard library.
- Documentation dependencies live under `docs`.
- Developer tooling dependencies live under `dev`.
- Any future runtime dependency must be justified as part of the generic engine,
  not merely convenient for one theory repository.

---

## TRK-D-0007: Documentation is descriptive and must not define Lean semantics

### Date recorded

2026-06-01

### Decision

Documentation for this package describes the Python API, repository mechanics,
and reference workflow.

It must not define or reinterpret Lean theory semantics.

### Rationale

The package services formal theory repositories, but it is not the authority for
formal theory content.

### Consequences

- API documentation may be generated from Python docstrings.
- Workflow documentation may describe how reference artifacts are loaded,
  checked, scaffolded, and exported.
- Formal definitions remain in the owning Lean repositories.

---

## TRK-D-0008: Public command surface is stable from first implementation

### Date recorded

2026-06-01

### Decision

`se-theory-reference-kit` exposes its intended public command surface from the
start of implementation rather than publishing temporary command names or
narrow interim entry points.

The authoritative command declaration is `pyproject.toml`.
The command behavior contract is documented in the command documentation and
covered by CLI tests.

### Rationale

This package is shared infrastructure for multiple theory repositories. Stable
entry points reduce downstream churn and keep repository workflows aligned while
the internal engine matures.

### Consequences

- Public entry points are changed only as package contract changes.
- CLI tests must protect the published command surface.
- Command documentation must match the implemented command surface.
- Command modules delegate to engine modules rather than owning validation,
  export, scaffolding, or catalog behavior.

---

## TRK-D-0009: API reference pages are generated from source

### Date recorded

2026-06-01

### Decision

Python API reference pages are generated from the source tree during the
documentation build.

The documentation build configuration owns the generation mechanism.
The Python source tree owns the API surface.
Generated API pages are not hand-maintained.

### Rationale

Hand-maintained API reference pages duplicate source structure and drift as
modules move, split, or merge. Generated API documentation preserves the source
tree as the API reference authority.

### Consequences

- Human-authored documentation describes architecture, workflow, and package
  boundaries.
- Generated API documentation mirrors the current source tree.
- The generator is documentation tooling, not runtime package behavior.
- If the pattern becomes shared across SE Python repositories, ownership should
  move to shared SE repository tooling.

---

## TRK-D-0010: Validation uses an immutable check registry

### Date recorded

2026-06-01

### Decision

Validation is organized around an immutable check registry and runner.

The source code owns the validation types, default registry, execution behavior,
and result vocabulary. The documentation describes the validation boundary
without duplicating implementation declarations.

### Rationale

The kit needs a generic validation extension seam that supports shared default
checks and repo-specific checks without allowing consumers to mutate kit-owned
defaults.

An immutable registry preserves deterministic order, explicit extension, and
stable validation composition across theory repositories.

### Consequences

- The default validation registry contains only checks that are generic across
  supported theory repositories.
- Repo-specific validation is appended by the owning theory repository.
- Validation execution must preserve crash isolation and deterministic ordering.
- Tests protect duplicate-id rejection, extension behavior, strict-mode behavior,
  and default-registry stability.

---

## TRK-D-0011: Repository declarations are declarative data loaded by the kit

### Date recorded

2026-06-03

### Decision

Each theory repository declares its repository identity, Lean public surface
mapping, reference layout, and export specifications in a single declarative
file, `reference/theory-reference.toml`.

The kit reads that file into typed declaration models and does not import
repository-owned Python configuration modules.

### Rationale

Repository configuration is data, not behavior. Expressing it as data keeps the
generic engine the only place that holds loading logic, makes each repository's
declaration inspectable and diffable, and lets a new theory repository join by
writing one configuration file rather than authoring code.

A single declarative source also removes any executable surface from repository
configuration, so configuration cannot carry behavior or import-time side
effects.

### Consequences

- A conforming repository provides `reference/theory-reference.toml`; it does not
  provide importable configuration modules.
- The kit owns the declaration model shapes, such as `TheoryReferenceConfig` and
  `ExportSpec`; the repository owns only the values.
- The kit's configuration loader is the single place that knows the file's shape;
  command and engine code consume typed models.
- A new theory repository is onboarded by authoring one configuration file.

---

## TRK-D-0012: The declared public surface is derived from reference artifacts

### Date recorded

2026-06-03

### Decision

The kit derives a repository's declared public surface from its reference
artifacts. Lean remains the source of truth for formal declarations; the
reference artifacts are the source of truth for the repository's declared,
classified, and exportable public surface.

Public symbols are not listed a second time in configuration.

### Rationale

The reference artifacts already enumerate the public symbols and their citation
identifiers, so they are the single source of truth for the symbol set.
Declaring the same symbols again in configuration would create two sources that
can disagree, and synchronization validation would then have to police the
duplication it exists to prevent.

Treating the artifacts as the source keeps the symbol set in one place and makes
adding or removing a symbol a single edit in the owning artifact.

### Consequences

- Surface symbols live only in the reference artifacts; configuration carries the
  kind-to-artifact mapping, not the symbols.
- `SurfaceSymbols` is built by reading the mapped artifacts, not from a
  configuration list.
- A symbol change is a change to one reference artifact, checked against Lean.
- Synchronization validation compares the Lean public surface against the
  artifact-derived surface, with no third copy to reconcile.

<!-- markdownlint-enable MD024 -->
