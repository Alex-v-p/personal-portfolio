import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { BlogPostDetail } from '@domains/blog/model/blog-post-detail.model';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { CollectionResponse } from '@core/http/public-api/common.contracts';
import { BlogPostDetailApi, BlogPostSummaryApi } from '@core/http/public-api/blog.contracts';
import { normalizeBlogPostDetail, normalizeBlogPostSummaries } from '@core/http/public-api/blog.mappers';
import { PublicHttpService } from '@core/http/public-api/public-http.service';

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
