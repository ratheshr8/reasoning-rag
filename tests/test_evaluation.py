"""Evaluation harness unit tests (no live CLI invocation required)."""

from pathlib import Path

from reasoning_rag.config import Settings
from reasoning_rag.evaluation.dataset import load_eval_dataset
from reasoning_rag.evaluation.metrics import METRIC_DEFINITIONS, aggregate_metrics, score_case
from reasoning_rag.evaluation.runner import parse_modes, run_evaluation
from reasoning_rag.models.answer import Answer
from reasoning_rag.models.common import RetrievalMode
from reasoning_rag.models.evaluation import EvaluationCase
from reasoning_rag.models.trace import AskResult
from reasoning_rag.models.verification import VerificationReport

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "eval" / "v0" / "dataset.json"


def test_load_eval_dataset() -> None:
    dataset = load_eval_dataset(DATASET)
    assert dataset.dataset_version == "eval-v0"
    assert len(dataset.cases) >= 4
    assert "abstention_accuracy" in METRIC_DEFINITIONS


def test_parse_modes() -> None:
    modes = parse_modes("tree-first,tree-lexical")
    assert modes == [RetrievalMode.TREE_FIRST, RetrievalMode.TREE_LEXICAL]


def test_score_case_abstention() -> None:
    case = EvaluationCase(
        id="c1",
        question="What is the capital of France?",
        document_ids=["doc"],
        corpus_version="v0",
        answerable=False,
        expected_answer_properties={"expect_abstain": True},
    )
    result = AskResult(
        trace_id="t1",
        question=case.question,
        document_id="doc",
        retrieval_mode=RetrievalMode.TREE_FIRST,
        evidence=[],
        answer=Answer(
            abstained=True,
            abstention_reason="not enough evidence",
            trace_id="t1",
        ),
        verification=VerificationReport(),
    )
    row = score_case(case, result, latency_ms=12.0, estimated_cost_usd=0.0)
    assert row["passed"] is True
    assert row["abstention_correct"] is True


def test_aggregate_metrics_smoke() -> None:
    rows = [
        {
            "answerable": True,
            "abstained": False,
            "abstention_correct": True,
            "contains_ok": True,
            "section_hit": True,
            "expect_conflict": False,
            "conflict_ok": None,
            "citation_resolution_rate": 1.0,
            "unsupported_claims": False,
            "latency_ms": 10.0,
            "estimated_cost_usd": 0.0,
            "passed": True,
        },
        {
            "answerable": False,
            "abstained": True,
            "abstention_correct": True,
            "contains_ok": True,
            "section_hit": None,
            "expect_conflict": False,
            "conflict_ok": None,
            "citation_resolution_rate": 1.0,
            "unsupported_claims": False,
            "latency_ms": 20.0,
            "estimated_cost_usd": 0.0,
            "passed": True,
        },
    ]
    metrics = aggregate_metrics(rows)
    assert metrics["abstention_accuracy"] == 1.0
    assert metrics["latency_ms_median"] == 15.0


def test_run_evaluation_writes_report(tmp_path: Path) -> None:
    out = tmp_path / "report-out"
    report = run_evaluation(
        DATASET,
        modes=[RetrievalMode.TREE_FIRST],
        settings=Settings(),
        output_dir=out,
        repo_root=ROOT,
        include_vector_placeholder=True,
    )
    assert (out / "report.json").is_file()
    assert (out / "report.md").is_file()
    assert "tree-first" in report["modes"]
    assert report["modes"]["tree-first"]["status"] == "completed"
    assert report["modes"]["hybrid-comparison"]["metrics"] is None
    assert report["modes"]["tree-first"]["metrics"]["case_count"] >= 4
