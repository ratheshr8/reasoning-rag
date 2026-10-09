# Threat model — reasoning-rag (prototype)

**Status:** reviewed for local-demo / tagged prototype release  
**Date:** 2026-10-09  
**Scope:** local CLI, optional local FastAPI demo, fixture or configured model provider

## Assets

| Asset | Why it matters |
| --- | --- |
| Document text (uploads / samples) | May be confidential if a user supplies it |
| Model API keys | Credential; never committed |
| AskResult traces | May echo document excerpts and questions |
| Eval reports | May contain sample answers and timings |

## Actors

- **Local user** — runs CLI/demo on their machine (trusted for process control, untrusted for document content).
- **Document author** — content may include prompt-injection, malware-like Markdown, or conflicting claims.
- **External model provider** — only if `REASONING_RAG_MODEL_PROVIDER` is not `fixture`.
- **GitHub / CI** — builds and scans public repository artifacts.

## Trust boundaries

1. Document bytes → parser / tree / retriever / answer builder (untrusted).
2. Process → filesystem under configured `data_dir` / temp upload paths.
3. Process → external HTTPS model API (optional; disabled by default).
4. Demo binds `127.0.0.1` by default; not a multi-tenant edge service.

## Threats and mitigations

| ID | Threat | Mitigation (current) | Residual risk |
| --- | --- | --- | --- |
| T1 | Prompt injection via document text | Treat docs as untrusted; fixture path is extractive; abstain when evidence is weak; citation resolution | Non-fixture providers may still follow adversarial text |
| T2 | Oversized upload DoS | `max_upload_bytes` on ingest and `/api/ask/upload` | Local CPU/memory still bounded only lightly |
| T3 | Non-Markdown / binary upload | Extension allow-list (`.md`, `.markdown`) | Content sniffing is not deep |
| T4 | Path traversal via sample id | Sample catalog is an allow-list; no raw path from client | Catalog edits must stay curated |
| T5 | Secret leakage in git/logs | `.env` gitignored; placeholder key rejection; JSON logs avoid dumping API keys | Misconfigured log sinks could still capture document text |
| T6 | Accidental external send of confidential docs | Provider notice in health/samples/ask UI and API | User can ignore the notice |
| T7 | Citation / hallucination | Claim links + citation resolve; conflicts surfaced; abstention | Fixture heuristics are not a general LLM guardrail |
| T8 | Dependency compromise | Pin ranges in `pyproject.toml`; CI installs and tests | No full SBOM/signing pipeline yet |

## Out of scope (prototype)

- Authentication, authorization, multi-tenant isolation
- Hosted public internet exposure of the demo
- Guarantees against a determined local attacker with shell access
- Regulated healthcare/fintech production controls

## Review triggers

- Binding the demo beyond localhost
- Enabling a non-fixture model provider in a shared environment
- Accepting non-Markdown formats or remote URL ingestion
