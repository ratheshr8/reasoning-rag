# Public roadmap — reasoning-rag

**Status:** prototype  
**Internal execution plan:** [`AI-ARCHITECT-GITHUB-ROADMAP.md`](../AI-ARCHITECT-GITHUB-ROADMAP.md) (Cursor phases, portfolio backlog). This file is the visitor-facing plan.

## Skills this repository demonstrates

Each skill is proven only when the artifact exists. Profile copy must not present planned items as shipped.

| Skill | Artifact | Ready when |
| --- | --- | --- |
| AI system design | Architecture diagram and [ADR 0001](adr/0001-project-scope.md) | M1–M2 |
| Retrieval / RAG judgment | Tree-first vs lexical (and optional vector) baselines | M3, M5 |
| Agentic / planning | Bounded planner, budgets, inspectable traces | M4 |
| Evaluation / quality | Versioned dataset and failure analysis | M5 |
| Governance / risk | Threat model, abstention, limitations | M3, M6 |
| Security | Citation validation, prompt-injection tests, secret hygiene | M6 |
| Ops / platform | Cost/latency, provider interface, run metadata | M5–M6 |
| Spec / harness | Schemas, fixtures, quality gates | M1, M5 |
| Communication | This README trail and a later case study | M0, M7 |

## Now vs next

**Now (Phase 1):** installable package, typed contracts, config validation, CLI skeleton (`version` / `config` / `doctor`), Ruff/mypy/pytest CI. See [ADR 0002](adr/0002-language-and-tooling.md).

**Next public proofs**

1. **Phase 2 / M2 — Inspectable tree:** Markdown ingest, provenance, source-aware tree, visualization.
2. **M3 — Grounded baseline:** cited answer plus abstention on a known unanswerable question.
3. **M5 — Measured system:** reproducible eval report with cost and latency.
4. **M6 — Public beta:** tagged release, security notes, clean-clone quickstart.

Supporting GitHub repositories (governance, agentic SDLC, healthcare, harness, control plane) stay backlog until **M5** and are never pinned empty.

## Milestones

- **M0** Identity on `ratheshr8` — profile README must match this story
- **M1** Scope approved — this brief + ADR 0001
- **M2** Inspectable documents
- **M3** Cited answers and abstention
- **M4** Query analysis and bounded navigation
- **M5** Evaluation harness and baselines
- **M6** Tagged prototype release
- **M7** GitHub, LinkedIn, and website aligned
- **M8** One complementary repo with its own release bar (after M5)

## Retrieval modes (when implemented)

- **Tree-first** — primary
- **Tree + lexical** — keyword assist
- **Hybrid comparison** — optional vector baseline for experiments

## Headline rule

Healthcare and FinTech do not appear in the GitHub/LinkedIn/website headline until a labeled synthetic or reference-only case study exists. See the internal roadmap, Section 2.
