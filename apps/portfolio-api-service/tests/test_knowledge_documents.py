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

    assert english_profile.metadata_json.get('headline') == 'a software engineering and AI student'
    assert dutch_profile.metadata_json.get('headline') == 'een softwareontwikkelaar en AI-student'
    assert 'I am a Software Engineering student at Thomas More in Geel' in english_profile.content_markdown
    assert 'Ik ben een Software Engineering student aan Thomas More in Geel' in dutch_profile.content_markdown
