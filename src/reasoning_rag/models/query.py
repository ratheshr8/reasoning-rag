"""Query analysis contract."""

from typing import Annotated

from pydantic import BaseModel, Field

from reasoning_rag.models.common import SchemaVersion


class QueryAnalysis(BaseModel):
    schema_version: SchemaVersion = "v1"
    normalized_query: Annotated[str, Field(min_length=1, max_length=4000)]
    intent: Annotated[str, Field(min_length=1, max_length=128)]
    entities: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    subquestions: list[str] = Field(default_factory=list)
    expected_answer_type: Annotated[str, Field(min_length=1, max_length=128)] = "factual"
