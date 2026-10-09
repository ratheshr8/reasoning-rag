"""Document knowledge-tree contract."""

from __future__ import annotations

from typing import Annotated, Self

from pydantic import BaseModel, Field, model_validator

from reasoning_rag.models.common import SchemaVersion
from reasoning_rag.models.document import Document
from reasoning_rag.models.node import Node


class DocumentTree(BaseModel):
    """Hierarchical tree of nodes with stable IDs and source ranges."""

    schema_version: SchemaVersion = "v1"
    document: Document
    root_id: Annotated[str, Field(min_length=1, max_length=128)]
    nodes: dict[str, Node]
    builder_version: Annotated[str, Field(min_length=1, max_length=64)] = "tree-v1"
    summarizer_provider: str | None = None
    summarizer_model: str | None = None
    prompt_version: str | None = None

    @model_validator(mode="after")
    def validate_tree_integrity(self) -> Self:
        if self.root_id not in self.nodes:
            raise ValueError(f"root_id '{self.root_id}' missing from nodes")
        for node_id, node in self.nodes.items():
            if node.id != node_id:
                raise ValueError(f"node key '{node_id}' does not match node.id '{node.id}'")
            if node.parent_id is not None and node.parent_id not in self.nodes:
                raise ValueError(f"node '{node_id}' parent '{node.parent_id}' missing")
            for child_id in node.child_ids:
                if child_id not in self.nodes:
                    raise ValueError(f"node '{node_id}' child '{child_id}' missing")
                if self.nodes[child_id].parent_id != node_id:
                    raise ValueError(
                        f"child '{child_id}' parent_id does not point back to '{node_id}'"
                    )
        return self
