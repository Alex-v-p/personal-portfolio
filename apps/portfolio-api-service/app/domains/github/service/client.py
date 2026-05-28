from __future__ import annotations

import json
from typing import Any
from urllib import error, request

from app.core.config import get_settings
from app.domains.github.service.models import GithubStatsSyncError


class GithubHttpClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.api_version = '2022-11-28'

    def get_json(self, url: str, *, use_token: bool = True) -> dict[str, Any] | list[Any]:
        text = self.get_text(url, accept='application/vnd.github+json', use_token=use_token)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise GithubStatsSyncError(f'GitHub returned invalid JSON for {url}.') from exc

    def get_text(self, url: str, *, accept: str, use_token: bool = True) -> str:
        headers = {
            'Accept': accept,
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (compatible; portfolio-api-service/1.0; +https://github.com)',
        }
        if 'api.github.com' in url:
            headers['X-GitHub-Api-Version'] = self.api_version
            token = self.settings.github_api_token.strip() if use_token else ''
            if token:
                headers['Authorization'] = f'Bearer {token}'
        req = request.Request(url, headers=headers)
        try:
            with request.urlopen(req, timeout=20) as response:
                return response.read().decode('utf-8')
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='ignore')
            raise GithubStatsSyncError(self._format_http_error(exc.code, detail or exc.reason, url)) from exc
        except error.URLError as exc:
            raise GithubStatsSyncError(f'GitHub request failed before a response was received: {exc.reason}') from exc

    @staticmethod
    def _format_http_error(status_code: int, detail: str, url: str) -> str:
        normalized_detail = detail.strip()
        if status_code == 401:
            return 'GitHub rejected the configured token. Check that GITHUB_API_TOKEN is valid and has not expired.'
        if status_code == 403:
            lowered = normalized_detail.lower()
            if 'rate limit' in lowered:
                return 'GitHub rate limited the stats refresh. Wait for the limit to reset or use a valid GITHUB_API_TOKEN.'
            return f'GitHub blocked the stats refresh with HTTP 403. Check token permissions, rate limits, and profile visibility. Detail: {normalized_detail}'
        if status_code == 404 and '/users/' in url:
            return 'GitHub username not found. Check the username configured for the stats refresh.'
        if status_code == 406:
            return 'GitHub rejected the public contribution request format with HTTP 406. The refresh now retries public scraping with browser-compatible headers, but GitHub may still block the public profile endpoint; using a valid GITHUB_API_TOKEN is more reliable.'
        return f'GitHub request failed with HTTP {status_code}: {normalized_detail}'
