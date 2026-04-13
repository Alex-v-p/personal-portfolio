from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.repositories.admin.content import AdminContentManagementRepository
from app.schemas.admin import (
    AdminBlogPostOut,
    AdminBlogPostUpsertIn,
    AdminBlogPostsListOut,
    AdminExperienceOut,
    AdminExperienceUpsertIn,
    AdminExperiencesListOut,
    AdminNavigationItemOut,
    AdminNavigationItemUpsertIn,
    AdminNavigationItemsListOut,
    AdminProfileOut,
    AdminProfileUpdateIn,
    AdminProjectOut,
    AdminProjectsListOut,
    AdminProjectUpsertIn,
)

router = APIRouter()


def repository(session: SessionDep) -> AdminContentManagementRepository:
    return AdminContentManagementRepository(session)


@router.get('/projects', response_model=AdminProjectsListOut)
def list_projects(_: CurrentAdminDep, session: SessionDep) -> AdminProjectsListOut:
    items = repository(session).list_projects()
    return AdminProjectsListOut(items=items, total=len(items))


@router.get('/projects/{project_id}', response_model=AdminProjectOut)
def get_project(project_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    project = repository(session).get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.post('/projects', response_model=AdminProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: AdminProjectUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    return repository(session).create_project(payload)


@router.put('/projects/{project_id}', response_model=AdminProjectOut)
def update_project(project_id: UUID, payload: AdminProjectUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    project = repository(session).update_project(project_id, payload)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.delete('/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_project(project_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = repository(session).delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Project not found.')


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


@router.get('/experiences', response_model=AdminExperiencesListOut)
def list_experiences(_: CurrentAdminDep, session: SessionDep) -> AdminExperiencesListOut:
    items = repository(session).list_experiences()
    return AdminExperiencesListOut(items=items, total=len(items))


@router.get('/experiences/{experience_id}', response_model=AdminExperienceOut)
def get_experience(experience_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    experience = repository(session).get_experience(experience_id)
    if experience is None:
        raise HTTPException(status_code=404, detail='Experience entry not found.')
    return experience


@router.post('/experiences', response_model=AdminExperienceOut, status_code=status.HTTP_201_CREATED)
def create_experience(payload: AdminExperienceUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    return repository(session).create_experience(payload)


@router.put('/experiences/{experience_id}', response_model=AdminExperienceOut)
def update_experience(experience_id: UUID, payload: AdminExperienceUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    experience = repository(session).update_experience(experience_id, payload)
    if experience is None:
        raise HTTPException(status_code=404, detail='Experience entry not found.')
    return experience


@router.delete('/experiences/{experience_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_experience(experience_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = repository(session).delete_experience(experience_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Experience entry not found.')


@router.get('/navigation-items', response_model=AdminNavigationItemsListOut)
def list_navigation_items(_: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemsListOut:
    items = repository(session).list_navigation_items()
    return AdminNavigationItemsListOut(items=items, total=len(items))


@router.post('/navigation-items', response_model=AdminNavigationItemOut, status_code=status.HTTP_201_CREATED)
def create_navigation_item(payload: AdminNavigationItemUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemOut:
    return repository(session).create_navigation_item(payload)


@router.put('/navigation-items/{item_id}', response_model=AdminNavigationItemOut)
def update_navigation_item(item_id: UUID, payload: AdminNavigationItemUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminNavigationItemOut:
    item = repository(session).update_navigation_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail='Navigation item not found.')
    return item


@router.delete('/navigation-items/{item_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_navigation_item(item_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = repository(session).delete_navigation_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Navigation item not found.')


@router.get('/profile', response_model=AdminProfileOut)
def get_profile(_: CurrentAdminDep, session: SessionDep) -> AdminProfileOut:
    profile = repository(session).get_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail='Profile not found.')
    return profile


@router.put('/profile', response_model=AdminProfileOut)
def update_profile(payload: AdminProfileUpdateIn, _: CurrentAdminDep, session: SessionDep) -> AdminProfileOut:
    profile = repository(session).update_profile(payload)
    if profile is None:
        raise HTTPException(status_code=404, detail='Profile not found.')
    return profile
