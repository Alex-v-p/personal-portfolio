import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { GithubSnapshot } from '@domains/stats/model/github-snapshot.model';
import { StatsPageData } from '@domains/stats/model/stats-page.model';
import { GithubSnapshotApi, StatsApi } from '@core/http/public-api/stats.contracts';
import { normalizeGithubSnapshot, normalizeStats } from '@core/http/public-api/stats.mappers';
import { PublicHttpService } from '@core/http/public-api/public-http.service';
import { I18nService } from '@core/i18n/i18n.service';

@Injectable({ providedIn: 'root' })
export class PublicStatsApiService {
  private readonly publicHttp = inject(PublicHttpService);
  private readonly i18n = inject(I18nService);

  getGithubSnapshot(): Observable<GithubSnapshot> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:github-snapshot:${locale}`, () =>
      this.publicHttp.http
        .get<GithubSnapshotApi>(`${this.publicHttp.apiBaseUrl}/public/github`, { params: this.publicHttp.localeParams(locale) })
        .pipe(map((snapshot) => normalizeGithubSnapshot(snapshot)))
    );
  }

  getStats(): Observable<StatsPageData> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:stats:${locale}`, () =>
      this.publicHttp.http
        .get<StatsApi>(`${this.publicHttp.apiBaseUrl}/public/stats`, { params: this.publicHttp.localeParams(locale) })
        .pipe(map((stats) => normalizeStats(stats)))
    );
  }
}
