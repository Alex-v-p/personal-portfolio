from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import (
    AdminBlogTagOut,
    AdminBlogTagUpsertIn,
    AdminSkillCategoryOut,
    AdminSkillCategoryUpsertIn,
    AdminSkillOut,
    AdminSkillUpsertIn,
)
from app.domains.admin.service.admin_taxonomy_service import AdminTaxonomyService

router = APIRouter()


@router.get('/skill-categories', response_model=list[AdminSkillCategoryOut])
def list_skill_categories(_: CurrentAdminDep, session: SessionDep) -> list[AdminSkillCategoryOut]:
    return AdminTaxonomyService(session).list_skill_categories()


@router.post('/skill-categories', response_model=AdminSkillCategoryOut, status_code=status.HTTP_201_CREATED)
def create_skill_category(payload: AdminSkillCategoryUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminSkillCategoryOut:
    return AdminTaxonomyService(session).create_skill_category(payload)


@router.put('/skill-categories/{category_id}', response_model=AdminSkillCategoryOut)
def update_skill_category(category_id: UUID, payload: AdminSkillCategoryUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminSkillCategoryOut:
    return AdminTaxonomyService(session).update_skill_category(category_id, payload)


@router.delete('/skill-categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_skill_category(category_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    AdminTaxonomyService(session).delete_skill_category(category_id)


@router.get('/skills', response_model=list[AdminSkillOut])
def list_skills(_: CurrentAdminDep, session: SessionDep) -> list[AdminSkillOut]:
    return AdminTaxonomyService(session).list_skills()


@router.post('/skills', response_model=AdminSkillOut, status_code=status.HTTP_201_CREATED)
def create_skill(payload: AdminSkillUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminSkillOut:
    return AdminTaxonomyService(session).create_skill(payload)


@router.put('/skills/{skill_id}', response_model=AdminSkillOut)
def update_skill(skill_id: UUID, payload: AdminSkillUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminSkillOut:
    return AdminTaxonomyService(session).update_skill(skill_id, payload)


@router.delete('/skills/{skill_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_skill(skill_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    AdminTaxonomyService(session).delete_skill(skill_id)


@router.get('/blog-tags', response_model=list[AdminBlogTagOut])
def list_blog_tags(_: CurrentAdminDep, session: SessionDep) -> list[AdminBlogTagOut]:
    return AdminTaxonomyService(session).list_blog_tags()


@router.post('/blog-tags', response_model=AdminBlogTagOut, status_code=status.HTTP_201_CREATED)
def create_blog_tag(payload: AdminBlogTagUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminBlogTagOut:
    return AdminTaxonomyService(session).create_blog_tag(payload)


@router.put('/blog-tags/{tag_id}', response_model=AdminBlogTagOut)
def update_blog_tag(tag_id: UUID, payload: AdminBlogTagUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminBlogTagOut:
    return AdminTaxonomyService(session).update_blog_tag(tag_id, payload)


@router.delete('/blog-tags/{tag_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_blog_tag(tag_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    AdminTaxonomyService(session).delete_blog_tag(tag_id)
