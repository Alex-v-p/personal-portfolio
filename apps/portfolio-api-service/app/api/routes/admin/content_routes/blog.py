from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import AdminBlogPostOut, AdminBlogPostsListOut, AdminBlogPostUpsertIn
from app.domains.admin.service.admin_blog_service import AdminBlogService

router = APIRouter()


@router.get('/blog-posts', response_model=AdminBlogPostsListOut)
def list_blog_posts(_: CurrentAdminDep, session: SessionDep) -> AdminBlogPostsListOut:
    return AdminBlogService(session).list_blog_posts()


@router.get('/blog-posts/{post_id}', response_model=AdminBlogPostOut)
def get_blog_post(post_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminBlogPostOut:
    return AdminBlogService(session).get_blog_post(post_id)


@router.post('/blog-posts', response_model=AdminBlogPostOut, status_code=status.HTTP_201_CREATED)
def create_blog_post(payload: AdminBlogPostUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminBlogPostOut:
    return AdminBlogService(session).create_blog_post(payload)


@router.put('/blog-posts/{post_id}', response_model=AdminBlogPostOut)
def update_blog_post(post_id: UUID, payload: AdminBlogPostUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminBlogPostOut:
    return AdminBlogService(session).update_blog_post(post_id, payload)


@router.delete('/blog-posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_blog_post(post_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    AdminBlogService(session).delete_blog_post(post_id)
