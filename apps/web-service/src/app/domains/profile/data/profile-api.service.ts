import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { HomePageData } from '@domains/home/model/home.model';
import { Profile } from '@domains/profile/model/profile.model';
import { NavigationItem, SiteShellData } from '@domains/profile/model/site-shell.model';
import { CollectionResponse } from '@core/http/public-api/common.contracts';
import { HomeApi } from '@core/http/public-api/home.contracts';
import { normalizeHome } from '@core/http/public-api/home.mappers';
import { normalizeNavigationItem, normalizeProfile, normalizeSiteShell } from '@core/http/public-api/profile.mappers';
import { NavigationItemApi, ProfileApi, SiteShellApi } from '@core/http/public-api/profile.contracts';
import { PublicHttpService } from '@core/http/public-api/public-http.service';
import { I18nService } from '@core/i18n/i18n.service';

@Injectable({ providedIn: 'root' })
export class PublicProfileApiService {
  private readonly publicHttp = inject(PublicHttpService);
  private readonly i18n = inject(I18nService);

  getProfile(): Observable<Profile> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:profile:${locale}`, () =>
      this.publicHttp.http
        .get<ProfileApi>(`${this.publicHttp.apiBaseUrl}/public/profile`, { params: this.publicHttp.localeParams(locale) })
        .pipe(map((profile) => normalizeProfile(profile)))
    );
  }

  getNavigation(): Observable<NavigationItem[]> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:navigation:${locale}`, () =>
      this.publicHttp.http
        .get<CollectionResponse<NavigationItemApi>>(`${this.publicHttp.apiBaseUrl}/public/navigation`, { params: this.publicHttp.localeParams(locale) })
        .pipe(map((response) => (response.items ?? []).map((item) => normalizeNavigationItem(item))))
    );
  }

  getSiteShell(): Observable<SiteShellData> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:site-shell:${locale}`, () =>
      this.publicHttp.http
        .get<SiteShellApi>(`${this.publicHttp.apiBaseUrl}/public/site-shell`, { params: this.publicHttp.localeParams(locale) })
        .pipe(map((shell) => normalizeSiteShell(shell)))
    );
  }

  getHome(): Observable<HomePageData> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:home:${locale}`, () =>
      this.publicHttp.http
        .get<HomeApi>(`${this.publicHttp.apiBaseUrl}/public/home`, { params: this.publicHttp.localeParams(locale) })
        .pipe(map((home) => normalizeHome(home, locale)))
    );
  }
}
