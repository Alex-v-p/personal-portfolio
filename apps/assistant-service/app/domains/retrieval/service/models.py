from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RetrievedChunk:
    title: str
    source_type: str
    canonical_url: str | None
    excerpt: str
    score: float


@dataclass(slots=True)
class QueryIntent:
    name: str
    preferred_sources: tuple[str, ...] = ()
    allowed_supporting_sources: tuple[str, ...] = ()
    suppress_sources: tuple[str, ...] = ()
    page_path_hint: str | None = None

    @property
    def source_priority(self) -> tuple[str, ...]:
        return self.preferred_sources + tuple(
            source for source in self.allowed_supporting_sources if source not in self.preferred_sources
        )
