"""Markdown parser adapter: sections with character offsets into normalized text."""

from __future__ import annotations

import re
from dataclasses import dataclass

from reasoning_rag.models.common import SourceRange
from reasoning_rag.models.normalized import (
    NormalizedSection,
    ParserWarning,
    ParserWarningCode,
)

PARSER_VERSION = "md-v1"
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_ALLOWED_EXTENSIONS = {".md", ".markdown"}


@dataclass(frozen=True)
class _RawSection:
    title: str
    level: int
    start: int
    heading_end: int
    body_start: int
    end: int
    heading_line: int | None


def allowed_markdown_extension(path_suffix: str) -> bool:
    return path_suffix.lower() in _ALLOWED_EXTENSIONS


def normalize_text(raw_text: str) -> tuple[str, list[ParserWarning]]:
    """Normalize line endings; reject NUL. Offsets always refer to this text."""
    warnings: list[ParserWarning] = []
    if "\x00" in raw_text:
        raise ValueError("document contains NUL bytes")
    if "\r" in raw_text:
        warnings.append(
            ParserWarning(
                code=ParserWarningCode.LINE_ENDING_NORMALIZED,
                message="CRLF/CR line endings were normalized to LF for stable offsets",
            )
        )
        text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    else:
        text = raw_text
    return text, warnings


def parse_markdown_sections(text: str, *, document_id: str) -> tuple[list[NormalizedSection], list[ParserWarning]]:
    """Split Markdown into heading sections with provenance ranges."""
    warnings: list[ParserWarning] = []
    if text == "":
        warnings.append(
            ParserWarning(
                code=ParserWarningCode.EMPTY_DOCUMENT,
                message="document text is empty after decoding",
            )
        )
        return [], warnings

    raw_sections = _collect_raw_sections(text, warnings)
    if len(raw_sections) == 1 and raw_sections[0].level == 0:
        warnings.append(
            ParserWarning(
                code=ParserWarningCode.NO_HEADINGS,
                message="no ATX headings found; entire document treated as one preamble section",
            )
        )

    sections: list[NormalizedSection] = []
    for index, raw in enumerate(raw_sections):
        section_text = text[raw.start : raw.end]
        if not section_text.strip():
            warnings.append(
                ParserWarning(
                    code=ParserWarningCode.EMPTY_SECTION,
                    message=f"section '{raw.title}' is empty",
                    line=raw.heading_line,
                )
            )

        heading_range = None
        if raw.level > 0:
            heading_range = SourceRange(
                start_offset=raw.start,
                end_offset=raw.heading_end,
                section_path=raw.title,
            )

        section_id = f"{document_id}:sec:{index:04d}"
        sections.append(
            NormalizedSection(
                id=section_id,
                title=raw.title,
                level=raw.level,
                text=section_text,
                source_range=SourceRange(
                    start_offset=raw.start,
                    end_offset=raw.end,
                    section_path=raw.title,
                ),
                heading_range=heading_range,
            )
        )

    return sections, warnings


def _collect_raw_sections(text: str, warnings: list[ParserWarning]) -> list[_RawSection]:
    lines = text.split("\n")
    # Re-attach newlines except after the final line if text has no trailing newline.
    offsets: list[int] = []
    cursor = 0
    for i, line in enumerate(lines):
        offsets.append(cursor)
        cursor += len(line)
        if i < len(lines) - 1:
            cursor += 1  # the '\n' separator from split

    heading_indices: list[tuple[int, int, str, int]] = []
    for line_no, line in enumerate(lines):
        match = _HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).rstrip()
        if title != match.group(2):
            warnings.append(
                ParserWarning(
                    code=ParserWarningCode.TRAILING_WHITESPACE_IN_HEADING,
                    message="heading title trailing whitespace was trimmed for the section title",
                    line=line_no + 1,
                )
            )
        # Strip optional closing hashes commonly used in ATX: "## Title ##"
        title = re.sub(r"\s+#+\s*$", "", title).strip() or "Untitled"
        heading_indices.append((line_no, level, title, offsets[line_no]))

    if not heading_indices:
        return [
            _RawSection(
                title="Preamble",
                level=0,
                start=0,
                heading_end=0,
                body_start=0,
                end=len(text),
                heading_line=None,
            )
        ]

    sections: list[_RawSection] = []
    first_heading_start = heading_indices[0][3]
    if first_heading_start > 0:
        preamble = text[:first_heading_start]
        if preamble.strip():
            sections.append(
                _RawSection(
                    title="Preamble",
                    level=0,
                    start=0,
                    heading_end=0,
                    body_start=0,
                    end=first_heading_start,
                    heading_line=None,
                )
            )

    for i, (line_no, level, title, start) in enumerate(heading_indices):
        line = lines[line_no]
        heading_end = start + len(line)
        # body starts after heading line newline if present
        if heading_end < len(text) and text[heading_end] == "\n":
            body_start = heading_end + 1
        else:
            body_start = heading_end

        if i + 1 < len(heading_indices):
            end = heading_indices[i + 1][3]
        else:
            end = len(text)

        sections.append(
            _RawSection(
                title=title,
                level=level,
                start=start,
                heading_end=heading_end,
                body_start=body_start,
                end=end,
                heading_line=line_no + 1,
            )
        )

    return sections
