import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { API_BASE_URL } from '../../core/config/api.config';

const ADMIN_CSRF_HEADER = 'X-Portfolio-CSRF';
const MUTATING_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

export const adminAuthInterceptor: HttpInterceptorFn = (request, next) => {
  const apiBaseUrl = inject(API_BASE_URL);
  const adminSession = inject(AdminSessionService);

  if (!request.url.startsWith(`${apiBaseUrl}/admin`)) {
    return next(request);
  }

  const setHeaders: Record<string, string> = {};
  if (MUTATING_METHODS.has(request.method.toUpperCase()) && adminSession.csrfToken) {
    setHeaders[ADMIN_CSRF_HEADER] = adminSession.csrfToken;
  }

  return next(
    request.clone({
      withCredentials: true,
      setHeaders,
    })
  );
};
