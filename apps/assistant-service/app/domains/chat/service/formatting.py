from __future__ import annotations

import re

from app.domains.chat.schema import CitationOut
from app.services.localization import detect_assistant_locale, locale_language_name, localize_internal_path


PRIVATE_CITATION_SOURCE_TYPES = {'assistant_note'}


def is_public_citation_source(source_type: str | None) -> bool:
    return (source_type or '').strip().lower() not in PRIVATE_CITATION_SOURCE_TYPES


def serialize_recent_history(conversation, *, max_history_messages: int) -> list[dict[str, str]]:
    messages = sorted(conversation.messages, key=lambda item: item.created_at)
    recent = messages[-max_history_messages:]
    return [
        {'role': item.role.value if hasattr(item.role, 'value') else str(item.role), 'text': item.message_text}
        for item in recent
    ]


def build_conversation_memory_block(conversation, *, locale: str = 'en') -> str | None:
    summary = (getattr(conversation, 'conversation_summary', None) or '').strip()
    if not summary:
        return None
    language = locale_language_name(resolve_response_locale(locale=locale))
    return (
        'Short-lived conversation memory for this same visitor chat. '
        'Use it only to understand follow-up questions and preferences; do not present it as permanent memory. '
        f'Preferred language: {language}.\n{summary}'
    )


def build_contextual_retrieval_query(
    *,
    question: str,
    conversation,
    max_history_messages: int,
    max_chars: int = 1400,
) -> str:
    """Add lightweight chat context to ambiguous retrieval queries without sending the full transcript."""
    parts = [question.strip()]

    summary = (getattr(conversation, 'conversation_summary', None) or '').strip()
    if summary:
        parts.append('Conversation summary: ' + summary)

    recent_history = serialize_recent_history(conversation, max_history_messages=max_history_messages)
    recent_user_turns = [item['text'].strip() for item in recent_history if item.get('role') == 'user' and item.get('text')]
    if recent_user_turns:
        parts.append('Recent visitor questions: ' + ' | '.join(recent_user_turns[-3:]))

    query = '\n\n'.join(part for part in parts if part)
    if len(query) > max_chars:
        query = query[: max_chars - 3].rstrip() + '...'
    return query


def resolve_response_locale(*, locale: str | None = None, page_path: str | None = None) -> str:
    return detect_assistant_locale(locale=locale, page_path=page_path)


def build_citations(retrieved, *, locale: str = 'en') -> list[CitationOut]:
    resolved_locale = resolve_response_locale(locale=locale)
    citations: list[CitationOut] = []
    for item in retrieved:
        if not is_public_citation_source(item.source_type):
            continue
        citations.append(
            CitationOut(
                title=item.title,
                source_type=item.source_type,
                canonical_url=localize_internal_path(item.canonical_url, resolved_locale),
                excerpt=item.excerpt,
            )
        )
    return citations


def build_context_blocks(retrieved, *, locale: str = 'en') -> list[str]:
    language = locale_language_name(resolve_response_locale(locale=locale))
    blocks: list[str] = []
    for index, item in enumerate(retrieved):
        visibility_note = 'background guidance' if item.source_type == 'assistant_note' else item.source_type
        blocks.append(
            f'[{index + 1}] {item.title} ({visibility_note}, locale={language}, relevance={item.score:.2f})\n{item.excerpt}'
        )
    return blocks


def build_conversational_answer(*, question: str, locale: str = 'en') -> str | None:
    resolved_locale = resolve_response_locale(locale=locale)
    normalized = _normalize(question)
    if not normalized:
        return _message(
            resolved_locale,
            en='Hi! I can help you explore Alex’s portfolio, projects, skills, experience, and blog posts.',
            nl='Hoi! Ik kan u helpen om Alex’ portfolio, projecten, vaardigheden, ervaring en blogposts te verkennen.',
        )

    if normalized in _THANKS_PATTERNS:
        return _message(
            resolved_locale,
            en='You’re welcome! Ask me anything about the portfolio whenever you like.',
            nl='Graag gedaan! Vraag gerust iets over het portfolio wanneer u wilt.',
        )

    if normalized in _GREETING_PATTERNS or normalized in _HOW_ARE_YOU_PATTERNS:
        return _message(
            resolved_locale,
            en='I’m doing well, thanks! I’m here as a guide for Alex’s portfolio. I can talk through his projects, skills, experience, blog posts, or what might make him a good fit for a role.',
            nl='Met mij gaat het goed, bedankt! Ik ben hier als gids voor Alex’ portfolio. Ik kan u helpen met Alex’ projecten, vaardigheden, ervaring, blogposts of waarom Alex bij een rol zou kunnen passen.',
        )

    if any(phrase in normalized for phrase in _CAPABILITY_PHRASES):
        return _message(
            resolved_locale,
            en='I can help you quickly understand Alex’s background: compare projects, summarize their strengths, point you to GitHub READMEs or blog posts, explain their tech stack, and answer recruiter-style questions.',
            nl='Ik kan u snel helpen Alex’ achtergrond te begrijpen: projecten vergelijken, sterktes samenvatten, u naar GitHub-README’s of blogposts verwijzen, de techstack uitleggen en recruiter-achtige vragen beantwoorden.',
        )

    return None


