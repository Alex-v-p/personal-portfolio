from __future__ import annotations

from typing import Annotated
from uuid import UUID
from dataclasses import asdict

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import AdminUser
from app.db.session import get_session
from app.repositories.admin_content_repository import AdminContentRepository
from app.schemas.admin import (
    AdminAuthTokenOut,
    AdminBlogPostOut,
    AdminBlogPostUpsertIn,
    AdminBlogPostsListOut,
    AdminBlogTagOut,
    AdminBlogTagUpsertIn,
    AdminAssistantKnowledgeRebuildIn,
    AdminAssistantKnowledgeRebuildOut,
    AdminAssistantKnowledgeStatusOut,
    AdminContactMessageOut,
    AdminContactMessagesListOut,
    AdminDashboardSummaryOut,
    AdminExperienceOut,
    AdminExperiencesListOut,
    AdminExperienceUpsertIn,
    AdminGithubSnapshotOut,
    AdminGithubSnapshotRefreshIn,
    AdminGithubSnapshotsListOut,
    AdminGithubSnapshotUpsertIn,
    AdminLoginIn,
    AdminMediaFileOut,
    AdminMediaUploadOut,
    AdminMessageStatusUpdateIn,
    AdminNavigationItemOut,
    AdminNavigationItemsListOut,
    AdminNavigationItemUpsertIn,
    AdminProfileOut,
    AdminProfileUpdateIn,
    AdminProjectOut,
    AdminProjectsListOut,
    AdminProjectUpsertIn,
    AdminReferenceDataOut,
    AdminSiteActivityOut,
    AdminSkillCategoryOut,
    AdminSkillCategoryUpsertIn,
    AdminSkillOut,
    AdminSkillUpsertIn,
    AdminUserCreateIn,
    AdminUserOut,
    AdminUserUpdateIn,
)
from app.services.github_stats_sync import GithubStatsSyncError, GithubStatsSyncService
from app.services.knowledge_sync import KnowledgeSyncService
from app.services.media_storage import AdminMediaStorageService
from app.services.security import create_admin_access_token, get_current_admin_user, verify_password

router = APIRouter()
AdminUserDependency = Annotated[AdminUser, Depends(get_current_admin_user)]


