# ADR 0007 — Multi-hop navigation and verification

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 6 must collect evidence across related tree nodes, keep citations resolvable, map every answer claim to evidence, and surface conflicting statements instead of silently merging them.

## Decision

1. **Navigation:** after plan-guided seeds, expand parent/child neighbors for up to `nav_max_hops`, capped by `nav_max_nodes`, scoring neighbors against subquestions.
2. **Citation verification:** drop evidence whose `source_range` does not resolve in the normalized document text.
3. **Conflicts:** detect distinct numeric values for the same topic across evidence (e.g. ambient temperature); record `EvidenceConflict` and append conflict notes to the answer/limitations — never average or hide values.
4. **Coverage:** mark each subquestion as covered/uncovered via lexical support; include gaps in `VerificationReport`.
5. **Claim mapping:** keep only claims with resolvable evidence IDs; if none remain, abstain.
6. **Trace:** emit navigation and verification events on `AskResult`.

## Options considered

- **LLM entailment verifier.** Deferred: fixture/deterministic checks first.
- **Merge conflicting numbers into one answer.** Rejected: hides disagreement.

## Consequences

- Answers may mention “Conflict noted” when sources disagree.
- Multi-hop expansion can pull related sections (e.g. safety + conflicting note).
- Still extractive/rules-based; not a semantic NLI verifier.

## Revisit triggers

- Need for table-aware conflict extraction or LLM claim entailment.
- Hop strategies that over-retrieve and hurt precision.
