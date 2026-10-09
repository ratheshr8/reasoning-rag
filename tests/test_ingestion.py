"""Markdown ingestion and provenance tests."""

from pathlib import Path

import pytest

from reasoning_rag.config import Settings
from reasoning_rag.ingestion import UnsupportedMediaTypeError, ValidationFailedError, ingest_markdown_path
from reasoning_rag.models.common import AccessClassification

CORPUS = Path(__file__).resolve().parents[1] / "data" / "corpus" / "v0" / "acme-widget-spec.md"


def test_ingest_sample_corpus_has_resolvable_sections() -> None:
    result = ingest_markdown_path(
        CORPUS,
        settings=Settings(),
        access_classification=AccessClassification.SYNTHETIC,
    )
    assert result.document.media_type == "text/markdown"
    assert result.document.parser_version == "md-v1"
    assert result.document.checksum.startswith("sha256:")
    assert len(result.sections) >= 3

    for section in result.sections:
        start = section.source_range.start_offset
        end = section.source_range.end_offset
        assert 0 <= start <= end <= len(result.text)
        assert result.text[start:end] == section.text


def test_section_titles_include_power_and_safety() -> None:
    result = ingest_markdown_path(CORPUS, settings=Settings())
    titles = {section.title for section in result.sections}
    assert "Power requirements" in titles
    assert "Safety limits" in titles


def test_rejects_unsupported_extension(tmp_path: Path) -> None:
    pdf = tmp_path / "note.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    with pytest.raises(UnsupportedMediaTypeError):
        ingest_markdown_path(pdf, settings=Settings())


def test_rejects_oversized_file(tmp_path: Path) -> None:
    path = tmp_path / "big.md"
    path.write_text("# Title\n\nbody\n", encoding="utf-8")
    settings = Settings(max_upload_bytes=8)
    with pytest.raises(ValidationFailedError) as exc:
        ingest_markdown_path(path, settings=settings)
    assert exc.value.code == "file_too_large"


def test_rejects_missing_path(tmp_path: Path) -> None:
    with pytest.raises(ValidationFailedError) as exc:
        ingest_markdown_path(tmp_path / "missing.md", settings=Settings())
    assert exc.value.code == "not_found"


def test_no_headings_warning(tmp_path: Path) -> None:
    path = tmp_path / "flat.md"
    path.write_text("just a paragraph\n", encoding="utf-8")
    result = ingest_markdown_path(path, settings=Settings())
    codes = {warning.code.value for warning in result.warnings}
    assert "no_headings" in codes
    assert result.sections[0].title == "Preamble"


def test_crlf_normalized_and_offsets_stable(tmp_path: Path) -> None:
    path = tmp_path / "crlf.md"
    path.write_bytes(b"# Title\r\n\r\nHello\r\n")
    result = ingest_markdown_path(path, settings=Settings())
    codes = {warning.code.value for warning in result.warnings}
    assert "line_ending_normalized" in codes
    assert "\r" not in result.text
    section = result.sections[0]
    assert result.text[section.source_range.start_offset : section.source_range.end_offset] == (
        section.text
    )
