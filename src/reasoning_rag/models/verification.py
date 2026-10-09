"""Verification, conflict, and coverage contracts."""

from typing import Annotated

from pydantic import BaseModel, Field

from reasoning_rag.models.common import SchemaVersion


class EvidenceConflict(BaseModel):
    schema_version: SchemaVersion = "v1"
    topic: Annotated[str, Field(min_length=1, max_length=128)]
    values: list[str] = Field(min_length=2)
    evidence_ids: list[Annotated[str, Field(min_length=1)]] = Field(min_length=2)
    note: str


class CoverageGap(BaseModel):
    schema_version: SchemaVersion = "v1"
    subquestion: Annotated[str, Field(min_length=1)]
    covered: bool
    evidence_ids: list[str] = Field(default_factory=list)
    rationale: str | None = None


class VerificationReport(BaseModel):
    schema_version: SchemaVersion = "v1"
    unresolved_citation_ids: list[str] = Field(default_factory=list)
    dropped_claim_count: int = 0
    conflicts: list[EvidenceConflict] = Field(default_factory=list)
    coverage: list[CoverageGap] = Field(default_factory=list)
