from __future__ import annotations

from app.domains.retrieval.service.models import QueryIntent
from app.domains.retrieval.service.text import contains_any, normalize_text


def infer_intent(*, query: str, page_path: str | None) -> QueryIntent:
    normalized = normalize_text(query)
    if contains_any(normalized, {'project', 'projects', 'build', 'built', 'case study', 'case studies'}):
        return QueryIntent(
            name='project',
            preferred_sources=('project',),
            allowed_supporting_sources=('blog_post', 'experience', 'profile'),
            suppress_sources=('profile',),
            page_path_hint='/projects',
        )
    if contains_any(normalized, {'experience', 'internship', 'job', 'work', 'worked', 'career', 'role', 'roles'}):
        return QueryIntent(
            name='experience',
            preferred_sources=('experience',),
            allowed_supporting_sources=('project', 'profile'),
            suppress_sources=('profile',),
            page_path_hint='/experience',
        )
    if contains_any(normalized, {'blog', 'blogs', 'post', 'posts', 'article', 'articles', 'write', 'wrote', 'writing'}):
        return QueryIntent(
            name='blog',
            preferred_sources=('blog_post',),
            allowed_supporting_sources=('project', 'profile'),
            suppress_sources=('profile',),
            page_path_hint='/blog',
        )
    if contains_any(normalized, {'skill', 'skills', 'stack', 'technology', 'technologies', 'tech', 'framework', 'frameworks', 'language', 'languages'}):
        return QueryIntent(
            name='skills',
            preferred_sources=('project', 'experience'),
            allowed_supporting_sources=('blog_post', 'profile'),
        )
    if contains_any(normalized, {'about', 'intro', 'introduction', 'bio', 'who is', 'who are', 'background'}):
        return QueryIntent(
            name='profile',
            preferred_sources=('profile',),
            allowed_supporting_sources=('experience', 'project'),
            page_path_hint='/',
        )

    normalized_path = normalize_text(page_path or '')
    if '/projects' in normalized_path:
        return QueryIntent(name='project_page', preferred_sources=('project',), allowed_supporting_sources=('blog_post', 'experience', 'profile'))
    if '/blog' in normalized_path:
        return QueryIntent(name='blog_page', preferred_sources=('blog_post',), allowed_supporting_sources=('project', 'profile'))
    if '/experience' in normalized_path:
        return QueryIntent(name='experience_page', preferred_sources=('experience',), allowed_supporting_sources=('project', 'profile'))
    return QueryIntent(name='general', preferred_sources=(), allowed_supporting_sources=('project', 'experience', 'blog_post', 'profile'))


def source_multiplier(*, source_type: str, intent: QueryIntent, page_path: str | None) -> float:
    multiplier = 1.0
    if source_type in intent.preferred_sources:
        multiplier *= 1.45
    elif source_type in intent.allowed_supporting_sources:
        multiplier *= 1.0
    elif intent.source_priority:
        multiplier *= 0.82

    if page_path and source_type == 'profile' and intent.name in {'project', 'experience', 'blog'}:
        multiplier *= 0.78
    if page_path and intent.page_path_hint and intent.page_path_hint in page_path and source_type in intent.preferred_sources:
        multiplier *= 1.08
    return multiplier
