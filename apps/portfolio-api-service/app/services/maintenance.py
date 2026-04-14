from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import lru_cache
import logging
from typing import Protocol
from uuid import uuid4

from redis import Redis
from redis.exceptions import RedisError
from sqlalchemy import delete, select
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings, get_settings
from app.db.models import AssistantConversation, AssistantMessage, SiteEvent
from app.db.session import get_session_factory

logger = logging.getLogger(__name__)

RETENTION_CLEANUP_JOB = 'retention-cleanup'
GITHUB_AUTO_REFRESH_JOB = 'github-auto-refresh'


class RedisStateClient(Protocol):
    def get(self, name: str) -> str | None: ...

    def set(
        self,
        name: str,
        value: str,
        *,
        nx: bool | None = None,
        ex: int | None = None,
    ) -> bool | None: ...

    def delete(self, name: str) -> int: ...

    def hgetall(self, name: str) -> dict[str, str]: ...

    def hset(self, name: str, mapping: dict[str, str]) -> int: ...

    def expire(self, name: str, time: int) -> bool: ...


@dataclass(slots=True)
class RetentionCleanupReport:
    ran_at: datetime
    site_events_deleted: int
    assistant_conversations_deleted: int
    assistant_messages_deleted: int


@dataclass(slots=True)
class MaintenanceJobStatus:
    enabled: bool
    status: str
    next_run_at: datetime | None
    seconds_until_next_run: int | None
    last_attempt_at: datetime | None
    last_success_at: datetime | None
    last_failed_at: datetime | None
    last_error: str | None


