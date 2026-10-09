"""Hierarchical multi-hop navigation from seed nodes."""

from __future__ import annotations

from reasoning_rag.models.normalized import NormalizedDocument
from reasoning_rag.models.query import QueryAnalysis
from reasoning_rag.models.tree import DocumentTree
from reasoning_rag.retrieval.lexical import score_nodes_lexical
from reasoning_rag.retrieval.tokenize import query_terms
from reasoning_rag.retrieval.tree_walk import select_nodes_tree_first


def expand_multihop(
    seeds: list[tuple[str, float, str]],
    *,
    analysis: QueryAnalysis,
    tree: DocumentTree,
    normalized: NormalizedDocument,
    max_hops: int,
    max_nodes: int,
    min_score: float,
    use_lexical: bool,
) -> tuple[list[tuple[str, float, str]], list[dict[str, object]]]:
    """Expand seed nodes via parent/child links for uncovered subquestions.

    Returns (selected_nodes, hop_trace_details).
    """
    selected: dict[str, tuple[float, str]] = {
        node_id: (score, rationale) for node_id, score, rationale in seeds
    }
    hop_trace: list[dict[str, object]] = []
    if max_hops <= 0 or max_nodes <= 0:
        return _sorted(selected)[:max_nodes], hop_trace

    questions = analysis.subquestions or [analysis.normalized_query]
    frontier = list(selected.keys())

    for hop in range(1, max_hops + 1):
        if len(selected) >= max_nodes:
            break
        neighbors: set[str] = set()
        for node_id in frontier:
            node = tree.nodes.get(node_id)
            if node is None:
                continue
            if node.parent_id and node.parent_id in tree.nodes:
                parent = tree.nodes[node.parent_id]
                if parent.metadata.get("kind") != "document_root":
                    neighbors.add(node.parent_id)
            neighbors.update(child_id for child_id in node.child_ids if child_id in tree.nodes)

        # Drop already selected.
        candidates = [node_id for node_id in neighbors if node_id not in selected]
        if not candidates:
            hop_trace.append({"hop": hop, "added": [], "reason": "no_neighbors"})
            break

        scored = _score_subset(
            questions,
            candidates,
            tree=tree,
            normalized=normalized,
            use_lexical=use_lexical,
            top_k=max_nodes,
        )
        added: list[str] = []
        for node_id, score, rationale in scored:
            if score < min_score:
                continue
            selected[node_id] = (score, f"hop{hop}:{rationale}")
            added.append(node_id)
            if len(selected) >= max_nodes:
                break

        hop_trace.append(
            {
                "hop": hop,
                "neighbors_considered": len(candidates),
                "added": added,
            }
        )
        frontier = added
        if not added:
            break

    return _sorted(selected)[:max_nodes], hop_trace


def _score_subset(
    questions: list[str],
    candidate_ids: list[str],
    *,
    tree: DocumentTree,
    normalized: NormalizedDocument,
    use_lexical: bool,
    top_k: int,
) -> list[tuple[str, float, str]]:
    merged: dict[str, tuple[float, str]] = {}
    for question in questions:
        if use_lexical:
            scored = score_nodes_lexical(question, tree, normalized, top_k=top_k * 2)
        else:
            scored = select_nodes_tree_first(question, tree, normalized, top_k=top_k * 2)
        for node_id, score, rationale in scored:
            if node_id not in candidate_ids:
                continue
            prior = merged.get(node_id)
            if prior is None or score > prior[0]:
                merged[node_id] = (score, rationale)

    # Title-term fallback if scorer returned nothing for neighbors.
    if not merged:
        terms = set()
        for question in questions:
            terms.update(query_terms(question))
        for node_id in candidate_ids:
            node = tree.nodes[node_id]
            title_terms = set(query_terms(node.title))
            overlap = terms & title_terms
            if overlap:
                merged[node_id] = (0.25 * len(overlap), f"neighbor_title_overlap={sorted(overlap)}")

    return sorted(
        ((node_id, score, rationale) for node_id, (score, rationale) in merged.items()),
        key=lambda item: (-item[1], item[0]),
    )


def _sorted(selected: dict[str, tuple[float, str]]) -> list[tuple[str, float, str]]:
    return sorted(
        ((node_id, score, rationale) for node_id, (score, rationale) in selected.items()),
        key=lambda item: (-item[1], item[0]),
    )
