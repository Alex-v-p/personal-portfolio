from __future__ import annotations

import json
from typing import Any
from urllib import error, request

from app.core.config import get_settings
from app.services.github_stats.models import GithubStatsSyncError


class GithubHttpClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.api_version = '2022-11-28'

    def get_json(self, url: str) -> dict[str, Any] | list[Any]:
        text = self.get_text(url, accept='application/vnd.github+json')
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise GithubStatsSyncError(f'GitHub returned invalid JSON for {url}.') from exc

    def get_text(self, url: str, *, accept: str) -> str:
        headers = {
            'Accept': accept,
            'User-Agent': 'portfolio-api-service',
            'X-GitHub-Api-Version': self.api_version,
        }
        token = self.settings.github_api_token.strip()
        if token and 'api.github.com' in url:
            headers['Authorization'] = f'Bearer {token}'
        req = request.Request(url, headers=headers)
        try:
            with request.urlopen(req, timeout=20) as response:
                return response.read().decode('utf-8')
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore')
            raise GithubStatsSyncError(f'GitHub request failed: {exc.code} {detail or exc.reason}') from exc
        except error.URLError as exc:
            raise GithubStatsSyncError(f'GitHub request failed: {exc.reason}') from exc
