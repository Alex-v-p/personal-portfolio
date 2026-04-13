import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { BlogPostDetail } from '../../models/blog-post-detail.model';
import { BlogPostSummary } from '../../models/blog-post-summary.model';
import { BlogPostDetailApi, BlogPostSummaryApi, CollectionResponse } from './public-api.contracts';
import { normalizeBlogPostDetail, normalizeBlogPostSummaries } from './public-api.mappers';
import { PublicHttpService } from './public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicBlogApiService {
  private readonly publicHttp = inject(PublicHttpService);

  getBlogPosts(): Observable<BlogPostSummary[]> {
    return this.publicHttp.http
      .get<CollectionResponse<BlogPostSummaryApi>>(`${this.publicHttp.apiBaseUrl}/public/blog-posts`)
      .pipe(map((response) => normalizeBlogPostSummaries(response.items)));
  }

  getBlogPostBySlug(slug: string): Observable<BlogPostDetail> {
    return this.publicHttp.http
      .get<BlogPostDetailApi>(`${this.publicHttp.apiBaseUrl}/public/blog-posts/${slug}`)
      .pipe(map((post) => normalizeBlogPostDetail(post)));
  }
}
