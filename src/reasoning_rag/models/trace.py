"""Run trace for inspectable retrieval and answering."""

from typing import Annotated, Any

from pydantic import BaseModel, Field

from reasoning_rag.models.answer import Answer
from reasoning_rag.models.common import RetrievalMode, SchemaVersion
from reasoning_rag.models.evidence import Evidence


class TraceEvent(BaseModel):
    component: Annotated[str, Field(min_length=1, max_length=64)]
    action: Annotated[str, Field(min_length=1, max_length=64)]
    detail: dict[str, Any] = Field(default_factory=dict)


class AskResult(BaseModel):
    schema_version: SchemaVersion = "v1"
    trace_id: Annotated[str, Field(min_length=1, max_length=128)]
    question: Annotated[str, Field(min_length=1)]
    document_id: Annotated[str, Field(min_length=1, max_length=128)]
    retrieval_mode: RetrievalMode
    evidence: list[Evidence] = Field(default_factory=list)
    answer: Answer
    events: list[TraceEvent] = Field(default_factory=list)
