import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Profile } from '../../models/profile.model';
import { NavigationItem, SiteShellData } from '../../models/site-shell.model';
import { HomePageData } from '../../models/home.model';
import { CollectionResponse, NavigationItemApi, ProfileApi, SiteShellApi, HomeApi } from './public-api.contracts';
import { normalizeHome, normalizeNavigationItem, normalizeProfile, normalizeSiteShell } from './public-api.mappers';
import { PublicHttpService } from './public-http.service';

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
