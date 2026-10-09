"""Deterministic fixture summarizer for tests and offline demos."""

from __future__ import annotations

import re

from reasoning_rag.config import Settings


class FixtureSummarizer:
    """Extractive summary: first non-heading sentence/clause, truncated."""

    provider = "fixture"
    model = "fixture-v0"
    prompt_version = "summary-extract-v1"

    def __init__(self, *, model: str | None = None) -> None:
        if model:
            self.model = model

    def summarize(self, *, title: str, text: str, max_chars: int) -> str:
        body = _strip_leading_heading(text).strip()
        if not body:
            return f"{title}: (empty section)"[:max_chars]
        # Collapse whitespace for a compact one-line summary.
        collapsed = re.sub(r"\s+", " ", body).strip()
        # Prefer first sentence-ish chunk.
        match = re.match(r"(.+?[.!?])(\s|$)", collapsed)
        snippet = match.group(1) if match else collapsed
        if len(snippet) > max_chars:
            snippet = snippet[: max(0, max_chars - 1)].rstrip() + "…"
        return snippet


def get_summarizer(settings: Settings) -> FixtureSummarizer:
    """Resolve summarizer from settings. Only fixture is implemented in Phase 3."""
    provider = settings.model_provider.lower()
    if provider != "fixture":
        raise ValueError(
            f"model provider '{settings.model_provider}' is not implemented; "
            "use REASONING_RAG_MODEL_PROVIDER=fixture"
        )
    return FixtureSummarizer(model=settings.model_name)


def _strip_leading_heading(text: str) -> str:
    lines = text.split("\n")
    if lines and re.match(r"^#{1,6}\s+", lines[0]):
        return "\n".join(lines[1:]).lstrip("\n")
    return text
