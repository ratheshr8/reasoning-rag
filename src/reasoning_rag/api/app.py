"""FastAPI application for the local demo and API boundary."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from reasoning_rag import __version__
from reasoning_rag.api.schemas import (
    AskRequest,
    AskResponse,
    ErrorResponse,
    HealthResponse,
    SamplesResponse,
)
from reasoning_rag.api.service import (
    list_samples,
    provider_notice,
    resolve_sample_path,
    trace_summary,
)
from reasoning_rag.config import Settings, load_settings
from reasoning_rag.ingestion import IngestionError
from reasoning_rag.models.common import AccessClassification, RetrievalMode
from reasoning_rag.qa import ask_document
from reasoning_rag.tree import TreeBuildError

DEMO_STATIC = Path(__file__).resolve().parent.parent / "demo" / "static"


def create_app(
    *,
    settings: Settings | None = None,
    repo_root: Path | None = None,
) -> FastAPI:
    cfg = settings or load_settings()
    root = (repo_root or Path.cwd()).resolve()

    app = FastAPI(
        title="reasoning-rag local demo",
        version=__version__,
        description=(
            "Local prototype API. Treat uploads as untrusted. "
            "Fixture mode keeps document text local."
        ),
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            package_version=__version__,
            provider_notice=provider_notice(cfg),
        )

    @app.get("/api/samples", response_model=SamplesResponse)
    def samples() -> SamplesResponse:
        return SamplesResponse(
            samples=list_samples(root, cfg),
            max_upload_bytes=cfg.max_upload_bytes,
            provider_notice=provider_notice(cfg),
        )

    @app.post(
        "/api/ask",
        response_model=AskResponse,
        responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}},
    )
    def ask_json(body: AskRequest) -> AskResponse:
        if not body.sample_id:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "sample_id required for JSON ask; use /api/ask/upload for files",
                    "code": "sample_required",
                },
            )
        try:
            path = resolve_sample_path(body.sample_id, root)
        except KeyError as exc:
            raise HTTPException(
                status_code=400,
                detail={"error": str(exc), "code": "unknown_sample"},
            ) from exc
        except FileNotFoundError as exc:
            raise HTTPException(
                status_code=400,
                detail={"error": str(exc), "code": "sample_missing"},
            ) from exc
        return _run_ask(
            path,
            body.question,
            mode=body.retrieval_mode,
            synthetic=body.synthetic,
            settings=cfg,
        )

    @app.post(
        "/api/ask/upload",
        response_model=AskResponse,
        responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}},
    )
    async def ask_upload(
        question: Annotated[str, Form(min_length=1, max_length=4000)],
        file: Annotated[UploadFile, File()],
        retrieval_mode: Annotated[str, Form()] = RetrievalMode.TREE_FIRST.value,
        synthetic: Annotated[bool, Form()] = True,
    ) -> AskResponse:
        filename = file.filename or "upload.md"
        suffix = Path(filename).suffix.lower()
        if suffix not in {".md", ".markdown"}:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "only Markdown uploads (.md, .markdown) are supported",
                    "code": "unsupported_media_type",
                },
            )

        raw = await file.read(cfg.max_upload_bytes + 1)
        if len(raw) > cfg.max_upload_bytes:
            raise HTTPException(
                status_code=413,
                detail={
                    "error": f"upload exceeds max_upload_bytes={cfg.max_upload_bytes}",
                    "code": "file_too_large",
                },
            )
        if not raw:
            raise HTTPException(
                status_code=400,
                detail={"error": "empty upload", "code": "empty_upload"},
            )

        try:
            mode = RetrievalMode(retrieval_mode)
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail={"error": f"invalid retrieval_mode: {retrieval_mode}", "code": "bad_mode"},
            ) from exc

        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=suffix or ".md",
            delete=False,
        ) as handle:
            handle.write(raw)
            temp_path = Path(handle.name)

        try:
            return _run_ask(
                temp_path,
                question,
                mode=mode,
                synthetic=synthetic,
                settings=cfg,
            )
        finally:
            temp_path.unlink(missing_ok=True)

    if DEMO_STATIC.is_dir():
        app.mount("/static", StaticFiles(directory=str(DEMO_STATIC)), name="static")

        @app.get("/")
        def demo_index() -> FileResponse:
            return FileResponse(DEMO_STATIC / "index.html")

    return app


def _run_ask(
    path: Path,
    question: str,
    *,
    mode: RetrievalMode,
    synthetic: bool,
    settings: Settings,
) -> AskResponse:
    classification = AccessClassification.SYNTHETIC if synthetic else AccessClassification.PUBLIC
    try:
        result = ask_document(
            path,
            question,
            settings=settings,
            access_classification=classification,
            retrieval_mode=mode,
        )
    except IngestionError as exc:
        raise HTTPException(
            status_code=400,
            detail={"error": exc.message, "code": exc.code},
        ) from exc
    except (TreeBuildError, ValueError) as exc:
        message = getattr(exc, "message", str(exc))
        code = getattr(exc, "code", "ask_error")
        raise HTTPException(
            status_code=400,
            detail={"error": message, "code": code},
        ) from exc

    return AskResponse(
        result=result,
        trace_summary=trace_summary(result),
        provider_notice=provider_notice(settings),
        upload_limits={
            "max_upload_bytes": settings.max_upload_bytes,
            "allowed_extensions": [".md", ".markdown"],
        },
    )
