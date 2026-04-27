from __future__ import annotations

from app.schemas.base import ApiSchema


class AdminBackupImportOut(ApiSchema):
    imported: dict[str, int]
    skipped_files: list[str] = []
    replace_existing: bool = True
    warnings: list[str] = []


__all__ = ['AdminBackupImportOut']
