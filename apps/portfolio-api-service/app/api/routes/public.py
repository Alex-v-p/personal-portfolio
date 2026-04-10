from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.public_content_repository import PublicContentRepository
from app.schemas.public import BlogPostOut, BlogPostsListOut, ProfileOut, ProjectsListOut

router = APIRouter()


@router.get('/profile', response_model=ProfileOut)
def get_profile(session: Session = Depends(get_session)) -> ProfileOut:
    repository = PublicContentRepository(session)
    profile = repository.get_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail='Public profile not found.')
    return profile


@router.get('/projects', response_model=ProjectsListOut)
def list_projects(session: Session = Depends(get_session)) -> ProjectsListOut:
    repository = PublicContentRepository(session)
    items = repository.list_projects()
    return ProjectsListOut(items=items, total=len(items))


@router.get('/blog-posts', response_model=BlogPostsListOut)
def list_blog_posts(session: Session = Depends(get_session)) -> BlogPostsListOut:
    repository = PublicContentRepository(session)
    items = repository.list_blog_posts()
    return BlogPostsListOut(items=items, total=len(items))


@router.get('/blog-posts/{slug}', response_model=BlogPostOut)
def get_blog_post(slug: str, session: Session = Depends(get_session)) -> BlogPostOut:
    repository = PublicContentRepository(session)
    post = repository.get_blog_post_by_slug(slug)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')

    return post


@router.get('/experience')
def list_experience() -> dict:
    return {
        'items': [],
        'message': 'Experience endpoint scaffolded.',
    }
