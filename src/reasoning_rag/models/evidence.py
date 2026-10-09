"""Evidence contract."""

from typing import Annotated

from pydantic import BaseModel, Field

from reasoning_rag.models.common import SchemaVersion, SourceRange


class Evidence(BaseModel):
    schema_version: SchemaVersion = "v1"
    id: Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.:-]+$")]
    document_id: Annotated[str, Field(min_length=1, max_length=128)]
    node_id: Annotated[str, Field(min_length=1, max_length=128)]
    exact_text: Annotated[str, Field(min_length=1)]
    source_range: SourceRange
    provenance: Annotated[str, Field(min_length=1, max_length=256)]
    relevance_rationale: str | None = None
