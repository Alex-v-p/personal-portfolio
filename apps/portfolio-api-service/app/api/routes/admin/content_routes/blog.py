from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.api.routes.admin.content_routes.common import repository
from app.domains.admin.schema import AdminBlogPostOut, AdminBlogPostsListOut, AdminBlogPostUpsertIn

router = APIRouter()


@router.get('/blog-posts', response_model=AdminBlogPostsListOut)
def list_blog_posts(_: CurrentAdminDep, session: SessionDep) -> AdminBlogPostsListOut:
    items = repository(session).list_blog_posts()
    return AdminBlogPostsListOut(items=items, total=len(items))


@router.get('/blog-posts/{post_id}', response_model=AdminBlogPostOut)
def get_blog_post(post_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminBlogPostOut:
    post = repository(session).get_blog_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')
    return post


@router.post('/blog-posts', response_model=AdminBlogPostOut, status_code=status.HTTP_201_CREATED)
def create_blog_post(payload: AdminBlogPostUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminBlogPostOut:
    return repository(session).create_blog_post(payload)


@router.put('/blog-posts/{post_id}', response_model=AdminBlogPostOut)
def update_blog_post(post_id: UUID, payload: AdminBlogPostUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminBlogPostOut:
    post = repository(session).update_blog_post(post_id, payload)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')
    return post


@router.delete('/blog-posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_blog_post(post_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = repository(session).delete_blog_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Blog post not found.')
