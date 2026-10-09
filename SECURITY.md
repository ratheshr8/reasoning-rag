# Security

## Reporting

If you find a vulnerability in this repository, open a private GitHub security advisory on [ratheshr8/reasoning-rag](https://github.com/ratheshr8/reasoning-rag) or contact the maintainer through the profile contact route. Do not file public issues for secrets or exploitable paths.

## Scope notes

- This project is a **prototype**. It is not a production multi-tenant service.
- Treat document content as untrusted input (prompt-injection risk).
- Do not send confidential documents to external model providers unless you intentionally configure that and accept the risk.
- Default examples and evaluation fixtures must be synthetic or redistributable public documents only.

## Maintainer practices

- Secrets belong in environment variables or a secret manager; `.env` is gitignored.
- Prefer fixture/mock model mode for local development when no API access is needed.
- Citation resolution and upload limits are part of later phases; until then, assume parsers and model calls are incomplete and unsafe for untrusted uploads at scale.
