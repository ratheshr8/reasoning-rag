"""Markdown evaluation report writer."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def write_report(report: dict[str, Any], output_dir: Path) -> Path:
    lines: list[str] = [
        f"# Evaluation report — {report['dataset_version']}",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Package: `{report['package_version']}`",
        f"- Corpus: `{report['corpus_version']}`",
        f"- Document: `{report['document_path']}`",
        f"- Command: `{report['command']}`",
        "",
        "## Metric definitions",
        "",
    ]
    for name, definition in report["metric_definitions"].items():
        lines.append(f"- **{name}:** {definition}")

    lines.extend(["", "## Results by mode", ""])
    for mode, payload in report["modes"].items():
        lines.append(f"### `{mode}`")
        status = payload.get("status", "unknown")
        lines.append(f"- Status: {status}")
        metrics = payload.get("metrics")
        if not metrics:
            lines.append("")
            continue
        lines.append(
            f"- Cases passed: {metrics.get('pass_count', 0)} / {metrics.get('case_count', 0)}"
        )
        for key in (
            "abstention_accuracy",
            "answerable_success_rate",
            "section_hit_rate",
            "citation_resolution_rate",
            "conflict_detection_rate",
            "unsupported_claim_rate",
            "latency_ms_median",
            "latency_ms_p95",
            "estimated_cost_usd",
        ):
            value = metrics.get(key)
            if isinstance(value, float):
                lines.append(f"- `{key}`: {value:.4f}")
            else:
                lines.append(f"- `{key}`: {value}")
        lines.append("")

        failures = [row for row in payload.get("cases", []) if not row.get("passed")]
        if failures:
            lines.append("#### Failures")
            lines.append("")
            lines.append("| Case | Failures | Abstained |")
            lines.append("| --- | --- | --- |")
            for row in failures:
                tags = ", ".join(row.get("failures", []))
                lines.append(
                    f"| `{row['case_id']}` | {tags or '(none)'} | {row.get('abstained')} |"
                )
            lines.append("")
        else:
            lines.append("No case-level failures for this mode.")
            lines.append("")

    lines.extend(["## Notes", ""])
    for note in report.get("notes", []):
        lines.append(f"- {note}")
    lines.append("")

    path = output_dir / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
