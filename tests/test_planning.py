"""Query analysis and bounded planner tests."""

from pathlib import Path
from typing import Any

from reasoning_rag.config import Settings
from reasoning_rag.ingestion import ingest_markdown_path
from reasoning_rag.models.common import AccessClassification, RetrievalMode
from reasoning_rag.planning import analyze_query, build_retrieval_plan
from reasoning_rag.planning.analyze import FixtureQueryAnalyzer
from reasoning_rag.qa import ask_document
from reasoning_rag.tree import build_document_tree

CORPUS = Path(__file__).resolve().parents[1] / "data" / "corpus" / "v0" / "acme-widget-spec.md"


class BrokenAnalyzer:
    version = "broken-v0"

    def analyze_raw(self, question: str) -> dict[str, Any]:
        return {"normalized_query": question, "intent": 123}  # invalid types


def test_rules_analyzer_detects_procedural_intent() -> None:
    analysis, fallback, version = analyze_query(
        "How do I perform firmware updates on the Acme Widget?",
        analyzer=FixtureQueryAnalyzer(),
    )
    assert fallback is False
    assert analysis.intent == "procedural"
    assert analysis.subquestions
    assert version == FixtureQueryAnalyzer.version


def test_malformed_analyzer_falls_back() -> None:
    analysis, fallback, _version = analyze_query(
        "What voltage is required?",
        analyzer=BrokenAnalyzer(),
    )
    assert fallback is True
    assert analysis.intent == "lookup"
    assert analysis.normalized_query


def test_plan_respects_node_budget() -> None:
    settings = Settings(plan_max_nodes=2, retrieve_top_k=5, plan_max_depth=6)
    normalized = ingest_markdown_path(
        CORPUS,
        settings=settings,
        access_classification=AccessClassification.SYNTHETIC,
    )
    tree = build_document_tree(normalized, settings=settings)
    analysis, _, _ = analyze_query("What supply voltage does the Acme Widget require?")
    plan = build_retrieval_plan(
        analysis,
        tree,
        normalized,
        settings=settings,
        retrieval_mode=RetrievalMode.TREE_FIRST,
    )
    assert plan.budgets.max_nodes == 2
    assert len(plan.candidate_node_ids) <= 2
    assert plan.steps[-1].action == "stop"
    assert all(
        tree.nodes[node_id].level <= plan.budgets.max_depth for node_id in plan.candidate_node_ids
    )


def test_ask_includes_plan_and_analysis() -> None:
    result = ask_document(
        CORPUS,
        "What is the maximum ambient temperature?",
        settings=Settings(),
        access_classification=AccessClassification.SYNTHETIC,
    )
    assert result.query_analysis is not None
    assert result.retrieval_plan is not None
    assert result.retrieval_plan.candidate_node_ids
    assert any(event.component == "planner" for event in result.events)