def build_fallback_answer(*, citations: list[CitationOut], locale: str = 'en') -> str:
    resolved_locale = resolve_response_locale(locale=locale)
    if resolved_locale == 'nl':
        if not citations:
            return (
                'Ik heb nog niet genoeg details om dat goed te beantwoorden. '
                'U kunt wel iets vragen over Alex’ projecten, ervaring, vaardigheden, blogposts of algemene profiel.'
            )
        opening = 'Dit komt het dichtst in de buurt:'
    else:
        if not citations:
            return (
                "I don't have enough detail to answer that confidently yet. "
                "You can ask me about Alex's projects, experience, skills, blog posts, or overall profile."
            )
        opening = 'Here’s the closest useful match I found:'

    relevant = []
    for citation in citations[:3]:
        excerpt = citation.excerpt.strip()
        if len(excerpt) > 220:
            excerpt = excerpt[:217].rstrip() + '...'
        source_label = citation.source_type.replace('_', ' ')
        relevant.append(f'- {citation.title} ({source_label}): {excerpt}')
    return opening + '\n\n' + '\n'.join(relevant)


_SOURCE_DISCLOSURE_PATTERNS = (
    (re.compile(r"\b(?:based on|according to|from)\s+(?:the\s+)?(?:provided|retrieved|available)\s+(?:information|context|details|data)[:,]?\s*", re.IGNORECASE), ''),
    (re.compile(r"\b(?:based on|according to|from)\s+(?:the\s+)?(?:portfolio|context)[:,]?\s*", re.IGNORECASE), ''),
    (re.compile(r"\b(?:the\s+)?(?:provided|retrieved|available)\s+(?:information|context|details|data)\s+(?:shows|suggests|indicates|says|mentions)\s+that\s+", re.IGNORECASE), ''),
    (re.compile(r"\b(?:the\s+)?(?:provided|retrieved|available)\s+(?:information|context|details|data)\b", re.IGNORECASE), 'the portfolio'),
    (re.compile(r"\b(?:retrieved|indexed)\s+(?:chunks|context|matches)\b", re.IGNORECASE), 'portfolio details'),
)


def sanitize_assistant_answer(answer: str) -> str:
    """Remove retrieval/source-mechanics wording from user-facing assistant replies."""
    cleaned = answer.strip()
    cleaned = cleaned.replace('’', "'").replace('‘', "'").replace('�', "'")
    for pattern, replacement in _SOURCE_DISCLOSURE_PATTERNS:
        cleaned = pattern.sub(replacement, cleaned)
    cleaned = re.sub(r'\s+([,.;:!?])', r'\1', cleaned)
    cleaned = re.sub(r'(?m)^\s*,\s*', '', cleaned)
    cleaned = re.sub(r'(?m)^\s*[:;]\s*', '', cleaned)
    cleaned = re.sub(r' {2,}', ' ', cleaned)
    cleaned = re.sub(r'(^|[.!?]\s+)(the portfolio)\b', lambda match: match.group(1) + 'The portfolio', cleaned)
    return cleaned.strip()


def trim_conversation_summary(summary: str, *, max_chars: int) -> str:
    normalized = re.sub(r'\s+', ' ', summary).strip()
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + '...'


def _normalize(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9' ]+", ' ', text.lower())
    return re.sub(r'\s+', ' ', text).strip()


def _message(locale: str, *, en: str, nl: str) -> str:
    return nl if resolve_response_locale(locale=locale) == 'nl' else en


_GREETING_PATTERNS = {
    'hi', 'hello', 'hey', 'yo', 'good morning', 'good afternoon', 'good evening', 'hoi', 'hallo', 'hey daar',
}

_HOW_ARE_YOU_PATTERNS = {
    'how are you', 'how are you doing', "how's it going", 'how is it going', 'are you ok', 'are you okay',
    'hoe gaat het', 'hoe gaat het met je', 'alles goed', 'hoe is het',
}

_THANKS_PATTERNS = {
    'thanks', 'thank you', 'thx', 'ty', 'bedankt', 'dank je', 'dankjewel', 'merci',
}

_CAPABILITY_PHRASES = {
    'what can you do', 'what do you do', 'how can you help', 'help me with', 'who are you',
    'wat kan je', 'wat kun je', 'waarmee kan je helpen', 'wie ben je',
}
