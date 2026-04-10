from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from app.schemas.contact import ContactMessageIn, ContactMessageOut


class ContactMessageStore:
    def __init__(self, storage_file: Path | None = None) -> None:
        default_path = Path(__file__).resolve().parents[1] / 'data' / 'contact_messages.runtime.json'
        self.storage_file = storage_file or default_path

    def save(self, payload: ContactMessageIn) -> ContactMessageOut:
        timestamp = datetime.now(UTC).isoformat()
        item = ContactMessageOut(
            id=str(uuid4()),
            name=payload.name,
            email=payload.email,
            subject=payload.subject,
            message=payload.message,
            source_page=payload.source_page,
            is_read=False,
            created_at=timestamp,
            updated_at=timestamp,
        )

        existing = self._read()
        existing.append(item.model_dump(mode='json', by_alias=True))
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.storage_file.write_text(json.dumps(existing, indent=2), encoding='utf-8')
        return item

    def _read(self) -> list[dict]:
        if not self.storage_file.exists():
            return []

        try:
            data = json.loads(self.storage_file.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            return []

        return data if isinstance(data, list) else []
