"""Document contract."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from reasoning_rag.models.common import AccessClassification, SchemaVersion


class Document(BaseModel):
    schema_version: SchemaVersion = "v1"
    id: Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.:-]+$")]
    source_name: Annotated[str, Field(min_length=1, max_length=512)]
    checksum: Annotated[str, Field(min_length=8, max_length=128)]
    media_type: Annotated[str, Field(pattern=r"^text/markdown$")] = "text/markdown"
    ingested_at: datetime
    parser_version: Annotated[str, Field(min_length=1, max_length=64)]
    access_classification: AccessClassification = AccessClassification.PUBLIC

    @field_validator("checksum")
    @classmethod
    def checksum_hex_or_prefixed(cls, value: str) -> str:
        normalized = value.lower().removeprefix("sha256:")
        if any(c not in "0123456789abcdef" for c in normalized):
            raise ValueError("checksum must be hex (optionally prefixed with sha256:)")
        return value
