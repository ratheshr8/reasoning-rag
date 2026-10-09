"""Knowledge tree construction and round-trip tests."""

from pathlib import Path

import pytest

from reasoning_rag.config import Settings
from reasoning_rag.ingestion import ingest_markdown_path
from reasoning_rag.models.common import AccessClassification
from reasoning_rag.tree import (
    TreeBuildError,
    build_document_tree,
    dump_tree_json,
    load_tree_json,
    render_tree_text,
)

CORPUS = Path(__file__).resolve().parents[1] / "data" / "corpus" / "v0" / "acme-widget-spec.md"


def _normalized():
    return ingest_markdown_path(
        CORPUS,
        settings=Settings(),
        access_classification=AccessClassification.SYNTHETIC,
    )


def test_build_tree_every_node_has_source_range() -> None:
    tree = build_document_tree(_normalized(), settings=Settings(), summarize=False)
    assert tree.root_id in tree.nodes
    assert len(tree.nodes) == len(_normalized().sections) + 1
    for node in tree.nodes.values():
        start = node.source_range.start_offset
        end = node.source_range.end_offset
        assert 0 <= start <= end


def test_heading_nesting_power_contains_battery() -> None:
    tree = build_document_tree(_normalized(), settings=Settings())
    by_title = {node.title: node for node in tree.nodes.values()}
    power = by_title["Power requirements"]
    battery = by_title["Battery mode"]
    assert battery.parent_id == power.id
    assert battery.id in power.child_ids


def test_round_trip_json() -> None:
    tree = build_document_tree(_normalized(), settings=Settings(), summarize=True)
    restored = load_tree_json(dump_tree_json(tree))
    assert restored.root_id == tree.root_id
    assert set(restored.nodes) == set(tree.nodes)
    assert restored.summarizer_provider == "fixture"
    assert restored.prompt_version == "summary-extract-v1"
    for node_id, node in restored.nodes.items():
        assert node.source_range == tree.nodes[node_id].source_range


def test_visualization_contains_titles() -> None:
    tree = build_document_tree(_normalized(), settings=Settings())
    text = render_tree_text(tree)
    assert "Safety limits" in text
    assert "Appendix A" in text or "Appendix A — Error codes" in text


def test_summary_budget_respected(tmp_path: Path) -> None:
    path = tmp_path / "many.md"
    parts = ["# Doc\n"] + [f"## S{i}\n\nBody {i}.\n" for i in range(5)]
    path.write_text("".join(parts), encoding="utf-8")
    normalized = ingest_markdown_path(path, settings=Settings())
    settings = Settings(tree_max_summaries=2)
    tree = build_document_tree(normalized, settings=settings, summarize=True)
    summarized = [n for n in tree.nodes.values() if n.summary is not None]
    assert len(summarized) == 2


def test_too_many_nodes_fails(tmp_path: Path) -> None:
    path = tmp_path / "big.md"
    path.write_text("# A\n\n## B\n\ntext\n", encoding="utf-8")
    normalized = ingest_markdown_path(path, settings=Settings())
    with pytest.raises(TreeBuildError) as exc:
        build_document_tree(normalized, settings=Settings(tree_max_nodes=1))
    assert exc.value.code == "too_many_nodes"
