import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ProjectDetail } from '../../models/project-detail.model';
import { ProjectSummary } from '../../models/project-summary.model';
import { CollectionResponse, ProjectDetailApi, ProjectSummaryApi } from './public-api.contracts';
import { normalizeProjectDetail, normalizeProjectSummaries } from './public-api.mappers';
import { PublicHttpService } from './public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicProjectsApiService {
  private readonly publicHttp = inject(PublicHttpService);

  getProjects(): Observable<ProjectSummary[]> {
    return this.publicHttp.http
      .get<CollectionResponse<ProjectSummaryApi>>(`${this.publicHttp.apiBaseUrl}/public/projects`)
      .pipe(map((response) => normalizeProjectSummaries(response.items)));
  }

  getProjectBySlug(slug: string): Observable<ProjectDetail> {
    return this.publicHttp.http
      .get<ProjectDetailApi>(`${this.publicHttp.apiBaseUrl}/public/projects/${slug}`)
      .pipe(map((project) => normalizeProjectDetail(project)));
  }
}