@router.post('/auth/login', response_model=AdminAuthTokenOut)
def login(payload: AdminLoginIn, session: Session = Depends(get_session)) -> AdminAuthTokenOut:
    repository = AdminContentRepository(session)
    admin_user = repository.get_admin_user_by_email(payload.email)
    if admin_user is None or not admin_user.is_active or not verify_password(payload.password, admin_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid admin email or password.')
    token, expires_in_seconds = create_admin_access_token(admin_user=admin_user)
    return AdminAuthTokenOut(access_token=token, expires_in_seconds=expires_in_seconds, user=repository.map_admin_user(admin_user))


@router.get('/auth/me', response_model=AdminUserOut)
def get_me(current_admin: AdminUserDependency, session: Session = Depends(get_session)) -> AdminUserOut:
    return AdminContentRepository(session).map_admin_user(current_admin)


@router.get('/dashboard', response_model=AdminDashboardSummaryOut)
def get_dashboard_summary(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminDashboardSummaryOut:
    return AdminContentRepository(session).get_dashboard_summary()


@router.get('/reference-data', response_model=AdminReferenceDataOut)
def get_reference_data(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminReferenceDataOut:
    return AdminContentRepository(session).get_reference_data()


@router.get('/media-files', response_model=list[AdminMediaFileOut])
def list_media_files(_: AdminUserDependency, session: Session = Depends(get_session)) -> list[AdminMediaFileOut]:
    return AdminContentRepository(session).list_media_files()


@router.post('/media-files/upload', response_model=AdminMediaUploadOut, status_code=status.HTTP_201_CREATED)
async def upload_media_file(
    current_admin: AdminUserDependency,
    session: Session = Depends(get_session),
    file: UploadFile = File(...),
    folder: str | None = Form(default=None),
    title: str | None = Form(default=None),
    alt_text: str | None = Form(default=None, alias='altText'),
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


@router.delete('/media-files/{media_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_media_file(media_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    repository = AdminContentRepository(session)
    media_file = repository.get_media_file(media_id)
    if media_file is None:
        raise HTTPException(status_code=404, detail='Media file not found.')

    storage_service = AdminMediaStorageService()
    try:
        storage_service.delete_object(bucket_name=media_file.bucket_name, object_key=media_file.object_key)
    except Exception:
        pass

    deleted = repository.delete_media_file(media_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Media file not found.')


@router.get('/skill-categories', response_model=list[AdminSkillCategoryOut])
def list_skill_categories(_: AdminUserDependency, session: Session = Depends(get_session)) -> list[AdminSkillCategoryOut]:
    return AdminContentRepository(session).list_skill_categories()


@router.post('/skill-categories', response_model=AdminSkillCategoryOut, status_code=status.HTTP_201_CREATED)
def create_skill_category(payload: AdminSkillCategoryUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminSkillCategoryOut:
    return AdminContentRepository(session).create_skill_category(payload)


@router.put('/skill-categories/{category_id}', response_model=AdminSkillCategoryOut)
def update_skill_category(category_id: UUID, payload: AdminSkillCategoryUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminSkillCategoryOut:
    category = AdminContentRepository(session).update_skill_category(category_id, payload)
    if category is None:
        raise HTTPException(status_code=404, detail='Skill category not found.')
    return category


@router.delete('/skill-categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_skill_category(category_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    deleted, reason = AdminContentRepository(session).delete_skill_category(category_id)
    if reason == 'not_found':
        raise HTTPException(status_code=404, detail='Skill category not found.')
    if reason == 'in_use':
        raise HTTPException(status_code=409, detail='Skill category is still assigned to one or more skills.')
    if not deleted:
        raise HTTPException(status_code=400, detail='Skill category could not be deleted.')


@router.get('/skills', response_model=list[AdminSkillOut])
def list_skills(_: AdminUserDependency, session: Session = Depends(get_session)) -> list[AdminSkillOut]:
    return AdminContentRepository(session).list_skills()


@router.post('/skills', response_model=AdminSkillOut, status_code=status.HTTP_201_CREATED)
def create_skill(payload: AdminSkillUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminSkillOut:
    return AdminContentRepository(session).create_skill(payload)


@router.put('/skills/{skill_id}', response_model=AdminSkillOut)
def update_skill(skill_id: UUID, payload: AdminSkillUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminSkillOut:
    skill = AdminContentRepository(session).update_skill(skill_id, payload)
    if skill is None:
        raise HTTPException(status_code=404, detail='Skill not found.')
    return skill


@router.delete('/skills/{skill_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_skill(skill_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    deleted = AdminContentRepository(session).delete_skill(skill_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Skill not found.')


@router.get('/blog-tags', response_model=list[AdminBlogTagOut])
def list_blog_tags(_: AdminUserDependency, session: Session = Depends(get_session)) -> list[AdminBlogTagOut]:
    return AdminContentRepository(session).list_blog_tags()


@router.post('/blog-tags', response_model=AdminBlogTagOut, status_code=status.HTTP_201_CREATED)
def create_blog_tag(payload: AdminBlogTagUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogTagOut:
    return AdminContentRepository(session).create_blog_tag(payload)


@router.put('/blog-tags/{tag_id}', response_model=AdminBlogTagOut)
def update_blog_tag(tag_id: UUID, payload: AdminBlogTagUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogTagOut:
    tag = AdminContentRepository(session).update_blog_tag(tag_id, payload)
    if tag is None:
        raise HTTPException(status_code=404, detail='Blog tag not found.')
    return tag


@router.delete('/blog-tags/{tag_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_blog_tag(tag_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    deleted = AdminContentRepository(session).delete_blog_tag(tag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Blog tag not found.')


@router.get('/projects', response_model=AdminProjectsListOut)
def list_projects(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProjectsListOut:
    items = AdminContentRepository(session).list_projects()
    return AdminProjectsListOut(items=items, total=len(items))


@router.get('/projects/{project_id}', response_model=AdminProjectOut)
def get_project(project_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProjectOut:
    project = AdminContentRepository(session).get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.post('/projects', response_model=AdminProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: AdminProjectUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProjectOut:
    return AdminContentRepository(session).create_project(payload)


@router.put('/projects/{project_id}', response_model=AdminProjectOut)
def update_project(project_id: UUID, payload: AdminProjectUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProjectOut:
    project = AdminContentRepository(session).update_project(project_id, payload)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.delete('/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_project(project_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    deleted = AdminContentRepository(session).delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Project not found.')


@router.get('/blog-posts', response_model=AdminBlogPostsListOut)
def list_blog_posts(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogPostsListOut:
    items = AdminContentRepository(session).list_blog_posts()
    return AdminBlogPostsListOut(items=items, total=len(items))


@router.get('/blog-posts/{post_id}', response_model=AdminBlogPostOut)
def get_blog_post(post_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogPostOut:
    post = AdminContentRepository(session).get_blog_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')
    return post


@router.post('/blog-posts', response_model=AdminBlogPostOut, status_code=status.HTTP_201_CREATED)
def create_blog_post(payload: AdminBlogPostUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogPostOut:
    return AdminContentRepository(session).create_blog_post(payload)


@router.put('/blog-posts/{post_id}', response_model=AdminBlogPostOut)
def update_blog_post(post_id: UUID, payload: AdminBlogPostUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminBlogPostOut:
    post = AdminContentRepository(session).update_blog_post(post_id, payload)
    if post is None:
        raise HTTPException(status_code=404, detail='Blog post not found.')
    return post


@router.delete('/blog-posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_blog_post(post_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    deleted = AdminContentRepository(session).delete_blog_post(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Blog post not found.')


@router.get('/experiences', response_model=AdminExperiencesListOut)
def list_experiences(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminExperiencesListOut:
    items = AdminContentRepository(session).list_experiences()
    return AdminExperiencesListOut(items=items, total=len(items))


@router.get('/experiences/{experience_id}', response_model=AdminExperienceOut)
def get_experience(experience_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminExperienceOut:
    experience = AdminContentRepository(session).get_experience(experience_id)
    if experience is None:
        raise HTTPException(status_code=404, detail='Experience not found.')
    return experience


@router.post('/experiences', response_model=AdminExperienceOut, status_code=status.HTTP_201_CREATED)
def create_experience(payload: AdminExperienceUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminExperienceOut:
    return AdminContentRepository(session).create_experience(payload)


@router.put('/experiences/{experience_id}', response_model=AdminExperienceOut)
def update_experience(experience_id: UUID, payload: AdminExperienceUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminExperienceOut:
    experience = AdminContentRepository(session).update_experience(experience_id, payload)
    if experience is None:
        raise HTTPException(status_code=404, detail='Experience not found.')
    return experience


@router.delete('/experiences/{experience_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_experience(experience_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    deleted = AdminContentRepository(session).delete_experience(experience_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Experience not found.')


@router.get('/navigation-items', response_model=AdminNavigationItemsListOut)
def list_navigation_items(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminNavigationItemsListOut:
    items = AdminContentRepository(session).list_navigation_items()
    return AdminNavigationItemsListOut(items=items, total=len(items))


@router.post('/navigation-items', response_model=AdminNavigationItemOut, status_code=status.HTTP_201_CREATED)
def create_navigation_item(payload: AdminNavigationItemUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminNavigationItemOut:
    return AdminContentRepository(session).create_navigation_item(payload)


@router.put('/navigation-items/{item_id}', response_model=AdminNavigationItemOut)
def update_navigation_item(item_id: UUID, payload: AdminNavigationItemUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminNavigationItemOut:
    item = AdminContentRepository(session).update_navigation_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail='Navigation item not found.')
    return item


@router.delete('/navigation-items/{item_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_navigation_item(item_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    deleted = AdminContentRepository(session).delete_navigation_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Navigation item not found.')


@router.get('/github-snapshots', response_model=AdminGithubSnapshotsListOut)
def list_github_snapshots(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminGithubSnapshotsListOut:
    items = AdminContentRepository(session).list_github_snapshots()
    return AdminGithubSnapshotsListOut(items=items, total=len(items))


@router.get('/github-snapshots/{snapshot_id}', response_model=AdminGithubSnapshotOut)
def get_github_snapshot(snapshot_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminGithubSnapshotOut:
    snapshot = AdminContentRepository(session).get_github_snapshot(snapshot_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail='GitHub snapshot not found.')
    return snapshot


@router.post('/github-snapshots', response_model=AdminGithubSnapshotOut, status_code=status.HTTP_201_CREATED)
def create_github_snapshot(payload: AdminGithubSnapshotUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminGithubSnapshotOut:
    return AdminContentRepository(session).create_github_snapshot(payload)


@router.post('/github-snapshots/refresh', response_model=AdminGithubSnapshotOut)
def refresh_github_snapshot(payload: AdminGithubSnapshotRefreshIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminGithubSnapshotOut:
    try:
        synced = GithubStatsSyncService().sync_profile(payload.username)
    except GithubStatsSyncError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return AdminContentRepository(session).refresh_github_snapshot(synced, prune_history=payload.prune_history)


@router.put('/github-snapshots/{snapshot_id}', response_model=AdminGithubSnapshotOut)
def update_github_snapshot(snapshot_id: UUID, payload: AdminGithubSnapshotUpsertIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminGithubSnapshotOut:
    snapshot = AdminContentRepository(session).update_github_snapshot(snapshot_id, payload)
    if snapshot is None:
        raise HTTPException(status_code=404, detail='GitHub snapshot not found.')
    return snapshot


@router.delete('/github-snapshots/{snapshot_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_github_snapshot(snapshot_id: UUID, _: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    deleted = AdminContentRepository(session).delete_github_snapshot(snapshot_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='GitHub snapshot not found.')


@router.get('/admin-users', response_model=list[AdminUserOut])
def list_admin_users(_: AdminUserDependency, session: Session = Depends(get_session)) -> list[AdminUserOut]:
    return AdminContentRepository(session).list_admin_users()


@router.post('/admin-users', response_model=AdminUserOut, status_code=status.HTTP_201_CREATED)
def create_admin_user(payload: AdminUserCreateIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminUserOut:
    return AdminContentRepository(session).create_admin_user(payload)


@router.put('/admin-users/{admin_user_id}', response_model=AdminUserOut)
def update_admin_user(admin_user_id: UUID, payload: AdminUserUpdateIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminUserOut:
    user = AdminContentRepository(session).update_admin_user(admin_user_id, payload)
    if user is None:
        raise HTTPException(status_code=404, detail='Admin user not found.')
    return user


@router.delete('/admin-users/{admin_user_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_admin_user(admin_user_id: UUID, current_admin: AdminUserDependency, session: Session = Depends(get_session)) -> None:
    if current_admin.id == admin_user_id:
        raise HTTPException(status_code=400, detail='You cannot delete the currently signed-in admin user.')
    deleted = AdminContentRepository(session).delete_admin_user(admin_user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Admin user not found.')


@router.get('/profile', response_model=AdminProfileOut)
def get_profile(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProfileOut:
    profile = AdminContentRepository(session).get_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail='Profile not found.')
    return profile


@router.put('/profile', response_model=AdminProfileOut)
def update_profile(payload: AdminProfileUpdateIn, _: AdminUserDependency, session: Session = Depends(get_session)) -> AdminProfileOut:
    profile = AdminContentRepository(session).update_profile(payload)
    if profile is None:
        raise HTTPException(status_code=404, detail='Profile not found.')
    return profile




@router.get('/site-activity', response_model=AdminSiteActivityOut)
def get_site_activity(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminSiteActivityOut:
    return AdminContentRepository(session).get_site_activity()


@router.get('/assistant/knowledge', response_model=AdminAssistantKnowledgeStatusOut)
def get_assistant_knowledge_status(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminAssistantKnowledgeStatusOut:
    return AdminAssistantKnowledgeStatusOut(**asdict(KnowledgeSyncService(session).get_status()))


@router.post('/assistant/knowledge/rebuild', response_model=AdminAssistantKnowledgeRebuildOut)
def rebuild_assistant_knowledge(
    payload: AdminAssistantKnowledgeRebuildIn,
    _: AdminUserDependency,
    session: Session = Depends(get_session),
) -> AdminAssistantKnowledgeRebuildOut:
    del payload
    return AdminAssistantKnowledgeRebuildOut(**asdict(KnowledgeSyncService(session).rebuild()))


@router.get('/contact-messages', response_model=AdminContactMessagesListOut)
def list_contact_messages(_: AdminUserDependency, session: Session = Depends(get_session)) -> AdminContactMessagesListOut:
    items = AdminContentRepository(session).list_contact_messages()
    return AdminContactMessagesListOut(items=items, total=len(items))


@router.patch('/contact-messages/{message_id}', response_model=AdminContactMessageOut)
def update_contact_message(
    message_id: UUID,
    payload: AdminMessageStatusUpdateIn,
    _: AdminUserDependency,
    session: Session = Depends(get_session),
) -> AdminContactMessageOut:
    message = AdminContentRepository(session).update_contact_message_status(message_id, is_read=payload.is_read)
    if message is None:
        raise HTTPException(status_code=404, detail='Contact message not found.')
    return message
