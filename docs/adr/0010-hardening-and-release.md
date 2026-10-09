# ADR 0010 — Hardening and first public prototype tag

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 9 closes the build path with a reviewable public prototype: security notes, support/limitations, reproducible checks, and a version tag visitors can cite.

## Decision

1. Publish a written [threat model](../THREAT_MODEL.md), [limitations](../LIMITATIONS.md), and [support](../SUPPORT.md) page; refresh [SECURITY.md](../../SECURITY.md).
2. Keep the demo localhost-bound by default; do not add auth or multi-tenant hosting in this tag.
3. Ship regression tests for upload limits, placeholder secret rejection, and document-side instruction injection on the fixture path.
4. Tag `v0.1.0` after CI-green checks on `master`; status remains **prototype**, not production.
5. Defer Docker/K8s unless needed for clean-clone pain; document `pip install -e ".[dev,demo]"` as the reproducible environment.

## Options considered

- **Hosted demo.** Rejected for this tag (threat model T6/T8 expansion).
- **Claim “production ready”.** Rejected; evidence does not support it.

## Consequences

- Visitors get clear security and support boundaries.
- Profile and README can link concrete artifacts (threat model, eval, demo) without overclaiming.

## Revisit triggers

- Public internet exposure of the API
- Non-fixture default provider
- Multi-document or regulated domain case studies
