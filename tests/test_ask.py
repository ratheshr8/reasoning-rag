"""Baseline ask / citation / abstention tests."""

from pathlib import Path

from reasoning_rag.config import Settings
from reasoning_rag.ingestion import ingest_markdown_path
from reasoning_rag.models.common import AccessClassification, RetrievalMode
from reasoning_rag.qa import ask_document
from reasoning_rag.qa.citations import citations_resolve

CORPUS = Path(__file__).resolve().parents[1] / "data" / "corpus" / "v0" / "acme-widget-spec.md"


def test_ask_voltage_returns_cited_answer() -> None:
    result = ask_document(
        CORPUS,
        "What supply voltage does the Acme Widget require?",
        settings=Settings(),
        access_classification=AccessClassification.SYNTHETIC,
        retrieval_mode=RetrievalMode.TREE_FIRST,
    )
    assert result.answer.abstained is False
    assert result.evidence
    assert result.answer.claim_links
    assert "5V" in result.answer.text or "5v" in result.answer.text.lower()
    normalized = ingest_markdown_path(CORPUS, settings=Settings())
    assert citations_resolve(result.evidence, normalized) == []


def test_ask_firmware_abstains() -> None:
    result = ask_document(
        CORPUS,
        "How do I perform firmware updates on the Acme Widget?",
        settings=Settings(),
        access_classification=AccessClassification.SYNTHETIC,
    )
    assert result.answer.abstained is True
    assert result.answer.abstention_reason


def test_ask_unrelated_abstains() -> None:
    result = ask_document(
        CORPUS,
        "What is the capital of France?",
        settings=Settings(),
        access_classification=AccessClassification.SYNTHETIC,
    )
    assert result.answer.abstained is True


def test_lexical_mode_finds_error_code() -> None:
    result = ask_document(
        CORPUS,
        "What does error code E01 mean?",
        settings=Settings(),
        access_classification=AccessClassification.SYNTHETIC,
        retrieval_mode=RetrievalMode.TREE_LEXICAL,
    )
    assert result.answer.abstained is False
    blob = " ".join(item.exact_text for item in result.evidence)
    assert "Thermal" in blob or "thermal" in blob.lower()
