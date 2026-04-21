import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ProjectDetail } from '@domains/projects/model/project-detail.model';
import { ProjectSummary } from '@domains/projects/model/project-summary.model';
import { CollectionResponse } from '@core/http/public-api/common.contracts';
import { normalizeProjectDetail, normalizeProjectSummaries } from '@core/http/public-api/projects.mappers';
import { ProjectDetailApi, ProjectSummaryApi } from '@core/http/public-api/projects.contracts';
import { PublicHttpService } from '@core/http/public-api/public-http.service';
import { I18nService } from '@core/i18n/i18n.service';

@Injectable({ providedIn: 'root' })
export class PublicProjectsApiService {
  private readonly publicHttp = inject(PublicHttpService);
  private readonly i18n = inject(I18nService);

  getProjects(): Observable<ProjectSummary[]> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:projects:${locale}`, () =>
      this.publicHttp.http
        .get<CollectionResponse<ProjectSummaryApi>>(`${this.publicHttp.apiBaseUrl}/public/projects`, { params: this.publicHttp.localeParams(locale) })
        .pipe(map((response) => normalizeProjectSummaries(response.items, locale)))
    );
  }

  getProjectBySlug(slug: string): Observable<ProjectDetail> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:projects:${slug}:${locale}`, () =>
      this.publicHttp.http
        .get<ProjectDetailApi>(`${this.publicHttp.apiBaseUrl}/public/projects/${slug}`, { params: this.publicHttp.localeParams(locale) })
        .pipe(map((project) => normalizeProjectDetail(project, locale)))
    );
  }
}
