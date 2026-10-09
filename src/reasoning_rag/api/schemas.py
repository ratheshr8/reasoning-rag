"""Validated request/response schemas for the local API."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field

from reasoning_rag.models.common import RetrievalMode
from reasoning_rag.models.trace import AskResult


class ProviderNotice(BaseModel):
    model_provider: str
    model_name: str
    sends_document_text_externally: bool
    message: str


class SampleDocument(BaseModel):
    id: str
    title: str
    path: str
    access_classification: Literal["public", "synthetic"] = "synthetic"
    description: str = ""


class SamplesResponse(BaseModel):
    samples: list[SampleDocument]
    max_upload_bytes: int
    provider_notice: ProviderNotice


class AskRequest(BaseModel):
    question: Annotated[str, Field(min_length=1, max_length=4000)]
    sample_id: str | None = None
    retrieval_mode: RetrievalMode = RetrievalMode.TREE_FIRST
    synthetic: bool = True


class TraceSummary(BaseModel):
    event_count: int
    components: list[str]
    candidate_node_ids: list[str] = Field(default_factory=list)
    conflict_topics: list[str] = Field(default_factory=list)


class AskResponse(BaseModel):
    result: AskResult
    trace_summary: TraceSummary
    provider_notice: ProviderNotice
    upload_limits: dict[str, Any]


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    package_version: str
    provider_notice: ProviderNotice


class ErrorResponse(BaseModel):
    error: str
    code: str
    detail: str | None = None
