# reasoning-rag

**Status:** prototype (Phase 6 — multi-hop navigation and verification)

Hierarchy-aware document question answering: navigate a document tree, gather evidence, cite sources, and abstain when evidence is weak.

This is an independent project. It may study public ideas such as hierarchical document trees and reasoning-based retrieval. It is not PageIndex, does not copy PageIndex, and is not affiliated with it.

## What works now

- Markdown ingestion, knowledge trees, query analysis, and bounded retrieval plans
- Multi-hop parent/child navigation from planned seed nodes
- Citation verification, subquestion coverage checks, and conflict surfacing
- Claim-to-evidence mapping; unresolved claims are dropped or trigger abstention
- CLI: `ingest`, `tree`, `plan`, `ask` (`--show-plan`)

## What is not implemented yet

- Evaluation harness / fair baselines report, demo UI
- LLM verifier and vector baseline

## Retrieval mode

Primary path is **tree-first**, plan-guided, with optional multi-hop expansion. Conflicting values are reported, not merged. Runs record analysis, plan, evidence, and `verification` on `AskResult`.

## Quickstart

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

reasoning-rag ask data/corpus/v0/acme-widget-spec.md \
  -q "What is the maximum ambient temperature for operating the widget?" \
  --synthetic --show-plan
```

## Docs

1. [Product brief](docs/PRODUCT_BRIEF.md)
2. [Public roadmap](docs/ROADMAP.md)
3. [ADR 0007 — navigation and verification](docs/adr/0007-navigation-and-verification.md)
4. [Corpus v0 dataset card](data/corpus/v0/DATASET_CARD.md)

## Limitations

- Deterministic/fixture verification — not LLM entailment
- Markdown only; prototype — not a production service
- Sample corpus is synthetic / CC0-1.0

## License

Apache License 2.0. See [LICENSE](LICENSE).
