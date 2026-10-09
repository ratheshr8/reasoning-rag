"""Evaluation case contract."""

from typing import Annotated, Any

from pydantic import BaseModel, Field

from reasoning_rag.models.common import SchemaVersion


class EvaluationCase(BaseModel):
    schema_version: SchemaVersion = "v1"
    id: Annotated[str, Field(min_length=1, max_length=128)]
    question: Annotated[str, Field(min_length=1)]
    document_ids: list[Annotated[str, Field(min_length=1)]] = Field(min_length=1)
    corpus_version: Annotated[str, Field(min_length=1, max_length=64)]
    expected_evidence_sections: list[str] = Field(default_factory=list)
    expected_answer_properties: dict[str, Any] = Field(default_factory=dict)
    answerable: bool = True
    difficulty: Annotated[str, Field(min_length=1, max_length=32)] = "easy"
    tags: list[str] = Field(default_factory=list)
