import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminBlogPost, AdminBlogPostUpsert, AdminCollectionResponse, AdminExperience, AdminExperienceUpsert, AdminNavigationItem, AdminNavigationItemUpsert, AdminProject, AdminProjectUpsert } from '@domains/admin/model/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminContentApiService {
  private readonly adminHttp = inject(AdminHttpService);

  getProjects(): Observable<AdminCollectionResponse<AdminProject>> {
    return this.adminHttp.http.get<AdminCollectionResponse<AdminProject>>(this.adminHttp.adminUrl('projects'));
  }

  createProject(payload: AdminProjectUpsert): Observable<AdminProject> {
    return this.adminHttp.http.post<AdminProject>(this.adminHttp.adminUrl('projects'), payload);
  }

  updateProject(projectId: string, payload: AdminProjectUpsert): Observable<AdminProject> {
    return this.adminHttp.http.put<AdminProject>(this.adminHttp.adminUrl(`projects/${projectId}`), payload);
  }

  deleteProject(projectId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`projects/${projectId}`));
  }

  getBlogPosts(): Observable<AdminCollectionResponse<AdminBlogPost>> {
    return this.adminHttp.http.get<AdminCollectionResponse<AdminBlogPost>>(this.adminHttp.adminUrl('blog-posts'));
  }

  createBlogPost(payload: AdminBlogPostUpsert): Observable<AdminBlogPost> {
    return this.adminHttp.http.post<AdminBlogPost>(this.adminHttp.adminUrl('blog-posts'), payload);
  }

  updateBlogPost(postId: string, payload: AdminBlogPostUpsert): Observable<AdminBlogPost> {
    return this.adminHttp.http.put<AdminBlogPost>(this.adminHttp.adminUrl(`blog-posts/${postId}`), payload);
  }

  deleteBlogPost(postId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`blog-posts/${postId}`));
  }

  getExperiences(): Observable<AdminCollectionResponse<AdminExperience>> {
    return this.adminHttp.http.get<AdminCollectionResponse<AdminExperience>>(this.adminHttp.adminUrl('experiences'));
  }

  createExperience(payload: AdminExperienceUpsert): Observable<AdminExperience> {
    return this.adminHttp.http.post<AdminExperience>(this.adminHttp.adminUrl('experiences'), payload);
  }

  updateExperience(experienceId: string, payload: AdminExperienceUpsert): Observable<AdminExperience> {
    return this.adminHttp.http.put<AdminExperience>(this.adminHttp.adminUrl(`experiences/${experienceId}`), payload);
  }

  deleteExperience(experienceId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`experiences/${experienceId}`));
  }

  getNavigationItems(): Observable<AdminCollectionResponse<AdminNavigationItem>> {
    return this.adminHttp.http.get<AdminCollectionResponse<AdminNavigationItem>>(this.adminHttp.adminUrl('navigation-items'));
  }

  createNavigationItem(payload: AdminNavigationItemUpsert): Observable<AdminNavigationItem> {
    return this.adminHttp.http.post<AdminNavigationItem>(this.adminHttp.adminUrl('navigation-items'), payload);
  }

  updateNavigationItem(itemId: string, payload: AdminNavigationItemUpsert): Observable<AdminNavigationItem> {
    return this.adminHttp.http.put<AdminNavigationItem>(this.adminHttp.adminUrl(`navigation-items/${itemId}`), payload);
  }

  deleteNavigationItem(itemId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`navigation-items/${itemId}`));
  }
}
