# SBOM — financial-research-analyst-agent (Phase 7, 28 Oct 2026)

## Runtime dependencies
None. The pipeline is standard-library only (including its HTTP
server): no third-party package is imported at runtime. That is
the whole runtime SBOM.

## CI / developer dependencies (pinned, versions measured 28 Oct 2026)
| Tool | Version | Used for |
| --- | --- | --- |
| pytest | 9.2.0 | Suite (46 tests) |
| ruff | 0.17.3 | Lint (`ruff check analyst/ tests/`, see ruff.toml) |
| mypy | 2.4.0 | Type guardrail (`mypy analyst/`, default settings — see mypy.ini) |

## Supply-chain status (config vs enabled)
- Dependency pinning: DONE (this file + pinned CI installs).
- CodeQL workflow: config added; GitHub-side enablement TO VERIFY.
- Dependabot config: added (weekly); enablement TO VERIFY.
- Secret scanning / push protection: GitHub settings, TO VERIFY;
  no secret has ever been committed here (no keys in code; the
  server runs locally, spend_usd is always 0).
- Reproducible builds: pure Python, no compiled steps.
