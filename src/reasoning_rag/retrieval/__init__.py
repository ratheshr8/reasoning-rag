"""Baseline retrieval strategies."""

from reasoning_rag.retrieval.assemble import assemble_evidence
from reasoning_rag.retrieval.lexical import score_nodes_lexical
from reasoning_rag.retrieval.tree_walk import select_nodes_tree_first

__all__ = [
    "assemble_evidence",
    "score_nodes_lexical",
    "select_nodes_tree_first",
]
