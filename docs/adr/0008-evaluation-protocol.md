# ADR 0008 — Evaluation protocol

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 7 needs reproducible comparison of retrieval modes on a fixed corpus without overclaiming quality. Metrics must be defined, failures inspectable, and cost/latency reported even when the model provider is a free fixture.

## Decision

1. **Dataset:** versioned JSON at `data/eval/v0/dataset.json` (`eval-v0`) referencing the synthetic corpus.
2. **Harness:** `reasoning-rag eval` runs selected modes with identical settings and writes `report.json`, `report.md`, and per-case `AskResult` traces.
3. **Baselines:** `tree-first` and `tree-lexical` are executed; `hybrid-comparison` / vector is recorded as **not implemented** with equal-protocol notes (no invented scores).
4. **Metrics:** documented in [`docs/EVALUATION.md`](../EVALUATION.md) and embedded in every report.
5. **Cost:** fixture provider reports `estimated_cost_usd = 0.0` and states that explicitly.
6. **Claims:** reports must not say “better than vector RAG” unless a vector baseline actually ran under the same protocol.

## Options considered

- **Leaderboard single score.** Rejected: hides abstention/conflict/citation failures.
- **Fake vector numbers for completeness.** Rejected: violates evidence-before-claims.

## Consequences

- Portfolio can show measured M5 evidence from a documented command.
- Vector comparison remains a future, explicitly labeled gap.

## Revisit triggers

- Real embedding baseline with pinned model and equal context budgets.
- Human rubric sampling for citation usefulness.
