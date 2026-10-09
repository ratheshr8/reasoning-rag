"""Citation resolution against normalized document text."""

from __future__ import annotations

from reasoning_rag.models.evidence import Evidence
from reasoning_rag.models.normalized import NormalizedDocument


def citations_resolve(evidence: list[Evidence], normalized: NormalizedDocument) -> list[str]:
    """Return evidence IDs whose source ranges do not match document text."""
    unresolved: list[str] = []
    text = normalized.text
    for item in evidence:
        start = item.source_range.start_offset
        end = item.source_range.end_offset
        if start < 0 or end > len(text) or end < start:
            unresolved.append(item.id)
            continue
        slice_text = text[start:end]
        # exact_text may be truncated with ellipsis for CLI budgets
        core = item.exact_text.removesuffix("…")
        if core and core not in slice_text and not slice_text.startswith(core.rstrip()):
            # Allow whitespace-normalized containment of the leading portion.
            if core.strip() not in slice_text and not slice_text.strip().startswith(
                core.strip()[:80]
            ):
                unresolved.append(item.id)
    return unresolved
