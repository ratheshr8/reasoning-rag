# ADR 0005 — Retrieval baselines and cited answers

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 4 needs an end-to-end path from a Markdown document to a cited answer or abstention, without claiming LLM synthesis quality. Modes must be explicit, citations must resolve to source ranges, and demos must run offline with the fixture stack.

## Decision

1. **Modes:** `tree-first` (default) boosts structural/title cues over lexical overlap; `tree-lexical` uses keyword overlap only; `hybrid-comparison` uses the tree-first baseline until a vector path exists.
2. **Evidence:** assemble exact section text with `source_range` and stable evidence IDs; enforce `evidence_max_chars`.
3. **Answers:** extractive fixture composer — answer text comes from top evidence; every non-abstaining answer includes a claim→evidence link.
4. **Abstention:** when score is below `retrieve_min_score`, no evidence matches, the question is unrelated, or the corpus marks content as absent (e.g. firmware updates).
5. **Traces:** emit `AskResult` with retrieval events (node IDs/scores), not hidden chain-of-thought.
6. **Cases:** keep a small `data/corpus/v0/cases.json` and optional JSON traces under `examples/traces/`.

## Options considered

- **LLM answer generation in Phase 4.** Deferred: increases cost/provider coupling before citation plumbing is proven.
- **Vector baseline now.** Deferred to evaluation phase; would blur the tree-first thesis if unlabeled.

## Consequences

- CLI `ask` can demo grounded answers and abstention on the synthetic corpus.
- Evaluation later can compare modes fairly on the same cases.
- Answer quality is intentionally shallow; documentation must not overclaim.

## Revisit triggers

- Need for multi-hop planning (Phase 5+) or verifier claim mapping (Phase 6).
- Introduction of a true vector comparator with equal corpus and budgets.
