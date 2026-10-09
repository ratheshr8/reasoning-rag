# ADR 0006 — Query analysis and retrieval planning

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 5 needs inspectable query understanding and a bounded plan before evidence gathering. Model-produced structured output may be malformed or unavailable; the system must fall back safely without crashing the ask path.

## Decision

1. **Analyzer:** rules-based `FixtureQueryAnalyzer` produces typed `QueryAnalysis` (intent, entities, constraints, subquestions).
2. **Validation:** all analyzer output is validated against the Pydantic schema; on failure, use `fallback_query_analysis` and record `analysis_fallback=true`.
3. **Planner:** `rules-planner-v1` scores nodes, merges subquestion candidates, then applies budgets (`plan_max_depth`, `plan_max_nodes`, `plan_max_model_calls`, `plan_max_context_tokens`).
4. **Ask path:** analyze → plan → plan-guided retrieval → evidence → answer; plan and analysis are attached to `AskResult`.
5. **CLI:** `reasoning-rag plan` shows analysis/plan without answering; `ask --show-plan` prints the plan before the answer.
6. **Model calls:** fixture path uses `plan_max_model_calls=0`; paid/LLM analyzers are not implemented yet.

## Options considered

- **Always call an LLM for analysis.** Rejected for Phase 5: blocks offline demos and CI.
- **Plan without schema validation.** Rejected: silent malformed plans break trust.

## Consequences

- Retrieval becomes plan-guided and budget-aware.
- Malformed structured output no longer fails the request.
- Planner quality is rules-level; documentation must not claim agentic LLM planning.

## Revisit triggers

- LLM analyzer/planner behind the existing provider interface.
- Multi-hop navigation that expands nodes beyond the static candidate list (Phase 6).
