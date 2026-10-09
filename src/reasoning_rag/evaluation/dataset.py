"""Versioned evaluation dataset loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field

from reasoning_rag.models.evaluation import EvaluationCase


class EvalDataset(BaseModel):
    dataset_version: Annotated[str, Field(min_length=1, max_length=64)]
    corpus_version: Annotated[str, Field(min_length=1, max_length=64)]
    document_path: Annotated[str, Field(min_length=1)]
    access_classification: Literal["public", "synthetic", "internal"] = "synthetic"
    description: str = ""
    cases: list[EvaluationCase] = Field(min_length=1)


def load_eval_dataset(path: Path | str) -> EvalDataset:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    # Allow raw dict cases from JSON without forcing document_ids shape issues.
    if "cases" in payload:
        for case in payload["cases"]:
            case.setdefault("schema_version", "v1")
            props = case.get("expected_answer_properties") or {}
            if "expect_abstain" not in props and "answerable" in case:
                props["expect_abstain"] = not bool(case["answerable"])
                case["expected_answer_properties"] = props
    return EvalDataset.model_validate(payload)


def expect_abstain(case: EvaluationCase) -> bool:
    props: dict[str, Any] = case.expected_answer_properties or {}
    if "expect_abstain" in props:
        return bool(props["expect_abstain"])
    return not case.answerable