class MaintenanceJobInspector:
    def __init__(
        self,
        *,
        settings: Settings | None = None,
        redis_client: RedisStateClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.redis_client = redis_client or build_maintenance_redis_client(self.settings.redis_url)

    def github_auto_refresh_status(self, *, now: datetime | None = None) -> MaintenanceJobStatus:
        effective_now = ensure_utc_datetime(now)
        if not self.settings.github_auto_refresh_enabled:
            return MaintenanceJobStatus(
                enabled=False,
                status='disabled',
                next_run_at=None,
                seconds_until_next_run=None,
                last_attempt_at=None,
                last_success_at=None,
                last_failed_at=None,
                last_error=None,
            )

        state = self._job_state(GITHUB_AUTO_REFRESH_JOB)
        last_attempt_at = parse_iso_datetime(state.get('last_attempt_at'))
        last_success_at = parse_iso_datetime(state.get('last_success_at'))
        last_failed_at = parse_iso_datetime(state.get('last_failed_at'))
        last_error = (state.get('last_error') or '').strip() or None

        base_due_at = effective_now
        if last_success_at is not None:
            base_due_at = max(
                base_due_at,
                last_success_at + timedelta(seconds=self.settings.github_auto_refresh_interval_seconds),
            )
        if last_attempt_at is not None:
            base_due_at = max(
                base_due_at,
                last_attempt_at + timedelta(seconds=self.settings.github_auto_refresh_retry_interval_seconds),
            )

        if last_failed_at is not None and last_error:
            status = 'retry_scheduled' if base_due_at > effective_now else 'due'
        else:
            status = 'scheduled' if base_due_at > effective_now else 'due'

        seconds_until_next_run = max(int((base_due_at - effective_now).total_seconds()), 0)
        return MaintenanceJobStatus(
            enabled=True,
            status=status,
            next_run_at=base_due_at,
            seconds_until_next_run=seconds_until_next_run,
            last_attempt_at=last_attempt_at,
            last_success_at=last_success_at,
            last_failed_at=last_failed_at,
            last_error=last_error,
        )

    def _job_state(self, job_name: str) -> dict[str, str]:
        if self.redis_client is None:
            return {}
        try:
            return self.redis_client.hgetall(MaintenanceCoordinator._state_key(job_name))
        except RedisError:
            logger.exception('Maintenance inspector could not read state for job %s.', job_name)
            return {}


class RetentionCleanupService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def run(
        self,
        *,
        now: datetime | None = None,
        site_events_retention_days: int,
        assistant_activity_retention_days: int,
    ) -> RetentionCleanupReport:
        effective_now = ensure_utc_datetime(now)
        site_events_cutoff = effective_now - timedelta(days=site_events_retention_days)
        assistant_cutoff = effective_now - timedelta(days=assistant_activity_retention_days)

        try:
            site_events_deleted = self._delete_site_events_older_than(site_events_cutoff)
            assistant_messages_deleted, assistant_conversations_deleted = self._delete_assistant_activity_older_than(
                assistant_cutoff
            )
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        return RetentionCleanupReport(
            ran_at=effective_now,
            site_events_deleted=site_events_deleted,
            assistant_conversations_deleted=assistant_conversations_deleted,
            assistant_messages_deleted=assistant_messages_deleted,
        )

    def _delete_site_events_older_than(self, cutoff: datetime) -> int:
        result = self.session.execute(delete(SiteEvent).where(SiteEvent.created_at < cutoff))
        return max(int(result.rowcount or 0), 0)

    def _delete_assistant_activity_older_than(self, cutoff: datetime) -> tuple[int, int]:
        stale_conversation_ids = select(AssistantConversation.id).where(AssistantConversation.last_message_at < cutoff)
        message_result = self.session.execute(
            delete(AssistantMessage).where(AssistantMessage.conversation_id.in_(stale_conversation_ids))
        )
        conversation_result = self.session.execute(
            delete(AssistantConversation).where(AssistantConversation.id.in_(stale_conversation_ids))
        )
        return max(int(message_result.rowcount or 0), 0), max(int(conversation_result.rowcount or 0), 0)


class MaintenanceCoordinator:
    def __init__(
        self,
        *,
        settings: Settings | None = None,
        session_factory: sessionmaker[Session] | None = None,
        redis_client: RedisStateClient | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.session_factory = session_factory or get_session_factory()
        self.redis_client = redis_client or build_maintenance_redis_client(self.settings.redis_url)
        self.instance_token = uuid4().hex
        self._next_check_at: datetime | None = None

    @property
    def enabled(self) -> bool:
        return self.redis_client is not None

    def run_due_tasks(self, *, now: datetime | None = None) -> list[str]:
        effective_now = ensure_utc_datetime(now)
        if self._next_check_at is not None and effective_now < self._next_check_at:
            return []
        self._next_check_at = effective_now + timedelta(seconds=self.settings.maintenance_check_interval_seconds)

        if not self.enabled:
            return []

        completed_jobs: list[str] = []
        self._run_retention_cleanup_if_due(effective_now, completed_jobs)
        self._run_github_auto_refresh_if_due(effective_now, completed_jobs)
        return completed_jobs

    def _run_retention_cleanup_if_due(self, now: datetime, completed_jobs: list[str]) -> None:
        self._run_job_if_due(
            job_name=RETENTION_CLEANUP_JOB,
            now=now,
            success_interval_seconds=self.settings.retention_cleanup_interval_seconds,
            retry_interval_seconds=self.settings.retention_cleanup_retry_interval_seconds,
            completed_jobs=completed_jobs,
            action=self._execute_retention_cleanup,
        )

    def _run_github_auto_refresh_if_due(self, now: datetime, completed_jobs: list[str]) -> None:
        if not self.settings.github_auto_refresh_enabled:
            return
        username = self.settings.github_stats_username.strip()
        if not username:
            return
        self._run_job_if_due(
            job_name=GITHUB_AUTO_REFRESH_JOB,
            now=now,
            success_interval_seconds=self.settings.github_auto_refresh_interval_seconds,
            retry_interval_seconds=self.settings.github_auto_refresh_retry_interval_seconds,
            completed_jobs=completed_jobs,
            action=lambda: self._execute_github_auto_refresh(username),
        )

    def _run_job_if_due(
        self,
        *,
        job_name: str,
        now: datetime,
        success_interval_seconds: int,
        retry_interval_seconds: int,
        completed_jobs: list[str],
        action,
    ) -> None:
        try:
            if not self._job_is_due(
                job_name,
                now=now,
                success_interval_seconds=success_interval_seconds,
                retry_interval_seconds=retry_interval_seconds,
            ):
                return
            if not self._acquire_lock(job_name):
                return
        except RedisError:
            logger.exception('Maintenance scheduler could not evaluate job %s due to Redis state failure.', job_name)
            return

        try:
            self._mark_attempt(job_name, now=now)
            action()
        except Exception as exc:  # noqa: BLE001
            try:
                self._mark_failure(job_name, now=now, error_message=str(exc))
            except RedisError:
                logger.exception('Maintenance scheduler could not persist failure state for job %s.', job_name)
            logger.exception('Maintenance job %s failed: %s', job_name, exc)
        else:
            try:
                self._mark_success(job_name, now=now)
            except RedisError:
                logger.exception('Maintenance scheduler could not persist success state for job %s.', job_name)
            completed_jobs.append(job_name)
        finally:
            try:
                self._release_lock(job_name)
            except RedisError:
                logger.exception('Maintenance scheduler could not release lock for job %s.', job_name)

    def _execute_retention_cleanup(self) -> None:
        with self.session_factory() as session:
            report = RetentionCleanupService(session).run(
                site_events_retention_days=self.settings.site_events_retention_days,
                assistant_activity_retention_days=self.settings.assistant_activity_retention_days,
            )
        logger.info(
            'Maintenance retention cleanup completed. deleted_site_events=%s deleted_assistant_conversations=%s deleted_assistant_messages=%s',
            report.site_events_deleted,
            report.assistant_conversations_deleted,
            report.assistant_messages_deleted,
        )

    def _execute_github_auto_refresh(self, username: str) -> None:
        from app.domains.admin.service.github_snapshot_service import AdminGithubSnapshotService

        with self.session_factory() as session:
            snapshot = AdminGithubSnapshotService(session).refresh(username, prune_history=True)
        logger.info(
            'Maintenance GitHub auto refresh completed. username=%s snapshot_id=%s snapshot_date=%s',
            snapshot.username,
            snapshot.id,
            snapshot.snapshot_date,
        )

    def _job_is_due(
        self,
        job_name: str,
        *,
        now: datetime,
        success_interval_seconds: int,
        retry_interval_seconds: int,
    ) -> bool:
        state = self._job_state(job_name)
        last_success_at = parse_iso_datetime(state.get('last_success_at'))
        if last_success_at is not None and now < last_success_at + timedelta(seconds=success_interval_seconds):
            return False

        last_attempt_at = parse_iso_datetime(state.get('last_attempt_at'))
        if last_attempt_at is not None and now < last_attempt_at + timedelta(seconds=retry_interval_seconds):
            return False
        return True

    def _acquire_lock(self, job_name: str) -> bool:
        client = self._redis_client()
        result = client.set(
            self._lock_key(job_name),
            self.instance_token,
            nx=True,
            ex=self.settings.maintenance_lock_ttl_seconds,
        )
        return bool(result)

    def _release_lock(self, job_name: str) -> None:
        client = self._redis_client()
        lock_key = self._lock_key(job_name)
        if client.get(lock_key) == self.instance_token:
            client.delete(lock_key)

    def _mark_attempt(self, job_name: str, *, now: datetime) -> None:
        client = self._redis_client()
        state_key = self._state_key(job_name)
        client.hset(
            state_key,
            mapping={
                'last_attempt_at': now.isoformat(),
            },
        )
        client.expire(state_key, self.settings.maintenance_state_ttl_seconds)

    def _mark_success(self, job_name: str, *, now: datetime) -> None:
        client = self._redis_client()
        state_key = self._state_key(job_name)
        client.hset(
            state_key,
            mapping={
                'last_success_at': now.isoformat(),
                'last_error': '',
                'last_failed_at': '',
            },
        )
        client.expire(state_key, self.settings.maintenance_state_ttl_seconds)

    def _mark_failure(self, job_name: str, *, now: datetime, error_message: str) -> None:
        client = self._redis_client()
        state_key = self._state_key(job_name)
        client.hset(
            state_key,
            mapping={
                'last_failed_at': now.isoformat(),
                'last_error': error_message[:1000],
            },
        )
        client.expire(state_key, self.settings.maintenance_state_ttl_seconds)

    def _job_state(self, job_name: str) -> dict[str, str]:
        return self._redis_client().hgetall(self._state_key(job_name))

    def _redis_client(self) -> RedisStateClient:
        if self.redis_client is None:
            raise RedisError('Maintenance Redis client is unavailable.')
        return self.redis_client

    @staticmethod
    def _state_key(job_name: str) -> str:
        return f'portfolio:maintenance:{job_name}:state'

    @staticmethod
    def _lock_key(job_name: str) -> str:
        return f'portfolio:maintenance:{job_name}:lock'


@lru_cache
def build_maintenance_redis_client(redis_url: str) -> Redis | None:
    normalized = redis_url.strip()
    if not normalized or normalized.startswith('memory://'):
        return None
    return Redis.from_url(normalized, decode_responses=True)


def reset_maintenance_runtime_cache() -> None:
    build_maintenance_redis_client.cache_clear()


def ensure_utc_datetime(value: datetime | None) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return ensure_utc_datetime(parsed)
