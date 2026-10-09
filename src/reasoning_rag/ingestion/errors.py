"""Ingestion failure types. Fail safely; do not silently repair bad inputs."""


class IngestionError(Exception):
    """Base class for ingestion failures."""

    def __init__(self, message: str, *, code: str = "ingestion_error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationFailedError(IngestionError):
    def __init__(self, message: str, *, code: str = "validation_failed") -> None:
        super().__init__(message, code=code)


class UnsupportedMediaTypeError(IngestionError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="unsupported_media_type")
