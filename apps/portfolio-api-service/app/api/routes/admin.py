from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import AdminUser
from app.db.session import get_session
from app.repositories.admin_content_repository import AdminContentRepository
from app.schemas.admin import (
    AdminMediaFileOut,
    AdminMediaUploadOut,
    AdminAuthTokenOut,
    AdminBlogPostOut,
    AdminBlogPostUpsertIn,
    AdminBlogPostsListOut,
    AdminContactMessageOut,
    AdminContactMessagesListOut,
    AdminDashboardSummaryOut,
    AdminLoginIn,
    AdminMessageStatusUpdateIn,
    AdminProfileOut,
    AdminProfileUpdateIn,
    AdminProjectOut,
    AdminProjectsListOut,
    AdminProjectUpsertIn,
    AdminReferenceDataOut,
    AdminUserOut,
)
from app.services.media_storage import AdminMediaStorageService
from app.services.security import (
    create_admin_access_token,
    get_current_admin_user,
    verify_password,
)

router = APIRouter()
AdminUserDependency = Annotated[AdminUser, Depends(get_current_admin_user)]


@router.post('/auth/login', response_model=AdminAuthTokenOut)
def login(payload: AdminLoginIn, session: Session = Depends(get_session)) -> AdminAuthTokenOut:
    repository = AdminContentRepository(session)
    admin_user = repository.get_admin_user_by_email(payload.email)
    if admin_user is None or not admin_user.is_active or not verify_password(payload.password, admin_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid admin email or password.')

    token, expires_in_seconds = create_admin_access_token(admin_user=admin_user)
    return AdminAuthTokenOut(
        access_token=token,
        expires_in_seconds=expires_in_seconds,
        user=repository.map_admin_user(admin_user),
    )


@router.get('/auth/me', response_model=AdminUserOut)
def get_me(current_admin: AdminUserDependency, session: Session = Depends(get_session)) -> AdminUserOut:
    repository = AdminContentRepository(session)
    return repository.map_admin_user(current_admin)


@router.get('/dashboard', response_model=AdminDashboardSummaryOut)
def get_dashboard_summary(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminDashboardSummaryOut:
    repository = AdminContentRepository(session)
    return repository.get_dashboard_summary()


@router.get('/reference-data', response_model=AdminReferenceDataOut)
def get_reference_data(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminReferenceDataOut:
    repository = AdminContentRepository(session)
    return repository.get_reference_data()


@router.get('/media-files', response_model=list[AdminMediaFileOut])
def list_media_files(_: AdminUserDependency, session: Session = Depends(get_session)) -> list[AdminMediaFileOut]:
    repository = AdminContentRepository(session)
    return repository.list_media_files()


@router.post('/media-files/upload', response_model=AdminMediaUploadOut, status_code=status.HTTP_201_CREATED)
async def upload_media_file(
    current_admin: AdminUserDependency,
    session: Session = Depends(get_session),
    file: UploadFile = File(...),
    folder: str | None = Form(default='uploads'),
    title: str | None = Form(default=None),
    alt_text: str | None = Form(default=None),
    description: str | None = Form(default=None),
    visibility: str = Form(default='public'),
) -> AdminMediaUploadOut:
    settings = get_settings()
    if visibility not in {'public', 'private', 'signed'}:
        raise HTTPException(status_code=400, detail='Invalid media visibility.')
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail='Uploaded file is empty.')
    if len(file_bytes) > settings.media_max_upload_bytes:
        raise HTTPException(status_code=413, detail='Uploaded file exceeds the configured size limit.')

    storage_service = AdminMediaStorageService()
    repository = AdminContentRepository(session)
    stored_object = storage_service.upload_bytes(
        file_bytes=file_bytes,
        original_filename=file.filename or 'upload',
        mime_type=file.content_type,
        folder=folder,
    )
    try:
        return repository.create_media_file(
            stored_object=stored_object,
            uploaded_by_id=current_admin.id,
            title=title,
            alt_text=alt_text,
            description=description,
            visibility=visibility,
        )
    except Exception:
        storage_service.delete_object(bucket_name=stored_object.bucket_name, object_key=stored_object.object_key)
        raise


@router.get('/projects', response_model=AdminProjectsListOut)
def list_projects(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProjectsListOut:
    repository = AdminContentRepository(session)
    items = repository.list_projects()
    return AdminProjectsListOut(items=items, total=len(items))


@router.get('/projects/{project_id}', response_model=AdminProjectOut)
def get_project(project_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProjectOut:
    repository = AdminContentRepository(session)
    project = repository.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.post('/projects', response_model=AdminProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: AdminProjectUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProjectOut:
    repository = AdminContentRepository(session)
    return repository.create_project(payload)


@router.put('/projects/{project_id}', response_model=AdminProjectOut)
def update_project(project_id: UUID, payload: AdminProjectUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProjectOut:
    repository = AdminContentRepository(session)
    project = repository.update_project(project_id, payload)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.delete('/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_project(project_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    repository = AdminContentRepository(session)
    deleted = repository.delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Project not found.')


@router.get('/blog-posts', response_model=AdminBlogPostsListOut)
def list_blog_posts(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogPostsListOut:
    repository = AdminContentRepository(session)
    items = repository.list_blog_posts()
    return AdminBlogPostsListOut(items=items, total=len(items))


@router.get('/blog-posts/{post_id}', response_model=AdminBlogPostOut)
def get_blog_post(post_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogPostOut:
    repository = AdminContentRepository(session)
    post = repository.get_blog_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')
    return post


@router.post('/blog-posts', response_model=AdminBlogPostOut, status_code=status.HTTP_201_CREATED)
def create_blog_post(payload: AdminBlogPostUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogPostOut:
    repository = AdminContentRepository(session)
    return repository.create_blog_post(payload)


@router.put('/blog-posts/{post_id}', response_model=AdminBlogPostOut)
def update_blog_post(post_id: UUID, payload: AdminBlogPostUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogPostOut:
    repository = AdminContentRepository(session)
    post = repository.update_blog_post(post_id, payload)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')
    return post


@router.delete('/blog-posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_blog_post(post_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    repository = AdminContentRepository(session)
    deleted = repository.delete_blog_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Blog post not found.')


@router.get('/profile', response_model=AdminProfileOut)
def get_profile(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProfileOut:
    repository = AdminContentRepository(session)
    profile = repository.get_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail='Profile not found.')
    return profile


@router.put('/profile', response_model=AdminProfileOut)
def update_profile(payload: AdminProfileUpdateIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProfileOut:
    repository = AdminContentRepository(session)
    profile = repository.update_profile(payload)
    if profile is None:
        raise HTTPException(status_code=404, detail='Profile not found.')
    return profile


@router.get('/contact-messages', response_model=AdminContactMessagesListOut)
def list_contact_messages(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminContactMessagesListOut:
    repository = AdminContentRepository(session)
    items = repository.list_contact_messages()
    return AdminContactMessagesListOut(items=items, total=len(items))


@router.patch('/contact-messages/{message_id}', response_model=AdminContactMessageOut)
def update_contact_message(
    message_id: UUID,
    payload: AdminMessageStatusUpdateIn,
    _: AdminUserDependency,
    session: Session = Depends(get_session),
) -> AdminContactMessageOut:
    repository = AdminContentRepository(session)
    message = repository.update_contact_message_status(message_id, is_read=payload.is_read)
    if message is None:
        raise HTTPException(status_code=404, detail='Contact message not found.')
    return message
