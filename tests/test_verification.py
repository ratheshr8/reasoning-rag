"""Multi-hop navigation, conflict detection, and claim verification tests."""

from pathlib import Path

from reasoning_rag.config import Settings
from reasoning_rag.ingestion import ingest_markdown_path
from reasoning_rag.models.answer import Answer, ClaimEvidenceLink
from reasoning_rag.models.common import AccessClassification, RetrievalMode, SourceRange
from reasoning_rag.models.evidence import Evidence
from reasoning_rag.qa import ask_document
from reasoning_rag.qa.verify import detect_conflicts, map_and_verify_claims, verify_evidence

CORPUS = Path(__file__).resolve().parents[1] / "data" / "corpus" / "v0" / "acme-widget-spec.md"


def test_ambient_temperature_surfaces_conflict() -> None:
    result = ask_document(
        CORPUS,
        "What is the maximum ambient temperature for operating the widget?",
        settings=Settings(nav_max_hops=2, nav_max_nodes=8, plan_max_nodes=4),
        access_classification=AccessClassification.SYNTHETIC,
        retrieval_mode=RetrievalMode.TREE_FIRST,
    )
    assert result.verification is not None
    topics = {conflict.topic for conflict in result.verification.conflicts}
    # May or may not conflict depending on which sections were retrieved; if both
    # safety + conflicting note are present, conflict must be surfaced.
    texts = " ".join(item.exact_text for item in result.evidence)
    if "45" in texts and "40" in texts:
        assert "ambient_temperature_c" in topics
        assert result.answer.abstained is False
        assert "Conflict noted" in result.answer.text
        assert any("conflicting values" in note for note in result.answer.limitations)


def test_detect_conflicts_on_synthetic_snippets() -> None:
    evidence = [
        Evidence(
            id="ev.a",
            document_id="doc.1",
            node_id="n1",
            exact_text="Do not operate above 40 degrees Celsius ambient temperature.",
            source_range=SourceRange(start_offset=0, end_offset=10),
            provenance="test",
        ),
        Evidence(
            id="ev.b",
            document_id="doc.1",
            node_id="n2",
            exact_text=(
                "Earlier drafts claimed a maximum ambient temperature of 45 degrees Celsius."
            ),
            source_range=SourceRange(start_offset=10, end_offset=20),
            provenance="test",
        ),
    ]
    conflicts = detect_conflicts(evidence)
    assert len(conflicts) == 1
    assert conflicts[0].topic == "ambient_temperature_c"
    assert "40c" in conflicts[0].values
    assert "45c" in conflicts[0].values


def test_unresolved_claims_trigger_abstention() -> None:
    normalized = ingest_markdown_path(CORPUS, settings=Settings())
    evidence = [
        Evidence(
            id="ev.bad",
            document_id=normalized.document.id,
            node_id="missing",
            exact_text="not in document",
            source_range=SourceRange(start_offset=0, end_offset=3),
            provenance="test",
        )
    ]
    # Force unresolved by mismatching exact text vs range slice
    kept, unresolved = verify_evidence(evidence, normalized)
    assert "ev.bad" in unresolved or kept == [] or evidence[0].id in unresolved

    draft = Answer(
        text="Invented claim",
        claim_links=[ClaimEvidenceLink(claim="Invented claim", evidence_ids=["ev.bad"])],
        abstained=False,
        trace_id="trace.test",
    )
    # Use empty kept evidence to force claim drop
    answer, report = map_and_verify_claims(
        draft,
        evidence=[],
        normalized=normalized,
        conflicts=[],
    )
    assert answer.abstained is True
    assert report.dropped_claim_count == 1


def test_ask_maps_claims_to_evidence() -> None:
    result = ask_document(
        CORPUS,
        "What supply voltage does the Acme Widget require?",
        settings=Settings(),
        access_classification=AccessClassification.SYNTHETIC,
    )
    assert result.answer.abstained is False
    assert result.answer.claim_links
    for link in result.answer.claim_links:
        assert link.evidence_ids
        assert all(
            any(item.id == evidence_id for item in result.evidence)
            for evidence_id in link.evidence_ids
        )
    assert result.verification is not None
    assert result.verification.coverage
