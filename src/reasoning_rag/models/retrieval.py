"""Retrieval plan contracts."""

from typing import Annotated

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt

from reasoning_rag.models.common import RetrievalMode, SchemaVersion


class RetrievalBudgets(BaseModel):
    max_depth: PositiveInt = 4
    max_nodes: PositiveInt = 32
    max_model_calls: NonNegativeInt = 8
    max_context_tokens: PositiveInt = 4000


class RetrievalStep(BaseModel):
    action: Annotated[str, Field(min_length=1, max_length=64)]
    target_node_ids: list[str] = Field(default_factory=list)
    rationale: str | None = None


class RetrievalPlan(BaseModel):
    schema_version: SchemaVersion = "v1"
    strategy: RetrievalMode = RetrievalMode.TREE_FIRST
    steps: list[RetrievalStep] = Field(default_factory=list)
    candidate_node_ids: list[str] = Field(default_factory=list)
    budgets: RetrievalBudgets = Field(default_factory=RetrievalBudgets)
    planner_version: Annotated[str, Field(min_length=1, max_length=64)] = "rules-v0"
