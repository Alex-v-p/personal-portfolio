from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_engine, get_session_factory, reset_database_caches
from app.services.async_tasks import reset_admin_task_queue_cache
from app.services.maintenance import MaintenanceCoordinator, RetentionCleanupService, reset_maintenance_runtime_cache
from app.services.rate_limit import reset_rate_limit_state
from infra.postgres.bootstrap.bootstrap_core import initialize_database


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.hashes: dict[str, dict[str, str]] = {}

    def get(self, name: str) -> str | None:
        return self.values.get(name)

    def set(self, name: str, value: str, *, nx: bool | None = None, ex: int | None = None) -> bool | None:
        if nx and name in self.values:
            return False
        self.values[name] = value
        return True

    def delete(self, name: str) -> int:
        existed = 1 if name in self.values else 0
        self.values.pop(name, None)
        self.hashes.pop(name, None)
        return existed

    def hgetall(self, name: str) -> dict[str, str]:
        return dict(self.hashes.get(name, {}))

    def hset(self, name: str, mapping: dict[str, str]) -> int:
        bucket = self.hashes.setdefault(name, {})
        bucket.update(mapping)
        return len(mapping)

    def expire(self, name: str, time: int) -> bool:
        return True


def _initialize_database(tmp_path: Path) -> None:
    database_path = tmp_path / 'portfolio-maintenance.sqlite3'
    os.environ['DATABASE_URL'] = f'sqlite:///{database_path}'
    os.environ['MEDIA_PUBLIC_BASE_URL'] = 'http://media.example.test'
    os.environ['REDIS_URL'] = 'memory://'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    os.environ['ADMIN_PASSWORD'] = 'test-admin-pass'
    os.environ['ADMIN_DISPLAY_NAME'] = 'Test Admin'
    get_settings.cache_clear()
    reset_database_caches()
    reset_rate_limit_state()
    reset_admin_task_queue_cache()
    reset_maintenance_runtime_cache()
    assert initialize_database(auto_seed=True, recreate_on_drift=True, raise_on_error=True) is True


def test_retention_cleanup_removes_old_site_events_and_stale_assistant_activity(tmp_path: Path) -> None:
    _initialize_database(tmp_path)

    from app.db.models import AssistantConversation, AssistantMessage, AssistantRole, EventType, SiteEvent

    now = datetime(2026, 4, 14, 12, 0, tzinfo=timezone.utc)
    old_time = now - timedelta(days=120)
    recent_time = now - timedelta(days=7)

    with Session(get_engine()) as session:
        stale_conversation = AssistantConversation(session_id='stale-session', started_at=old_time, last_message_at=old_time)
        fresh_conversation = AssistantConversation(session_id='fresh-session', started_at=recent_time, last_message_at=recent_time)
        session.add_all(
            [
                SiteEvent(
                    visitor_id='visitor-old',
                    session_id='session-old',
                    page_path='/assistant',
                    event_type=EventType.ASSISTANT_MESSAGE,
                    created_at=old_time,
                ),
                SiteEvent(
                    visitor_id='visitor-fresh',
                    session_id='session-fresh',
                    page_path='/projects',
                    event_type=EventType.PAGE_VIEW,
                    created_at=recent_time,
                ),
                stale_conversation,
                fresh_conversation,
            ]
        )
        session.flush()
        session.add_all(
            [
                AssistantMessage(
                    conversation_id=stale_conversation.id,
                    role=AssistantRole.USER,
                    message_text='Old question',
                    created_at=old_time,
                ),
                AssistantMessage(
                    conversation_id=stale_conversation.id,
                    role=AssistantRole.ASSISTANT,
                    message_text='Old answer',
                    created_at=old_time,
                ),
                AssistantMessage(
                    conversation_id=fresh_conversation.id,
                    role=AssistantRole.USER,
                    message_text='Fresh question',
                    created_at=recent_time,
                ),
            ]
        )
        session.commit()

    with Session(get_engine()) as session:
        report = RetentionCleanupService(session).run(
            now=now,
            site_events_retention_days=90,
            assistant_activity_retention_days=90,
        )
        assert report.site_events_deleted == 1
        assert report.assistant_conversations_deleted == 1
        assert report.assistant_messages_deleted == 2

    with Session(get_engine()) as session:
        remaining_events = session.scalars(select(SiteEvent).order_by(SiteEvent.created_at.asc())).all()
        remaining_conversations = session.scalars(select(AssistantConversation).order_by(AssistantConversation.session_id.asc())).all()
        remaining_messages = session.scalars(select(AssistantMessage).order_by(AssistantMessage.created_at.asc())).all()

    assert len(remaining_events) == 1
    assert remaining_events[0].visitor_id == 'visitor-fresh'
    assert [conversation.session_id for conversation in remaining_conversations] == ['fresh-session']
    assert len(remaining_messages) == 1
    assert remaining_messages[0].message_text == 'Fresh question'



