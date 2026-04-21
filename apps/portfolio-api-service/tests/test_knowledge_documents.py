from __future__ import annotations

from app.db.session import get_session_factory
from app.domains.knowledge.service.documents import KnowledgeDocumentBuilder


def test_knowledge_builder_generates_english_and_dutch_documents(client) -> None:
    session_factory = get_session_factory()

    with session_factory() as session:
        documents = KnowledgeDocumentBuilder(session).build_documents()

    assert documents
    locales = {document.metadata_json.get('locale') for document in documents if isinstance(document.metadata_json, dict)}
    assert locales == {'en', 'nl'}

    profile_documents = [document for document in documents if getattr(document.source_type, 'value', document.source_type) == 'profile']
    assert len(profile_documents) == 2

    english_profile = next(document for document in profile_documents if document.metadata_json.get('locale') == 'en')
    dutch_profile = next(document for document in profile_documents if document.metadata_json.get('locale') == 'nl')

    assert 'student software engineering and AI' in english_profile.content_markdown
    assert 'student software engineering en AI' in dutch_profile.content_markdown
