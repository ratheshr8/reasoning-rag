"""CLI skeleton for local developer experience."""

from __future__ import annotations

import json
from typing import Annotated

import typer
from pydantic import ValidationError
from rich.console import Console

from reasoning_rag import __version__
from reasoning_rag.config import load_settings
from reasoning_rag.logging_setup import configure_logging, get_logger

app = typer.Typer(
    name="reasoning-rag",
    help="Hierarchy-aware document QA (prototype skeleton).",
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
        "skeleton_ok mode=%s provider=%s",
        settings.retrieval_mode.value,
        settings.model_provider,
    )
    typer.echo("ok: configuration validated; retrieval runtime not implemented yet")


if __name__ == "__main__":
    app()
