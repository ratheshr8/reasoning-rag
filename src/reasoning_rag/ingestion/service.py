"""Ingestion orchestration: validate path/size/type, parse Markdown, attach provenance."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from reasoning_rag.config import Settings, load_settings
from reasoning_rag.ingestion.checksum import document_id_from_name, sha256_prefixed
from reasoning_rag.ingestion.errors import UnsupportedMediaTypeError, ValidationFailedError
from reasoning_rag.ingestion.markdown import (
    PARSER_VERSION,
    allowed_markdown_extension,
    normalize_text,
    parse_markdown_sections,
)
from reasoning_rag.models.common import AccessClassification
from reasoning_rag.models.document import Document
from reasoning_rag.models.normalized import NormalizedDocument, ParserWarning


def ingest_markdown_path(
    path: Path | str,
    *,
    settings: Settings | None = None,
    access_classification: AccessClassification = AccessClassification.PUBLIC,
) -> NormalizedDocument:
    """Ingest a Markdown file into a normalized, provenance-aware document."""
    cfg = settings or load_settings()
    file_path = Path(path)

    if not file_path.exists():
        raise ValidationFailedError(f"path does not exist: {file_path}", code="not_found")
    if not file_path.is_file():
        raise ValidationFailedError(f"path is not a file: {file_path}", code="not_a_file")
    if not allowed_markdown_extension(file_path.suffix):
        raise UnsupportedMediaTypeError(
            f"unsupported extension '{file_path.suffix or '(none)'}'; expected .md or .markdown"
        )

    size = file_path.stat().st_size
    if size > cfg.max_upload_bytes:
        raise ValidationFailedError(
            f"file size {size} bytes exceeds max_upload_bytes={cfg.max_upload_bytes}",
            code="file_too_large",
        )
    if size == 0:
        # Still produce a normalized empty document with warnings rather than hard-fail,
        # so callers can inspect provenance structure. Empty is valid but warned.
        raw = b""
    else:
        raw = file_path.read_bytes()
        if len(raw) > cfg.max_upload_bytes:
            raise ValidationFailedError(
                f"file size {len(raw)} bytes exceeds max_upload_bytes={cfg.max_upload_bytes}",
                code="file_too_large",
            )

    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValidationFailedError(
            f"file is not valid UTF-8: {exc.reason} at byte {exc.start}",
            code="invalid_encoding",
        ) from exc

    try:
        text, norm_warnings = normalize_text(decoded)
    except ValueError as exc:
        raise ValidationFailedError(str(exc), code="invalid_content") from exc

    checksum = sha256_prefixed(raw)
    doc_id = document_id_from_name(file_path.name, checksum.removeprefix("sha256:"))
    sections, parse_warnings = parse_markdown_sections(text, document_id=doc_id)
    warnings: list[ParserWarning] = [*norm_warnings, *parse_warnings]

    document = Document(
        id=doc_id,
        source_name=file_path.name,
        checksum=checksum,
        media_type="text/markdown",
        ingested_at=datetime.now(UTC),
        parser_version=PARSER_VERSION,
        access_classification=access_classification,
    )

    return NormalizedDocument(
        document=document,
        text=text,
        sections=sections,
        warnings=warnings,
        parser="markdown",
        parser_version=PARSER_VERSION,
    )
