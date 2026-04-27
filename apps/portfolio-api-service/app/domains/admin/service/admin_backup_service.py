from __future__ import annotations

import csv
import io
import json
import zipfile
from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import PurePosixPath
from typing import Any, Iterable
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Boolean, Date, DateTime, Integer, JSON, Enum as SqlEnum, Uuid

from app.db.models import (
    AssistantContextNote,
    BlogPost,
    BlogPostTag,
    BlogTag,
    ContactMessage,
    Experience,
    ExperienceSkill,
    GithubContributionDay,
    GithubSnapshot,
    MediaFile,
    NavigationItem,
    Profile,
    Project,
    ProjectImage,
    ProjectSkill,
    Skill,
    SkillCategory,
    SocialLink,
)
from app.domains.media.service.storage import AdminMediaStorageService


@dataclass(frozen=True)
class CsvTableConfig:
    filename: str
    model: type
    label: str


IMPORT_TABLES: tuple[CsvTableConfig, ...] = (
    CsvTableConfig('media_files.csv', MediaFile, 'media files'),
    CsvTableConfig('profiles.csv', Profile, 'profiles'),
    CsvTableConfig('social_links.csv', SocialLink, 'social links'),
    CsvTableConfig('skill_categories.csv', SkillCategory, 'skill categories'),
    CsvTableConfig('skills.csv', Skill, 'skills'),
    CsvTableConfig('experience.csv', Experience, 'experience items'),
    CsvTableConfig('experience_skills.csv', ExperienceSkill, 'experience skill links'),
    CsvTableConfig('projects.csv', Project, 'projects'),
    CsvTableConfig('project_images.csv', ProjectImage, 'project gallery images'),
    CsvTableConfig('project_skills.csv', ProjectSkill, 'project skill links'),
    CsvTableConfig('blog_tags.csv', BlogTag, 'blog tags'),
    CsvTableConfig('blog_posts.csv', BlogPost, 'blog posts'),
    CsvTableConfig('blog_post_tags.csv', BlogPostTag, 'blog post tag links'),
    CsvTableConfig('navigation_items.csv', NavigationItem, 'navigation items'),
    CsvTableConfig('github_snapshots.csv', GithubSnapshot, 'GitHub snapshots'),
    CsvTableConfig('github_contribution_days.csv', GithubContributionDay, 'GitHub contribution days'),
    CsvTableConfig('assistant_context_notes.csv', AssistantContextNote, 'assistant context notes'),
    CsvTableConfig('contact_messages.csv', ContactMessage, 'contact messages'),
)

DELETE_TABLES: tuple[CsvTableConfig, ...] = tuple(reversed(IMPORT_TABLES))
EXPORT_TABLES = IMPORT_TABLES


