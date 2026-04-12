from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.db.models import AssistantConversation, AssistantMessage, AssistantRole
from app.schemas.chat import CitationOut
from app.services.provider_client import ProviderClient
from app.services.retrieval_service import KnowledgeRetrievalService

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
        page_path: str | None = None,
    ) -> dict:
        conversation = self._get_or_create_conversation(conversation_id=conversation_id, session_id=session_id)
        history = self._serialize_recent_history(conversation)
        retrieved = self.retrieval.search(message, page_path=page_path)
        citations = [
            CitationOut(
                title=item.title,
                source_type=item.source_type,
                canonical_url=item.canonical_url,
                excerpt=item.excerpt,
            )
            for item in retrieved
        ]
        context_blocks = [
            f'[{index + 1}] {item.title} ({item.source_type}, relevance={item.score:.2f})\n{item.excerpt}'
            for index, item in enumerate(retrieved)
        ]

        generated = None
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

        answer = generated or self._build_fallback_answer(citations=citations)

        now = datetime.now(timezone.utc)
        conversation.last_message_at = now
        self.session.add(AssistantMessage(conversation_id=conversation.id, role=AssistantRole.USER, message_text=message))
        self.session.add(AssistantMessage(conversation_id=conversation.id, role=AssistantRole.ASSISTANT, message_text=answer))
        self.session.add(conversation)
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

    def _serialize_recent_history(self, conversation: AssistantConversation) -> list[dict[str, str]]:
        messages = sorted(conversation.messages, key=lambda item: item.created_at)
        recent = messages[-self.settings.max_history_messages :]
        return [{'role': item.role.value if hasattr(item.role, 'value') else str(item.role), 'text': item.message_text} for item in recent]

    def _build_fallback_answer(self, *, citations: list[CitationOut]) -> str:
        if not citations:
            return (
                "I couldn't find enough relevant indexed portfolio content to answer that confidently yet. "
                'Try asking about projects, experience, blog posts, skills, or the overall portfolio.'
            )

        opening = (
            'I could not generate a polished answer just now, but these portfolio sections look most relevant '
            'to that question.'
        )
        relevant = []
        for citation in citations[:3]:
            excerpt = citation.excerpt.strip()
            if len(excerpt) > 220:
                excerpt = excerpt[:217].rstrip() + '...'
            relevant.append(f'- {citation.title} ({citation.source_type}): {excerpt}')
        return opening + '\n\n' + '\n'.join(relevant)
