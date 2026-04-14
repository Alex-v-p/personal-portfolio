import { inject } from '@angular/core';
import { CanActivateFn, Router, UrlTree } from '@angular/router';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { AdminSessionService } from '@domains/admin/data/admin-session.service';

function requireAuthenticatedAdmin(): Observable<boolean | UrlTree> | boolean | UrlTree {
  const session = inject(AdminSessionService);
  const router = inject(Router);

  if (session.isAuthenticated) {
    return true;
  }

  return session.restoreSession().pipe(
    map((user) => (user ? true : router.createUrlTree(['/admin/login']))),
    catchError(() => of(router.createUrlTree(['/admin/login'])))
  );
}

function requireGuestAdmin(): Observable<boolean | UrlTree> | boolean | UrlTree {
  const session = inject(AdminSessionService);
  const router = inject(Router);

  if (session.isAuthenticated) {
    return router.createUrlTree(['/admin']);
  }

  return session.restoreSession().pipe(
    map((user) => (user ? router.createUrlTree(['/admin']) : true)),
    catchError(() => of(true))
  );
}

export const adminAuthGuard: CanActivateFn = () => requireAuthenticatedAdmin();
export const adminGuestGuard: CanActivateFn = () => requireGuestAdmin();
