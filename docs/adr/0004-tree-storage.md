# ADR 0004 — Tree construction and storage

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 3 needs a deterministic hierarchy over ingested Markdown sections so later retrieval can navigate by structure. Summaries may help navigation but must not be required for a usable tree, and must record model/prompt identity when used.

## Decision

1. **Builder:** stack-based nesting by Markdown heading level (preamble=0, H1–H6=1–6); document root node `{doc_id}:root` is the parent of top-level sections.
2. **Stable IDs:** section nodes reuse ingestion section IDs; root uses `:root` suffix.
3. **Provenance:** every node has a `source_range` into the normalized document text.
4. **Storage:** serialize `DocumentTree` as versioned JSON (in-memory / file); SQLite deferred.
5. **Summaries:** optional, behind a `Summarizer` protocol; only `fixture` extractive summarizer is implemented; budgets via `tree_max_summaries` and `tree_summary_max_chars`.
6. **Budgets:** `tree_max_nodes` caps section count before build fails safely.

## Options considered

- **Require LLM summaries for every node.** Rejected: blocks offline demos and CI.
- **Immediate SQLite persistence.** Deferred until retrieval needs queryable storage.
- **Rebuild IDs at tree time.** Rejected: keep section IDs stable across ingest→tree.

## Consequences

- CLI `tree` can show ASCII visualization or JSON for inspection.
- Round-trip JSON validation catches broken parent/child links.
- Paid model providers remain unimplemented until a later ADR.

## Revisit triggers

- Need for setext headings or non-heading structural nodes (tables as nodes).
- Persistence/query patterns that justify SQLite or another store.
