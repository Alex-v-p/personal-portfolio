from __future__ import annotations

import logging
import time

from app.db.session import get_session_factory
from app.domains.chat.schema import ChatResponse
from app.domains.chat.service.service import ChatService
from app.services.async_tasks import CHAT_RESPONSE_TASK, TaskQueueUnavailable, get_chat_task_queue

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')


def _process_chat_task(payload: dict[str, object]) -> dict[str, object]:
    session_factory = get_session_factory()
    with session_factory() as session:
        response = ChatService(session).respond(
            message=str(payload.get('message') or ''),
            conversation_id=str(payload.get('conversation_id') or '') or None,
            session_id=str(payload.get('session_id') or '') or None,
            site_session_id=str(payload.get('site_session_id') or '') or None,
            visitor_id=str(payload.get('visitor_id') or '') or None,
            page_path=str(payload.get('page_path') or '') or None,
            request=None,
        )
        # Store worker results in Python-native snake_case inside Redis.
        # The API layer can still serialize aliases for clients, and existing
        # queued tasks with camelCase fields remain readable via validation_alias.
        return ChatResponse(**response).model_dump(mode='json')


def main() -> None:
    queue = get_chat_task_queue()
    if not queue.enabled:
        logger.error('Chat task worker requires Redis. REDIS_URL=%s', queue.redis_url)
        return
    try:
        restored = queue.restore_processing_tasks()
    except TaskQueueUnavailable as exc:
        logger.error('Could not restore chat processing tasks: %s', exc)
        return
    if restored:
        logger.info('Re-queued %s chat task(s) left in processing.', restored)

    logger.info('Chat task worker started.')
    while True:
        envelope = None
        raw_item = ''
        try:
            reserved = queue.reserve(timeout_seconds=5)
            if reserved is None:
                continue
            envelope, raw_item = reserved
            if envelope.task_type != CHAT_RESPONSE_TASK:
                raise ValueError(f'Unsupported chat task type: {envelope.task_type}')
            logger.info('Processing chat task %s', envelope.task_id)
            result = _process_chat_task(envelope.payload)
            queue.mark_succeeded(envelope.task_id, result=result, raw_item=raw_item)
            logger.info('Completed chat task %s', envelope.task_id)
        except KeyboardInterrupt:
            logger.info('Chat task worker stopped.')
            return
        except TaskQueueUnavailable as exc:
            logger.error('Redis chat queue unavailable: %s', exc)
            time.sleep(2)
        except Exception as exc:  # noqa: BLE001
            task_id = envelope.task_id if envelope is not None else 'unknown'
            logger.exception('Chat task %s failed: %s', task_id, exc)
            if task_id != 'unknown' and raw_item:
                try:
                    queue.mark_failed(task_id, error_message=str(exc), raw_item=raw_item)
                except TaskQueueUnavailable:
                    logger.error('Failed to update chat task %s failure state.', task_id)


if __name__ == '__main__':
    main()
