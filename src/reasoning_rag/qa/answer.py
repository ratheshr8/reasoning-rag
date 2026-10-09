"""Deterministic cited-answer and abstention builder (fixture baseline)."""

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
            limitations=["baseline retriever found insufficient lexical support"],
            abstained=True,
            abstention_reason="not enough evidence in the selected document sections",
            trace_id=tid,
        )

    # Unanswerable cue: corpus explicitly says content is absent.
    if _looks_unanswerable(question, evidence):
        return Answer(
            text="",
            claim_links=[],
            limitations=["document states the requested information is elsewhere/absent"],
            abstained=True,
            abstention_reason=(
                "the corpus indicates the answer is not present in this document"
            ),
            trace_id=tid,
        )

    primary = evidence[0]
    snippet = _first_sentence(primary.exact_text)
    terms = query_terms(question)
    claim = snippet if snippet else primary.exact_text[:240]
    text = claim
    if terms:
        text = f"{claim}"

    return Answer(
        text=text,
        claim_links=[ClaimEvidenceLink(claim=claim, evidence_ids=[primary.id])],
        limitations=[
            "Phase 4 baseline: extractive answer from top evidence; not an LLM synthesis",
        ],
        abstained=False,
        abstention_reason=None,
        trace_id=tid,
    )


def _first_sentence(text: str) -> str:
    cleaned = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    match = re.match(r"(.+?[.!?])(\s|$)", cleaned)
    if match:
        return match.group(1).strip()
    return cleaned[:300].strip()


def _looks_unanswerable(question: str, evidence: list[Evidence]) -> bool:
    q = question.lower()
    if "firmware" not in q and "update procedure" not in q and "how do i update" not in q:
        # Still check evidence for explicit absence language when question asks how-to.
        if not any(word in q for word in ("how", "where", "procedure", "steps")):
            return False
    absence_markers = (
        "intentionally absent",
        "separate document",
        "not present in this",
        "described in a separate",
    )
    blob = " ".join(item.exact_text.lower() for item in evidence)
    return any(marker in blob for marker in absence_markers)
