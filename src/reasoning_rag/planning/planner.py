"""Bounded retrieval planner: schema-valid plans within depth/node/call budgets."""

from __future__ import annotations

from reasoning_rag.config import Settings
from reasoning_rag.models.common import RetrievalMode
from reasoning_rag.models.normalized import NormalizedDocument
from reasoning_rag.models.query import QueryAnalysis
from reasoning_rag.models.retrieval import RetrievalBudgets, RetrievalPlan, RetrievalStep
from reasoning_rag.models.tree import DocumentTree
from reasoning_rag.retrieval.lexical import score_nodes_lexical
from reasoning_rag.retrieval.tree_walk import select_nodes_tree_first

PLANNER_VERSION = "rules-planner-v1"


def build_retrieval_plan(
    analysis: QueryAnalysis,
    tree: DocumentTree,
    normalized: NormalizedDocument,
    *,
    settings: Settings,
    retrieval_mode: RetrievalMode,
) -> RetrievalPlan:
    """Create an inspectable, budget-bounded retrieval plan."""
    budgets = RetrievalBudgets(
        max_depth=settings.plan_max_depth,
        max_nodes=min(settings.plan_max_nodes, settings.retrieve_top_k),
        max_model_calls=settings.plan_max_model_calls,
        max_context_tokens=settings.plan_max_context_tokens,
    )

    steps: list[RetrievalStep] = [
        RetrievalStep(
            action="analyze_query",
            target_node_ids=[],
            rationale=(
                f"intent={analysis.intent}; subquestions={len(analysis.subquestions)}; "
                f"entities={analysis.entities[:5]}"
            ),
        )
    ]

    # Fixture planner consumes zero model calls; enforce budget explicitly.
    model_calls_used = 0
    if model_calls_used > budgets.max_model_calls:
        steps.append(
            RetrievalStep(
                action="stop",
                rationale="model call budget exhausted before scoring",
            )
        )
        return RetrievalPlan(
            strategy=retrieval_mode,
            steps=steps,
            candidate_node_ids=[],
            budgets=budgets,
            planner_version=PLANNER_VERSION,
        )

    top_k = max(budgets.max_nodes, 1)
    if retrieval_mode == RetrievalMode.TREE_LEXICAL:
        scored = score_nodes_lexical(
            analysis.normalized_query, tree, normalized, top_k=top_k * 2
        )
        score_action = "score_lexical"
    else:
        scored = select_nodes_tree_first(
            analysis.normalized_query, tree, normalized, top_k=top_k * 2
        )
        score_action = "score_tree_first"

    # Also score subquestions lightly and merge unique node ids (still bounded).
    merged: dict[str, tuple[float, str]] = {
        node_id: (score, rationale) for node_id, score, rationale in scored
    }
    for sub_q in analysis.subquestions[1 : 1 + max(0, budgets.max_model_calls)]:
        # Subquestion expansion is rules-only (no model call).
        extra = (
            score_nodes_lexical(sub_q, tree, normalized, top_k=top_k)
            if retrieval_mode == RetrievalMode.TREE_LEXICAL
            else select_nodes_tree_first(sub_q, tree, normalized, top_k=top_k)
        )
        for node_id, score, rationale in extra:
            prior = merged.get(node_id)
            if prior is None or score > prior[0]:
                merged[node_id] = (score, f"{rationale}; via_subquestion")

    steps.append(
        RetrievalStep(
            action=score_action,
            target_node_ids=list(merged.keys())[: budgets.max_nodes * 2],
            rationale=f"scored={len(merged)} unique nodes before depth/node caps",
        )
    )

    ranked = sorted(merged.items(), key=lambda item: (-item[1][0], item[0]))
    candidates: list[str] = []
    for node_id, (_score, _rationale) in ranked:
        node = tree.nodes.get(node_id)
        if node is None:
            continue
        if node.level > budgets.max_depth:
            continue
        candidates.append(node_id)
        if len(candidates) >= budgets.max_nodes:
            break

    steps.append(
        RetrievalStep(
            action="select_candidates",
            target_node_ids=candidates,
            rationale=(
                f"applied max_depth={budgets.max_depth}, "
                f"max_nodes={budgets.max_nodes}, "
                f"max_model_calls={budgets.max_model_calls}"
            ),
        )
    )
    steps.append(
        RetrievalStep(
            action="stop",
            target_node_ids=candidates,
            rationale="budget-aware stopping criteria reached",
        )
    )

    return RetrievalPlan(
        strategy=retrieval_mode,
        steps=steps,
        candidate_node_ids=candidates,
        budgets=budgets,
        planner_version=PLANNER_VERSION,
    )
