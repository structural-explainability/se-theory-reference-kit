# Commands

| Command          | Durable responsibility                                                                                                      |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `validate`       | Check reference artifacts, declared public surface, discovered Lean declarations, and export freshness when requested.      |
| `scaffold`       | Create missing reference stubs from repo-owned public-surface declarations.                                                 |
| `export`         | Write generated JSON artifacts from repo-owned export specs and reference artifacts.                                        |
| `export --check` | Verify generated JSON artifacts are current without writing.                                                                |
| `catalog`        | Build or check the generic reference catalog.                                                                               |
| `inspect`        | Print resolved repository configuration, discovered Lean files, public declarations, reference artifacts, and export specs. |
