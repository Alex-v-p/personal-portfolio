from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class KnowledgeSyncReport:
    total_documents: int
    total_chunks: int
    documents_by_source_type: dict[str, int]
    latest_updated_at: str | None
