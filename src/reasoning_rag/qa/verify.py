"""Citation verification, coverage checks, and conflict detection."""

from __future__ import annotations

import re

from reasoning_rag.models.answer import Answer, ClaimEvidenceLink
from reasoning_rag.models.evidence import Evidence
from reasoning_rag.models.normalized import NormalizedDocument
from reasoning_rag.models.query import QueryAnalysis
from reasoning_rag.models.verification import CoverageGap, EvidenceConflict, VerificationReport
from reasoning_rag.qa.citations import citations_resolve
from reasoning_rag.retrieval.tokenize import query_terms

_NUMBER_UNIT = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?:degrees?\s+)?(?P<unit>°?\s*c|celsius|v|mv|ma|a|hours?|h)\b",
    re.IGNORECASE,
)

_TOPIC_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ambient_temperature_c", re.compile(r"ambient", re.I)),
    ("supply_voltage_v", re.compile(r"supply|\b\d+\s*v\b|voltage", re.I)),
    ("current_ma", re.compile(r"\d+\s*mA|inrush|maximum of \d+\s*mA", re.I)),
]


def verify_evidence(
    evidence: list[Evidence],
    normalized: NormalizedDocument,
) -> tuple[list[Evidence], list[str]]:
    """Drop evidence with unresolved citations; return (kept, unresolved_ids)."""
    unresolved = set(citations_resolve(evidence, normalized))
    kept = [item for item in evidence if item.id not in unresolved]
    return kept, sorted(unresolved)


def detect_conflicts(evidence: list[Evidence]) -> list[EvidenceConflict]:
    """Surface numeric conflicts on the same topic; do not merge values."""
    conflicts: list[EvidenceConflict] = []
    for topic, topic_re in _TOPIC_PATTERNS:
        values: dict[str, list[str]] = {}
        for item in evidence:
            for sentence in _sentences(item.exact_text):
                if not topic_re.search(sentence):
                    continue
                for match in _NUMBER_UNIT.finditer(sentence):
                    unit = re.sub(r"\s+", "", match.group("unit").lower())
                    unit = unit.replace("celsius", "c").replace("°c", "c")
                    if topic == "ambient_temperature_c" and unit != "c":
                        continue
                    if topic == "supply_voltage_v" and unit != "v":
                        continue
                    if topic == "current_ma" and unit not in {"ma", "a"}:
                        continue
                    key = f"{match.group('value')}{unit}"
                    values.setdefault(key, []).append(item.id)

        distinct = sorted(values.keys(), key=_value_sort_key)
        if len(distinct) >= 2:
            evidence_ids: list[str] = []
            for key in distinct:
                evidence_ids.extend(values[key])
            ordered_ids = _unique(evidence_ids)
            conflicts.append(
                EvidenceConflict(
                    topic=topic,
                    values=distinct,
                    evidence_ids=ordered_ids,
                    note=(
                        f"conflicting values for {topic}: {', '.join(distinct)}; "
                        "surfaced rather than merged"
                    ),
                )
            )
    return conflicts


def check_coverage(
    analysis: QueryAnalysis,
    evidence: list[Evidence],
) -> list[CoverageGap]:
    """Mark whether each subquestion has lexical support in assembled evidence."""
    gaps: list[CoverageGap] = []
    blob_by_id = {item.id: item.exact_text.lower() for item in evidence}
    for sub_q in analysis.subquestions or [analysis.normalized_query]:
        terms = query_terms(sub_q)
        supporting: list[str] = []
        for evidence_id, text in blob_by_id.items():
            if not terms:
                continue
            hits = sum(1 for term in terms if term in text)
            if hits >= max(1, len(terms) // 2):
                supporting.append(evidence_id)
        gaps.append(
            CoverageGap(
                subquestion=sub_q,
                covered=bool(supporting),
                evidence_ids=supporting,
                rationale=None if supporting else "no evidence met lexical coverage threshold",
            )
        )
    return gaps


def map_and_verify_claims(
    answer: Answer,
    evidence: list[Evidence],
    normalized: NormalizedDocument,
    *,
    conflicts: list[EvidenceConflict],
) -> tuple[Answer, VerificationReport]:
    """Ensure every remaining claim links to resolvable evidence; else abstain."""
    evidence_ids = {item.id for item in evidence}
    unresolved = citations_resolve(evidence, normalized)
    unresolved_set = set(unresolved)

    kept_links: list[ClaimEvidenceLink] = []
    dropped = 0
    for link in answer.claim_links:
        valid_ids = [
            evidence_id
            for evidence_id in link.evidence_ids
            if evidence_id in evidence_ids and evidence_id not in unresolved_set
        ]
        if not valid_ids:
            dropped += 1
            continue
        kept_links.append(ClaimEvidenceLink(claim=link.claim, evidence_ids=valid_ids))

    limitations = list(answer.limitations)
    for conflict in conflicts:
        limitations.append(conflict.note)

    if not kept_links and not answer.abstained:
        verified = Answer(
            text="",
            claim_links=[],
            limitations=limitations
            + ["all claims removed because citations could not be verified"],
            abstained=True,
            abstention_reason="unresolved or missing claim-to-evidence links",
            trace_id=answer.trace_id,
        )
    elif answer.abstained:
        verified = Answer(
            text=answer.text,
            claim_links=[],
            limitations=limitations,
            abstained=True,
            abstention_reason=answer.abstention_reason,
            trace_id=answer.trace_id,
        )
    else:
        text = answer.text
        if conflicts:
            conflict_bits = "; ".join(
                f"{conflict.topic}: {', '.join(conflict.values)}" for conflict in conflicts
            )
            text = f"{text} Conflict noted — {conflict_bits}."
        verified = Answer(
            text=text,
            claim_links=kept_links,
            limitations=limitations,
            abstained=False,
            abstention_reason=None,
            trace_id=answer.trace_id,
        )

    report = VerificationReport(
        unresolved_citation_ids=unresolved,
        dropped_claim_count=dropped,
        conflicts=conflicts,
        coverage=[],
    )
    return verified, report


def _sentences(text: str) -> list[str]:
    cleaned = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    parts = re.split(r"(?<=[.!?])\s+|\n+", cleaned)
    return [part.strip() for part in parts if part.strip()]


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def _value_sort_key(value: str) -> tuple[float, str]:
    match = re.match(r"(\d+(?:\.\d+)?)(.*)", value)
    if not match:
        return (0.0, value)
    return (float(match.group(1)), match.group(2))
