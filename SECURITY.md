# Security

## Reporting

If you find a vulnerability in this repository, open a private GitHub security advisory on [ratheshr8/reasoning-rag](https://github.com/ratheshr8/reasoning-rag) or contact the maintainer through the profile contact route. Do not file public issues for secrets or exploitable paths.

## Scope notes

- This project is a **prototype**. It is not a production multi-tenant service.
- Treat document content as untrusted input (prompt-injection risk). See [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md).
- Do not send confidential documents to external model providers unless you intentionally configure that and accept the risk. The demo surfaces a provider notice when the provider is not `fixture`.
- Default examples and evaluation fixtures are synthetic or redistributable public documents only (CC0-1.0 corpus v0).

## Controls in this release

- Upload size (`max_upload_bytes`) and Markdown extension allow-list
- Sample documents resolved from a server-side catalog (no client path)
- Citation resolution before claims are kept
- Placeholder API key rejection (`changeme`, etc.)
- Localhost default for `reasoning-rag serve`
- CI secret scan hook (gitleaks, best-effort)

## Maintainer practices

- Secrets belong in environment variables or a secret manager; `.env` is gitignored.
- Prefer fixture/mock model mode for local development when no API access is needed.
- Review [docs/LIMITATIONS.md](docs/LIMITATIONS.md) and [docs/SUPPORT.md](docs/SUPPORT.md) before exposing the demo beyond your machine.
