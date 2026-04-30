from __future__ import annotations

from app.domains.retrieval.service.intent import infer_intent, source_multiplier
from app.domains.retrieval.service.models import QueryIntent
from app.domains.retrieval.service.text import excerpt, is_smalltalk, normalize_text, parse_vector, tokenize


def test_infer_intent_prefers_project_sources_for_project_queries() -> None:
    intent = infer_intent(query='What projects did you build with FastAPI?', page_path='/')

    assert intent.name == 'project'
    assert intent.preferred_sources == ('project',)
    assert 'experience' in intent.allowed_supporting_sources


def test_infer_intent_routes_recruiter_logistics_to_private_guidance() -> None:
    intent = infer_intent(query='Is Alex available for a hybrid opportunity in Belgium?', page_path='/')

    assert intent.name == 'portfolio_fit'
    assert intent.preferred_sources == ('assistant_note', 'profile')
    assert 'project' in intent.allowed_supporting_sources


def test_source_multiplier_boosts_preferred_source_on_matching_page() -> None:
    intent = QueryIntent(name='project', preferred_sources=('project',), page_path_hint='/projects')

    boosted = source_multiplier(source_type='project', intent=intent, page_path='/projects/portfolio')
    suppressed = source_multiplier(source_type='profile', intent=intent, page_path='/projects/portfolio')

    assert boosted > 1.0
    assert suppressed < 1.0


def test_text_helpers_handle_tokenization_excerpt_and_vectors() -> None:
    assert normalize_text('  Hello   World ') == 'hello world'
    assert is_smalltalk('hello') is True
    assert 'fastapi' in tokenize('FastAPI portfolio project')
    assert excerpt('This portfolio uses FastAPI and Angular for the project.', ['angular']).startswith('This portfolio')
    assert parse_vector('[1, 2.5,3]') == [1.0, 2.5, 3.0]
