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
