import { InjectionToken } from '@angular/core';

const resolveApiBaseUrl = (): string => {
  if (typeof window === 'undefined') {
    return 'http://localhost:8001/api';
  }

  const { hostname, protocol } = window.location;

  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return `${protocol}//${hostname}:8001/api`;
  }

  return '/api';
};

export const API_BASE_URL = new InjectionToken<string>('API_BASE_URL', {
  providedIn: 'root',
  factory: resolveApiBaseUrl
});
