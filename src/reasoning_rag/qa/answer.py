"""Deterministic cited-answer and abstention builder with claim mapping."""

from __future__ import annotations

import re
import uuid

from reasoning_rag.models.answer import Answer, ClaimEvidenceLink
from reasoning_rag.models.evidence import Evidence
from reasoning_rag.retrieval.tokenize import query_terms


def build_answer_from_evidence(
    question: str,
    evidence: list[Evidence],
    *,
    min_score_hint: float,
    best_score: float,
    trace_id: str | None = None,
) -> Answer:
    """Compose an answer only from selected evidence, or abstain."""
    tid = trace_id or f"trace.{uuid.uuid4().hex[:12]}"

    if not evidence or best_score < min_score_hint:
        return Answer(
            text="",
            claim_links=[],
            limitations=["retriever found insufficient lexical support"],
            abstained=True,
            abstention_reason="not enough evidence in the selected document sections",
            trace_id=tid,
        )

    if _looks_unanswerable(question, evidence):
        return Answer(
            text="",
            claim_links=[],
            limitations=["document states the requested information is elsewhere/absent"],
            abstained=True,
            abstention_reason=("the corpus indicates the answer is not present in this document"),
            trace_id=tid,
        )

    terms = query_terms(question)
    ranked = sorted(
        evidence,
        key=lambda item: _term_overlap(item.exact_text, terms),
        reverse=True,
    )

    claim_links: list[ClaimEvidenceLink] = []
    for item in ranked[:3]:
        claim = _first_sentence(item.exact_text) or item.exact_text[:240]
        if not claim.strip():
            continue
        claim_links.append(ClaimEvidenceLink(claim=claim, evidence_ids=[item.id]))

    if not claim_links:
        return Answer(
            text="",
            claim_links=[],
            limitations=["no extractive claims could be formed from evidence"],
            abstained=True,
            abstention_reason="not enough evidence in the selected document sections",
            trace_id=tid,
        )

    # Primary answer text from the claim with strongest question-term overlap.
    text = claim_links[0].claim

    return Answer(
        text=text,
        claim_links=claim_links,
        limitations=[
            "Phase 6: extractive claims mapped to evidence; conflicts are surfaced, not merged",
        ],
        abstained=False,
        abstention_reason=None,
        trace_id=tid,
    )


def _term_overlap(text: str, terms: list[str]) -> int:
    blob = text.lower()
    return sum(1 for term in terms if term.lower() in blob)


def _first_sentence(text: str) -> str:
    cleaned = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    match = re.match(r"(.+?[.!?])(\s|$)", cleaned)
    if match:
        return match.group(1).strip()
    return cleaned[:300].strip()


def _looks_unanswerable(question: str, evidence: list[Evidence]) -> bool:
    q = question.lower()
    if (
        "firmware" not in q
        and "update procedure" not in q
        and "how do i update" not in q
        and not any(word in q for word in ("how", "where", "procedure", "steps"))
    ):
        return False
    absence_markers = (
        "intentionally absent",
        "separate document",
        "not present in this",
        "described in a separate",
    )
    blob = " ".join(item.exact_text.lower() for item in evidence)
    return any(marker in blob for marker in absence_markers)
