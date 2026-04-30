from __future__ import annotations

from pathlib import PurePosixPath
from urllib.parse import quote
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.db.models import MediaFile, MediaVisibility
from app.db.session import get_session
from app.domains.public_site.repository import DEFAULT_PUBLIC_LOCALE, PublicLocale
from app.domains.public_site.schema import (
    BlogPostDetailOut,
    BlogPostsListOut,
    ExperienceListOut,
    GithubSnapshotOut,
    HomeOut,
    NavigationListOut,
    ProfileOut,
    ProjectDetailOut,
    ProjectsListOut,
    SiteShellOut,
    StatsOut,
)
from app.domains.public_site.service.public_content_query_service import PublicContentQueryService
from app.domains.media.service.resolver import sanitize_public_download_filename
from app.domains.media.service.storage import AdminMediaStorageService

router = APIRouter()


def resolve_public_locale(locale: PublicLocale = Query(default=DEFAULT_PUBLIC_LOCALE)) -> PublicLocale:
    return locale



@router.get('/media-files/{media_id}/{filename}', response_model=None)
def download_public_media_file(media_id: UUID, filename: str, session: Session = Depends(get_session)) -> Response:
    media_file = session.get(MediaFile, media_id)
    if media_file is None or media_file.visibility != MediaVisibility.PUBLIC:
        raise HTTPException(status_code=404, detail='Media file not found.')

    file_bytes = AdminMediaStorageService().download_object(bucket_name=media_file.bucket_name, object_key=media_file.object_key)
    download_filename = sanitize_public_download_filename(media_file.original_filename or filename or media_file.stored_filename)
    quoted_filename = quote(download_filename)
    fallback_filename = ''.join(character if ord(character) < 128 else '-' for character in download_filename) or PurePosixPath(filename).name or 'download'

    response = Response(content=file_bytes, media_type=media_file.mime_type or 'application/octet-stream')
    response.headers['Content-Disposition'] = f'attachment; filename="{fallback_filename}"; filename*=UTF-8\'\'{quoted_filename}'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@router.get('/profile', response_model=ProfileOut)
def get_profile(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> ProfileOut:
    return PublicContentQueryService(session, locale=locale).get_profile()


@router.get('/navigation', response_model=NavigationListOut)
def get_navigation(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> NavigationListOut:
    return PublicContentQueryService(session, locale=locale).list_navigation()


@router.get('/site-shell', response_model=SiteShellOut)
def get_site_shell(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> SiteShellOut:
    return PublicContentQueryService(session, locale=locale).get_site_shell()


@router.get('/home', response_model=HomeOut)
def get_home(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> HomeOut:
    return PublicContentQueryService(session, locale=locale).get_home()


@router.get('/projects', response_model=ProjectsListOut)
def list_projects(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> ProjectsListOut:
    return PublicContentQueryService(session, locale=locale).list_projects()


@router.get('/projects/{slug}', response_model=ProjectDetailOut)
def get_project(slug: str, locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> ProjectDetailOut:
    return PublicContentQueryService(session, locale=locale).get_project(slug)


@router.get('/blog-posts', response_model=BlogPostsListOut)
def list_blog_posts(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> BlogPostsListOut:
    return PublicContentQueryService(session, locale=locale).list_blog_posts()


@router.get('/blog-posts/{slug}', response_model=BlogPostDetailOut)
def get_blog_post(slug: str, locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> BlogPostDetailOut:
    return PublicContentQueryService(session, locale=locale).get_blog_post(slug)


@router.get('/experience', response_model=ExperienceListOut)
def list_experience(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> ExperienceListOut:
    return PublicContentQueryService(session, locale=locale).list_experience()


@router.get('/github', response_model=GithubSnapshotOut)
def get_github_snapshot(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> GithubSnapshotOut:
    return PublicContentQueryService(session, locale=locale).get_github_snapshot()


@router.get('/stats', response_model=StatsOut)
def get_stats(locale: PublicLocale = Depends(resolve_public_locale), session: Session = Depends(get_session)) -> StatsOut:
    return PublicContentQueryService(session, locale=locale).get_stats()
