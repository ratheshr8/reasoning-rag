"""Human-readable plan rendering for the CLI."""

from __future__ import annotations

from reasoning_rag.models.query import QueryAnalysis
from reasoning_rag.models.retrieval import RetrievalPlan


def render_plan_text(analysis: QueryAnalysis, plan: RetrievalPlan) -> str:
    lines = [
        "Query analysis",
        f"  normalized: {analysis.normalized_query}",
        f"  intent: {analysis.intent}",
        f"  expected_answer_type: {analysis.expected_answer_type}",
        f"  entities: {', '.join(analysis.entities) if analysis.entities else '(none)'}",
        f"  constraints: {', '.join(analysis.constraints) if analysis.constraints else '(none)'}",
        "  subquestions:",
    ]
    for index, sub in enumerate(analysis.subquestions, start=1):
        lines.append(f"    {index}. {sub}")

    lines.extend(
        [
            "",
            "Retrieval plan",
            f"  strategy: {plan.strategy.value}",
            f"  planner_version: {plan.planner_version}",
            (
                "  budgets: "
                f"depth={plan.budgets.max_depth}, "
                f"nodes={plan.budgets.max_nodes}, "
                f"model_calls={plan.budgets.max_model_calls}, "
                f"context_tokens={plan.budgets.max_context_tokens}"
            ),
            f"  candidates ({len(plan.candidate_node_ids)}):",
        ]
    )
    if plan.candidate_node_ids:
        for node_id in plan.candidate_node_ids:
            lines.append(f"    - {node_id}")
    else:
        lines.append("    (none)")

    lines.append("  steps:")
    for index, step in enumerate(plan.steps, start=1):
        targets = ", ".join(step.target_node_ids[:5])
        if len(step.target_node_ids) > 5:
            targets += ", …"
        rationale = step.rationale or ""
        lines.append(f"    {index}. {step.action}")
        if targets:
            lines.append(f"       targets: {targets}")
        if rationale:
            lines.append(f"       rationale: {rationale}")

    return "\n".join(lines) + "\n"
