from __future__ import annotations

import re

VALID_ICON_KEYS: frozenset[str] = frozenset({
    'github',
    'linkedin',
    'twitter',
    'instagram',
    'mail',
    'phone',
    'map-pin',
    'globe',
    'code',
    'server',
    'brain',
    'database',
    'workflow',
    'languages',
    'angular',
    'laravel',
    'python',
    'docker',
    'git',
    'typescript',
    'tailwindcss',
    'sql',
    'kubernetes',
})

ICON_ALIASES: dict[str, str] = {
    'email': 'mail',
    'e-mail': 'mail',
    'mailto': 'mail',
    'telephone': 'phone',
    'phonecall': 'phone',
    'call': 'phone',
    'location': 'map-pin',
    'map': 'map-pin',
    'pin': 'map-pin',
    'marker': 'map-pin',
    'website': 'globe',
    'web': 'globe',
    'world': 'globe',
    'portfolio': 'globe',
    'frontend': 'code',
    'front-end': 'code',
    'back-end': 'server',
    'backend': 'server',
    'api': 'server',
    'fastapi': 'server',
    'proxmox': 'server',
    'network': 'globe',
    'networking': 'globe',
    'networking-basics': 'globe',
    'data-ai': 'brain',
    'machine-learning': 'brain',
    'ai': 'brain',
    'pandas': 'database',
    'infrastructure-tools': 'database',
    'analysis-collaboration': 'workflow',
    'analysis-and-collaboration': 'workflow',
    'requirements-analysis': 'workflow',
    'clipboard-search': 'workflow',
    'layout-template': 'workflow',
    'users': 'workflow',
    'prototyping': 'workflow',
    'team-leadership': 'workflow',
    'language': 'languages',
    'tailwind': 'tailwindcss',
    'tailwind-css': 'tailwindcss',
    'ts': 'typescript',
    'linked-in': 'linkedin',
    'x': 'twitter',
    'csharp': 'code',
    'c-sharp': 'code',
}


SOCIAL_PLATFORM_ICON_DEFAULTS: dict[str, str] = {
    'github': 'github',
    'linkedin': 'linkedin',
    'twitter': 'twitter',
    'x': 'twitter',
    'instagram': 'instagram',
    'email': 'mail',
    'phone': 'phone',
    'location': 'map-pin',
    'website': 'globe',
    'portfolio': 'globe',
}


CATEGORY_ICON_DEFAULTS: dict[str, str] = {
    'front-end': 'code',
    'back-end': 'server',
    'data-ai': 'brain',
    'infrastructure-tools': 'database',
    'analysis-collaboration': 'workflow',
    'languages': 'languages',
}


SKILL_ICON_DEFAULTS: dict[str, str] = {
    'angular': 'angular',
    'tailwind-css': 'tailwindcss',
    'tailwind': 'tailwindcss',
    'typescript': 'typescript',
    'laravel': 'laravel',
    'fastapi': 'server',
    'sql': 'sql',
    'python': 'python',
    'machine-learning': 'brain',
    'pandas': 'database',
    'git': 'git',
    'docker': 'docker',
    'networking-basics': 'globe',
    'proxmox': 'server',
    'kubernetes': 'kubernetes',
    'requirements-analysis': 'workflow',
    'uml': 'workflow',
    'prototyping': 'workflow',
    'team-leadership': 'workflow',
    'dutch': 'languages',
    'english': 'languages',
    'portuguese': 'languages',
}


_non_alphanumeric_pattern = re.compile(r'[^a-z0-9-]')
_whitespace_pattern = re.compile(r'[\s_]+')


def normalize_icon_key(value: str | None) -> str:
    normalized = _whitespace_pattern.sub('-', (value or '').strip().lower())
    normalized = _non_alphanumeric_pattern.sub('', normalized)
    normalized = re.sub(r'-{2,}', '-', normalized).strip('-')
    return normalized


def resolve_icon_key(value: str | None) -> str | None:
    normalized = normalize_icon_key(value)
    if not normalized:
        return None
    if normalized in VALID_ICON_KEYS:
        return normalized
    return ICON_ALIASES.get(normalized)


def _resolve_candidates(*candidates: str | None) -> str | None:
    for candidate in candidates:
        resolved = resolve_icon_key(candidate)
        if resolved:
            return resolved
    return None


def infer_social_icon_key(platform: str | None, label: str | None = None) -> str | None:
    normalized_platform = normalize_icon_key(platform)
    return _resolve_candidates(
        platform,
        SOCIAL_PLATFORM_ICON_DEFAULTS.get(normalized_platform),
        label,
    )


def infer_category_icon_key(name: str | None) -> str | None:
    normalized_name = normalize_icon_key(name)
    return _resolve_candidates(name, CATEGORY_ICON_DEFAULTS.get(normalized_name))


def infer_skill_icon_key(name: str | None, category_name: str | None = None) -> str | None:
    normalized_name = normalize_icon_key(name)
    return _resolve_candidates(
        name,
        SKILL_ICON_DEFAULTS.get(normalized_name),
        infer_category_icon_key(category_name),
    )


def choose_icon_key(explicit_icon_key: str | None, *fallback_candidates: str | None) -> str | None:
    return _resolve_candidates(explicit_icon_key, *fallback_candidates)
