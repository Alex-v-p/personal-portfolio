from app.services.knowledge.chunking import chunk_markdown


def test_chunk_markdown_keeps_short_blocks_together() -> None:
    markdown = '# Title\n\nShort intro.\n\nAnother short paragraph.'

    chunks = chunk_markdown(markdown, chunk_target_chars=80)

    assert chunks == ['# Title\n\nShort intro.\n\nAnother short paragraph.']


def test_chunk_markdown_splits_long_blocks_by_sentence() -> None:
    markdown = 'First sentence is deliberately long enough. Second sentence is also fairly long. Third sentence continues the idea.'

    chunks = chunk_markdown(markdown, chunk_target_chars=45)

    assert len(chunks) >= 2
    assert chunks[0].startswith('First sentence')
    assert any('Third sentence' in chunk for chunk in chunks)


def test_chunk_markdown_ignores_blank_input() -> None:
    assert chunk_markdown('   \n\n  ') == []
