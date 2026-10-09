"""End-to-end ask pipeline: ingest → tree → retrieve → evidence → answer."""

from __future__ import annotations

import uuid
from pathlib import Path

from reasoning_rag.config import Settings, load_settings
from reasoning_rag.ingestion.service import ingest_markdown_path
from reasoning_rag.models.common import AccessClassification, RetrievalMode
from reasoning_rag.models.trace import AskResult, TraceEvent
from reasoning_rag.qa.answer import build_answer_from_evidence
from reasoning_rag.retrieval.assemble import assemble_evidence
from reasoning_rag.retrieval.lexical import score_nodes_lexical
from reasoning_rag.retrieval.tree_walk import select_nodes_tree_first
from reasoning_rag.tree.builder import build_document_tree


def ask_document(
    path: Path | str,
    question: str,
    *,
    settings: Settings | None = None,
    access_classification: AccessClassification = AccessClassification.PUBLIC,
    retrieval_mode: RetrievalMode | None = None,
) -> AskResult:
    """Answer a question from a Markdown document with citations or abstention."""
    cfg = settings or load_settings()
    mode = retrieval_mode or cfg.retrieval_mode
    trace_id = f"trace.{uuid.uuid4().hex[:12]}"
    events: list[TraceEvent] = []

    normalized = ingest_markdown_path(
        path,
        settings=cfg,
        access_classification=access_classification,
    )
    events.append(
        TraceEvent(
            component="ingestion",
            action="normalized",
            detail={
                "document_id": normalized.document.id,
                "sections": len(normalized.sections),
            },
        )
    )

    tree = build_document_tree(normalized, settings=cfg, summarize=False)
    events.append(
        TraceEvent(
            component="tree",
            action="built",
            detail={"nodes": len(tree.nodes), "root_id": tree.root_id},
        )
    )

    if mode == RetrievalMode.TREE_LEXICAL:
        selected = score_nodes_lexical(
            question, tree, normalized, top_k=cfg.retrieve_top_k
        )
        selector = "lexical"
    else:
        # TREE_FIRST and HYBRID_COMPARISON use tree-first baseline for Phase 4.
        selected = select_nodes_tree_first(
            question, tree, normalized, top_k=cfg.retrieve_top_k
        )
        selector = "tree-first"

    best_score = selected[0][1] if selected else 0.0
    events.append(
        TraceEvent(
            component="retrieval",
            action="selected_nodes",
            detail={
                "mode": mode.value,
                "selector": selector,
                "node_ids": [node_id for node_id, _, _ in selected],
                "scores": [score for _, score, _ in selected],
            },
        )
    )

    evidence = assemble_evidence(
        selected,
        tree,
        normalized,
        max_chars=cfg.evidence_max_chars,
    )
    events.append(
        TraceEvent(
            component="evidence",
            action="assembled",
            detail={"evidence_ids": [item.id for item in evidence]},
        )
    )

    answer = build_answer_from_evidence(
        question,
        evidence,
        min_score_hint=cfg.retrieve_min_score,
        best_score=best_score,
        trace_id=trace_id,
    )
    events.append(
        TraceEvent(
            component="answer",
            action="abstained" if answer.abstained else "answered",
            detail={
                "claim_count": len(answer.claim_links),
                "abstention_reason": answer.abstention_reason,
            },
        )
    )

    return AskResult(
        trace_id=trace_id,
        question=question,
        document_id=tree.document.id,
        retrieval_mode=mode,
        evidence=evidence,
        answer=answer,
        events=events,
    )
