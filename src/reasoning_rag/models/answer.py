"""Answer and citation link contracts."""

from typing import Annotated

from pydantic import BaseModel, Field

from reasoning_rag.models.common import SchemaVersion


class ClaimEvidenceLink(BaseModel):
    claim: Annotated[str, Field(min_length=1)]
    evidence_ids: list[Annotated[str, Field(min_length=1)]] = Field(min_length=1)


class Answer(BaseModel):
    schema_version: SchemaVersion = "v1"
    text: str = ""
    claim_links: list[ClaimEvidenceLink] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    abstained: bool = False
    abstention_reason: str | None = None
    trace_id: Annotated[str, Field(min_length=1, max_length=128)]

    def model_post_init(self, __context: object) -> None:
        if self.abstained and not self.abstention_reason:
            raise ValueError("abstention_reason is required when abstained is true")
        if not self.abstained and not self.text.strip():
            raise ValueError("text is required when not abstaining")
