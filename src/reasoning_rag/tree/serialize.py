"""JSON serialization for document trees."""

from __future__ import annotations

from pathlib import Path

from reasoning_rag.models.tree import DocumentTree


def dump_tree_json(tree: DocumentTree, *, indent: int = 2) -> str:
    return tree.model_dump_json(indent=indent)


def load_tree_json(payload: str | bytes) -> DocumentTree:
    return DocumentTree.model_validate_json(payload)


def write_tree_json(tree: DocumentTree, path: Path | str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dump_tree_json(tree) + "\n", encoding="utf-8")


def read_tree_json(path: Path | str) -> DocumentTree:
    return load_tree_json(Path(path).read_text(encoding="utf-8"))
