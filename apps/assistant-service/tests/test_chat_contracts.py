from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient


def test_chat_endpoint_accepts_camel_case_request_and_returns_frontend_contract(tmp_path: Path) -> None:
    database_path = tmp_path / 'assistant-contract.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['ASSISTANT_PROVIDER_BACKEND'] = 'mock'

    from app.core.config import get_settings
    from app.db.models import Base, KnowledgeChunk, KnowledgeDocument, KnowledgeSourceType
    from app.db.session import get_engine, get_session_factory

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    engine = get_engine()
    Base.metadata.create_all(engine)

    from sqlalchemy.orm import Session

    now = datetime.now(timezone.utc)
    with Session(engine) as session:
        document = KnowledgeDocument(
            source_type=KnowledgeSourceType.PROJECT,
            source_id=None,
            title='Personal Portfolio',
            canonical_url='/projects/personal-portfolio',
            content_markdown='Angular frontend and FastAPI backend.',
            content_platform='portfolio',
            metadata_json={'skills': ['Angular', 'FastAPI']},
            created_at=now,
            updated_at=now,
        )
        session.add(document)
        session.flush()
        session.add(
            KnowledgeChunk(
                document_id=document.id,
                chunk_index=0,
                chunk_text='The portfolio uses Angular for the frontend and FastAPI for the backend.',
                embedding_vector=None,
                metadata_json={'section': 'summary'},
            )
        )
        session.commit()

    from app.main import create_app

    with TestClient(create_app()) as client:
        response = client.post(
            '/api/chat/respond',
            json={
                'message': 'What backend does the portfolio use?',
                'conversationId': None,
                'sessionId': 'assistant-session-1',
                'siteSessionId': 'site-session-1',
                'visitorId': 'visitor-1',
                'pagePath': '/projects/personal-portfolio',
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert {'conversationId', 'message', 'providerBackend', 'citations'} <= set(body)
    assert body['providerBackend'] == 'mock'
    assert 'FastAPI' in body['message']
    assert {'title', 'sourceType', 'canonicalUrl', 'excerpt'} <= set(body['citations'][0])


def test_private_assistant_notes_are_used_as_context_but_not_returned_as_citations() -> None:
    from app.domains.chat.service.formatting import build_citations, build_context_blocks
    from app.domains.retrieval.service.models import RetrievedChunk

    retrieved = [
        RetrievedChunk(
            title='Overall skills and strengths',
            source_type='assistant_note',
            canonical_url=None,
            excerpt='Alex is strongest when a project combines practical software engineering and clear communication.',
            score=0.94,
        ),
        RetrievedChunk(
            title='Portfolio project',
            source_type='project',
            canonical_url='https://github.com/shuzu/portfolio#readme',
            excerpt='A project using Angular and FastAPI.',
            score=0.88,
        ),
    ]

    context_blocks = build_context_blocks(retrieved, locale='en')
    citations = build_citations(retrieved, locale='en')

    assert any('Alex is strongest' in block for block in context_blocks)
    assert all(citation.source_type != 'assistant_note' for citation in citations)
    assert [citation.source_type for citation in citations] == ['project']
