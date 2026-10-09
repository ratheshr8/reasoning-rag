"""Typed query analysis with safe fallback on malformed output."""

from __future__ import annotations

import re
from typing import Any, Protocol

from pydantic import ValidationError

from reasoning_rag.models.query import QueryAnalysis
from reasoning_rag.retrieval.tokenize import query_terms

ANALYZER_VERSION = "rules-analyzer-v1"


class QueryAnalyzer(Protocol):
    """Produces structured analysis; may return a dict that must be validated."""

    version: str

    def analyze_raw(self, question: str) -> QueryAnalysis | dict[str, Any]: ...


class FixtureQueryAnalyzer:
    """Deterministic rules-based analyzer (no paid model calls)."""

    version = ANALYZER_VERSION

    def analyze_raw(self, question: str) -> QueryAnalysis:
        return _rules_analysis(question)


def fallback_query_analysis(question: str) -> QueryAnalysis:
    """Minimal valid analysis used when model/rules output is unusable."""
    normalized = " ".join(question.strip().split()) or "empty question"
    return QueryAnalysis(
        normalized_query=normalized[:4000],
        intent="lookup",
        entities=query_terms(normalized)[:8],
        constraints=[],
        subquestions=[normalized[:4000]],
        expected_answer_type="factual",
    )


def analyze_query(
    question: str,
    *,
    analyzer: QueryAnalyzer | None = None,
) -> tuple[QueryAnalysis, bool, str]:
    """Analyze a question and validate against the schema.

    Returns (analysis, used_fallback, analyzer_version).
    """
    active = analyzer or FixtureQueryAnalyzer()
    version = getattr(active, "version", "unknown")
    try:
        raw = active.analyze_raw(question)
        if isinstance(raw, QueryAnalysis):
            return raw, False, version
        parsed = QueryAnalysis.model_validate(raw)
        return parsed, False, version
    except (ValidationError, TypeError, ValueError, KeyError, AttributeError):
        return fallback_query_analysis(question), True, version


def _rules_analysis(question: str) -> QueryAnalysis:
    normalized = " ".join(question.strip().split())
    if not normalized:
        return fallback_query_analysis(question)

    lower = normalized.lower()
    intent = _detect_intent(lower)
    answer_type = {
        "procedural": "steps",
        "comparison": "comparison",
        "explanatory": "explanation",
        "lookup": "factual",
    }.get(intent, "factual")

    entities = _extract_entities(normalized)
    constraints = _extract_constraints(lower)
    subquestions = _decompose_subquestions(normalized, lower)

    return QueryAnalysis(
        normalized_query=normalized[:4000],
        intent=intent,
        entities=entities,
        constraints=constraints,
        subquestions=subquestions,
        expected_answer_type=answer_type,
    )


def _detect_intent(lower: str) -> str:
    if any(token in lower for token in ("compare", "difference", " vs ", "versus", "both")):
        return "comparison"
    if lower.startswith("why ") or " why " in lower:
        return "explanatory"
    if (
        any(lower.startswith(prefix) for prefix in ("how do", "how can", "how to", "how should"))
        or "procedure" in lower
    ):
        return "procedural"
    return "lookup"


def _extract_entities(question: str) -> list[str]:
    # Prefer multi-word Capitalized spans, then distinctive query terms.
    entities: list[str] = []
    for match in re.finditer(r"\b([A-Z][a-z0-9]+(?:\s+[A-Z][a-z0-9]+)*)\b", question):
        span = match.group(1).strip()
        if span.lower() not in {"what", "how", "when", "where", "which"}:
            entities.append(span)
    for term in query_terms(question):
        if term not in {e.lower() for e in entities} and len(term) > 2:
            entities.append(term)
    # Deduplicate preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for item in entities:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            ordered.append(item)
    return ordered[:12]


def _extract_constraints(lower: str) -> list[str]:
    constraints: list[str] = []
    if "maximum" in lower or "max " in lower:
        constraints.append("prefer_maximum_limit")
    if "minimum" in lower or "min " in lower:
        constraints.append("prefer_minimum_limit")
    if "error code" in lower or re.search(r"\be\d{2}\b", lower):
        constraints.append("error_code_lookup")
    if "not" in lower and "document" in lower:
        constraints.append("may_be_unanswerable")
    return constraints


def _decompose_subquestions(normalized: str, lower: str) -> list[str]:
    if " and " in lower and any(cue in lower for cue in ("what is", "what are", "how", "compare")):
        parts = re.split(r"\band\b", normalized, maxsplit=1, flags=re.IGNORECASE)
        cleaned = [" ".join(part.strip(" ?").split()) for part in parts if part.strip()]
        if len(cleaned) == 2 and all(len(part) > 8 for part in cleaned):
            return [f"{cleaned[0]}?", cleaned[1] if cleaned[1].endswith("?") else f"{cleaned[1]}?"]
    if "compare" in lower or "difference" in lower:
        return [
            normalized if normalized.endswith("?") else f"{normalized}?",
            "What evidence supports each side of the comparison?",
        ]
    return [normalized if normalized.endswith("?") else f"{normalized}?"]
