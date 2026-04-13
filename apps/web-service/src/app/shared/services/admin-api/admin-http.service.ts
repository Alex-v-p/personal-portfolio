import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { API_BASE_URL } from '../../../core/config/api.config';

@Injectable({ providedIn: 'root' })
export class AdminHttpService {
  readonly http = inject(HttpClient);
  readonly apiBaseUrl = inject(API_BASE_URL);

  adminUrl(path: string): string {
    return `${this.apiBaseUrl}/admin/${path}`;
  }
}
