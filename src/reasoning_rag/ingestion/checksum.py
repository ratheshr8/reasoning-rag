"""Checksum helpers for provenance."""

from __future__ import annotations

import hashlib
import re


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_prefixed(data: bytes) -> str:
    return f"sha256:{sha256_hex(data)}"


def document_id_from_name(source_name: str, checksum_hex: str) -> str:
    """Stable-ish document id from filename stem and checksum prefix."""
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", source_name.rsplit(".", 1)[0]).strip("-._")
    if not stem:
        stem = "document"
    stem = stem[:80]
    return f"doc.{stem}.{checksum_hex[:12]}"
