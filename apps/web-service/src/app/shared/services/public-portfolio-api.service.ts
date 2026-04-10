import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { API_BASE_URL } from '../../core/config/api.config';
import { BlogPost } from '../models/blog-post.model';
import { ContactMessageCreatedResponse, ContactMessageDraft } from '../models/contact-message.model';
import { Profile } from '../models/profile.model';
import { Project } from '../models/project.model';

interface CollectionResponse<T> {
  items?: T[] | null;
  total?: number;
}

@Injectable({ providedIn: 'root' })
export class PublicPortfolioApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = inject(API_BASE_URL);

  getProfile(): Observable<Profile> {
    return this.http.get<Profile>(`${this.apiBaseUrl}/public/profile`);
  }

  getProjects(): Observable<Project[]> {
    return this.http
      .get<CollectionResponse<Project>>(`${this.apiBaseUrl}/public/projects`)
      .pipe(map((response) => this.normalizeProjects(response.items)));
  }

  getBlogPosts(): Observable<BlogPost[]> {
    return this.http
      .get<CollectionResponse<BlogPost>>(`${this.apiBaseUrl}/public/blog-posts`)
      .pipe(map((response) => this.normalizeBlogPosts(response.items)));
  }

  getBlogPostBySlug(slug: string): Observable<BlogPost> {
    return this.http.get<BlogPost>(`${this.apiBaseUrl}/public/blog-posts/${slug}`).pipe(map((post) => this.normalizeBlogPost(post)));
  }

  submitContactMessage(payload: ContactMessageDraft): Observable<ContactMessageCreatedResponse> {
    return this.http.post<ContactMessageCreatedResponse>(`${this.apiBaseUrl}/contact/messages`, payload);
  }

  private normalizeProjects(items: Project[] | null | undefined): Project[] {
    if (!Array.isArray(items)) {
      return [];
    }

    return items.map((project) => this.normalizeProject(project));
  }

  private normalizeProject(project: Project): Project {
    return {
      ...project,
      teaser: project.teaser ?? project.shortDescription ?? '',
      shortDescription: project.shortDescription ?? project.teaser ?? '',
      summary: project.summary ?? '',
      descriptionMarkdown: project.descriptionMarkdown ?? undefined,
      organization: project.organization ?? '',
      duration: project.duration ?? project.durationLabel ?? '',
      durationLabel: project.durationLabel ?? project.duration ?? '',
      status: project.status ?? '',
      category: project.category ?? '',
      tags: Array.isArray(project.tags) ? project.tags : [],
      featured: !!project.featured,
      isFeatured: project.isFeatured ?? !!project.featured,
      imageAlt: project.imageAlt ?? project.coverImageAlt ?? 'Project cover placeholder',
      coverImageAlt: project.coverImageAlt ?? project.imageAlt ?? 'Project cover placeholder',
      coverImageFileId: project.coverImageFileId ?? null,
      coverImageUrl: project.coverImageUrl ?? undefined,
      highlight: project.highlight ?? project.summary ?? '',
      githubUrl: project.githubUrl ?? undefined,
      githubRepoName: project.githubRepoName ?? undefined,
      demoUrl: project.demoUrl ?? undefined,
      startedOn: project.startedOn ?? null,
      endedOn: project.endedOn ?? null,
      publishedAt: project.publishedAt ?? null,
      sortOrder: typeof project.sortOrder === 'number' ? project.sortOrder : Number.MAX_SAFE_INTEGER,
      links: Array.isArray(project.links)
        ? project.links.map((link) => ({
            label: link.label ?? 'Open',
            href: link.href ?? undefined,
            routerLink: link.routerLink ?? undefined
          }))
        : []
    };
  }

  private normalizeBlogPosts(items: BlogPost[] | null | undefined): BlogPost[] {
    if (!Array.isArray(items)) {
      return [];
    }

    return items.map((post) => this.normalizeBlogPost(post));
  }

  private normalizeBlogPost(post: BlogPost): BlogPost {
    return {
      ...post,
      excerpt: post.excerpt ?? '',
      publishedAt: post.publishedAt ?? '',
      readTime: post.readTime ?? `${post.readingTimeMinutes ?? 0} min read`,
      readingTimeMinutes: typeof post.readingTimeMinutes === 'number' ? post.readingTimeMinutes : 0,
      category: post.category ?? 'General',
      tags: Array.isArray(post.tags) ? post.tags : [],
      featured: !!post.featured,
      isFeatured: post.isFeatured ?? !!post.featured,
      coverAlt: post.coverAlt ?? post.coverImageAlt ?? 'Blog post cover placeholder',
      coverImageAlt: post.coverImageAlt ?? post.coverAlt ?? 'Blog post cover placeholder',
      coverImageFileId: post.coverImageFileId ?? null,
      coverImageUrl: post.coverImageUrl ?? undefined,
      contentMarkdown: post.contentMarkdown ?? '',
      seoTitle: post.seoTitle ?? undefined,
      seoDescription: post.seoDescription ?? undefined
    };
  }
}
