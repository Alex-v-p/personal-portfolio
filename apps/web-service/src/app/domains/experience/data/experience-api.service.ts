import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Experience } from '@domains/experience/model/experience.model';
import { CollectionResponse } from '@core/http/public-api/common.contracts';
import { ExperienceApi } from '@core/http/public-api/experience.contracts';
import { normalizeExperienceList } from '@core/http/public-api/experience.mappers';
import { PublicHttpService } from '@core/http/public-api/public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicExperienceApiService {
  private readonly publicHttp = inject(PublicHttpService);

  getExperience(): Observable<Experience[]> {
    return this.publicHttp.http
      .get<CollectionResponse<ExperienceApi>>(`${this.publicHttp.apiBaseUrl}/public/experience`)
      .pipe(map((response) => normalizeExperienceList(response.items)));
  }
}
