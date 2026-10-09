"""Central configuration with startup validation."""

from enum import StrEnum
from pathlib import Path

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from reasoning_rag.models.common import RetrievalMode


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Settings(BaseSettings):
    """Application settings. Secrets stay in the environment; never commit them."""

    model_config = SettingsConfigDict(
        env_prefix="REASONING_RAG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    data_dir: Path = Field(default=Path("data"), description="Local data and corpus directory")
    store_dir: Path = Field(default=Path(".store"), description="Local document/tree store")
    retrieval_mode: RetrievalMode = RetrievalMode.TREE_FIRST
    log_level: LogLevel = LogLevel.INFO
    log_json: bool = True
    max_upload_bytes: int = Field(default=2_000_000, ge=1_024, le=50_000_000)
    model_provider: str = Field(default="fixture", min_length=1, max_length=64)
    model_name: str = Field(default="fixture-v0", min_length=1, max_length=128)
    # Optional; fixture mode does not require a key.
    model_api_key: str | None = Field(default=None, repr=False)
    tree_max_nodes: int = Field(default=500, ge=1, le=50_000)
    tree_max_summaries: int = Field(default=64, ge=0, le=50_000)
    tree_summary_max_chars: int = Field(default=240, ge=32, le=4_000)
    retrieve_top_k: int = Field(default=3, ge=1, le=50)
    retrieve_min_score: float = Field(default=0.2, ge=0.0, le=10.0)
    evidence_max_chars: int = Field(default=1200, ge=64, le=20_000)
    plan_max_depth: int = Field(default=6, ge=0, le=32)
    plan_max_nodes: int = Field(default=3, ge=1, le=50)
    plan_max_model_calls: int = Field(default=0, ge=0, le=32)
    plan_max_context_tokens: int = Field(default=4000, ge=128, le=200_000)

    @field_validator("data_dir", "store_dir", mode="before")
    @classmethod
    def coerce_path(cls, value: object) -> object:
        if isinstance(value, str) and value.strip() == "":
            raise ValueError("path settings must not be empty")
        return value

    @field_validator("model_api_key")
    @classmethod
    def reject_placeholder_keys(cls, value: str | None, info: ValidationInfo) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if stripped == "":
            return None
        if stripped.lower() in {"changeme", "your_api_key_here", "xxx"}:
            raise ValueError(
                f"{info.field_name} looks like a placeholder; unset it or provide a real secret"
            )
        return stripped


def load_settings() -> Settings:
    """Load and validate settings. Raises pydantic.ValidationError with actionable messages."""
    return Settings()
