from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
import math
import re
from uuid import UUID

from sqlalchemy import select

_slug_cleanup_pattern = re.compile(r'[^a-z0-9]+')


class AdminRepositoryParsingMixin:
    def _slugify(self, value: str) -> str:
        cleaned = _slug_cleanup_pattern.sub('-', value.strip().lower()).strip('-')
        return cleaned or 'item'

    def _ensure_unique_slug(self, model, value: str, current_id: UUID | None = None) -> str:
        base_slug = self._slugify(value)
        slug = base_slug
        index = 2

        while True:
            query = select(model.id).where(model.slug == slug)

            if current_id is not None:
                query = query.where(model.id != current_id)

            exists = self.session.scalar(query.limit(1))

            if exists is None:
                return slug

            slug = f'{base_slug}-{index}'
            index += 1

    def _normalize_optional_text(self, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()
        return cleaned or None

    def _parse_date(self, value: str | None) -> date | None:
        if value is None or not value.strip():
            return None

        return date.fromisoformat(value)

    def _parse_datetime(self, value: str | None) -> datetime | None:
        if value is None or not value.strip():
            return None

        raw = value.strip()

        if raw.endswith('Z'):
            raw = raw.replace('Z', '+00:00')

        parsed = datetime.fromisoformat(raw)

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)

    def _optional_uuid(self, value: str | None) -> UUID | None:
        if value is None or not str(value).strip():
            return None
        return UUID(str(value).strip())

    def _required_uuid(self, value: str) -> UUID:
        return UUID(value.strip())

    def _ensure_utc_datetime(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    def _serialize_datetime(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        return self._ensure_utc_datetime(value).isoformat()

    def _future_deadline(self, anchor: datetime, *, seconds: int, now: datetime | None = None) -> tuple[str, int]:
        effective_anchor = self._ensure_utc_datetime(anchor)
        effective_now = self._ensure_utc_datetime(now or datetime.now(UTC))
        deadline = effective_anchor + timedelta(seconds=seconds)
        remaining_seconds = max(int(math.ceil((deadline - effective_now).total_seconds())), 0)
        return deadline.isoformat(), remaining_seconds
