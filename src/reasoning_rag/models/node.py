"""Hierarchical document node contract."""

from typing import Annotated, Any

from pydantic import BaseModel, Field

from reasoning_rag.models.common import SchemaVersion, SourceRange


class Node(BaseModel):
    schema_version: SchemaVersion = "v1"
    id: Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.:-]+$")]
    parent_id: Annotated[str, Field(min_length=1, max_length=128)] | None = None
    title: Annotated[str, Field(min_length=1, max_length=512)]
    summary: str | None = None
    level: Annotated[int, Field(ge=0, le=32)]
    source_range: SourceRange
    child_ids: list[Annotated[str, Field(min_length=1, max_length=128)]] = Field(
        default_factory=list
    )
    metadata: dict[str, Any] = Field(default_factory=dict)
