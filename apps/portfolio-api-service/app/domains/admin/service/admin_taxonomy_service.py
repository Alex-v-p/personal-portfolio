from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.domains.admin.repository.taxonomy import AdminTaxonomyRepository
from app.domains.admin.schema import (
    AdminBlogTagOut,
    AdminBlogTagUpsertIn,
    AdminSkillCategoryOut,
    AdminSkillCategoryUpsertIn,
    AdminSkillOut,
    AdminSkillUpsertIn,
)


class AdminTaxonomyService:
    def __init__(self, session: Session) -> None:
        self.repository = AdminTaxonomyRepository(session)

    def list_skill_categories(self) -> list[AdminSkillCategoryOut]:
        return self.repository.list_skill_categories()

    def create_skill_category(self, payload: AdminSkillCategoryUpsertIn) -> AdminSkillCategoryOut:
        return self.repository.create_skill_category(payload)

    def update_skill_category(self, category_id: UUID, payload: AdminSkillCategoryUpsertIn) -> AdminSkillCategoryOut:
        category = self.repository.update_skill_category(category_id, payload)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill category not found.')
        return category

    def delete_skill_category(self, category_id: UUID) -> None:
        deleted, reason = self.repository.delete_skill_category(category_id)
        if reason == 'not_found':
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill category not found.')
        if reason == 'in_use':
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Skill category is still assigned to one or more skills.')
        if not deleted:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Skill category could not be deleted.')

    def list_skills(self) -> list[AdminSkillOut]:
        return self.repository.list_skills()

    def create_skill(self, payload: AdminSkillUpsertIn) -> AdminSkillOut:
        return self.repository.create_skill(payload)

    def update_skill(self, skill_id: UUID, payload: AdminSkillUpsertIn) -> AdminSkillOut:
        skill = self.repository.update_skill(skill_id, payload)
        if skill is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill not found.')
        return skill

    def delete_skill(self, skill_id: UUID) -> None:
        deleted = self.repository.delete_skill(skill_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Skill not found.')

    def list_blog_tags(self) -> list[AdminBlogTagOut]:
        return self.repository.list_blog_tags()

    def create_blog_tag(self, payload: AdminBlogTagUpsertIn) -> AdminBlogTagOut:
        return self.repository.create_blog_tag(payload)

    def update_blog_tag(self, tag_id: UUID, payload: AdminBlogTagUpsertIn) -> AdminBlogTagOut:
        tag = self.repository.update_blog_tag(tag_id, payload)
        if tag is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog tag not found.')
        return tag

    def delete_blog_tag(self, tag_id: UUID) -> None:
        deleted = self.repository.delete_blog_tag(tag_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog tag not found.')
