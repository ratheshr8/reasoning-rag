"""Model provider interfaces (fixture by default)."""

from reasoning_rag.providers.base import Summarizer
from reasoning_rag.providers.fixture import FixtureSummarizer, get_summarizer

__all__ = ["FixtureSummarizer", "Summarizer", "get_summarizer"]
