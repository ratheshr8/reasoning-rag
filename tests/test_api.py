"""Local demo API tests (uses TestClient; does not start a long-lived server)."""

from pathlib import Path

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient

from reasoning_rag.api import create_app
from reasoning_rag.config import Settings

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def client() -> TestClient:
    app = create_app(settings=Settings(), repo_root=ROOT)
    return TestClient(app)


def test_health_and_samples(client: TestClient) -> None:
    health = client.get("/health")
    assert health.status_code == 200
    body = health.json()
    assert body["status"] == "ok"
    assert body["provider_notice"]["model_provider"] == "fixture"
    assert body["provider_notice"]["sends_document_text_externally"] is False

    samples = client.get("/api/samples")
    assert samples.status_code == 200
    payload = samples.json()
    assert payload["max_upload_bytes"] > 0
    assert any(item["id"] == "acme-widget-spec" for item in payload["samples"])


def test_ask_sample_returns_citations_or_abstain(client: TestClient) -> None:
    response = client.post(
        "/api/ask",
        json={
            "question": "What supply voltage does the Acme Widget require?",
            "sample_id": "acme-widget-spec",
            "retrieval_mode": "tree-first",
            "synthetic": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "trace_summary" in payload
    assert payload["result"]["answer"]["abstained"] is False
    assert payload["result"]["answer"]["claim_links"]


def test_upload_rejects_non_markdown(client: TestClient) -> None:
    response = client.post(
        "/api/ask/upload",
        data={"question": "hello", "retrieval_mode": "tree-first", "synthetic": "true"},
        files={"file": ("note.pdf", b"%PDF-1.4", "application/pdf")},
    )
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "unsupported_media_type"


def test_demo_index_served(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "reasoning-rag" in response.text
