# Contributing

Thanks for interest in `reasoning-rag`. This is a portfolio prototype with a narrow Phase scope; prefer small, reviewable changes that match the current phase in [docs/ROADMAP.md](docs/ROADMAP.md).

## Development setup

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Checks

```bash
ruff check src tests
ruff format --check src tests
mypy
pytest
```

Do not commit secrets, employer/customer documents, or unverified benchmark claims.

## Pull requests

- Keep diffs focused on one concern.
- Update docs/ADRs when behavior or trade-offs change.
- Mark status honestly (prototype vs planned).
