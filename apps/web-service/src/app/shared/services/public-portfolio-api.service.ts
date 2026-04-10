import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { API_BASE_URL } from '../../core/config/api.config';
import { BlogPost } from '../models/blog-post.model';
import { Profile } from '../models/profile.model';
import { Project } from '../models/project.model';

interface CollectionResponse<T> {
  items: T[];
  total: number;
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
      .pipe(map((response) => response.items));
  }

  getBlogPosts(): Observable<BlogPost[]> {
    return this.http
      .get<CollectionResponse<BlogPost>>(`${this.apiBaseUrl}/public/blog-posts`)
      .pipe(map((response) => response.items));
  }

  getBlogPostBySlug(slug: string): Observable<BlogPost> {
    return this.http.get<BlogPost>(`${this.apiBaseUrl}/public/blog-posts/${slug}`);
  }
}
