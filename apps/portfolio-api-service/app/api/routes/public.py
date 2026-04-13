from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.public_content_repository import PublicContentRepository
from app.schemas.public import (
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

router = APIRouter()


@router.get('/profile', response_model=ProfileOut)
def get_profile(session: Session = Depends(get_session)) -> ProfileOut:
    repository = PublicContentRepository(session)
    profile = repository.get_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail='Public profile not found.')
    return profile


@router.get('/navigation', response_model=NavigationListOut)
def get_navigation(session: Session = Depends(get_session)) -> NavigationListOut:
    repository = PublicContentRepository(session)
    items = repository.list_navigation()
    return NavigationListOut(items=items, total=len(items))


@router.get('/site-shell', response_model=SiteShellOut)
def get_site_shell(session: Session = Depends(get_session)) -> SiteShellOut:
    repository = PublicContentRepository(session)
    shell = repository.get_site_shell()
    if shell is None:
        raise HTTPException(status_code=404, detail='Site shell not found.')
    return shell


@router.get('/home', response_model=HomeOut)
def get_home(session: Session = Depends(get_session)) -> HomeOut:
    repository = PublicContentRepository(session)
    home = repository.get_home()
    if home is None:
        raise HTTPException(status_code=404, detail='Public home content not found.')
    return home


@router.get('/projects', response_model=ProjectsListOut)
def list_projects(session: Session = Depends(get_session)) -> ProjectsListOut:
    repository = PublicContentRepository(session)
    items = repository.list_projects()
    return ProjectsListOut(items=items, total=len(items))


@router.get('/projects/{slug}', response_model=ProjectDetailOut)
def get_project(slug: str, session: Session = Depends(get_session)) -> ProjectDetailOut:
    repository = PublicContentRepository(session)
    project = repository.get_project_by_slug(slug)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.get('/blog-posts', response_model=BlogPostsListOut)
def list_blog_posts(session: Session = Depends(get_session)) -> BlogPostsListOut:
    repository = PublicContentRepository(session)
    items = repository.list_blog_posts()
    return BlogPostsListOut(items=items, total=len(items))


@router.get('/blog-posts/{slug}', response_model=BlogPostDetailOut)
def get_blog_post(slug: str, session: Session = Depends(get_session)) -> BlogPostDetailOut:
    repository = PublicContentRepository(session)
    post = repository.get_blog_post_by_slug(slug)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')
    return post


@router.get('/experience', response_model=ExperienceListOut)
def list_experience(session: Session = Depends(get_session)) -> ExperienceListOut:
    repository = PublicContentRepository(session)
    items = repository.list_experience()
    return ExperienceListOut(items=items, total=len(items))


@router.get('/github', response_model=GithubSnapshotOut)
def get_github_snapshot(session: Session = Depends(get_session)) -> GithubSnapshotOut:
    repository = PublicContentRepository(session)
    snapshot = repository.get_latest_github_snapshot()
    if snapshot is None:
        raise HTTPException(status_code=404, detail='GitHub snapshot not found.')
    return snapshot


@router.get('/stats', response_model=StatsOut)
def get_stats(session: Session = Depends(get_session)) -> StatsOut:
    repository = PublicContentRepository(session)
    return repository.get_stats()
