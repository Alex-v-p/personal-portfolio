from __future__ import annotations

from sqlalchemy import func, select

from app.db.models import AdminUser, BlogPost, BlogTag, ContactMessage, Experience, GithubSnapshot, MediaFile, NavigationItem, Project, ProjectState, PublicationStatus, Skill, SkillCategory
from app.schemas.admin import AdminDashboardSummaryOut, AdminReferenceDataOut
from app.repositories.admin.support import AdminRepositorySupport


class AdminOverviewRepository(AdminRepositorySupport):
    def get_dashboard_summary(self) -> AdminDashboardSummaryOut:
        return AdminDashboardSummaryOut(
            projects=self.session.scalar(select(func.count(Project.id))) or 0,
            blog_posts=self.session.scalar(select(func.count(BlogPost.id))) or 0,
            unread_messages=self.session.scalar(select(func.count(ContactMessage.id)).where(ContactMessage.is_read.is_(False))) or 0,
            skills=self.session.scalar(select(func.count(Skill.id))) or 0,
            skill_categories=self.session.scalar(select(func.count(SkillCategory.id))) or 0,
            media_files=self.session.scalar(select(func.count(MediaFile.id))) or 0,
            experiences=self.session.scalar(select(func.count(Experience.id))) or 0,
            navigation_items=self.session.scalar(select(func.count(NavigationItem.id))) or 0,
            blog_tags=self.session.scalar(select(func.count(BlogTag.id))) or 0,
            admin_users=self.session.scalar(select(func.count(AdminUser.id))) or 0,
            github_snapshots=self.session.scalar(select(func.count(GithubSnapshot.id))) or 0,
        )

    def get_reference_data(self) -> AdminReferenceDataOut:
        skills = self.list_skills()
        skill_categories = self.list_skill_categories()
        media_files = self.list_media_files()
        blog_tags = self.list_blog_tags()
        return AdminReferenceDataOut(
            skills=skills,
            skill_categories=skill_categories,
            media_files=media_files,
            blog_tags=blog_tags,
            project_states=[state.value for state in ProjectState],
            publication_statuses=[status.value for status in PublicationStatus],
        )
