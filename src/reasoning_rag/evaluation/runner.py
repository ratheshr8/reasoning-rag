"""Evaluation runner across retrieval modes."""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from reasoning_rag import __version__
from reasoning_rag.config import Settings
from reasoning_rag.evaluation.dataset import EvalDataset, load_eval_dataset
from reasoning_rag.evaluation.metrics import METRIC_DEFINITIONS, aggregate_metrics, score_case
from reasoning_rag.evaluation.report import write_report
from reasoning_rag.models.common import AccessClassification, RetrievalMode
from reasoning_rag.qa import ask_document

VECTOR_BASELINE_STATUS = (
    "not_implemented: vector / hybrid-comparison baseline is recorded for protocol "
    "parity but does not invent scores in eval-v0"
)


def run_evaluation(
    dataset_path: Path | str,
    *,
    modes: list[RetrievalMode],
    settings: Settings,
    output_dir: Path | str,
    repo_root: Path | str | None = None,
    include_vector_placeholder: bool = True,
) -> dict[str, Any]:
    """Run baselines on a versioned dataset and write a reproducible report."""
    root = Path(repo_root) if repo_root else Path.cwd()
    dataset = load_eval_dataset(dataset_path)
    document_path = Path(dataset.document_path)
    if not document_path.is_absolute():
        document_path = (root / document_path).resolve()

    access = AccessClassification(dataset.access_classification)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    mode_reports: dict[str, Any] = {}
    for mode in modes:
        if mode == RetrievalMode.HYBRID_COMPARISON:
            mode_reports[mode.value] = {
                "status": VECTOR_BASELINE_STATUS,
                "metrics": None,
                "cases": [],
            }
            continue

        case_rows: list[dict[str, Any]] = []
        for case in dataset.cases:
            started = time.perf_counter()
            result = ask_document(
                document_path,
                case.question,
                settings=settings,
                access_classification=access,
                retrieval_mode=mode,
            )
            latency_ms = (time.perf_counter() - started) * 1000.0
            # Fixture provider: no billed tokens.
            estimated_cost = 0.0
            row = score_case(
                case,
                result,
                latency_ms=latency_ms,
                estimated_cost_usd=estimated_cost,
            )
            case_rows.append(row)

            case_dir = out / "cases" / mode.value
            case_dir.mkdir(parents=True, exist_ok=True)
            (case_dir / f"{case.id}.json").write_text(
                result.model_dump_json(indent=2) + "\n",
                encoding="utf-8",
            )

        mode_reports[mode.value] = {
            "status": "completed",
            "metrics": aggregate_metrics(case_rows),
            "cases": case_rows,
        }

    if include_vector_placeholder and RetrievalMode.HYBRID_COMPARISON.value not in mode_reports:
        mode_reports[RetrievalMode.HYBRID_COMPARISON.value] = {
            "status": VECTOR_BASELINE_STATUS,
            "metrics": None,
            "cases": [],
        }

    report: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(),
        "package_version": __version__,
        "dataset_version": dataset.dataset_version,
        "corpus_version": dataset.corpus_version,
        "document_path": str(document_path),
        "command": (
            f"reasoning-rag eval --dataset {dataset_path} "
            f"--modes {','.join(mode.value for mode in modes)} "
            f"--output {out}"
        ),
        "settings": _public_settings(settings),
        "metric_definitions": METRIC_DEFINITIONS,
        "modes": mode_reports,
        "notes": [
            "Fixture model provider: estimated_cost_usd is 0.0.",
            "Do not claim superiority over vector RAG unless a vector baseline ran under equal protocol.",
            VECTOR_BASELINE_STATUS,
        ],
    }

    write_report(report, out)
    (out / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    return report


def parse_modes(raw: str) -> list[RetrievalMode]:
    modes: list[RetrievalMode] = []
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        modes.append(RetrievalMode(token))
    if not modes:
        raise ValueError("at least one retrieval mode is required")
    return modes


def _public_settings(settings: Settings) -> dict[str, Any]:
    payload = settings.model_dump(mode="json")
    if payload.get("model_api_key"):
        payload["model_api_key"] = "***"
    return payload
