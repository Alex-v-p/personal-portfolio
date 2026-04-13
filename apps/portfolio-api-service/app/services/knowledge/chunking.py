from __future__ import annotations

import re


def chunk_markdown(markdown: str, chunk_target_chars: int = 550) -> list[str]:
    normalized = re.sub(r'\n{3,}', '\n\n', markdown or '').strip()
    if not normalized:
        return []
    blocks = [block.strip() for block in normalized.split('\n\n') if block.strip()]
    chunks: list[str] = []
    current = ''
    for block in blocks:
        candidate = f'{current}\n\n{block}'.strip() if current else block
        if len(candidate) <= chunk_target_chars:
            current = candidate
            continue
        if current:
            chunks.append(current)
            current = ''
        if len(block) <= chunk_target_chars:
            current = block
            continue
        sentences = re.split(r'(?<=[.!?])\s+', block)
        segment = ''
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            candidate_sentence = f'{segment} {sentence}'.strip() if segment else sentence
            if len(candidate_sentence) <= chunk_target_chars:
                segment = candidate_sentence
                continue
            if segment:
                chunks.append(segment)
            segment = sentence
        if segment:
            current = segment
    if current:
        chunks.append(current)
    return chunks
