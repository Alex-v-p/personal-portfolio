import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';

import { API_BASE_URL } from '../../../core/config/api.config';

@Injectable({ providedIn: 'root' })
export class PublicHttpService {
  readonly http = inject(HttpClient);
  readonly apiBaseUrl = inject(API_BASE_URL);
}