def test_maintenance_coordinator_runs_daily_jobs_only_when_due(monkeypatch) -> None:
    now = datetime(2026, 4, 14, 9, 0, tzinfo=timezone.utc)
    redis = FakeRedis()
    calls: list[str] = []
    settings = Settings(
        redis_url='redis://maintenance.example.test/0',
        maintenance_check_interval_seconds=60,
        retention_cleanup_interval_seconds=60 * 60 * 24,
        retention_cleanup_retry_interval_seconds=60 * 60,
        github_auto_refresh_enabled=True,
        github_auto_refresh_interval_seconds=60 * 60 * 24,
        github_auto_refresh_retry_interval_seconds=60 * 60,
    )
    coordinator = MaintenanceCoordinator(settings=settings, session_factory=get_session_factory(), redis_client=redis)

    monkeypatch.setattr(coordinator, '_execute_retention_cleanup', lambda: calls.append('cleanup'))
    monkeypatch.setattr(coordinator, '_execute_github_auto_refresh', lambda username: calls.append(f'github:{username}'))

    first_completed = coordinator.run_due_tasks(now=now)
    second_completed = coordinator.run_due_tasks(now=now + timedelta(seconds=30))
    third_completed = coordinator.run_due_tasks(now=now + timedelta(minutes=2))
    fourth_completed = coordinator.run_due_tasks(now=now + timedelta(days=1, minutes=2))

    assert first_completed == ['retention-cleanup', 'github-auto-refresh']
    assert second_completed == []
    assert third_completed == []
    assert fourth_completed == ['retention-cleanup', 'github-auto-refresh']
    assert calls == ['cleanup', 'github:Alex-v-p', 'cleanup', 'github:Alex-v-p']



def test_maintenance_coordinator_retries_github_refresh_after_retry_window(monkeypatch) -> None:
    now = datetime(2026, 4, 14, 10, 0, tzinfo=timezone.utc)
    redis = FakeRedis()
    calls = {'count': 0}
    settings = Settings(
        redis_url='redis://maintenance.example.test/0',
        maintenance_check_interval_seconds=60,
        retention_cleanup_interval_seconds=60 * 60 * 24,
        retention_cleanup_retry_interval_seconds=60 * 60,
        github_auto_refresh_enabled=True,
        github_auto_refresh_interval_seconds=60 * 60 * 24,
        github_auto_refresh_retry_interval_seconds=60 * 60,
    )
    coordinator = MaintenanceCoordinator(settings=settings, session_factory=get_session_factory(), redis_client=redis)

    monkeypatch.setattr(coordinator, '_execute_retention_cleanup', lambda: None)

    def failing_once(username: str) -> None:
        calls['count'] += 1
        if calls['count'] == 1:
            raise RuntimeError('temporary GitHub failure')

    monkeypatch.setattr(coordinator, '_execute_github_auto_refresh', failing_once)

    first_completed = coordinator.run_due_tasks(now=now)
    failed_state = redis.hgetall('portfolio:maintenance:github-auto-refresh:state')
    second_completed = coordinator.run_due_tasks(now=now + timedelta(minutes=2))
    third_completed = coordinator.run_due_tasks(now=now + timedelta(hours=1, minutes=2))

    assert first_completed == ['retention-cleanup']
    assert 'temporary GitHub failure' in failed_state.get('last_error', '')
    assert second_completed == []
    assert third_completed == ['github-auto-refresh']
    assert calls['count'] == 2
    state = redis.hgetall('portfolio:maintenance:github-auto-refresh:state')
    assert state['last_success_at'] == (now + timedelta(hours=1, minutes=2)).isoformat()
    assert state.get('last_error', '') == ''
