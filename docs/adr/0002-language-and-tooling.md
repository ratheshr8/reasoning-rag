# ADR 0002 — Language and tooling

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 1 needs a typed package layout, validated configuration, a CLI entrypoint, and CI that can run without paid model access. ADR 0001 already locked Python 3.12+. Remaining choices: schema library, CLI framework, lint/type tooling, and packaging.

## Decision

1. **Schemas:** Pydantic v2 models for all domain contracts; validate at boundaries.
2. **Settings:** `pydantic-settings` with `REASONING_RAG_` prefix and optional `.env`.
3. **CLI:** Typer + Rich for help/errors; commands for `version`, `config`, and `doctor` in the skeleton.
4. **Logging:** stdlib logging with optional JSON formatter; no document bodies or secrets by default.
5. **Quality:** Ruff (lint/format), mypy (strict), pytest; GitHub Actions CI on push/PR.
6. **Packaging:** `src/` layout, Hatchling, console script `reasoning-rag`.
7. **Model access:** default `fixture` provider; API key optional and redacted in `config` output.

## Options considered

- **dataclass + JSON Schema only.** Rejected: weaker validation ergonomics for nested contracts.
- **Click without Typer.** Viable; Typer reduces boilerplate for a small CLI.
- **structlog.** Deferred; stdlib JSON logs are enough for Phase 1.

## Consequences

- Developers can install and validate config without secrets.
- Retrieval/ingest behavior remains unimplemented until later phases.
- CI will fail on formatting, type, or schema-test regressions.

## Revisit triggers

- Need for async web API that favors another stack.
- Logging volume that requires a richer structured logging library.
