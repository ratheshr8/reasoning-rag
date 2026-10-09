"""Configuration validation tests."""

import pytest
from pydantic import ValidationError

from reasoning_rag.config import Settings


def test_default_settings_need_no_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("REASONING_RAG_MODEL_API_KEY", raising=False)
    settings = Settings()
    assert settings.model_provider == "fixture"
    assert settings.model_api_key is None


def test_placeholder_api_key_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REASONING_RAG_MODEL_API_KEY", "changeme")
    with pytest.raises(ValidationError):
        Settings()
