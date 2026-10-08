# ADR 0001 — Project scope

- **Status:** Accepted
- **Date:** 2026-10-07
- **Decision owners:** Rathesh R

## Context

`reasoning-rag` is the flagship public project for an AI Architecture skills showcase on GitHub (`ratheshr8`). Scope must be narrow enough to ship evidence (tree, citations, abstention, eval) and wide enough to show architecture judgment. Open choices that would stall Phase 1: document format, first corpus family, language/runtime, and how far the portfolio should sprawl.

## Decision

1. **Product:** a document QA system whose primary retrieval path is hierarchy navigation over a document tree, with citations and abstention. Vector similarity is not required for v1 indexing or retrieval.
2. **Format:** Markdown only in v1. PDF is deferred.
3. **Corpus:** small in-repo public/synthetic Markdown specs with a dataset card. No employer, customer, or regulated documents.
4. **Runtime:** Python 3.12+, typed domain models, CLI-first modular monolith, model calls behind an interface with a fixture/mock mode.
5. **Portfolio:** this repository is the only public build until milestone M5 (measured eval). No empty supporting repos and no pins that fail the release bar.
6. **Identity:** all GitHub paths use `ratheshr8` (`ratheshr8/ratheshr8`, `ratheshr8/reasoning-rag`).
7. **Independence:** public concepts including PageIndex may inform the thesis; their code, branding, prompts, and docs must not be copied, and no affiliation is implied.

## Options considered

- **Do nothing / keep scope unbounded.** Rejected: a skills showcase with many empty repos reads as a wish list.
- **PDF-first corpus.** Rejected for v1: parser risk and provenance complexity delay the first cited-answer proof.
- **TypeScript/Node.** Viable for CLI and schemas, but Python is the default ecosystem for retrieval evaluation, scientific reporting, and typical hiring-manager expectation for this problem class.
- **Vector-first RAG with a tree as garnish.** Rejected: it would not test the stated thesis.
- **Multi-repo portfolio in parallel.** Rejected until M5; dilutes signal.

## Consequences

- First skill proofs are M2 (tree) and M3 (cite/abstain), not a hosted demo.
- Evaluation can include an optional vector baseline later without renaming tree-first runs as “vectorless.”
- Healthcare/FinTech wording stays out of headlines until a labeled synthetic/reference case study exists.
- Phase 1 can proceed on Python packaging, schemas, and CLI without revisiting format or corpus family.

## Risks

- Markdown-only may look less “document AI” than PDF until a later adapter exists. Mitigate with a real public spec and honest README status.
- Python lock-in at the edges (packaging). Mitigate with a small provider/storage interface.

## Revisit triggers

- A required target corpus is PDF-only and cannot be legally converted to Markdown.
- Evaluation shows tree-first retrieval is unusable without lexical or vector recall on the chosen spec family.
- Runtime constraints (deployment target, team skill) make Python the wrong vehicle.

## References

- [Product brief](../PRODUCT_BRIEF.md)
- [Public roadmap](../ROADMAP.md)
