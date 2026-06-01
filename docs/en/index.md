# SE Theory: Reference Kit

`se-theory-reference-kit` is shared Python infrastructure for Structural
Explainability theory repositories.

It provides generic tooling for maintaining theory-reference artifacts that
mirror Lean public surfaces. The kit supports loading, inspecting, validating,
scaffolding, exporting, and cataloging reference material supplied by the
owning theory repository.

## Purpose

The package exists so Structural Explainability theory repositories can share
one reference-tooling engine instead of each maintaining separate Python
tooling for the same repository mechanics.

The kit serves theory repositories that maintain Lean source and repo-owned
reference artifacts. It does not define theory content.

## Scope

The kit owns generic infrastructure for:

- repository-relative path handling,
- typed declaration loading,
- Lean source inspection,
- reference artifact loading,
- reference registry construction,
- reference validation,
- scaffold support,
- generated export support,
- catalog support,
- command orchestration.

The kit does not own:

- Lean semantics,
- formal definitions,
- public symbol lists,
- theory-specific export maps,
- contract packaging,
- operational validation pipelines,
- domain mappings,
- runtime systems.

## Repository ownership boundary

Each theory repository owns its own declared public Lean surface and export
specifications.

The shared kit consumes those declarations through typed repository-provided
objects. This keeps theory content in the theory repository and keeps the kit
focused on reusable mechanics.

## Public command

The package exposes one public command:

```shell
se-theory-reference
```

See [Commands](./commands.md) for the command responsibilities.

## API reference

The Python API reference is generated from source during documentation builds.

See [API Reference](./api/) for generated package documentation.
