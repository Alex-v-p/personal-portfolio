import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Experience } from '@domains/experience/model/experience.model';
import { CollectionResponse } from '@core/http/public-api/common.contracts';
import { normalizeExperienceList } from '@core/http/public-api/experience.mappers';
import { ExperienceApi } from '@core/http/public-api/experience.contracts';
import { PublicHttpService } from '@core/http/public-api/public-http.service';
import { I18nService } from '@core/i18n/i18n.service';

@Injectable({ providedIn: 'root' })
export class PublicExperienceApiService {
  private readonly publicHttp = inject(PublicHttpService);
  private readonly i18n = inject(I18nService);

  getExperience(): Observable<Experience[]> {
    const locale = this.i18n.currentLocale();

    return this.publicHttp.cacheRequest(`public:experience:${locale}`, () =>
      this.publicHttp.http
        .get<CollectionResponse<ExperienceApi>>(`${this.publicHttp.apiBaseUrl}/public/experience`)
        .pipe(map((response) => normalizeExperienceList(response.items, locale)))
    );
  }
}
