import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Profile } from '@domains/profile/model/profile.model';
import { NavigationItem, SiteShellData } from '@domains/profile/model/site-shell.model';
import { HomePageData } from '@domains/home/model/home.model';
import { CollectionResponse } from '@core/http/public-api/common.contracts';
import { HomeApi } from '@core/http/public-api/home.contracts';
import { NavigationItemApi, ProfileApi, SiteShellApi } from '@core/http/public-api/profile.contracts';
import { normalizeHome } from '@core/http/public-api/home.mappers';
import { normalizeNavigationItem, normalizeProfile, normalizeSiteShell } from '@core/http/public-api/profile.mappers';
import { PublicHttpService } from '@core/http/public-api/public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicProfileApiService {
  private readonly publicHttp = inject(PublicHttpService);

  getProfile(): Observable<Profile> {
    return this.publicHttp.http.get<ProfileApi>(`${this.publicHttp.apiBaseUrl}/public/profile`).pipe(map((profile) => normalizeProfile(profile)));
  }

  getNavigation(): Observable<NavigationItem[]> {
    return this.publicHttp.http
      .get<CollectionResponse<NavigationItemApi>>(`${this.publicHttp.apiBaseUrl}/public/navigation`)
      .pipe(map((response) => (response.items ?? []).map((item) => normalizeNavigationItem(item))));
  }

  getSiteShell(): Observable<SiteShellData> {
    return this.publicHttp.http.get<SiteShellApi>(`${this.publicHttp.apiBaseUrl}/public/site-shell`).pipe(map((shell) => normalizeSiteShell(shell)));
  }

  getHome(): Observable<HomePageData> {
    return this.publicHttp.http.get<HomeApi>(`${this.publicHttp.apiBaseUrl}/public/home`).pipe(map((home) => normalizeHome(home)));
  }
}
