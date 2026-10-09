"""Shared enums and value objects."""

from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field, NonNegativeInt

SchemaVersion = Annotated[str, Field(pattern=r"^v\d+$", examples=["v1"])]


class AccessClassification(StrEnum):
    PUBLIC = "public"
    SYNTHETIC = "synthetic"
    INTERNAL = "internal"  # not for public demos


class RetrievalMode(StrEnum):
    TREE_FIRST = "tree-first"
    TREE_LEXICAL = "tree-lexical"
    HYBRID_COMPARISON = "hybrid-comparison"


class SourceRange(BaseModel):
    """Character offsets into the normalized document text (0-based, end exclusive)."""

    start_offset: NonNegativeInt
    end_offset: NonNegativeInt
    section_path: str | None = None
    page: int | None = Field(default=None, ge=1)

    def model_post_init(self, __context: object) -> None:
        if self.end_offset < self.start_offset:
            raise ValueError("end_offset must be >= start_offset")
