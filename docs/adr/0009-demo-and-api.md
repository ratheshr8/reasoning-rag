# ADR 0009 — Local demo and API boundary

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 8 needs a usable local demo: choose a sample document or upload Markdown, ask a question, and inspect citations plus a retrieval trace summary. External model providers must not receive document text without clear notice.

## Decision

1. **Stack:** optional FastAPI + Uvicorn extras (`pip install -e ".[demo]"`); core package stays CLI-first without web deps.
2. **API:** validated schemas for `/health`, `/api/samples`, `/api/ask`, `/api/ask/upload`; OpenAPI at `/docs`.
3. **Demo UI:** static page at `/` listing samples, upload limits, provider notice, answer/citations/conflicts/trace summary.
4. **Limits:** enforce `max_upload_bytes` and Markdown-only uploads; actionable error codes on failure.
5. **Provider notice:** fixture mode states text stays local; non-fixture providers warn that document text may be sent externally.
6. **CLI:** `reasoning-rag serve` binds localhost by default.

## Options considered

- **Bundle FastAPI in core deps.** Rejected: heavier install for users who only need CLI/eval.
- **Hosted multi-tenant demo.** Out of scope; prototype remains local.

## Consequences

- Portfolio visitors can run a browser demo after installing demo extras.
- Security/privacy expectations are explicit in the UI and API responses.

## Revisit triggers

- Auth/multi-user hosting requirements.
- Streaming responses or websocket traces.
