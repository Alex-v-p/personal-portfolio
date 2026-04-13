import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { GithubSnapshot } from '../../models/github-snapshot.model';
import { StatsPageData } from '../../models/stats-page.model';
import { GithubSnapshotApi, StatsApi } from './public-api.contracts';
import { normalizeGithubSnapshot, normalizeStats } from './public-api.mappers';
import { PublicHttpService } from './public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicStatsApiService {
  private readonly publicHttp = inject(PublicHttpService);

  getGithubSnapshot(): Observable<GithubSnapshot> {
    return this.publicHttp.http
      .get<GithubSnapshotApi>(`${this.publicHttp.apiBaseUrl}/public/github`)
      .pipe(map((snapshot) => normalizeGithubSnapshot(snapshot)));
  }

  getStats(): Observable<StatsPageData> {
    return this.publicHttp.http
      .get<StatsApi>(`${this.publicHttp.apiBaseUrl}/public/stats`)
      .pipe(map((stats) => normalizeStats(stats)));
  }
}
