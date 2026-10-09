"""Tree-first node selection: prefer title/path matches, then lexical fallback."""

from __future__ import annotations

from reasoning_rag.models.normalized import NormalizedDocument
from reasoning_rag.models.tree import DocumentTree
from reasoning_rag.retrieval.lexical import score_nodes_lexical
from reasoning_rag.retrieval.tokenize import query_terms, tokenize


def select_nodes_tree_first(
    question: str,
    tree: DocumentTree,
    normalized: NormalizedDocument,
    *,
    top_k: int,
) -> list[tuple[str, float, str]]:
    """Select nodes by hierarchy-aware cues, then lexical scores.

    Strategy:
    1. Score section nodes lexically (title + body).
    2. Boost nodes whose title tokens overlap the query (structural cue).
    3. Prefer shallower, more specific matched sections over the document root.
    """
    terms = set(query_terms(question))
    lexical = score_nodes_lexical(question, tree, normalized, top_k=max(top_k * 3, top_k))
    if not lexical:
        return []

    boosted: list[tuple[str, float, str]] = []
    for node_id, score, rationale in lexical:
        node = tree.nodes[node_id]
        title_tokens = set(tokenize(node.title))
        title_overlap = terms & title_tokens
        path_boost = 0.35 * len(title_overlap)
        # Mild preference for mid-depth sections over very deep noise.
        depth_factor = 1.0 + min(node.level, 4) * 0.02
        final = (score + path_boost) * depth_factor
        detail = rationale
        if title_overlap:
            detail = f"{rationale}; title_match={sorted(title_overlap)}"
        boosted.append((node_id, final, detail))

    boosted.sort(key=lambda item: (-item[1], item[0]))
    return boosted[:top_k]