class AdminBackupService:
    """Exports and imports CMS-owned portfolio data as a CSV zip archive.

    The archive intentionally excludes admin users/sessions, visitor analytics, assistant chat logs,
    and generated knowledge chunks. Knowledge should be rebuilt after import.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    def export_csv_zip(self) -> bytes:
        buffer = io.BytesIO()
        exported_counts: dict[str, int] = {}
        generated_at = datetime.now(timezone.utc).isoformat()

        with zipfile.ZipFile(buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('README.txt', self._readme(generated_at))
            archive.writestr(
                'manifest.json',
                json.dumps(
                    {
                        'format': 'portfolio-cms-csv-backup',
                        'version': 2,
                        'generatedAt': generated_at,
                        'notes': [
                            'CSV files contain database records for CMS-managed content.',
                            'Uploaded media files are included under media/ when they can be read from object storage.',
                            'media_binaries_manifest.csv maps media database records to files inside the backup archive.',
                            'The import action restores database records only; restore media files to object storage manually or re-upload them after a full volume wipe.',
                            'Generated knowledge documents/chunks are not included; rebuild assistant knowledge after import.',
                            'Admin users, sessions, MFA secrets, and visitor analytics are intentionally excluded.',
                        ],
                        'tables': [table.filename for table in EXPORT_TABLES],
                        'mediaDirectory': 'media/',
                        'mediaManifest': 'media_binaries_manifest.csv',
                    },
                    indent=2,
                    sort_keys=True,
                ),
            )

            for table in EXPORT_TABLES:
                csv_text, row_count = self._export_table(table.model)
                archive.writestr(table.filename, csv_text)
                exported_counts[table.filename] = row_count

            media_manifest = self._export_media_binaries(archive)
            archive.writestr('media_binaries_manifest.csv', self._media_manifest_csv(media_manifest))

            archive.writestr(
                'summary.json',
                json.dumps(
                    {
                        'exported': exported_counts,
                        'mediaBinaries': self._summarize_media_manifest(media_manifest),
                    },
                    indent=2,
                    sort_keys=True,
                ),
            )

        return buffer.getvalue()

    def import_csv_zip(self, file_bytes: bytes, *, replace_existing: bool = True) -> dict[str, Any]:
        if not zipfile.is_zipfile(io.BytesIO(file_bytes)):
            raise ValueError('Backup import expects a .zip file generated by the CMS export action.')

        imported_counts: dict[str, int] = {}
        skipped_files: list[str] = []

        with zipfile.ZipFile(io.BytesIO(file_bytes), mode='r') as archive:
            available_files = set(archive.namelist())
            has_media_binaries = any(name.startswith('media/') for name in available_files)
            if not any(table.filename in available_files for table in IMPORT_TABLES):
                raise ValueError('No recognized CMS CSV files were found in this backup archive.')

            if replace_existing:
                self._clear_existing_content()

            for table in IMPORT_TABLES:
                if table.filename not in available_files:
                    skipped_files.append(table.filename)
                    continue

                with archive.open(table.filename, mode='r') as csv_file:
                    text = io.TextIOWrapper(csv_file, encoding='utf-8-sig', newline='')
                    imported_counts[table.filename] = self._import_table(table.model, text)

        self.session.flush()
        warnings = [
            'Assistant knowledge documents/chunks are generated data. Rebuild assistant knowledge after import.',
        ]
        if has_media_binaries:
            warnings.insert(
                0,
                'This backup contains media files under the media/ folder, but this import currently restores database records only. Restore those files to object storage manually or re-upload them in the CMS.',
            )
        else:
            warnings.insert(
                0,
                'Media file metadata was imported, but this archive did not contain media binaries. Uploaded files must still exist in object storage or be restored separately.',
            )

        return {
            'imported': imported_counts,
            'skippedFiles': skipped_files,
            'replaceExisting': replace_existing,
            'warnings': warnings,
        }

    def _export_table(self, model: type) -> tuple[str, int]:
        columns = list(model.__table__.columns)
        output = io.StringIO(newline='')
        writer = csv.DictWriter(output, fieldnames=[column.name for column in columns], lineterminator='\n')
        writer.writeheader()

        rows = list(self.session.scalars(select(model)))
        for row in rows:
            writer.writerow({column.name: self._serialize_value(getattr(row, column.name)) for column in columns})

        return output.getvalue(), len(rows)

    def _export_media_binaries(self, archive: zipfile.ZipFile) -> list[dict[str, str]]:
        manifest_rows: list[dict[str, str]] = []
        media_files = list(self.session.scalars(select(MediaFile)))
        storage: AdminMediaStorageService | None = None

        for media_file in media_files:
            archive_path = self._media_archive_path(media_file)
            row = {
                'id': str(media_file.id),
                'bucket_name': media_file.bucket_name or '',
                'object_key': media_file.object_key or '',
                'archive_path': archive_path,
                'original_filename': media_file.original_filename or '',
                'stored_filename': media_file.stored_filename or '',
                'mime_type': media_file.mime_type or '',
                'expected_size_bytes': str(media_file.file_size_bytes or ''),
                'exported_size_bytes': '',
                'status': 'skipped',
                'error': '',
            }

            if not media_file.bucket_name or not media_file.object_key:
                row['error'] = 'Missing bucket_name or object_key.'
                manifest_rows.append(row)
                continue

            try:
                if storage is None:
                    storage = AdminMediaStorageService()
                file_bytes = storage.download_object(bucket_name=media_file.bucket_name, object_key=media_file.object_key)
                archive.writestr(archive_path, file_bytes)
                row['exported_size_bytes'] = str(len(file_bytes))
                row['status'] = 'exported'
            except Exception as exc:  # pragma: no cover - depends on live object storage
                row['status'] = 'missing'
                row['error'] = self._format_backup_error(exc)

            manifest_rows.append(row)

        return manifest_rows

    @staticmethod
    def _media_archive_path(media_file: MediaFile) -> str:
        suffix = PurePosixPath(media_file.original_filename or media_file.stored_filename or media_file.object_key or '').suffix
        filename = PurePosixPath(media_file.stored_filename or media_file.original_filename or f'media-file{suffix}').name
        safe_filename = ''.join(character if character.isalnum() or character in {'-', '_', '.', ' '} else '-' for character in filename).strip('. ')
        if not safe_filename:
            safe_filename = f'media-file{suffix or ".bin"}'
        return f'media/{media_file.id}/{safe_filename}'

    @staticmethod
    def _media_manifest_csv(rows: list[dict[str, str]]) -> str:
        fieldnames = [
            'id',
            'bucket_name',
            'object_key',
            'archive_path',
            'original_filename',
            'stored_filename',
            'mime_type',
            'expected_size_bytes',
            'exported_size_bytes',
            'status',
            'error',
        ]
        output = io.StringIO(newline='')
        writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
        return output.getvalue()

    @staticmethod
    def _summarize_media_manifest(rows: list[dict[str, str]]) -> dict[str, int]:
        summary = {'total': len(rows), 'exported': 0, 'missing': 0, 'skipped': 0}
        for row in rows:
            status = row.get('status') or 'skipped'
            summary[status] = summary.get(status, 0) + 1
        return summary

    @staticmethod
    def _format_backup_error(error: Exception) -> str:
        message = f'{error.__class__.__name__}: {error}'
        return message[:240]

    def _import_table(self, model: type, csv_text: Iterable[str]) -> int:
        reader = csv.DictReader(csv_text)
        if not reader.fieldnames:
            return 0

        columns_by_name = {column.name: column for column in model.__table__.columns}
        count = 0
        for raw_row in reader:
            payload: dict[str, Any] = {}
            for column_name, column in columns_by_name.items():
                if column_name not in raw_row:
                    continue
                payload[column_name] = self._deserialize_value(raw_row[column_name], column)
            self.session.add(model(**payload))
            count += 1

        return count

    def _clear_existing_content(self) -> None:
        for table in DELETE_TABLES:
            self.session.execute(delete(table.model))
        self.session.flush()

    @staticmethod
    def _serialize_value(value: Any) -> str:
        if value is None:
            return ''
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        if isinstance(value, UUID):
            return str(value)
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        if isinstance(value, bool):
            return 'true' if value else 'false'
        return str(value)

    @staticmethod
    def _deserialize_value(value: str | None, column: Any) -> Any:
        if value is None or value == '':
            return None

        column_type = column.type
        if isinstance(column_type, SqlEnum):
            enum_class = column_type.enum_class
            if enum_class is None:
                return value
            try:
                return enum_class(value)
            except ValueError:
                return enum_class[value]

        if isinstance(column_type, Uuid):
            return UUID(value)
        if isinstance(column_type, Boolean):
            return value.strip().lower() in {'1', 'true', 'yes', 'y', 'on'}
        if isinstance(column_type, Integer):
            return int(value)
        if isinstance(column_type, DateTime):
            parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
            return parsed
        if isinstance(column_type, Date):
            return date.fromisoformat(value)
        if isinstance(column_type, JSON):
            return json.loads(value)

        return value

    @staticmethod
    def _readme(generated_at: str) -> str:
        return f"""Portfolio CMS CSV backup\nGenerated at: {generated_at}\n\nThis archive contains CSV exports for CMS-managed portfolio records.\n\nIncluded:\n- profile, social links, navigation\n- taxonomy, skills, project and experience relationships\n- projects, project galleries, blog posts and tags\n- media metadata/object keys\n- uploaded media files under media/ when object storage is reachable\n- GitHub snapshot/stat records\n- assistant-only context notes\n- contact messages\n\nIncluded media files:\n- uploaded media files are included under media/ when they can be read from object storage\n- media_binaries_manifest.csv maps each media record to the file path inside this backup archive\n\nNot included:\n- admin users, passwords, MFA secrets, sessions\n- visitor analytics/activity logs\n- assistant chat transcripts\n- generated knowledge documents/chunks/embeddings\n\nAfter importing, rebuild assistant knowledge from the CMS. The current import restores database records only; if your MinIO/object-storage volume was wiped, copy the files from the media/ folder back into object storage according to media_files.csv and media_binaries_manifest.csv, or re-upload them in the CMS.\n"""
