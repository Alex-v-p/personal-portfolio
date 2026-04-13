import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { GithubSnapshot } from '@domains/stats/model/github-snapshot.model';
import { StatsPageData } from '@domains/stats/model/stats-page.model';
import { GithubSnapshotApi, StatsApi } from '@core/http/public-api/public-api.contracts';
import { normalizeGithubSnapshot, normalizeStats } from '@core/http/public-api/public-api.mappers';
import { PublicHttpService } from '@core/http/public-api/public-http.service';

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
