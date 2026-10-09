# Known limitations

Honest constraints for the current prototype. Do not read this as a production readiness claim.

## Product

- Single-document Markdown focus; no multi-document corpus orchestration yet.
- Answers are extractive / heuristic under the fixture provider, not a general LLM QA system.
- Vector retrieval baseline is a documented placeholder, not a fair comparison claim.
- Demo UI is local-only; no auth, tenancy, or rate limiting for internet exposure.

## Quality

- Tree-first ranking can still prefer title/overview sections; claim ranking by term overlap mitigates but does not eliminate this.
- Conflict detection covers a small set of numeric topics (temperature, voltage, current).
- Evaluation set `eval-v0` is small and synthetic; metrics are directional.

## Security and privacy

- Document text is untrusted (prompt injection). See [THREAT_MODEL.md](THREAT_MODEL.md).
- Non-fixture providers may send document text externally — the UI/API warn, they do not block.
- Upload limits are size/extension checks, not a full content sandbox.

## Operations

- No container orchestration, metrics backend, or durable store beyond local paths.
- Cost estimates are zero under fixture mode; real provider costs are not metered yet.
