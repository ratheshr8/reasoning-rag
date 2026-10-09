# reasoning-rag

**Status:** prototype (Phase 7 — evaluation harness and fair baselines)

Hierarchy-aware document question answering: navigate a document tree, gather evidence, cite sources, and abstain when evidence is weak.

This is an independent project. It may study public ideas such as hierarchical document trees and reasoning-based retrieval. It is not PageIndex, does not copy PageIndex, and is not affiliated with it.

## What works now

- Markdown ingestion, knowledge trees, planning, multi-hop navigation, verification
- Versioned eval dataset (`eval-v0`) with tree-first and lexical baselines
- Reproducible reports: metrics, latency, cost (fixture=$0), per-case failures
- Vector/hybrid baseline explicitly marked not implemented (no invented scores)
- CLI: `ingest`, `tree`, `plan`, `ask`, `eval`

## What is not implemented yet

- Demo UI / small API, release hardening
- Live vector baseline and paid-model cost metering

## Retrieval mode

Primary path is **tree-first**. Evaluation compares modes under equal corpus and settings. See [docs/EVALUATION.md](docs/EVALUATION.md).

## Quickstart

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

reasoning-rag ask data/corpus/v0/acme-widget-spec.md \
  -q "What supply voltage does the Acme Widget require?" \
  --synthetic

reasoning-rag eval \
  --dataset data/eval/v0/dataset.json \
  --modes tree-first,tree-lexical \
  --output reports/eval-v0
```

## Docs

1. [Product brief](docs/PRODUCT_BRIEF.md)
2. [Public roadmap](docs/ROADMAP.md)
3. [Evaluation protocol](docs/EVALUATION.md)
4. [ADR 0008 — evaluation protocol](docs/adr/0008-evaluation-protocol.md)

## Limitations

- Fixture baselines only; vector comparison not implemented in eval-v0
- Markdown only; prototype — not a production service
- Sample corpus is synthetic / CC0-1.0

## License

Apache License 2.0. See [LICENSE](LICENSE).
