import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../../core/config/api.config';
import {
  AdminAuthToken,
  AdminBlogPost,
  AdminBlogPostUpsert,
  AdminCollectionResponse,
  AdminContactMessage,
  AdminDashboardSummary,
  AdminMediaFile,
  AdminProfile,
  AdminProfileUpdate,
  AdminProject,
  AdminProjectUpsert,
  AdminReferenceData,
  AdminUser,
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

  getDashboardSummary(): Observable<AdminDashboardSummary> {
    return this.http.get<AdminDashboardSummary>(`${this.apiBaseUrl}/admin/dashboard`);
  }

  getReferenceData(): Observable<AdminReferenceData> {
    return this.http.get<AdminReferenceData>(`${this.apiBaseUrl}/admin/reference-data`);
  }

  uploadMedia(formData: FormData): Observable<AdminMediaFile> {
    return this.http.post<AdminMediaFile>(`${this.apiBaseUrl}/admin/media-files/upload`, formData);
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
