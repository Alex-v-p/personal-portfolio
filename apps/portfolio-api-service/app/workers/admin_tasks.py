from __future__ import annotations

from dataclasses import asdict
import logging
import time

from app.db.session import get_session_factory
from app.domains.admin.schema import AdminAssistantKnowledgeStatusOut, AdminGithubSnapshotOut
from app.domains.admin.service.github_snapshot_service import AdminGithubSnapshotService
from app.domains.knowledge.service.service import KnowledgeSyncService
from app.services.async_tasks import (
    GITHUB_REFRESH_TASK,
    KNOWLEDGE_REBUILD_TASK,
    TaskQueueUnavailable,
    get_admin_task_queue,
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')


def _process_task(task_type: str, payload: dict[str, object]) -> dict[str, object]:
    session_factory = get_session_factory()
    with session_factory() as session:
        if task_type == GITHUB_REFRESH_TASK:
            snapshot = AdminGithubSnapshotService(session).refresh(
                payload.get('username') if isinstance(payload.get('username'), str) else None,
                prune_history=bool(payload.get('prune_history', True)),
            )
            return AdminGithubSnapshotOut.model_validate(snapshot).model_dump(mode='json', by_alias=True)
        if task_type == KNOWLEDGE_REBUILD_TASK:
            report = KnowledgeSyncService(session).rebuild()
            return AdminAssistantKnowledgeStatusOut(**asdict(report)).model_dump(mode='json', by_alias=True)
    raise ValueError(f'Unsupported admin task type: {task_type}')


def main() -> None:
    queue = get_admin_task_queue()
    if not queue.enabled:
        logger.error('Admin task worker requires Redis. REDIS_URL=%s', queue.redis_url)
        return
    try:
        restored = queue.restore_processing_tasks()
    except TaskQueueUnavailable as exc:
        logger.error('Could not restore admin processing tasks: %s', exc)
        return
    if restored:
        logger.info('Re-queued %s admin task(s) left in processing.', restored)

    logger.info('Admin task worker started.')
    while True:
        envelope = None
        raw_item = ''
        try:
            reserved = queue.reserve(timeout_seconds=5)
            if reserved is None:
                continue
            envelope, raw_item = reserved
            logger.info('Processing admin task %s (%s)', envelope.task_id, envelope.task_type)
            result = _process_task(envelope.task_type, envelope.payload)
            queue.mark_succeeded(envelope.task_id, result=result, raw_item=raw_item)
            logger.info('Completed admin task %s (%s)', envelope.task_id, envelope.task_type)
        except KeyboardInterrupt:
            logger.info('Admin task worker stopped.')
            return
        except TaskQueueUnavailable as exc:
            logger.error('Redis task queue unavailable: %s', exc)
            time.sleep(2)
        except Exception as exc:  # noqa: BLE001
            task_id = envelope.task_id if envelope is not None else 'unknown'
            logger.exception('Admin task %s failed: %s', task_id, exc)
            if task_id != 'unknown' and raw_item:
                try:
                    queue.mark_failed(task_id, error_message=str(exc), raw_item=raw_item)
                except TaskQueueUnavailable:
                    logger.error('Failed to update admin task %s failure state.', task_id)


if __name__ == '__main__':
    main()
