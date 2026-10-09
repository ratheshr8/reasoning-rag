"""CLI for local developer experience and inspectable ingestion."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console

from reasoning_rag import __version__
from reasoning_rag.config import load_settings
from reasoning_rag.ingestion import IngestionError, ingest_markdown_path
from reasoning_rag.logging_setup import configure_logging, get_logger
from reasoning_rag.models.common import AccessClassification

app = typer.Typer(
    name="reasoning-rag",
    help="Hierarchy-aware document QA (prototype).",
    no_args_is_help=True,
    add_completion=False,
)
err_console = Console(stderr=True)


def _print_validation_error(exc: ValidationError) -> None:
    err_console.print("[bold red]Configuration error[/bold red]")
    for error in exc.errors():
        loc = ".".join(str(part) for part in error.get("loc", ()))
        msg = error.get("msg", "invalid value")
        err_console.print(f"  - {loc or 'settings'}: {msg}")
    err_console.print(
        "Set REASONING_RAG_* environment variables or create a .env from .env.example."
    )


@app.callback()
def main(
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable DEBUG logging."),
    ] = False,
) -> None:
    """reasoning-rag command group."""
    try:
        settings = load_settings()
    except ValidationError as exc:
        _print_validation_error(exc)
        raise typer.Exit(code=2) from exc

    level = "DEBUG" if verbose else settings.log_level.value
    configure_logging(level=level, json_logs=settings.log_json)


@app.command("version")
def version_cmd() -> None:
    """Print the package version."""
    typer.echo(__version__)


@app.command("config")
def config_cmd() -> None:
    """Validate and print the active configuration (secrets redacted)."""
    try:
        settings = load_settings()
    except ValidationError as exc:
        _print_validation_error(exc)
        raise typer.Exit(code=2) from exc

    payload = settings.model_dump(mode="json")
    if payload.get("model_api_key"):
        payload["model_api_key"] = "***"
    typer.echo(json.dumps(payload, indent=2, default=str))


@app.command("doctor")
def doctor_cmd() -> None:
    """Check that the skeleton can load settings without secrets."""
    log = get_logger(__name__, component="cli")
    try:
        settings = load_settings()
    except ValidationError as exc:
        _print_validation_error(exc)
        raise typer.Exit(code=2) from exc

    log.info(
        "doctor_ok mode=%s provider=%s",
        settings.retrieval_mode.value,
        settings.model_provider,
    )
    typer.echo("ok: configuration validated")


@app.command("ingest")
def ingest_cmd(
    path: Annotated[
        Path,
        typer.Argument(exists=False, readable=False, help="Path to a Markdown (.md) file."),
    ],
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Write normalized JSON to this path instead of stdout.",
        ),
    ] = None,
    synthetic: Annotated[
        bool,
        typer.Option("--synthetic", help="Mark access_classification as synthetic."),
    ] = False,
) -> None:
    """Ingest a Markdown file and print inspectable normalized JSON with provenance."""
    log = get_logger(__name__, component="cli")
    try:
        settings = load_settings()
    except ValidationError as exc:
        _print_validation_error(exc)
        raise typer.Exit(code=2) from exc

    classification = (
        AccessClassification.SYNTHETIC if synthetic else AccessClassification.PUBLIC
    )
    try:
        result = ingest_markdown_path(
            path,
            settings=settings,
            access_classification=classification,
        )
    except IngestionError as exc:
        err_console.print(f"[bold red]Ingestion failed[/bold red] ({exc.code}): {exc.message}")
        raise typer.Exit(code=1) from exc

    payload = result.model_dump(mode="json")
    # Avoid dumping huge bodies twice in default CLI view: keep text + sections.
    text = json.dumps(payload, indent=2, ensure_ascii=True)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
        log.info(
            "ingest_ok document_id=%s sections=%s warnings=%s output=%s",
            result.document.id,
            len(result.sections),
            len(result.warnings),
            str(output),
        )
        typer.echo(f"wrote {output}")
        return

    log.info(
        "ingest_ok document_id=%s sections=%s warnings=%s",
        result.document.id,
        len(result.sections),
        len(result.warnings),
    )
    typer.echo(text)


if __name__ == "__main__":
    app()
