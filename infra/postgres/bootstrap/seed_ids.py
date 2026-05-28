from __future__ import annotations

from uuid import UUID, uuid5

SEED_NAMESPACE = UUID('5f4f80ea-795f-4a03-bdaf-4d37ea9f6d67')


def seed_uuid(label: str | UUID) -> UUID:
    if isinstance(label, UUID):
        return label
    try:
        return UUID(str(label))
    except ValueError:
        return uuid5(SEED_NAMESPACE, str(label))


def seed_uuid_str(label: str | UUID) -> str:
    return str(seed_uuid(label))
