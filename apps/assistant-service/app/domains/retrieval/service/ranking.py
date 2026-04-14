from __future__ import annotations

from typing import Iterable

from app.db.models import KnowledgeChunk, KnowledgeDocument
from app.domains.retrieval.service.intent import source_multiplier
from app.domains.retrieval.service.models import QueryIntent, RetrievedChunk
from app.domains.retrieval.service.text import dot, excerpt, metadata_text, parse_vector


def score_chunk(
    *,
    document: KnowledgeDocument,
    chunk: KnowledgeChunk,
    query: str,
    tokens: Iterable[str],
    query_vector: list[float] | None,
    intent: QueryIntent,
    page_path: str | None,
    source_type: str,
) -> float:
    chunk_text = (chunk.chunk_text or '').lower()
    title = (document.title or '').lower()
    metadata = metadata_text(document.metadata_json) + ' ' + metadata_text(chunk.metadata_json)
    phrase = query.strip().lower()

    lexical_score = 0.0
    matched_tokens = 0
    token_list = list(tokens)
    for token in token_list:
        chunk_hits = chunk_text.count(token)
        title_hits = title.count(token)
        metadata_hits = metadata.count(token)
        if chunk_hits or title_hits or metadata_hits:
            matched_tokens += 1
        lexical_score += min(chunk_hits, 4) * 1.8
        lexical_score += min(title_hits, 2) * 3.4
        lexical_score += min(metadata_hits, 3) * 1.5

    if token_list:
        lexical_score += (matched_tokens / len(token_list)) * 6.0
    if phrase and phrase in chunk_text:
        lexical_score += 7.5
    if phrase and phrase in title:
        lexical_score += 8.5
    if phrase and phrase in metadata:
        lexical_score += 3.5

    semantic_score = 0.0
    if query_vector is not None:
        chunk_vector = parse_vector(chunk.embedding_vector)
        if chunk_vector is not None and len(chunk_vector) == len(query_vector):
            semantic_score = max(dot(query_vector, chunk_vector), 0.0) * 18.0

    total = (lexical_score + semantic_score) * source_multiplier(source_type=source_type, intent=intent, page_path=page_path)
    if source_type in intent.suppress_sources:
        total *= 0.55
    if matched_tokens == 0 and semantic_score < 4.8:
        return 0.0
    return total


def filter_ranked_results(results: list[RetrievedChunk], intent: QueryIntent, *, chunk_limit: int) -> list[RetrievedChunk]:
    if not results:
        return []

    best_by_source: dict[str, float] = {}
    for item in results:
        best_by_source[item.source_type] = max(best_by_source.get(item.source_type, 0.0), item.score)

    best_overall = results[0].score
    strong_preferred_exists = any(
        best_by_source.get(source, 0.0) >= best_overall * 0.72 for source in intent.preferred_sources
    )

    deduped: list[RetrievedChunk] = []
    seen = set()
    background_count = 0
    for item in results:
        key = (item.title, item.excerpt)
        if key in seen:
            continue

        is_preferred = item.source_type in intent.preferred_sources
        is_supporting = item.source_type in intent.allowed_supporting_sources
        if strong_preferred_exists and not is_preferred:
            if not is_supporting:
                continue
            if item.score < best_overall * 0.68:
                continue
            if background_count >= 1:
                continue
            background_count += 1
        elif intent.source_priority and item.source_type not in intent.source_priority and item.score < best_overall * 0.82:
            continue

        seen.add(key)
        deduped.append(item)
        if len(deduped) >= chunk_limit:
            break
    return deduped


def build_retrieved_chunk(*, document: KnowledgeDocument, source_type: str, chunk: KnowledgeChunk, tokens: Iterable[str], score: float) -> RetrievedChunk:
    return RetrievedChunk(
        title=document.title,
        source_type=source_type,
        canonical_url=document.canonical_url,
        excerpt=excerpt(chunk.chunk_text, tokens),
        score=score,
    )
