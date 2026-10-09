# reasoning-rag

**Status:** prototype (`v0.1.0`)

Hierarchy-aware document question answering: navigate a document tree, gather evidence, cite sources, and abstain when evidence is weak.

This is an independent project. It may study public ideas such as hierarchical document trees and reasoning-based retrieval. It is not PageIndex, does not copy PageIndex, and is not affiliated with it.

## What works now

- End-to-end tree-first ask path with planning, multi-hop navigation, and verification
- Evaluation harness (`eval-v0`) for tree-first and lexical baselines
- Local demo UI + validated API (`/`, `/api/ask`, `/api/samples`, `/docs`)
- Clear upload limits, provider notice, threat model, and support status

## What is not implemented yet

- Hosted multi-user deployment and authentication
- Live vector baseline under the same evaluation protocol

## Retrieval mode

Primary path is **tree-first**. Evaluation and the demo record the active mode on every run.

## Quickstart

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev,demo]"
cp .env.example .env

reasoning-rag ask data/corpus/v0/acme-widget-spec.md \
  -q "What supply voltage does the Acme Widget require?" \
  --synthetic

reasoning-rag serve
# open http://127.0.0.1:8000/
```

Fixture provider keeps document text local. If you change `REASONING_RAG_MODEL_PROVIDER` away from `fixture`, the demo shows a warning that document text may be sent to an external service.

## Docs

1. [Product brief](docs/PRODUCT_BRIEF.md)
2. [Public roadmap](docs/ROADMAP.md)
3. [Evaluation protocol](docs/EVALUATION.md)
4. [Threat model](docs/THREAT_MODEL.md)
5. [Limitations](docs/LIMITATIONS.md)
6. [Support status](docs/SUPPORT.md)
7. [Changelog](CHANGELOG.md)
8. [Security](SECURITY.md)

## Limitations

See [docs/LIMITATIONS.md](docs/LIMITATIONS.md). Short version: local prototype, Markdown only, synthetic corpus (CC0-1.0).

## License

Apache License 2.0. See [LICENSE](LICENSE).
