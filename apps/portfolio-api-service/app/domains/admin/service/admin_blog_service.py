from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.admin.repository.content import AdminContentManagementRepository
from app.domains.admin.schema import AdminBlogPostOut, AdminBlogPostsListOut, AdminBlogPostUpsertIn


class AdminBlogService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminContentManagementRepository(session)

    def list_blog_posts(self) -> AdminBlogPostsListOut:
        items = self.repository.list_blog_posts()
        return AdminBlogPostsListOut(items=items, total=len(items))

    def get_blog_post(self, post_id: UUID) -> AdminBlogPostOut:
        post = self.repository.get_blog_post(post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog post not found.')
        return post

    def create_blog_post(self, payload: AdminBlogPostUpsertIn) -> AdminBlogPostOut:
        return self.repository.create_blog_post(payload)

    def update_blog_post(self, post_id: UUID, payload: AdminBlogPostUpsertIn) -> AdminBlogPostOut:
        post = self.repository.update_blog_post(post_id, payload)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog post not found.')
        return post

    def delete_blog_post(self, post_id: UUID) -> None:
        deleted = self.repository.delete_blog_post(post_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog post not found.')
