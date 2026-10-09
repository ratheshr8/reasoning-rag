"""Normalized ingestion output contracts."""

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from reasoning_rag.models.common import SchemaVersion, SourceRange
from reasoning_rag.models.document import Document


class ParserWarningCode(StrEnum):
    EMPTY_DOCUMENT = "empty_document"
    NO_HEADINGS = "no_headings"
    LINE_ENDING_NORMALIZED = "line_ending_normalized"
    TRAILING_WHITESPACE_IN_HEADING = "trailing_whitespace_in_heading"
    EMPTY_SECTION = "empty_section"


class ParserWarning(BaseModel):
    code: ParserWarningCode
    message: str
    line: int | None = Field(default=None, ge=1)


class NormalizedSection(BaseModel):
    """A heading-delimited section with offsets into normalized document text."""

    id: Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.:-]+$")]
    title: Annotated[str, Field(min_length=1, max_length=512)]
    level: Annotated[int, Field(ge=0, le=6)]
    text: str
    source_range: SourceRange
    heading_range: SourceRange | None = None


class NormalizedDocument(BaseModel):
    schema_version: SchemaVersion = "v1"
    document: Document
    text: str
    sections: list[NormalizedSection]
    warnings: list[ParserWarning] = Field(default_factory=list)
    parser: Literal["markdown"] = "markdown"
    parser_version: Annotated[str, Field(min_length=1, max_length=64)]
