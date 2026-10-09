# Changelog

All notable changes to this project are documented here.

## [0.1.0] — 2026-10-09

First public prototype tag.

### Added

- End-to-end tree-first ask path with planning, multi-hop navigation, citations, abstention, and conflict surfacing
- Evaluation harness (`eval-v0`) with tree-first and lexical baselines
- Local demo UI and validated API (`reasoning-rag serve`)
- Threat model, limitations, and support status docs
- Synthetic Markdown corpus under CC0-1.0

### Security

- Upload size/extension limits
- Provider notice when document text may leave the machine
- Placeholder API key rejection
- CI secret scan hook (gitleaks, best-effort)

### Known gaps

- Vector baseline remains a placeholder
- Not a multi-tenant production service

[0.1.0]: https://github.com/ratheshr8/reasoning-rag/releases/tag/v0.1.0
