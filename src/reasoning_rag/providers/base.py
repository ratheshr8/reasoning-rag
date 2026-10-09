"""Provider protocols."""

from __future__ import annotations

from typing import Protocol


class Summarizer(Protocol):
    provider: str
    model: str
    prompt_version: str

    def summarize(self, *, title: str, text: str, max_chars: int) -> str:
        """Return a short summary. Must not invent citations."""
        ...
