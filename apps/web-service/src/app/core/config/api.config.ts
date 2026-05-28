import { InjectionToken } from '@angular/core';

const resolveApiBaseUrl = (): string => '/api';

export const API_BASE_URL = new InjectionToken<string>('API_BASE_URL', {
  providedIn: 'root',
  factory: resolveApiBaseUrl
});
