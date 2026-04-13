from __future__ import annotations

from typing import Any

from app.db.models import AssistantConversation, AssistantRole, EventType, SiteEvent
from app.domains.admin.schema import AdminAssistantConversationSummaryOut, AdminVisitSessionSummaryOut, AdminVisitorActivitySummaryOut


class AdminRepositoryActivityMixin:
    def _build_site_activity_rollups(
        self, events: list[SiteEvent]
    ) -> tuple[list[AdminVisitorActivitySummaryOut], list[AdminVisitSessionSummaryOut]]:
        visitor_rollups: dict[str, dict[str, Any]] = {}
        visit_rollups: dict[tuple[str, str], dict[str, Any]] = {}

        for event in reversed(events):
            metadata = event.metadata_json if isinstance(event.metadata_json, dict) else {}
            ip_address = metadata.get('ip_address') if isinstance(metadata.get('ip_address'), str) else None

            visitor_entry = visitor_rollups.setdefault(
                event.visitor_id,

                {
                    'visitor_id': event.visitor_id,
                    'first_seen_at': event.created_at,
                    'last_seen_at': event.created_at,
                    'total_events': 0,
                    'page_views': 0,
                    'assistant_messages': 0,
                    'contact_submissions': 0,
                    'session_ids': set(),
                    'latest_page_path': None,
                    'latest_ip_address': None,
                },
            )

            visitor_entry['first_seen_at'] = min(visitor_entry['first_seen_at'], event.created_at)
            visitor_entry['last_seen_at'] = max(visitor_entry['last_seen_at'], event.created_at)
            visitor_entry['total_events'] += 1

            if event.session_id:
                visitor_entry['session_ids'].add(event.session_id)

            if event.event_type == EventType.PAGE_VIEW:
                visitor_entry['page_views'] += 1

            elif event.event_type == EventType.ASSISTANT_MESSAGE:
                visitor_entry['assistant_messages'] += 1

            elif event.event_type == EventType.CONTACT_SUBMIT:
                visitor_entry['contact_submissions'] += 1

            if visitor_entry['last_seen_at'] == event.created_at:
                visitor_entry['latest_page_path'] = event.page_path
                visitor_entry['latest_ip_address'] = ip_address



            if event.session_id:

                visit_key = (event.visitor_id, event.session_id)
                visit_entry = visit_rollups.setdefault(
                    visit_key,
                    {
                        'session_id': event.session_id,
                        'visitor_id': event.visitor_id,
                        'started_at': event.created_at,
                        'last_activity_at': event.created_at,
                        'total_events': 0,
                        'page_views': 0,
                        'assistant_messages': 0,
                        'contact_submissions': 0,
                        'entry_page_path': event.page_path,
                        'last_page_path': event.page_path,
                        'ip_address': ip_address,
                    },
                )

                visit_entry['started_at'] = min(visit_entry['started_at'], event.created_at)
                visit_entry['last_activity_at'] = max(visit_entry['last_activity_at'], event.created_at)
                visit_entry['total_events'] += 1
                if event.event_type == EventType.PAGE_VIEW:
                    visit_entry['page_views'] += 1
                elif event.event_type == EventType.ASSISTANT_MESSAGE:
                    visit_entry['assistant_messages'] += 1
                elif event.event_type == EventType.CONTACT_SUBMIT:
                    visit_entry['contact_submissions'] += 1
                if event.created_at <= visit_entry['started_at']:
                    visit_entry['entry_page_path'] = event.page_path
                if event.created_at >= visit_entry['last_activity_at']:
                    visit_entry['last_page_path'] = event.page_path
                    if ip_address:
                        visit_entry['ip_address'] = ip_address



        visitors = [
            AdminVisitorActivitySummaryOut(
                visitor_id=item['visitor_id'],
                first_seen_at=item['first_seen_at'].isoformat(),
                last_seen_at=item['last_seen_at'].isoformat(),
                total_events=item['total_events'],
                unique_sessions=len(item['session_ids']),
                page_views=item['page_views'],
                assistant_messages=item['assistant_messages'],
                contact_submissions=item['contact_submissions'],
                latest_page_path=item['latest_page_path'],
                latest_ip_address=item['latest_ip_address'],
            )
            for item in sorted(visitor_rollups.values(), key=lambda value: value['last_seen_at'], reverse=True)
        ]

        visits = [
            AdminVisitSessionSummaryOut(
                session_id=item['session_id'],
                visitor_id=item['visitor_id'],
                started_at=item['started_at'].isoformat(),
                last_activity_at=item['last_activity_at'].isoformat(),
                total_events=item['total_events'],
                page_views=item['page_views'],
                assistant_messages=item['assistant_messages'],
                contact_submissions=item['contact_submissions'],
                entry_page_path=item['entry_page_path'],
                last_page_path=item['last_page_path'],
                ip_address=item['ip_address'],
            )
            for item in sorted(visit_rollups.values(), key=lambda value: value['last_activity_at'], reverse=True)
        ]
        return visitors, visits

    def _build_conversation_activity_links(self, events: list[SiteEvent]) -> dict[str, dict[str, Any]]:
        links: dict[str, dict[str, Any]] = {}

        for event in events:
            if event.event_type != EventType.ASSISTANT_MESSAGE or not isinstance(event.metadata_json, dict):
                continue

            conversation_id = event.metadata_json.get('conversation_id')

            if not isinstance(conversation_id, str) or conversation_id in links:
                continue

            used_fallback = event.metadata_json.get('used_fallback')

            links[conversation_id] = {
                'visitor_id': event.visitor_id,
                'site_session_id': event.session_id,
                'page_path': event.page_path,
                'used_fallback': bool(used_fallback) if isinstance(used_fallback, bool) else None,
            }
        return links

    def _map_assistant_conversation(
        self, conversation: AssistantConversation, activity_link: dict[str, Any] | None = None
    ) -> AdminAssistantConversationSummaryOut:

        ordered_messages = sorted(conversation.messages, key=lambda item: item.created_at)
        user_messages = [item for item in ordered_messages if item.role == AssistantRole.USER]
        assistant_messages = [item for item in ordered_messages if item.role == AssistantRole.ASSISTANT]

        return AdminAssistantConversationSummaryOut(
            id=str(conversation.id),
            session_id=conversation.session_id,
            visitor_id=activity_link.get('visitor_id') if activity_link else None,
            site_session_id=activity_link.get('site_session_id') if activity_link else None,
            page_path=activity_link.get('page_path') if activity_link else None,
            started_at=conversation.started_at.isoformat(),
            last_message_at=conversation.last_message_at.isoformat(),
            total_messages=len(ordered_messages),
            user_message_count=len(user_messages),
            assistant_message_count=len(assistant_messages),
            used_fallback=activity_link.get('used_fallback') if activity_link else None,
            first_user_message=user_messages[0].message_text if user_messages else None,
            latest_assistant_message=assistant_messages[-1].message_text if assistant_messages else None,
        )
