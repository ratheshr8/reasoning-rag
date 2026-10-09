"""Shared helpers for the local demo API."""

from __future__ import annotations

from pathlib import Path

from reasoning_rag.api.schemas import ProviderNotice, SampleDocument, TraceSummary
from reasoning_rag.config import Settings
from reasoning_rag.models.trace import AskResult

SAMPLE_CATALOG: list[dict[str, str]] = [
    {
        "id": "acme-widget-spec",
        "title": "Acme Widget Specification",
        "path": "data/corpus/v0/acme-widget-spec.md",
        "access_classification": "synthetic",
        "description": (
            "Synthetic technical spec with power, safety, abstention, and conflict fixtures."
        ),
    }
]


def provider_notice(settings: Settings) -> ProviderNotice:
    external = settings.model_provider.lower() != "fixture"
    if external:
        message = (
            f"Configured provider '{settings.model_provider}' may send document text to an "
            "external model service. Confirm that is intended before uploading confidential files."
        )
    else:
        message = (
            "Fixture provider is active: document text is processed locally and is not sent to "
            "an external model API by this demo."
        )
    return ProviderNotice(
        model_provider=settings.model_provider,
        model_name=settings.model_name,
        sends_document_text_externally=external,
        message=message,
    )


def list_samples(repo_root: Path, settings: Settings) -> list[SampleDocument]:
    samples: list[SampleDocument] = []
    for item in SAMPLE_CATALOG:
        path = (repo_root / item["path"]).resolve()
        if path.is_file():
            samples.append(
                SampleDocument(
                    id=item["id"],
                    title=item["title"],
                    path=str(path),
                    access_classification=item["access_classification"],  # type: ignore[arg-type]
                    description=item["description"],
                )
            )
    return samples


def resolve_sample_path(sample_id: str, repo_root: Path) -> Path:
    for item in SAMPLE_CATALOG:
        if item["id"] == sample_id:
            path = (repo_root / item["path"]).resolve()
            if not path.is_file():
                raise FileNotFoundError(f"sample file missing: {path}")
            return path
    raise KeyError(f"unknown sample_id: {sample_id}")


def trace_summary(result: AskResult) -> TraceSummary:
    components = sorted({event.component for event in result.events})
    candidates: list[str] = []
    if result.retrieval_plan:
        candidates = list(result.retrieval_plan.candidate_node_ids)
    conflict_topics: list[str] = []
    if result.verification:
        conflict_topics = [conflict.topic for conflict in result.verification.conflicts]
    return TraceSummary(
        event_count=len(result.events),
        components=components,
        candidate_node_ids=candidates,
        conflict_topics=conflict_topics,
    )
