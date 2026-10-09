# reasoning-rag

**Status:** prototype (Phase 4 — cited answers and abstention baseline)

Hierarchy-aware document question answering: navigate a document tree, gather evidence, cite sources, and abstain when evidence is weak.

This is an independent project. It may study public ideas such as hierarchical document trees and reasoning-based retrieval. It is not PageIndex, does not copy PageIndex, and is not affiliated with it.

## What works now

- Markdown ingestion with checksums, section offsets, and parser warnings
- Deterministic heading-based knowledge tree (JSON + text visualization)
- Tree-first and lexical retrieval baselines with evidence assembly
- Extractive cited answers or abstention when evidence is weak/absent
- Synthetic corpus, starter cases, and example trace instructions
- CLI: `version`, `config`, `doctor`, `ingest`, `tree`, `ask`

## What is not implemented yet

- Query planning / multi-hop verification, evaluation harness, and demo UI
- Vector baseline and LLM answer synthesis

## Retrieval mode

Primary path is **tree-first**. Use `--mode tree-lexical` for keyword-only comparison. Hybrid comparison currently follows tree-first until a vector path exists. Runs record the active mode in `AskResult`.

## Quickstart

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

reasoning-rag tree data/corpus/v0/acme-widget-spec.md --synthetic
reasoning-rag ask data/corpus/v0/acme-widget-spec.md \
  -q "What supply voltage does the Acme Widget require?" \
  --synthetic
reasoning-rag ask data/corpus/v0/acme-widget-spec.md \
  -q "How do I perform firmware updates on the Acme Widget?" \
  --synthetic
```

## Docs

1. [Product brief](docs/PRODUCT_BRIEF.md)
2. [Public roadmap](docs/ROADMAP.md)
3. [ADR 0005 — retrieval baselines](docs/adr/0005-retrieval-baselines.md)
4. [Corpus v0 dataset card](data/corpus/v0/DATASET_CARD.md)
5. [Example traces](examples/traces/README.md)

## Limitations

- Markdown only; answers are extractive fixture baselines, not LLM quality claims
- Prototype — not a production service
- Sample corpus is synthetic / CC0-1.0

## License

Apache License 2.0. See [LICENSE](LICENSE).
