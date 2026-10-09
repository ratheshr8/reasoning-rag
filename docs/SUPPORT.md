# Support status and supported configurations

**Project status:** tagged prototype (`v0.1.0`)  
**Support:** best-effort / portfolio prototype — not a commercial SLA

## Supported configurations

| Item | Supported |
| --- | --- |
| Python | 3.12+ |
| OS | Windows, macOS, Linux (local developer machines) |
| Install | `pip install -e ".[dev,demo]"` from a clean clone |
| Model provider | `fixture` (default, local) |
| Document format | Markdown (`.md`, `.markdown`) |
| Retrieval modes | `tree-first`, `tree-lexical` (eval/demo); vector baseline is placeholder only |
| Demo bind | `127.0.0.1` via `reasoning-rag serve` |

## Explicitly unsupported

- Production multi-tenant hosting
- Non-fixture providers without reviewing the [threat model](THREAT_MODEL.md) and provider notice
- PDF/HTML/DOCX ingestion
- Healthcare or FinTech regulated deployments (headline reserved until a labeled case study exists)
- Guaranteed answer correctness on arbitrary documents

## How to get help

- Bugs and docs: GitHub issues on [ratheshr8/reasoning-rag](https://github.com/ratheshr8/reasoning-rag)
- Security: see [SECURITY.md](../SECURITY.md)

## Related docs

- [Limitations](LIMITATIONS.md)
- [Threat model](THREAT_MODEL.md)
- [Evaluation protocol](EVALUATION.md)
