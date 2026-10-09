"""End-to-end ask pipeline: ingest → tree → analyze → plan → retrieve → answer."""

from __future__ import annotations

import uuid
from pathlib import Path

from reasoning_rag.config import Settings, load_settings
from reasoning_rag.ingestion.service import ingest_markdown_path
from reasoning_rag.models.common import AccessClassification, RetrievalMode
from reasoning_rag.models.normalized import NormalizedDocument
from reasoning_rag.models.trace import AskResult, TraceEvent
from reasoning_rag.models.tree import DocumentTree
from reasoning_rag.planning.analyze import QueryAnalyzer, analyze_query
from reasoning_rag.planning.planner import build_retrieval_plan
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
    analyzer: QueryAnalyzer | None = None,
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

    analysis, used_fallback, analyzer_version = analyze_query(question, analyzer=analyzer)
    events.append(
        TraceEvent(
            component="query_analysis",
            action="fallback" if used_fallback else "analyzed",
            detail={
                "analyzer_version": analyzer_version,
                "intent": analysis.intent,
                "subquestions": analysis.subquestions,
                "used_fallback": used_fallback,
            },
        )
    )

    plan = build_retrieval_plan(
        analysis,
        tree,
        normalized,
        settings=cfg,
        retrieval_mode=mode,
    )
    events.append(
        TraceEvent(
            component="planner",
            action="planned",
            detail={
                "planner_version": plan.planner_version,
                "candidate_node_ids": plan.candidate_node_ids,
                "budgets": plan.budgets.model_dump(),
                "steps": [step.action for step in plan.steps],
            },
        )
    )

    selected = _select_from_plan(
        plan.candidate_node_ids,
        question=analysis.normalized_query,
        tree=tree,
        normalized=normalized,
        mode=mode,
        top_k=plan.budgets.max_nodes,
    )
    best_score = selected[0][1] if selected else 0.0
    events.append(
        TraceEvent(
            component="retrieval",
            action="selected_nodes",
            detail={
                "mode": mode.value,
                "selector": "plan-guided",
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
        query_analysis=analysis,
        retrieval_plan=plan,
        analysis_fallback=used_fallback,
        evidence=evidence,
        answer=answer,
        events=events,
    )


def _select_from_plan(
    candidate_ids: list[str],
    *,
    question: str,
    tree: DocumentTree,
    normalized: NormalizedDocument,
    mode: RetrievalMode,
    top_k: int,
) -> list[tuple[str, float, str]]:
    """Score candidates from the plan; fall back to full scoring if the plan is empty."""
    if mode == RetrievalMode.TREE_LEXICAL:
        scored = score_nodes_lexical(question, tree, normalized, top_k=max(top_k * 3, top_k))
    else:
        scored = select_nodes_tree_first(question, tree, normalized, top_k=max(top_k * 3, top_k))

    if not candidate_ids:
        return scored[:top_k]

    by_id = {node_id: (score, rationale) for node_id, score, rationale in scored}
    selected: list[tuple[str, float, str]] = []
    for node_id in candidate_ids:
        if node_id in by_id:
            score, rationale = by_id[node_id]
            selected.append((node_id, score, rationale))
        else:
            selected.append((node_id, 0.0, "plan-candidate"))
        if len(selected) >= top_k:
            break
    selected.sort(key=lambda item: (-item[1], item[0]))
    return selected
