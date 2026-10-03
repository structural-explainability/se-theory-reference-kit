# Commands

| Command             | Responsibility                                                                                                              |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `validate`          | Check reference artifacts, declared public surface, discovered Lean declarations, and generated export freshness.           |
| `validate --strict` | Run validation with strict handling of unfinished-work and warning conditions.                                              |
| `scaffold`          | Create missing reference stubs from repo-owned public-surface declarations.                                                 |
| `export`            | Write generated JSON artifacts from repo-owned export specs and reference artifacts.                                        |
| `export --check`    | Verify generated JSON artifacts are current without writing.                                                                |
| `catalog`           | Build the generic reference catalog.                                                                                        |
| `catalog --check`   | Verify the generated reference catalog is current without writing.                                                          |
| `inspect`           | Print resolved repository configuration, discovered Lean files, public declarations, reference artifacts, and export specs. |
