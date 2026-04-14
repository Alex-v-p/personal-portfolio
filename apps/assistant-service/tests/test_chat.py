from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient


def test_chat_responds_with_retrieved_portfolio_content(tmp_path: Path) -> None:
    database_path = tmp_path / 'assistant-test.sqlite3'
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
            title='Portfolio CMS Project',
            canonical_url='/projects',
            content_markdown='Angular CMS with FastAPI and PostgreSQL.',
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
                chunk_text='This project uses Angular on the frontend and FastAPI on the backend.',
                embedding_vector=None,
                metadata_json={'section': 'summary'},
            )
        )
        session.commit()

    from app.main import create_app

    with TestClient(create_app()) as client:
        response = client.post('/api/chat/respond', json={'message': 'What does the portfolio use on the backend?'})
        assert response.status_code == 200
        payload = response.json()
        assert payload['conversationId']
        assert 'FastAPI' in payload['message']
        assert payload['citations'][0]['title'] == 'Portfolio CMS Project'



def test_chat_is_rate_limited(tmp_path: Path) -> None:
    database_path = tmp_path / 'assistant-rate-limit.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['REDIS_URL'] = 'memory://'
    os.environ['ASSISTANT_PROVIDER_BACKEND'] = 'mock'
    os.environ['CHAT_RATE_LIMIT_MAX_REQUESTS'] = '1'
    os.environ['CHAT_RATE_LIMIT_WINDOW_SECONDS'] = '60'

    from app.core.config import get_settings
    from app.db.models import Base
    from app.db.session import get_engine, get_session_factory
    from app.services.rate_limit import reset_rate_limit_state

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
    reset_rate_limit_state()

    engine = get_engine()
    Base.metadata.create_all(engine)

    from app.main import create_app

    with TestClient(create_app()) as client:
        payload = {'message': 'Tell me about the portfolio backend.', 'visitor_id': 'visitor-1'}
        first = client.post('/api/chat/respond', json=payload)
        second = client.post('/api/chat/respond', json=payload)

    assert first.status_code == 200
    assert second.status_code == 429
    assert second.json()['detail'] == 'Too many assistant messages were sent in a short period. Please wait a moment before trying again.'


def test_provider_daily_generation_cap_forces_fallback(tmp_path: Path, monkeypatch) -> None:
    database_path = tmp_path / 'assistant-budget.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['REDIS_URL'] = 'memory://'
    os.environ['ASSISTANT_PROVIDER_BACKEND'] = 'ollama'
    os.environ['PROVIDER_DAILY_GENERATION_CAP'] = '1'
    os.environ['CHAT_RATE_LIMIT_MAX_REQUESTS'] = '10'

    from app.core.config import get_settings
    from app.db.models import Base
    from app.db.session import get_engine, get_session_factory
    from app.domains.providers.client import ProviderClient
    from app.services.rate_limit import reset_rate_limit_state

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
    reset_rate_limit_state()

    engine = get_engine()
    Base.metadata.create_all(engine)

    monkeypatch.setattr(ProviderClient, 'generate_answer', lambda self, **kwargs: 'Generated portfolio answer.')

    from app.main import create_app

    with TestClient(create_app()) as client:
        first = client.post('/api/chat/respond', json={'message': 'Question one'})
        second = client.post('/api/chat/respond', json={'message': 'Question two'})

    assert first.status_code == 200
    assert first.json()['message'] == 'Generated portfolio answer.'
    assert second.status_code == 200
    assert "I couldn't find enough relevant indexed portfolio content" in second.json()['message']



def test_chat_returns_async_task_when_redis_queue_is_available(tmp_path: Path, monkeypatch) -> None:
    database_path = tmp_path / 'assistant-async.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['ASSISTANT_PROVIDER_BACKEND'] = 'mock'

    from app.core.config import get_settings
    from app.db.models import Base
    from app.db.session import get_engine, get_session_factory
    from app.main import create_app
    from app.services.async_tasks import ChatTaskRecord

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
    Base.metadata.create_all(get_engine())

    class FakeQueue:
        enabled = True
        poll_after_ms = 900

        def enqueue(self, task_type: str, payload: dict[str, object]) -> ChatTaskRecord:
            assert task_type == 'chat-response'
            assert payload['message'] == 'Tell me about the backend.'
            return ChatTaskRecord(task_id='chat-task-1', task_type=task_type, status='queued', submitted_at='2026-04-14T10:00:00+00:00')

    monkeypatch.setattr('app.api.routes.chat.get_chat_task_queue', lambda: FakeQueue())

    with TestClient(create_app()) as client:
        response = client.post('/api/chat/respond', json={'message': 'Tell me about the backend.'})

    assert response.status_code == 202
    body = response.json()
    assert body['taskId'] == 'chat-task-1'
    assert body['status'] == 'queued'
    assert body['pollAfterMs'] == 900
    assert body['conversationId']


def test_chat_task_status_returns_completed_payload(monkeypatch) -> None:
    from app.main import create_app
    from app.services.async_tasks import ChatTaskRecord

    class FakeQueue:
        def get(self, task_id: str) -> ChatTaskRecord | None:
            assert task_id == 'chat-task-1'
            return ChatTaskRecord(
                task_id='chat-task-1',
                task_type='chat-response',
                status='succeeded',
                submitted_at='2026-04-14T10:00:00+00:00',
                started_at='2026-04-14T10:00:01+00:00',
                completed_at='2026-04-14T10:00:05+00:00',
                result={
                    'conversationId': 'conversation-1',
                    'message': 'The backend uses FastAPI.',
                    'providerBackend': 'mock',
                    'citations': [],
                },
            )

    monkeypatch.setattr('app.api.routes.chat.get_chat_task_queue', lambda: FakeQueue())

    with TestClient(create_app()) as client:
        response = client.get('/api/chat/tasks/chat-task-1')

    assert response.status_code == 200
    assert response.json()['status'] == 'succeeded'
    assert response.json()['message'] == 'The backend uses FastAPI.'
