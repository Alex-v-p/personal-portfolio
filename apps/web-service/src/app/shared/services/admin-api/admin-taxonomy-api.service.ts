import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminBlogTag, AdminBlogTagUpsert, AdminSkillCategory, AdminSkillCategoryUpsert, AdminSkillOption, AdminSkillUpsert } from '../../models/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminTaxonomyApiService {
  private readonly adminHttp = inject(AdminHttpService);

  listSkillCategories(): Observable<AdminSkillCategory[]> {
    return this.adminHttp.http.get<AdminSkillCategory[]>(this.adminHttp.adminUrl('skill-categories'));
  }

  createSkillCategory(payload: AdminSkillCategoryUpsert): Observable<AdminSkillCategory> {
    return this.adminHttp.http.post<AdminSkillCategory>(this.adminHttp.adminUrl('skill-categories'), payload);
  }

  updateSkillCategory(categoryId: string, payload: AdminSkillCategoryUpsert): Observable<AdminSkillCategory> {
    return this.adminHttp.http.put<AdminSkillCategory>(this.adminHttp.adminUrl(`skill-categories/${categoryId}`), payload);
  }

  deleteSkillCategory(categoryId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`skill-categories/${categoryId}`));
  }

  listSkills(): Observable<AdminSkillOption[]> {
    return this.adminHttp.http.get<AdminSkillOption[]>(this.adminHttp.adminUrl('skills'));
  }

  createSkill(payload: AdminSkillUpsert): Observable<AdminSkillOption> {
    return this.adminHttp.http.post<AdminSkillOption>(this.adminHttp.adminUrl('skills'), payload);
  }

  updateSkill(skillId: string, payload: AdminSkillUpsert): Observable<AdminSkillOption> {
    return this.adminHttp.http.put<AdminSkillOption>(this.adminHttp.adminUrl(`skills/${skillId}`), payload);
  }

  deleteSkill(skillId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`skills/${skillId}`));
  }

  listBlogTags(): Observable<AdminBlogTag[]> {
    return this.adminHttp.http.get<AdminBlogTag[]>(this.adminHttp.adminUrl('blog-tags'));
  }

  createBlogTag(payload: AdminBlogTagUpsert): Observable<AdminBlogTag> {
    return this.adminHttp.http.post<AdminBlogTag>(this.adminHttp.adminUrl('blog-tags'), payload);
  }

  updateBlogTag(tagId: string, payload: AdminBlogTagUpsert): Observable<AdminBlogTag> {
    return this.adminHttp.http.put<AdminBlogTag>(this.adminHttp.adminUrl(`blog-tags/${tagId}`), payload);
  }

  deleteBlogTag(tagId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`blog-tags/${tagId}`));
  }
}
