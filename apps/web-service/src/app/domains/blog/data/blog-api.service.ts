import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { BlogPostDetail } from '@domains/blog/model/blog-post-detail.model';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { CollectionResponse } from '@core/http/public-api/common.contracts';
import { normalizeBlogPostDetail, normalizeBlogPostSummaries } from '@core/http/public-api/blog.mappers';
import { BlogPostDetailApi, BlogPostSummaryApi } from '@core/http/public-api/blog.contracts';
import { PublicHttpService } from '@core/http/public-api/public-http.service';
import { I18nService } from '@core/i18n/i18n.service';

@Injectable({ providedIn: 'root' })
export class PublicBlogApiService {
  private readonly publicHttp = inject(PublicHttpService);
  private readonly i18n = inject(I18nService);

  getBlogPosts(): Observable<BlogPostSummary[]> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:blog-posts:${locale}`, () =>
      this.publicHttp.http
        .get<CollectionResponse<BlogPostSummaryApi>>(`${this.publicHttp.apiBaseUrl}/public/blog-posts`)
        .pipe(map((response) => normalizeBlogPostSummaries(response.items, locale)))
    );
  }

  getBlogPostBySlug(slug: string): Observable<BlogPostDetail> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:blog-posts:${slug}:${locale}`, () =>
      this.publicHttp.http
        .get<BlogPostDetailApi>(`${this.publicHttp.apiBaseUrl}/public/blog-posts/${slug}`)
        .pipe(map((post) => normalizeBlogPostDetail(post, locale)))
    );
  }
}
