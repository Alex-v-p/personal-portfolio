from __future__ import annotations

SUPPORTED_ASSISTANT_LOCALES: tuple[str, ...] = ('en', 'nl')
DEFAULT_ASSISTANT_LOCALE = 'en'


def normalize_assistant_locale(locale: str | None) -> str:
    candidate = (locale or '').strip().lower()
    return candidate if candidate in SUPPORTED_ASSISTANT_LOCALES else DEFAULT_ASSISTANT_LOCALE


def detect_assistant_locale(*, locale: str | None = None, page_path: str | None = None) -> str:
    normalized = normalize_assistant_locale(locale)
    if normalized != DEFAULT_ASSISTANT_LOCALE or not page_path:
        return normalized

    first_segment = page_path.split('?', 1)[0].split('#', 1)[0].lstrip('/').split('/', 1)[0]
    return normalize_assistant_locale(first_segment)


def strip_locale_prefix(path: str) -> str:
    if not path:
        return '/'

    path_without_hash, hash_separator, hash_value = path.partition('#')
    pathname, query_separator, query_value = path_without_hash.partition('?')

    segments = (pathname or '/').lstrip('/').split('/', 1)
    first = segments[0] if segments else ''
    if first in SUPPORTED_ASSISTANT_LOCALES:
        stripped = f"/{segments[1]}" if len(segments) > 1 and segments[1] else '/'
    else:
        stripped = pathname if pathname.startswith('/') else f'/{pathname}'

    suffix = ''
    if query_separator:
        suffix += f'?{query_value}'
    if hash_separator:
        suffix += f'#{hash_value}'
    return f'{stripped}{suffix}'


def localize_internal_path(path: str | None, locale: str) -> str | None:
    if not path:
        return None
    if not path.startswith('/') or path.startswith('/admin'):
        return path

    normalized_locale = normalize_assistant_locale(locale)
    stripped = strip_locale_prefix(path)
    if stripped == '/':
        return f'/{normalized_locale}'
    return f'/{normalized_locale}{stripped}'


def locale_language_name(locale: str) -> str:
    return 'Dutch' if normalize_assistant_locale(locale) == 'nl' else 'English'
