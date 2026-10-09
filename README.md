# reasoning-rag

**Status:** prototype (Phase 5 — query analysis and bounded retrieval planning)

Hierarchy-aware document question answering: navigate a document tree, gather evidence, cite sources, and abstain when evidence is weak.

This is an independent project. It may study public ideas such as hierarchical document trees and reasoning-based retrieval. It is not PageIndex, does not copy PageIndex, and is not affiliated with it.

## What works now

- Markdown ingestion with provenance and heading-based knowledge trees
- Typed query analysis with safe fallback on malformed structured output
- Bounded retrieval plans (depth/node/model-call budgets) guiding evidence selection
- Tree-first and lexical baselines, extractive cited answers, or abstention
- CLI: `ingest`, `tree`, `plan`, `ask` (`--show-plan`)

## What is not implemented yet

- Multi-hop verification / conflict surfacing, evaluation harness, demo UI
- LLM analyzer/planner and vector baseline

## Retrieval mode

Primary path is **tree-first**, now plan-guided. Use `--mode tree-lexical` for keyword-only scoring inside the planner. Runs record mode, analysis, and plan in `AskResult`.

## Quickstart

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

reasoning-rag plan data/corpus/v0/acme-widget-spec.md \
  -q "What supply voltage does the Acme Widget require?" \
  --synthetic

reasoning-rag ask data/corpus/v0/acme-widget-spec.md \
  -q "What supply voltage does the Acme Widget require?" \
  --synthetic --show-plan
```

## Docs

1. [Product brief](docs/PRODUCT_BRIEF.md)
2. [Public roadmap](docs/ROADMAP.md)
3. [ADR 0006 — query planning](docs/adr/0006-query-planning.md)
4. [Corpus v0 dataset card](data/corpus/v0/DATASET_CARD.md)

## Limitations

- Analyzer/planner are deterministic fixture rules, not LLM agents
- Markdown only; prototype — not a production service
- Sample corpus is synthetic / CC0-1.0

## License

Apache License 2.0. See [LICENSE](LICENSE).
