from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

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

router = APIRouter()


def resolve_public_locale(locale: PublicLocale = Query(default=DEFAULT_PUBLIC_LOCALE)) -> PublicLocale:
    return locale


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
