import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { SiteEventCreatePayload } from '../../models/site-event.model';
import { PublicHttpService } from './public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicEventsApiService {
  private readonly publicHttp = inject(PublicHttpService);

  createSiteEvent(payload: SiteEventCreatePayload): Observable<{ message: string; eventId: string }> {
    return this.publicHttp.http.post<{ message: string; eventId: string }>(`${this.publicHttp.apiBaseUrl}/events`, payload);
  }
}
