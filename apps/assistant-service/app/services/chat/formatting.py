from __future__ import annotations

from app.schemas.chat import CitationOut


def serialize_recent_history(conversation, *, max_history_messages: int) -> list[dict[str, str]]:
    messages = sorted(conversation.messages, key=lambda item: item.created_at)
    recent = messages[-max_history_messages:]
    return [
        {'role': item.role.value if hasattr(item.role, 'value') else str(item.role), 'text': item.message_text}
        for item in recent
    ]


def build_citations(retrieved) -> list[CitationOut]:
    return [
        CitationOut(
            title=item.title,
            source_type=item.source_type,
            canonical_url=item.canonical_url,
            excerpt=item.excerpt,
        )
        for item in retrieved
    ]


def build_context_blocks(retrieved) -> list[str]:
    return [
        f'[{index + 1}] {item.title} ({item.source_type}, relevance={item.score:.2f})\n{item.excerpt}'
        for index, item in enumerate(retrieved)
    ]


def build_fallback_answer(*, citations: list[CitationOut]) -> str:
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
