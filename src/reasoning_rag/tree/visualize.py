"""Text visualization of a document tree."""

from __future__ import annotations

from reasoning_rag.models.tree import DocumentTree


def render_tree_text(tree: DocumentTree, *, include_summaries: bool = False) -> str:
    """Render an ASCII tree for inspection."""
    lines: list[str] = []

    def walk(node_id: str, prefix: str, is_last: bool) -> None:
        node = tree.nodes[node_id]
        connector = "└── " if is_last else "├── "
        if node_id == tree.root_id:
            label = f"{node.title} [root]"
            lines.append(label)
            child_prefix = ""
        else:
            label = f"{node.title} (L{node.level}, {node.id})"
            lines.append(f"{prefix}{connector}{label}")
            if include_summaries and node.summary:
                summary_prefix = f"{prefix}{'    ' if is_last else '│   '}    "
                lines.append(f"{summary_prefix}summary: {node.summary}")
            child_prefix = f"{prefix}{'    ' if is_last else '│   '}"

        children = node.child_ids
        for index, child_id in enumerate(children):
            walk(child_id, child_prefix, index == len(children) - 1)

    walk(tree.root_id, "", True)
    return "\n".join(lines) + "\n"
