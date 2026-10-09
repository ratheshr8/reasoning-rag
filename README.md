# reasoning-rag

**Status:** prototype (Phase 1 — package skeleton and typed contracts; no retrieval runtime yet)

Hierarchy-aware document question answering: navigate a document tree, gather evidence, cite sources, and abstain when evidence is weak.

This is an independent project. It may study public ideas such as hierarchical document trees and reasoning-based retrieval. It is not PageIndex, does not copy PageIndex, and is not affiliated with it.

## What works now

- Product brief, public roadmap, and scope ADRs
- Installable Python 3.12+ package with typed domain models
- Validated configuration (`REASONING_RAG_*`), structured logging, CLI skeleton
- Lint, format, type-check, and CI workflow

## What is not implemented yet

- Document ingestion, tree construction, retrieval, answering, evaluation harness, and demo

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

reasoning-rag --help
reasoning-rag version
reasoning-rag config
reasoning-rag doctor
```

Read:

1. [Product brief](docs/PRODUCT_BRIEF.md)
2. [Public roadmap](docs/ROADMAP.md)
3. [ADR 0001 — project scope](docs/adr/0001-project-scope.md)
4. [ADR 0002 — language and tooling](docs/adr/0002-language-and-tooling.md)

## Skills this repo is meant to demonstrate

See the [skills map](docs/ROADMAP.md#skills-this-repository-demonstrates). Spec/harness foundations (schemas, config validation, CI) are present; retrieval and evaluation proofs remain planned until M2+.

## Limitations

- Prototype skeleton only — not a production service
- No production deployment, no regulated-data handling, no professional-advice use
- Public samples will be synthetic or redistributable documents only

## License

Apache License 2.0. See [LICENSE](LICENSE).
