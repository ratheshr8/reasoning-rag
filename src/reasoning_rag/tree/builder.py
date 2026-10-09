"""Deterministic heading-based knowledge tree builder."""

from __future__ import annotations

from reasoning_rag.config import Settings
from reasoning_rag.models.common import SourceRange
from reasoning_rag.models.node import Node
from reasoning_rag.models.normalized import NormalizedDocument
from reasoning_rag.models.tree import DocumentTree
from reasoning_rag.providers.base import Summarizer
from reasoning_rag.providers.fixture import get_summarizer

BUILDER_VERSION = "tree-v1"


class TreeBuildError(Exception):
    def __init__(self, message: str, *, code: str = "tree_build_error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


def build_document_tree(
    normalized: NormalizedDocument,
    *,
    settings: Settings,
    summarize: bool = False,
    summarizer: Summarizer | None = None,
) -> DocumentTree:
    """Build a parent/child tree from normalized heading sections.

    Every node maps to a source range. Summary generation is optional and records
    provider/model/prompt versions when enabled.
    """
    if len(normalized.sections) > settings.tree_max_nodes:
        raise TreeBuildError(
            f"section count {len(normalized.sections)} exceeds "
            f"tree_max_nodes={settings.tree_max_nodes}",
            code="too_many_nodes",
        )

    doc = normalized.document
    root_id = f"{doc.id}:root"
    root = Node(
        id=root_id,
        parent_id=None,
        title=doc.source_name,
        summary=None,
        level=0,
        source_range=SourceRange(
            start_offset=0,
            end_offset=len(normalized.text),
            section_path=doc.source_name,
        ),
        child_ids=[],
        metadata={"kind": "document_root"},
    )
    nodes: dict[str, Node] = {root_id: root}

    # Stack of (heading_level, node_id). Root is level -1 sentinel.
    stack: list[tuple[int, str]] = [(-1, root_id)]

    active_summarizer: Summarizer | None = None
    summaries_made = 0
    if summarize:
        active_summarizer = summarizer or get_summarizer(settings)

    for section in normalized.sections:
        # Nest by Markdown heading level (preamble=0, H1=1..H6=6).
        # Parent is the nearest prior node with a strictly smaller level.
        node_level = section.level
        while stack and stack[-1][0] >= node_level:
            stack.pop()
        if not stack:
            raise TreeBuildError("internal stack underflow while assigning parents")

        parent_id = stack[-1][1]
        node = Node(
            id=section.id,
            parent_id=parent_id,
            title=section.title,
            summary=None,
            level=node_level,
            source_range=section.source_range,
            child_ids=[],
            metadata={
                "kind": "section",
                "section_id": section.id,
                "heading_level": section.level,
            },
        )

        if active_summarizer is not None and summaries_made < settings.tree_max_summaries:
            node.summary = active_summarizer.summarize(
                title=section.title,
                text=section.text,
                max_chars=settings.tree_summary_max_chars,
            )
            node.metadata["summary_provider"] = active_summarizer.provider
            node.metadata["summary_model"] = active_summarizer.model
            node.metadata["prompt_version"] = active_summarizer.prompt_version
            summaries_made += 1

        nodes[node.id] = node
        nodes[parent_id].child_ids.append(node.id)
        stack.append((node_level, node.id))

    return DocumentTree(
        document=doc,
        root_id=root_id,
        nodes=nodes,
        builder_version=BUILDER_VERSION,
        summarizer_provider=active_summarizer.provider if active_summarizer else None,
        summarizer_model=active_summarizer.model if active_summarizer else None,
        prompt_version=active_summarizer.prompt_version if active_summarizer else None,
    )
