from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.db.models import AssistantConversation, AssistantMessage, AssistantRole
from app.services.chat.events import record_assistant_site_event
from app.services.chat.formatting import build_citations, build_context_blocks, build_fallback_answer, serialize_recent_history
from app.services.provider_client import ProviderClient
from app.services.rate_limit import provider_budget_guard
from app.services.retrieval.service import KnowledgeRetrievalService

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.settings = get_settings()
        self.retrieval = KnowledgeRetrievalService(session)
        self.provider = ProviderClient()

    def respond(
        self,
        *,
        message: str,
        conversation_id: str | None = None,
        session_id: str | None = None,
        site_session_id: str | None = None,
        visitor_id: str | None = None,
        page_path: str | None = None,
        request: Request | None = None,
    ) -> dict:
        conversation = self._get_or_create_conversation(conversation_id=conversation_id, session_id=session_id)
        history = serialize_recent_history(conversation, max_history_messages=self.settings.max_history_messages)
        retrieved = self.retrieval.search(message, page_path=page_path)
        citations = build_citations(retrieved)
        context_blocks = build_context_blocks(retrieved)

        generated = None
        budget_scope = 'global'
        if provider_budget_guard.consume_generation_budget(
            scope=budget_scope,
            daily_limit=self.settings.provider_daily_generation_cap,
        ):
            try:
                generated = self.provider.generate_answer(
                    question=message,
                    context_blocks=context_blocks,
                    history=history,
                    page_path=page_path,
                )
            except Exception as exc:
                logger.exception(
                    'Assistant text generation failed using backend=%s model=%s: %s',
                    self.settings.provider_backend,
                    self.settings.provider_model,
                    exc,
                )
                generated = None
        else:
            logger.warning(
                'Assistant provider daily generation cap reached. backend=%s model=%s',
                self.settings.provider_backend,
                self.settings.provider_model,
            )

        if generated:
            logger.info(
                'Assistant response generated with backend=%s model=%s page_path=%s citations=%s',
                self.settings.provider_backend,
                self.settings.provider_model,
                page_path,
                len(citations),
            )
        else:
            logger.warning(
                'Assistant fell back to retrieval-only answer. backend=%s model=%s page_path=%s citations=%s',
                self.settings.provider_backend,
                self.settings.provider_model,
                page_path,
                len(citations),
            )

        answer = generated or build_fallback_answer(citations=citations)

        now = datetime.now(timezone.utc)
        conversation.last_message_at = now
        self.session.add(AssistantMessage(conversation_id=conversation.id, role=AssistantRole.USER, message_text=message))
        self.session.add(AssistantMessage(conversation_id=conversation.id, role=AssistantRole.ASSISTANT, message_text=answer))
        self.session.add(conversation)
        record_assistant_site_event(
            self.session,
            visitor_id=visitor_id,
            site_session_id=site_session_id,
            page_path=page_path,
            request=request,
            conversation_id=str(conversation.id),
            provider_backend=self.settings.provider_backend,
            citations=citations,
            question=message,
            answer=answer,
            used_fallback=generated is None,
            assistant_session_id=conversation.session_id,
        )
        self.session.commit()

        return {
            'conversation_id': str(conversation.id),
            'message': answer,
            'provider_backend': self.settings.provider_backend,
            'citations': citations,
        }

    def list_conversations(self) -> list[AssistantConversation]:
        return self.session.scalars(
            select(AssistantConversation)
            .options(selectinload(AssistantConversation.messages))
            .order_by(AssistantConversation.last_message_at.desc())
        ).all()

    def get_conversation(self, conversation_id: str) -> AssistantConversation | None:
        try:
            conversation_uuid = UUID(conversation_id)
        except ValueError:
            return None
        return self.session.scalar(
            select(AssistantConversation)
            .options(selectinload(AssistantConversation.messages))
            .where(AssistantConversation.id == conversation_uuid)
        )

    def _get_or_create_conversation(self, *, conversation_id: str | None, session_id: str | None) -> AssistantConversation:
        conversation: AssistantConversation | None = None

        if conversation_id:
            try:
                conversation_uuid = UUID(conversation_id)
            except ValueError:
                conversation_uuid = None
            if conversation_uuid is not None:
                conversation = self.session.get(AssistantConversation, conversation_uuid)

        if conversation is None and session_id:
            conversation = self.session.scalar(
                select(AssistantConversation).where(AssistantConversation.session_id == session_id)
            )

        if conversation is None:
            conversation = AssistantConversation(session_id=(session_id or uuid4().hex))
            self.session.add(conversation)
            self.session.flush()

        return conversation
