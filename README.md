# reasoning-rag

**Status:** prototype (Phase 0 — product brief and scope only; no retrieval runtime yet)

Hierarchy-aware document question answering: navigate a document tree, gather evidence, cite sources, and abstain when evidence is weak.

This is an independent project. It may study public ideas such as hierarchical document trees and reasoning-based retrieval. It is not PageIndex, does not copy PageIndex, and is not affiliated with it.

## What works now

- Product brief, public roadmap, and scope ADR
- Locked v1 choices: Markdown corpus, Python 3.12+, tree-first retrieval as the primary mode

## What is not implemented yet

- Document ingestion, tree construction, retrieval, answering, evaluation harness, and demo

## Retrieval mode

The intended primary path is **tree-first** (hierarchy navigation and node metadata). Lexical and optional vector baselines are for comparison, not the v1 default. No run will be labeled “vectorless” if vector similarity is on its primary path.

## Quickstart

There is no installable CLI yet. Read:

1. [Product brief](docs/PRODUCT_BRIEF.md)
2. [Public roadmap](docs/ROADMAP.md)
3. [ADR 0001 — project scope](docs/adr/0001-project-scope.md)

## Skills this repo is meant to demonstrate

See the [skills map](docs/ROADMAP.md#skills-this-repository-demonstrates). Until M2/M3 artifacts exist, treat those skills as planned, not proven.

## Limitations

- Prototype documentation only
- No production deployment, no regulated-data handling, no professional-advice use
- Public samples will be synthetic or redistributable documents only

## License

Apache License 2.0. See [LICENSE](LICENSE).
