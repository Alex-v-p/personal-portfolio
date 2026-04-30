from __future__ import annotations

from types import SimpleNamespace

from app.domains.chat.service.formatting import build_citations, build_context_blocks, build_fallback_answer, serialize_recent_history
from app.domains.retrieval.service.models import RetrievedChunk


def test_build_fallback_answer_limits_to_top_three_citations() -> None:
    citations = [SimpleNamespace(title=f'Title {index}', source_type='project', excerpt='x' * 240) for index in range(4)]

    answer = build_fallback_answer(citations=citations)

    assert 'Title 0' in answer
    assert 'Title 1' in answer
    assert 'Title 2' in answer
    assert 'Title 3' not in answer
    assert '...' in answer


def test_build_fallback_answer_can_reply_in_dutch() -> None:
    answer = build_fallback_answer(citations=[], locale='nl')
    assert 'Ik heb hier nog niet genoeg relevante informatie' in answer


def test_serialize_recent_history_uses_latest_messages_only() -> None:
    conversation = SimpleNamespace(
        messages=[SimpleNamespace(created_at=index, role=SimpleNamespace(value='user'), message_text=f'message-{index}') for index in range(5)]
    )

    history = serialize_recent_history(conversation, max_history_messages=2)

    assert history == [
        {'role': 'user', 'text': 'message-3'},
        {'role': 'user', 'text': 'message-4'},
    ]


def test_build_context_blocks_formats_scores_excerpt_and_locale() -> None:
    blocks = build_context_blocks([
        RetrievedChunk(
            title='Portfolio Project',
            source_type='project',
            canonical_url='/projects/portfolio-project',
            excerpt='FastAPI backend with Angular frontend.',
            score=9.876,
            locale='nl',
        )
    ], locale='nl')

    assert blocks == ['[1] Portfolio Project (project, locale=Dutch, relevance=9.88)\nFastAPI backend with Angular frontend.']


def test_build_citations_localizes_internal_paths() -> None:
    citations = build_citations([
        RetrievedChunk(
            title='Portfolio Project',
            source_type='project',
            canonical_url='/projects',
            excerpt='FastAPI backend with Angular frontend.',
            score=8.0,
            locale='nl',
        )
    ], locale='nl')

    assert citations[0].canonical_url == '/nl/projects'
