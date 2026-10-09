# reasoning-rag

**Status:** prototype (Phase 3 — inspectable knowledge tree; no retrieval/answer path yet)

Hierarchy-aware document question answering: navigate a document tree, gather evidence, cite sources, and abstain when evidence is weak.

This is an independent project. It may study public ideas such as hierarchical document trees and reasoning-based retrieval. It is not PageIndex, does not copy PageIndex, and is not affiliated with it.

## What works now

- Product brief, public roadmap, and ADRs
- Installable Python 3.12+ package with typed domain models and validated config
- Markdown ingestion with checksums, section offsets, and parser warnings
- Deterministic heading-based knowledge tree with JSON round-trip and text visualization
- Optional fixture extractive summaries (records provider/model/prompt version)
- Synthetic sample corpus under `data/corpus/v0/`
- CLI: `version`, `config`, `doctor`, `ingest`, `tree`
- Lint, format, type-check, and CI workflow

## What is not implemented yet

- Retrieval planning, answering with citations, evaluation harness, and demo UI

## Retrieval mode

The intended primary path is **tree-first** (hierarchy navigation and node metadata). Lexical and optional vector baselines are for comparison, not the v1 default. No run will be labeled “vectorless” if vector similarity is on its primary path. Default config uses `tree-first` with a `fixture` model provider (no API key required).

## Quickstart

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

reasoning-rag doctor
reasoning-rag ingest data/corpus/v0/acme-widget-spec.md --synthetic
reasoning-rag tree data/corpus/v0/acme-widget-spec.md --synthetic
reasoning-rag tree data/corpus/v0/acme-widget-spec.md --synthetic --summarize --format json
```

`tree` prints an ASCII outline by default. Use `--format json` or `-o tree.json` for a round-trippable `DocumentTree`.

Read:

1. [Product brief](docs/PRODUCT_BRIEF.md)
2. [Public roadmap](docs/ROADMAP.md)
3. [ADR 0001 — project scope](docs/adr/0001-project-scope.md)
4. [ADR 0002 — language and tooling](docs/adr/0002-language-and-tooling.md)
5. [ADR 0003 — ingestion and provenance](docs/adr/0003-ingestion-and-provenance.md)
6. [ADR 0004 — tree storage](docs/adr/0004-tree-storage.md)
7. [Corpus v0 dataset card](data/corpus/v0/DATASET_CARD.md)

## Skills this repo is meant to demonstrate

See the [skills map](docs/ROADMAP.md#skills-this-repository-demonstrates). Provenance and inspectable hierarchy are present; cited answers and evaluation remain planned until M3/M5.

## Limitations

- Markdown only; no PDF
- Summaries are optional fixture extractive stubs, not LLM quality claims
- Prototype — not a production service
- Sample corpus is synthetic / CC0-1.0

## License

Apache License 2.0. See [LICENSE](LICENSE).
