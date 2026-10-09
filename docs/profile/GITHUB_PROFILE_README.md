<!-- Published to https://github.com/ratheshr8/ratheshr8 (special profile README). Keep this draft in sync when profile claims change. -->

# Rathesh R

**AI Architecture & Engineering | Agentic Systems | AI Governance**

I design retrieval and agent workflows that can show their work: bounded plans, citations, abstention, and evaluation you can rerun.

[reasoning-rag `v0.1.0`](https://github.com/ratheshr8/reasoning-rag/releases/tag/v0.1.0) · [ratheshworld.com](https://ratheshworld.com)

## Start here

| If you have… | Open |
| --- | --- |
| 2 minutes | [reasoning-rag README](https://github.com/ratheshr8/reasoning-rag) — problem, what works, quickstart |
| 10 minutes | [Evaluation protocol](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/EVALUATION.md) and [threat model](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/THREAT_MODEL.md) |
| A design review | [ADR index](https://github.com/ratheshr8/reasoning-rag/tree/master/docs/adr) — scope, retrieval, planning, eval, demo, release |

## Featured work

### [reasoning-rag](https://github.com/ratheshr8/reasoning-rag) — prototype `v0.1.0`

Long technical documents hide answers across sections. Flat chunks return fragments and hide weak evidence. This prototype navigates a document tree, cites source ranges, surfaces conflicts, and abstains when the document does not support an answer.

| Decision | Where it shows up |
| --- | --- |
| Tree-first retrieval, with a lexical baseline under the same protocol | [ADR 0005](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/adr/0005-retrieval-baselines.md), [eval-v0](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/EVALUATION.md) |
| Bounded planner (depth, nodes, model calls) and inspectable traces | [ADR 0006](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/adr/0006-query-planning.md) |
| Claims only when citations resolve; conflicts stay visible | [ADR 0007](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/adr/0007-navigation-and-verification.md) |
| Local demo with upload limits and a provider notice before any external model call | [ADR 0009](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/adr/0009-demo-and-api.md), `reasoning-rag serve` |
| Honest scope: Markdown, synthetic CC0 corpus, no production tenancy | [Limitations](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/LIMITATIONS.md), [support status](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/SUPPORT.md) |

Vector RAG is not claimed as beaten. A vector baseline is documented as a placeholder until it runs under the same eval rules.

## Skills you can verify

- **System design** — product brief plus ADRs that record options rejected, not only the choice taken. Start at [ADR 0001](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/adr/0001-project-scope.md).
- **Retrieval judgment** — tree-first vs lexical on one versioned dataset, with metric definitions and failure traces. [EVALUATION.md](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/EVALUATION.md).
- **Agent bounds** — query analysis, budgets, and stop conditions you can read in the trace. [ADR 0006](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/adr/0006-query-planning.md).
- **Governance** — abstention, citation checks, threat model, and security reporting. [THREAT_MODEL.md](https://github.com/ratheshr8/reasoning-rag/blob/master/docs/THREAT_MODEL.md), [SECURITY.md](https://github.com/ratheshr8/reasoning-rag/blob/master/SECURITY.md).

## How I work

Public artifacts stay smaller than the claim. Status on this profile is **prototype**: a local system with a tagged release, tests, and a written threat model. It is not a hosted multi-tenant product.

Further projects appear here only after they have a working quickstart, architecture notes, a license, and stated limitations.
