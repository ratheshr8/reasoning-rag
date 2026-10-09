"""Schema validation tests for domain contracts."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from reasoning_rag.models import (
    Answer,
    Document,
    EvaluationCase,
    Evidence,
    Node,
    QueryAnalysis,
    RetrievalPlan,
    SourceRange,
)


def test_source_range_rejects_inverted_offsets() -> None:
    with pytest.raises(ValidationError):
        SourceRange(start_offset=10, end_offset=5)


def test_document_accepts_markdown_public_sample() -> None:
    doc = Document(
        id="doc.rfc.sample",
        source_name="sample.md",
        checksum="sha256:0123456789abcdef",
        ingested_at=datetime.now(UTC),
        parser_version="md-v0",
    )
    assert doc.media_type == "text/markdown"


def test_answer_requires_reason_when_abstaining() -> None:
    with pytest.raises(ValidationError):
        Answer(abstained=True, trace_id="trace-1")


def test_answer_abstention_ok() -> None:
    answer = Answer(
        abstained=True,
        abstention_reason="no supporting evidence",
        trace_id="trace-1",
    )
    assert answer.text == ""


def test_node_and_evidence_round_trip_json() -> None:
    node = Node(
        id="n1",
        title="Intro",
        level=1,
        source_range=SourceRange(start_offset=0, end_offset=12, section_path="Intro"),
        child_ids=["n2"],
    )
    evidence = Evidence(
        id="e1",
        document_id="doc.1",
        node_id=node.id,
        exact_text="hello world",
        source_range=node.source_range,
        provenance="fixture",
    )
    restored = Evidence.model_validate_json(evidence.model_dump_json())
    assert restored.node_id == "n1"


def test_query_plan_and_eval_defaults() -> None:
    analysis = QueryAnalysis(
        normalized_query="What is X?",
        intent="lookup",
    )
    plan = RetrievalPlan(candidate_node_ids=["n1"])
    case = EvaluationCase(
        id="case-1",
        question="What is X?",
        document_ids=["doc.1"],
        corpus_version="corpus-v0",
    )
    assert analysis.expected_answer_type == "factual"
    assert plan.strategy.value == "tree-first"
    assert case.answerable is True
