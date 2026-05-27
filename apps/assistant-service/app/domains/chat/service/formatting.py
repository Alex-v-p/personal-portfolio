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
    resolved_locale = resolve_response_locale(locale=locale)
    language = locale_language_name(resolved_locale)
    blocks: list[str] = []
    for index, item in enumerate(retrieved):
        visibility_note = _source_label(item.source_type, resolved_locale)
        if language == 'Dutch':
            blocks.append(
                f'[{index + 1}] {item.title} ({visibility_note}, taal=Nederlands, relevantie={item.score:.2f})\n{item.excerpt}'
            )
        else:
            blocks.append(
                f'[{index + 1}] {item.title} ({visibility_note}, language=English, relevance={item.score:.2f})\n{item.excerpt}'
            )
    return blocks


def _source_label(source_type: str, locale: str) -> str:
    normalized_locale = resolve_response_locale(locale=locale)
    normalized_source = (source_type or '').strip().lower()
    if normalized_locale == 'nl':
        return {
            'assistant_note': 'achtergrondrichtlijn',
            'blog_post': 'blogpost',
            'experience': 'ervaring',
            'profile': 'profiel',
            'project': 'project',
        }.get(normalized_source, normalized_source or 'bron')
    if normalized_source == 'assistant_note':
        return 'background guidance'
    return normalized_source or 'source'


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


def build_personal_story_guardrail_answer(*, question: str, locale: str = 'en') -> str | None:
    """Decline prompts that ask the portfolio assistant to invent personal anecdotes."""
    resolved_locale = resolve_response_locale(locale=locale)
    normalized = _normalize(question)
    if not normalized:
        return None

    if not _looks_like_personal_story_request(normalized):
        return None

    return _message(
        resolved_locale,
        en=(
            "I can't make up personal stories, jokes, roasts, or anecdotes about real people. "
            "For Alex, I can only answer from the portfolio details, so I can share a grounded summary of "
            "their projects, skills, experience, blog posts, or professional background instead."
        ),
        nl=(
            'Ik kan geen persoonlijke verhalen, grappen, roasts of anekdotes over echte personen verzinnen. '
            'Voor Alex kan ik alleen antwoorden op basis van het portfolio, dus ik kan wel een onderbouwde samenvatting geven '
            'van Alex’ projecten, vaardigheden, ervaring, blogposts of professionele achtergrond.'
        ),
    )

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


def sanitize_assistant_answer(answer: str, *, locale: str = 'en') -> str:
    """Remove retrieval/source-mechanics wording from user-facing assistant replies."""
    cleaned = answer.strip()
    cleaned = cleaned.replace('’', "'").replace('‘', "'").replace('�', "'")
    for pattern, replacement in _SOURCE_DISCLOSURE_PATTERNS:
        cleaned = pattern.sub(replacement, cleaned)
    if resolve_response_locale(locale=locale) == 'nl':
        cleaned = _sanitize_dutch_alex_first_person(cleaned)
    cleaned = re.sub(r'\s+([,.;:!?])', r'\1', cleaned)
    cleaned = re.sub(r'(?m)^\s*,\s*', '', cleaned)
    cleaned = re.sub(r'(?m)^\s*[:;]\s*', '', cleaned)
    cleaned = re.sub(r' {2,}', ' ', cleaned)
    cleaned = re.sub(r'(^|[.!?]\s+)(the portfolio)\b', lambda match: match.group(1) + 'The portfolio', cleaned)
    return cleaned.strip()


def _sanitize_dutch_alex_first_person(answer: str) -> str:
    """Repair common Dutch model drift where Alex is described in first person."""
    replacements = (
        (r'(?i)\bik heb gewerkt aan\b', 'Alex heeft gewerkt aan'),
        (r'(?i)\bik werkte aan\b', 'Alex werkte aan'),
        (r'(?i)\bik heb gebouwd\b', 'Alex heeft gebouwd'),
        (r'(?i)\bik bouwde\b', 'Alex bouwde'),
        (r'(?i)\bik heb ontwikkeld\b', 'Alex heeft ontwikkeld'),
        (r'(?i)\bik ontwikkelde\b', 'Alex ontwikkelde'),
        (r'(?i)\bik heb gemaakt\b', 'Alex heeft gemaakt'),
        (r'(?i)\bik maakte\b', 'Alex maakte'),
        (r'(?i)\bik heb gebruikt\b', 'Alex heeft gebruikt'),
        (r'(?i)\bik gebruikte\b', 'Alex gebruikte'),
        (r'(?i)\bik studeer(?:de)?\b', 'Alex studeert'),
        (r'(?i)\bik ben student\b', 'Alex is student'),
        (r'(?i)\bik ben een student\b', 'Alex is een student'),
        (r'(?i)\bmijn (portfolio|project|projecten|ervaring|stage|achtergrond|vaardigheden|werk|studie|studies)\b', r'Alex’ \1'),
    )
    cleaned = answer
    for pattern, replacement in replacements:
        cleaned = re.sub(pattern, replacement, cleaned)
    return cleaned


def trim_conversation_summary(summary: str, *, max_chars: int) -> str:
    normalized = re.sub(r'\s+', ' ', summary).strip()
    if len(normalized) <= max_chars:
        return normalized
    return normalized[: max_chars - 3].rstrip() + '...'


_PERSONAL_STORY_TERMS = {'story', 'anecdote', 'verhaal', 'anekdote'}

_CREATIVE_PERSONAL_CONTENT_TERMS = {
    'joke', 'roast', 'funny', 'embarrassing', 'weird', 'wild', 'random', 'fictional',
    'grap', 'mop', 'roast', 'grappig', 'genant', 'raar', 'wild', 'verzonnen',
}

_PERSON_REFERENCES = {
    'alex', "alex's", 'him', 'his', 'he', 'they', 'them', 'their', 'me', 'my', 'you', 'your',
    'alexs', 'alexa', 'persoon', 'hem', 'zijn', 'hen', 'hun', 'mij', 'mijn', 'jou', 'jouw', 'u', 'uw',
}

_FABRICATION_VERBS = {
    'invent', 'make up', 'fabricate', 'improvise', 'imagine', 'verzin', 'verzinnen', 'bedenk', 'maak op',
}


def _looks_like_personal_story_request(normalized: str) -> bool:
    words = set(normalized.split())
    has_story_request = bool(words & _PERSONAL_STORY_TERMS)
    has_creative_modifier = bool(words & _CREATIVE_PERSONAL_CONTENT_TERMS)
    has_person_reference = bool(words & _PERSON_REFERENCES)
    has_fabrication_request = any(phrase in normalized for phrase in _FABRICATION_VERBS)

    explicit_personal_story_phrases = (
        'story about alex',
        'story about me',
        'story about him',
        'story about them',
        'funny story',
        'embarrassing story',
        'personal story',
        'anecdote about alex',
        'joke about alex',
        'roast alex',
        'verhaal over alex',
        'verhaal over mij',
        'grappig verhaal',
        'persoonlijk verhaal',
        'anekdote over alex',
        'grap over alex',
        'mop over alex',
    )
    has_explicit_personal_story_phrase = any(phrase in normalized for phrase in explicit_personal_story_phrases)

    return (
        (has_creative_modifier and (has_person_reference or has_story_request))
        or (has_fabrication_request and (has_person_reference or has_story_request))
        or has_explicit_personal_story_phrase
    )

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
