import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

import { API_BASE_URL } from '../../core/config/api.config';

export const adminAuthInterceptor: HttpInterceptorFn = (request, next) => {
  const apiBaseUrl = inject(API_BASE_URL);
  const token = typeof localStorage === 'undefined' ? null : localStorage.getItem('portfolio.admin.access-token');

  if (!token || !request.url.startsWith(`${apiBaseUrl}/admin`)) {
    return next(request);
  }

  return next(
    request.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    })
  );
};
