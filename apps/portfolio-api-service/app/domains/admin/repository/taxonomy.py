from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select

from app.db.models import BlogTag, Skill, SkillCategory
from app.domains.admin.schema import (
    AdminBlogTagOut,
    AdminBlogTagUpsertIn,
    AdminSkillCategoryOut,
    AdminSkillCategoryUpsertIn,
    AdminSkillOut,
    AdminSkillUpsertIn,
)
from app.domains.admin.repository.support import AdminRepositorySupport


class AdminTaxonomyRepository(AdminRepositorySupport):
    def list_skill_categories(self) -> list[AdminSkillCategoryOut]:
        categories = self.session.scalars(select(SkillCategory).order_by(SkillCategory.sort_order.asc(), SkillCategory.name.asc())).all()
        return [self._map_skill_category(category) for category in categories]

    def create_skill_category(self, payload: AdminSkillCategoryUpsertIn) -> AdminSkillCategoryOut:
        category = SkillCategory(
            name=payload.name.strip(),
            name_nl=self._normalize_optional_text(payload.name_nl),
            description=self._normalize_optional_text(payload.description),
            description_nl=self._normalize_optional_text(payload.description_nl),
            icon_key=self._normalize_optional_text(payload.icon_key),
            sort_order=payload.sort_order,
        )
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return self._map_skill_category(category)

    def update_skill_category(self, category_id: UUID, payload: AdminSkillCategoryUpsertIn) -> AdminSkillCategoryOut | None:
        category = self.session.get(SkillCategory, category_id)
        if category is None:
            return None
        category.name = payload.name.strip()
        category.name_nl = self._normalize_optional_text(payload.name_nl)
        category.description = self._normalize_optional_text(payload.description)
        category.description_nl = self._normalize_optional_text(payload.description_nl)
        category.icon_key = self._normalize_optional_text(payload.icon_key)
        category.sort_order = payload.sort_order
        self.session.commit()
        self.session.refresh(category)
        return self._map_skill_category(category)

    def delete_skill_category(self, category_id: UUID) -> tuple[bool, str | None]:
        category = self.session.get(SkillCategory, category_id)
        if category is None:
            return False, 'not_found'
        in_use = self.session.scalar(select(func.count(Skill.id)).where(Skill.category_id == category_id)) or 0
        if in_use:
            return False, 'in_use'
        self.session.delete(category)
        self.session.commit()
        return True, None

    def list_skills(self) -> list[AdminSkillOut]:
        skills = self.session.scalars(select(Skill).order_by(Skill.sort_order.asc(), Skill.name.asc())).all()
        return [self._map_admin_skill(skill) for skill in skills]

    def create_skill(self, payload: AdminSkillUpsertIn) -> AdminSkillOut:
        skill = Skill(
            category_id=self._required_uuid(payload.category_id),
            name=payload.name.strip(),
            years_of_experience=payload.years_of_experience,
            icon_key=self._normalize_optional_text(payload.icon_key),
            sort_order=payload.sort_order,
            is_highlighted=payload.is_highlighted,
        )
        self.session.add(skill)
        self.session.commit()
        self.session.refresh(skill)
        return self._map_admin_skill(skill)

    def update_skill(self, skill_id: UUID, payload: AdminSkillUpsertIn) -> AdminSkillOut | None:
        skill = self.session.get(Skill, skill_id)
        if skill is None:
            return None
        skill.category_id = self._required_uuid(payload.category_id)
        skill.name = payload.name.strip()
        skill.years_of_experience = payload.years_of_experience
        skill.icon_key = self._normalize_optional_text(payload.icon_key)
        skill.sort_order = payload.sort_order
        skill.is_highlighted = payload.is_highlighted
        self.session.commit()
        self.session.refresh(skill)
        return self._map_admin_skill(skill)

    def delete_skill(self, skill_id: UUID) -> bool:
        skill = self.session.get(Skill, skill_id)
        if skill is None:
            return False
        self.session.delete(skill)
        self.session.commit()
        return True

    def list_blog_tags(self) -> list[AdminBlogTagOut]:
        tags = self.session.scalars(select(BlogTag).order_by(BlogTag.name.asc())).all()
        return [AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug) for tag in tags]

    def create_blog_tag(self, payload: AdminBlogTagUpsertIn) -> AdminBlogTagOut:
        name = payload.name.strip()
        tag = BlogTag(name=name, slug=self._ensure_unique_slug(BlogTag, payload.slug or name))
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug)

    def update_blog_tag(self, tag_id: UUID, payload: AdminBlogTagUpsertIn) -> AdminBlogTagOut | None:
        tag = self.session.get(BlogTag, tag_id)
        if tag is None:
            return None
        name = payload.name.strip()
        tag.name = name
        tag.slug = self._ensure_unique_slug(BlogTag, payload.slug or name, current_id=tag_id)
        self.session.commit()
        self.session.refresh(tag)
        return AdminBlogTagOut(id=str(tag.id), name=tag.name, slug=tag.slug)

    def delete_blog_tag(self, tag_id: UUID) -> bool:
        tag = self.session.get(BlogTag, tag_id)
        if tag is None:
            return False
        self.session.delete(tag)
        self.session.commit()
        return True
