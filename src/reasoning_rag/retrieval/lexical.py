"""Lexical (keyword overlap) scoring over tree nodes."""

from __future__ import annotations

from reasoning_rag.models.normalized import NormalizedDocument
from reasoning_rag.models.tree import DocumentTree
from reasoning_rag.retrieval.tokenize import query_terms, tokenize


def score_nodes_lexical(
    question: str,
    tree: DocumentTree,
    normalized: NormalizedDocument,
    *,
    top_k: int,
) -> list[tuple[str, float, str]]:
    """Return (node_id, score, rationale) for section nodes, highest first."""
    terms = query_terms(question)
    if not terms:
        return []

    section_text = {section.id: section.text for section in normalized.sections}
    scored: list[tuple[str, float, str]] = []
    for node_id, node in tree.nodes.items():
        if node.metadata.get("kind") == "document_root":
            continue
        text = section_text.get(node_id, "")
        haystack = f"{node.title}\n{text}\n{node.summary or ''}"
        tokens = tokenize(haystack)
        if not tokens:
            continue
        token_set = set(tokens)
        hits = [term for term in terms if term in token_set]
        if not hits:
            continue
        # Title matches weigh more than body-only overlap.
        title_tokens = set(tokenize(node.title))
        title_hits = sum(1 for term in terms if term in title_tokens)
        score = (len(hits) / len(terms)) + (0.25 * title_hits)
        rationale = f"lexical overlap terms={hits}"
        scored.append((node_id, score, rationale))

    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored[:top_k]
