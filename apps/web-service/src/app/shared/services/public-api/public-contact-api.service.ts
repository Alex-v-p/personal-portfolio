import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { ContactMessageCreatedResponse, ContactMessageDraft } from '../../models/contact-message.model';
import { PublicHttpService } from './public-http.service';

@Injectable({ providedIn: 'root' })
export class PublicContactApiService {
  private readonly publicHttp = inject(PublicHttpService);

  submitContactMessage(payload: ContactMessageDraft): Observable<ContactMessageCreatedResponse> {
    return this.publicHttp.http.post<ContactMessageCreatedResponse>(`${this.publicHttp.apiBaseUrl}/contact/messages`, payload);
  }
}
