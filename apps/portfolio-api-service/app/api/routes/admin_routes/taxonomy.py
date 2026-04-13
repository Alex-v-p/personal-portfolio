from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.repositories.admin.taxonomy import AdminTaxonomyRepository
from app.schemas.admin import (
    AdminBlogTagOut,
    AdminBlogTagUpsertIn,
    AdminSkillCategoryOut,
    AdminSkillCategoryUpsertIn,
    AdminSkillOut,
    AdminSkillUpsertIn,
)

router = APIRouter()


def taxonomy_repository(session: SessionDep) -> AdminTaxonomyRepository:
    return AdminTaxonomyRepository(session)


@router.get('/skill-categories', response_model=list[AdminSkillCategoryOut])
def list_skill_categories(_: CurrentAdminDep, session: SessionDep) -> list[AdminSkillCategoryOut]:
    return taxonomy_repository(session).list_skill_categories()


@router.post('/skill-categories', response_model=AdminSkillCategoryOut, status_code=status.HTTP_201_CREATED)
def create_skill_category(payload: AdminSkillCategoryUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminSkillCategoryOut:
    return taxonomy_repository(session).create_skill_category(payload)


@router.put('/skill-categories/{category_id}', response_model=AdminSkillCategoryOut)
def update_skill_category(category_id: UUID, payload: AdminSkillCategoryUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminSkillCategoryOut:
    category = taxonomy_repository(session).update_skill_category(category_id, payload)
    if category is None:
        raise HTTPException(status_code=404, detail='Skill category not found.')
    return category


@router.delete('/skill-categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_skill_category(category_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted, reason = taxonomy_repository(session).delete_skill_category(category_id)
    if reason == 'not_found':
        raise HTTPException(status_code=404, detail='Skill category not found.')
    if reason == 'in_use':
        raise HTTPException(status_code=409, detail='Skill category is still assigned to one or more skills.')
    if not deleted:
        raise HTTPException(status_code=400, detail='Skill category could not be deleted.')


@router.get('/skills', response_model=list[AdminSkillOut])
def list_skills(_: CurrentAdminDep, session: SessionDep) -> list[AdminSkillOut]:
    return taxonomy_repository(session).list_skills()


@router.post('/skills', response_model=AdminSkillOut, status_code=status.HTTP_201_CREATED)
def create_skill(payload: AdminSkillUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminSkillOut:
    return taxonomy_repository(session).create_skill(payload)


@router.put('/skills/{skill_id}', response_model=AdminSkillOut)
def update_skill(skill_id: UUID, payload: AdminSkillUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminSkillOut:
    skill = taxonomy_repository(session).update_skill(skill_id, payload)
    if skill is None:
        raise HTTPException(status_code=404, detail='Skill not found.')
    return skill


@router.delete('/skills/{skill_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_skill(skill_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = taxonomy_repository(session).delete_skill(skill_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Skill not found.')


@router.get('/blog-tags', response_model=list[AdminBlogTagOut])
def list_blog_tags(_: CurrentAdminDep, session: SessionDep) -> list[AdminBlogTagOut]:
    return taxonomy_repository(session).list_blog_tags()


@router.post('/blog-tags', response_model=AdminBlogTagOut, status_code=status.HTTP_201_CREATED)
def create_blog_tag(payload: AdminBlogTagUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminBlogTagOut:
    return taxonomy_repository(session).create_blog_tag(payload)


@router.put('/blog-tags/{tag_id}', response_model=AdminBlogTagOut)
def update_blog_tag(tag_id: UUID, payload: AdminBlogTagUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminBlogTagOut:
    tag = taxonomy_repository(session).update_blog_tag(tag_id, payload)
    if tag is None:
        raise HTTPException(status_code=404, detail='Blog tag not found.')
    return tag


@router.delete('/blog-tags/{tag_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_blog_tag(tag_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = taxonomy_repository(session).delete_blog_tag(tag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Blog tag not found.')
