from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.repositories.public_content_repository import PublicContentRepository
from app.schemas.public import BlogPostOut, BlogPostsListOut, ProfileOut, ProjectsListOut

router = APIRouter()
repository = PublicContentRepository()


@router.get('/profile', response_model=ProfileOut)
def get_profile() -> ProfileOut:
    return repository.get_profile()


@router.get('/projects', response_model=ProjectsListOut)
def list_projects() -> ProjectsListOut:
    items = repository.list_projects()
    return ProjectsListOut(items=items, total=len(items))


@router.get('/blog-posts', response_model=BlogPostsListOut)
def list_blog_posts() -> BlogPostsListOut:
    items = repository.list_blog_posts()
    return BlogPostsListOut(items=items, total=len(items))


@router.get('/blog-posts/{slug}', response_model=BlogPostOut)
def get_blog_post(slug: str) -> BlogPostOut:
    post = repository.get_blog_post_by_slug(slug)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')

    return post


@router.get('/experience')
def list_experience() -> dict:
    return {
        'items': [],
        'message': 'Experience endpoint scaffolded.'
    }
