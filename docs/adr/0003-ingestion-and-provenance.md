# ADR 0003 — Ingestion and provenance

- **Status:** Accepted
- **Date:** 2026-10-09
- **Decision owners:** Rathesh R

## Context

Phase 2 must ingest documents so later citation and tree stages can point back to exact source ranges. v1 is Markdown-only. Offsets must be stable, failures must be explicit, and sample data must be redistributable.

## Decision

1. **Adapter:** a dedicated Markdown ingest path (`.md` / `.markdown` only); PDF is out of scope.
2. **Normalization:** decode UTF-8; reject NUL; normalize CR/LF to `\n` and record a warning; character offsets always refer to the normalized text.
3. **Sections:** ATX headings (`#`–`######`) delimit sections; pre-heading content becomes a level-0 `Preamble` section when non-empty.
4. **Provenance:** each section carries `source_range` (and heading range when applicable) into the normalized text; document checksum is `sha256` of raw file bytes.
5. **Limits:** enforce `REASONING_RAG_MAX_UPLOAD_BYTES`; unsupported types and missing paths fail with typed errors (no silent repair).
6. **Corpus v0:** synthetic `acme-widget-spec.md` under `data/corpus/v0/` with a dataset card (CC0-1.0).

## Options considered

- **Store offsets into original bytes including CRLF.** Rejected: unstable across platforms.
- **HTML/CommonMark AST library.** Deferred: heading split is enough for Phase 2; can revisit if tables/lists need richer structure.
- **Fail hard on documents without headings.** Rejected: emit `no_headings` warning and a single preamble section so ingest remains inspectable.

## Consequences

- CLI `ingest` can emit JSON suitable for manual review and later tree building.
- Citation resolution in later phases can slice `NormalizedDocument.text` by offsets.
- PDF and binary formats remain unsupported until a new ADR.

## Revisit triggers

- Need for setext headings, Markdown inside HTML, or PDF page coordinates.
- Offset scheme proves inadequate for multi-file corpora.
