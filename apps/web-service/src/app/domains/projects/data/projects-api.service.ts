import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ProjectDetail } from '@domains/projects/model/project-detail.model';
import { ProjectSummary } from '@domains/projects/model/project-summary.model';
import { CollectionResponse } from '@core/http/public-api/common.contracts';
import { ProjectDetailApi, ProjectSummaryApi } from '@core/http/public-api/projects.contracts';
import { normalizeProjectDetail, normalizeProjectSummaries } from '@core/http/public-api/projects.mappers';
import { PublicHttpService } from '@core/http/public-api/public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicProjectsApiService {
  private readonly publicHttp = inject(PublicHttpService);

  getProjects(): Observable<ProjectSummary[]> {
    return this.publicHttp.cacheRequest('public:projects', () =>
      this.publicHttp.http
        .get<CollectionResponse<ProjectSummaryApi>>(`${this.publicHttp.apiBaseUrl}/public/projects`)
        .pipe(map((response) => normalizeProjectSummaries(response.items)))
    );
  }

  getProjectBySlug(slug: string): Observable<ProjectDetail> {
    return this.publicHttp.cacheRequest(`public:projects:${slug}`, () =>
      this.publicHttp.http
        .get<ProjectDetailApi>(`${this.publicHttp.apiBaseUrl}/public/projects/${slug}`)
        .pipe(map((project) => normalizeProjectDetail(project)))
    );
  }
}
