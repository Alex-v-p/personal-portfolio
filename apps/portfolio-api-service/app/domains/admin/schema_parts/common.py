from __future__ import annotations

from typing import Literal

ProjectStateLiteral = Literal['published', 'archived', 'completed', 'paused']
PublicationStatusLiteral = Literal['draft', 'published', 'archived']
MediaVisibilityLiteral = Literal['public', 'private', 'signed']

__all__ = ['ProjectStateLiteral', 'PublicationStatusLiteral', 'MediaVisibilityLiteral']
