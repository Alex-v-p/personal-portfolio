import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Experience } from '../../models/experience.model';
import { CollectionResponse, ExperienceApi } from './public-api.contracts';
import { normalizeExperienceList } from './public-api.mappers';
import { PublicHttpService } from './public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicExperienceApiService {
  private readonly publicHttp = inject(PublicHttpService);

  getExperience(): Observable<Experience[]> {
    return this.publicHttp.http
      .get<CollectionResponse<ExperienceApi>>(`${this.publicHttp.apiBaseUrl}/public/experience`)
      .pipe(map((response) => normalizeExperienceList(response.items)));
  }
}
