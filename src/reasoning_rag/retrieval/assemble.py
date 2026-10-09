"""Evidence assembly from selected tree nodes."""

from __future__ import annotations

from reasoning_rag.models.evidence import Evidence
from reasoning_rag.models.normalized import NormalizedDocument
from reasoning_rag.models.tree import DocumentTree


def assemble_evidence(
    selected: list[tuple[str, float, str]],
    tree: DocumentTree,
    normalized: NormalizedDocument,
    *,
    max_chars: int,
) -> list[Evidence]:
    """Build Evidence records with exact text slices and resolvable source ranges."""
    by_section = {section.id: section for section in normalized.sections}
    evidence: list[Evidence] = []
    seen_ranges: set[tuple[int, int]] = set()

    for index, (node_id, _score, rationale) in enumerate(selected):
        node = tree.nodes.get(node_id)
        if node is None or node.metadata.get("kind") == "document_root":
            continue
        section = by_section.get(node_id)
        if section is None:
            continue
        key = (section.source_range.start_offset, section.source_range.end_offset)
        if key in seen_ranges:
            continue
        seen_ranges.add(key)

        exact = section.text.strip()
        if not exact:
            continue
        if len(exact) > max_chars:
            exact = exact[: max_chars - 1].rstrip() + "…"

        evidence.append(
            Evidence(
                id=f"ev.{index:04d}",
                document_id=tree.document.id,
                node_id=node_id,
                exact_text=exact,
                source_range=section.source_range,
                provenance="tree-section",
                relevance_rationale=rationale,
            )
        )
    return evidence
