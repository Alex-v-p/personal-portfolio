import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../../core/config/api.config';
import {
  AdminAssistantKnowledgeStatus,
  AdminAuthToken,
  AdminBlogPost,
  AdminBlogPostUpsert,
  AdminBlogTag,
  AdminBlogTagUpsert,
  AdminCollectionResponse,
  AdminContactMessage,
  AdminDashboardSummary,
  AdminExperience,
  AdminExperienceUpsert,
  AdminGithubSnapshot,
  AdminGithubSnapshotRefreshRequest,
  AdminGithubSnapshotUpsert,
  AdminMediaFile,
  AdminNavigationItem,
  AdminNavigationItemUpsert,
  AdminProfile,
  AdminProfileUpdate,
  AdminProject,
  AdminProjectUpsert,
  AdminReferenceData,
  AdminSkillCategory,
  AdminSkillCategoryUpsert,
  AdminSkillOption,
  AdminSkillUpsert,
  AdminUser,
  AdminUserCreate,
  AdminUserUpdate,
} from '../models/admin.model';

@Injectable({ providedIn: 'root' })
export class AdminPortfolioApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = inject(API_BASE_URL);

  login(email: string, password: string): Observable<AdminAuthToken> {
    return this.http.post<AdminAuthToken>(`${this.apiBaseUrl}/admin/auth/login`, { email, password });
  }

  getCurrentAdmin(): Observable<AdminUser> {
    return this.http.get<AdminUser>(`${this.apiBaseUrl}/admin/auth/me`);
  }


  getAssistantKnowledgeStatus(): Observable<AdminAssistantKnowledgeStatus> {
    return this.http.get<AdminAssistantKnowledgeStatus>(`${this.apiBaseUrl}/admin/assistant/knowledge`);
  }

  rebuildAssistantKnowledge(): Observable<AdminAssistantKnowledgeStatus> {
    return this.http.post<AdminAssistantKnowledgeStatus>(`${this.apiBaseUrl}/admin/assistant/knowledge/rebuild`, {});
  }

  getDashboardSummary(): Observable<AdminDashboardSummary> {
    return this.http.get<AdminDashboardSummary>(`${this.apiBaseUrl}/admin/dashboard`);
  }

  getReferenceData(): Observable<AdminReferenceData> {
    return this.http.get<AdminReferenceData>(`${this.apiBaseUrl}/admin/reference-data`);
  }

  listMediaFiles(): Observable<AdminMediaFile[]> {
    return this.http.get<AdminMediaFile[]>(`${this.apiBaseUrl}/admin/media-files`);
  }

  uploadMedia(formData: FormData): Observable<AdminMediaFile> {
    return this.http.post<AdminMediaFile>(`${this.apiBaseUrl}/admin/media-files/upload`, formData);
  }

  listSkillCategories(): Observable<AdminSkillCategory[]> {
    return this.http.get<AdminSkillCategory[]>(`${this.apiBaseUrl}/admin/skill-categories`);
  }

  createSkillCategory(payload: AdminSkillCategoryUpsert): Observable<AdminSkillCategory> {
    return this.http.post<AdminSkillCategory>(`${this.apiBaseUrl}/admin/skill-categories`, payload);
  }

  updateSkillCategory(categoryId: string, payload: AdminSkillCategoryUpsert): Observable<AdminSkillCategory> {
    return this.http.put<AdminSkillCategory>(`${this.apiBaseUrl}/admin/skill-categories/${categoryId}`, payload);
  }

  deleteSkillCategory(categoryId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/skill-categories/${categoryId}`);
  }

  listSkills(): Observable<AdminSkillOption[]> {
    return this.http.get<AdminSkillOption[]>(`${this.apiBaseUrl}/admin/skills`);
  }

  createSkill(payload: AdminSkillUpsert): Observable<AdminSkillOption> {
    return this.http.post<AdminSkillOption>(`${this.apiBaseUrl}/admin/skills`, payload);
  }

  updateSkill(skillId: string, payload: AdminSkillUpsert): Observable<AdminSkillOption> {
    return this.http.put<AdminSkillOption>(`${this.apiBaseUrl}/admin/skills/${skillId}`, payload);
  }

  deleteSkill(skillId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/skills/${skillId}`);
  }

  listBlogTags(): Observable<AdminBlogTag[]> {
    return this.http.get<AdminBlogTag[]>(`${this.apiBaseUrl}/admin/blog-tags`);
  }

  createBlogTag(payload: AdminBlogTagUpsert): Observable<AdminBlogTag> {
    return this.http.post<AdminBlogTag>(`${this.apiBaseUrl}/admin/blog-tags`, payload);
  }

  updateBlogTag(tagId: string, payload: AdminBlogTagUpsert): Observable<AdminBlogTag> {
    return this.http.put<AdminBlogTag>(`${this.apiBaseUrl}/admin/blog-tags/${tagId}`, payload);
  }

  deleteBlogTag(tagId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/blog-tags/${tagId}`);
  }

  getProjects(): Observable<AdminCollectionResponse<AdminProject>> {
    return this.http.get<AdminCollectionResponse<AdminProject>>(`${this.apiBaseUrl}/admin/projects`);
  }

  createProject(payload: AdminProjectUpsert): Observable<AdminProject> {
    return this.http.post<AdminProject>(`${this.apiBaseUrl}/admin/projects`, payload);
  }

  updateProject(projectId: string, payload: AdminProjectUpsert): Observable<AdminProject> {
    return this.http.put<AdminProject>(`${this.apiBaseUrl}/admin/projects/${projectId}`, payload);
  }

  deleteProject(projectId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/projects/${projectId}`);
  }

  getBlogPosts(): Observable<AdminCollectionResponse<AdminBlogPost>> {
    return this.http.get<AdminCollectionResponse<AdminBlogPost>>(`${this.apiBaseUrl}/admin/blog-posts`);
  }

  createBlogPost(payload: AdminBlogPostUpsert): Observable<AdminBlogPost> {
    return this.http.post<AdminBlogPost>(`${this.apiBaseUrl}/admin/blog-posts`, payload);
  }

  updateBlogPost(postId: string, payload: AdminBlogPostUpsert): Observable<AdminBlogPost> {
    return this.http.put<AdminBlogPost>(`${this.apiBaseUrl}/admin/blog-posts/${postId}`, payload);
  }

  deleteBlogPost(postId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/blog-posts/${postId}`);
  }

  getExperiences(): Observable<AdminCollectionResponse<AdminExperience>> {
    return this.http.get<AdminCollectionResponse<AdminExperience>>(`${this.apiBaseUrl}/admin/experiences`);
  }

  createExperience(payload: AdminExperienceUpsert): Observable<AdminExperience> {
    return this.http.post<AdminExperience>(`${this.apiBaseUrl}/admin/experiences`, payload);
  }

  updateExperience(experienceId: string, payload: AdminExperienceUpsert): Observable<AdminExperience> {
    return this.http.put<AdminExperience>(`${this.apiBaseUrl}/admin/experiences/${experienceId}`, payload);
  }

  deleteExperience(experienceId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/experiences/${experienceId}`);
  }

  getNavigationItems(): Observable<AdminCollectionResponse<AdminNavigationItem>> {
    return this.http.get<AdminCollectionResponse<AdminNavigationItem>>(`${this.apiBaseUrl}/admin/navigation-items`);
  }

  createNavigationItem(payload: AdminNavigationItemUpsert): Observable<AdminNavigationItem> {
    return this.http.post<AdminNavigationItem>(`${this.apiBaseUrl}/admin/navigation-items`, payload);
  }

  updateNavigationItem(itemId: string, payload: AdminNavigationItemUpsert): Observable<AdminNavigationItem> {
    return this.http.put<AdminNavigationItem>(`${this.apiBaseUrl}/admin/navigation-items/${itemId}`, payload);
  }

  deleteNavigationItem(itemId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/navigation-items/${itemId}`);
  }

  getGithubSnapshots(): Observable<AdminCollectionResponse<AdminGithubSnapshot>> {
    return this.http.get<AdminCollectionResponse<AdminGithubSnapshot>>(`${this.apiBaseUrl}/admin/github-snapshots`);
  }

  createGithubSnapshot(payload: AdminGithubSnapshotUpsert): Observable<AdminGithubSnapshot> {
    return this.http.post<AdminGithubSnapshot>(`${this.apiBaseUrl}/admin/github-snapshots`, payload);
  }

  refreshGithubSnapshot(payload: AdminGithubSnapshotRefreshRequest): Observable<AdminGithubSnapshot> {
    return this.http.post<AdminGithubSnapshot>(`${this.apiBaseUrl}/admin/github-snapshots/refresh`, payload);
  }

  updateGithubSnapshot(snapshotId: string, payload: AdminGithubSnapshotUpsert): Observable<AdminGithubSnapshot> {
    return this.http.put<AdminGithubSnapshot>(`${this.apiBaseUrl}/admin/github-snapshots/${snapshotId}`, payload);
  }

  deleteGithubSnapshot(snapshotId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/github-snapshots/${snapshotId}`);
  }

  listAdminUsers(): Observable<AdminUser[]> {
    return this.http.get<AdminUser[]>(`${this.apiBaseUrl}/admin/admin-users`);
  }

  createAdminUser(payload: AdminUserCreate): Observable<AdminUser> {
    return this.http.post<AdminUser>(`${this.apiBaseUrl}/admin/admin-users`, payload);
  }

  updateAdminUser(adminUserId: string, payload: AdminUserUpdate): Observable<AdminUser> {
    return this.http.put<AdminUser>(`${this.apiBaseUrl}/admin/admin-users/${adminUserId}`, payload);
  }

  deleteAdminUser(adminUserId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiBaseUrl}/admin/admin-users/${adminUserId}`);
  }

  getProfile(): Observable<AdminProfile> {
    return this.http.get<AdminProfile>(`${this.apiBaseUrl}/admin/profile`);
  }

  updateProfile(payload: AdminProfileUpdate): Observable<AdminProfile> {
    return this.http.put<AdminProfile>(`${this.apiBaseUrl}/admin/profile`, payload);
  }

  getContactMessages(): Observable<AdminCollectionResponse<AdminContactMessage>> {
    return this.http.get<AdminCollectionResponse<AdminContactMessage>>(`${this.apiBaseUrl}/admin/contact-messages`);
  }

  updateContactMessage(messageId: string, isRead: boolean): Observable<AdminContactMessage> {
    return this.http.patch<AdminContactMessage>(`${this.apiBaseUrl}/admin/contact-messages/${messageId}`, { isRead });
  }
}
