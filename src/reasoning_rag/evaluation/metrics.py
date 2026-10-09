"""Metric definitions and per-case scoring."""

from __future__ import annotations

from statistics import median
from typing import Any

from reasoning_rag.evaluation.dataset import expect_abstain
from reasoning_rag.models.evaluation import EvaluationCase
from reasoning_rag.models.trace import AskResult

METRIC_DEFINITIONS: dict[str, str] = {
    "abstention_accuracy": ("Fraction of cases where answer.abstained matches expect_abstain."),
    "answerable_success_rate": (
        "Among answerable cases, fraction that did not abstain and matched must_contain_any."
    ),
    "section_hit_rate": (
        "Among cases with expected_evidence_sections, fraction with at least one section hit."
    ),
    "citation_resolution_rate": (
        "Fraction of kept evidence items that resolve against source ranges "
        "(unresolved_citation_ids empty relative to evidence count)."
    ),
    "conflict_detection_rate": (
        "Among expect_conflict cases, fraction with non-empty verification.conflicts."
    ),
    "unsupported_claim_rate": ("Fraction of non-abstaining answers with zero claim_links."),
    "latency_ms_median": "Median wall-clock ask latency in milliseconds.",
    "latency_ms_p95": "95th percentile wall-clock ask latency in milliseconds.",
    "estimated_cost_usd": "Estimated model cost in USD (0.0 for fixture provider).",
}


def score_case(
    case: EvaluationCase,
    result: AskResult,
    *,
    latency_ms: float,
    estimated_cost_usd: float,
) -> dict[str, Any]:
    props = case.expected_answer_properties or {}
    want_abstain = expect_abstain(case)
    abstain_ok = result.answer.abstained == want_abstain

    must_any = [str(item) for item in props.get("must_contain_any", [])]
    contains_ok = True
    if must_any and not result.answer.abstained:
        text = result.answer.text
        contains_ok = any(token.lower() in text.lower() for token in must_any)

    section_hit = None
    if case.expected_evidence_sections:
        blob = " ".join(
            f"{item.source_range.section_path or ''} {item.exact_text}" for item in result.evidence
        ).lower()
        section_hit = any(section.lower() in blob for section in case.expected_evidence_sections)

    expect_conflict = bool(props.get("expect_conflict", False))
    conflict_ok = None
    if expect_conflict:
        conflicts = result.verification.conflicts if result.verification else []
        conflict_ok = len(conflicts) > 0

    unresolved = list(result.verification.unresolved_citation_ids) if result.verification else []
    evidence_count = len(result.evidence)
    citation_ok_rate = (
        1.0
        if evidence_count == 0 and want_abstain
        else ((evidence_count - len(unresolved)) / evidence_count if evidence_count else 0.0)
    )

    unsupported_claims = (not result.answer.abstained) and len(result.answer.claim_links) == 0

    failures: list[str] = []
    if not abstain_ok:
        failures.append("false_abstain" if result.answer.abstained else "missed_abstain")
    if case.answerable and not result.answer.abstained and must_any and not contains_ok:
        failures.append("missing_answer_span")
    if section_hit is False:
        failures.append("missing_section")
    if conflict_ok is False:
        failures.append("missed_conflict")
    if unsupported_claims:
        failures.append("unsupported_claims")

    return {
        "case_id": case.id,
        "question": case.question,
        "tags": case.tags,
        "difficulty": case.difficulty,
        "answerable": case.answerable,
        "abstained": result.answer.abstained,
        "expect_abstain": want_abstain,
        "abstention_correct": abstain_ok,
        "contains_ok": contains_ok,
        "section_hit": section_hit,
        "conflict_detected": (
            bool(result.verification.conflicts) if result.verification else False
        ),
        "expect_conflict": expect_conflict,
        "conflict_ok": conflict_ok,
        "citation_resolution_rate": citation_ok_rate,
        "unsupported_claims": unsupported_claims,
        "latency_ms": latency_ms,
        "estimated_cost_usd": estimated_cost_usd,
        "failures": failures,
        "passed": len(failures) == 0,
    }


def aggregate_metrics(case_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not case_rows:
        return {name: None for name in METRIC_DEFINITIONS}

    def _mean(values: list[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    abstention_accuracy = _mean([1.0 if row["abstention_correct"] else 0.0 for row in case_rows])

    answerable_rows = [row for row in case_rows if row["answerable"]]
    answerable_success_rate = _mean(
        [
            1.0
            if (not row["abstained"] and row["contains_ok"] and row["abstention_correct"])
            else 0.0
            for row in answerable_rows
        ]
    )

    section_rows = [row for row in case_rows if row["section_hit"] is not None]
    section_hit_rate = _mean([1.0 if row["section_hit"] else 0.0 for row in section_rows])

    citation_resolution_rate = _mean([float(row["citation_resolution_rate"]) for row in case_rows])

    conflict_rows = [row for row in case_rows if row["expect_conflict"]]
    conflict_detection_rate = _mean([1.0 if row["conflict_ok"] else 0.0 for row in conflict_rows])

    non_abstain = [row for row in case_rows if not row["abstained"]]
    unsupported_claim_rate = _mean(
        [1.0 if row["unsupported_claims"] else 0.0 for row in non_abstain]
    )

    latencies = sorted(float(row["latency_ms"]) for row in case_rows)
    p95 = _percentile(latencies, 0.95)

    return {
        "abstention_accuracy": abstention_accuracy,
        "answerable_success_rate": answerable_success_rate,
        "section_hit_rate": section_hit_rate,
        "citation_resolution_rate": citation_resolution_rate,
        "conflict_detection_rate": conflict_detection_rate,
        "unsupported_claim_rate": unsupported_claim_rate,
        "latency_ms_median": float(median(latencies)) if latencies else 0.0,
        "latency_ms_p95": p95,
        "estimated_cost_usd": sum(float(row["estimated_cost_usd"]) for row in case_rows),
        "case_count": len(case_rows),
        "pass_count": sum(1 for row in case_rows if row["passed"]),
    }


def _percentile(sorted_values: list[float], percentile: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    index = int(round((len(sorted_values) - 1) * percentile))
    return sorted_values[max(0, min(index, len(sorted_values) - 1))]
