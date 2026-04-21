from __future__ import annotations

from app.domains.chat.schema import CitationOut
from app.services.localization import detect_assistant_locale, locale_language_name, localize_internal_path


def serialize_recent_history(conversation, *, max_history_messages: int) -> list[dict[str, str]]:
    messages = sorted(conversation.messages, key=lambda item: item.created_at)
    recent = messages[-max_history_messages:]
    return [
        {'role': item.role.value if hasattr(item.role, 'value') else str(item.role), 'text': item.message_text}
        for item in recent
    ]


def resolve_response_locale(*, locale: str | None = None, page_path: str | None = None) -> str:
    return detect_assistant_locale(locale=locale, page_path=page_path)


def build_citations(retrieved, *, locale: str = 'en') -> list[CitationOut]:
    resolved_locale = resolve_response_locale(locale=locale)
    return [
        CitationOut(
            title=item.title,
            source_type=item.source_type,
            canonical_url=localize_internal_path(item.canonical_url, resolved_locale),
            excerpt=item.excerpt,
        )
        for item in retrieved
    ]


def build_context_blocks(retrieved, *, locale: str = 'en') -> list[str]:
    language = locale_language_name(resolve_response_locale(locale=locale))
    return [
        f'[{index + 1}] {item.title} ({item.source_type}, locale={language}, relevance={item.score:.2f})\n{item.excerpt}'
        for index, item in enumerate(retrieved)
    ]


def build_fallback_answer(*, citations: list[CitationOut], locale: str = 'en') -> str:
    resolved_locale = resolve_response_locale(locale=locale)
    if resolved_locale == 'nl':
        if not citations:
            return (
                'Ik kon nog niet genoeg relevante geïndexeerde portfolio-inhoud vinden om daar met vertrouwen op te antwoorden. '
                'Probeer iets te vragen over projecten, ervaring, blogposts, skills of het portfolio in het algemeen.'
            )

        opening = 'Ik kon daar net geen volledig uitgewerkt antwoord op genereren, maar deze portfolio-onderdelen lijken het meest relevant.'
    else:
        if not citations:
            return (
                "I couldn't find enough relevant indexed portfolio content to answer that confidently yet. "
                'Try asking about projects, experience, blog posts, skills, or the overall portfolio.'
            )

        opening = 'I could not generate a polished answer just now, but these portfolio sections look most relevant to that question.'

    relevant = []
    for citation in citations[:3]:
        excerpt = citation.excerpt.strip()
        if len(excerpt) > 220:
            excerpt = excerpt[:217].rstrip() + '...'
        relevant.append(f'- {citation.title} ({citation.source_type}): {excerpt}')
    return opening + '\n\n' + '\n'.join(relevant)
