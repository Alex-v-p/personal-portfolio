import { inject } from '@angular/core';
import { CanActivateFn, Router, UrlTree } from '@angular/router';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { AdminSessionService } from '@domains/admin/data/admin-session.service';

function requireAuthenticatedAdmin(): Observable<boolean | UrlTree> | boolean | UrlTree {
  const session = inject(AdminSessionService);
  const router = inject(Router);

  if (session.isFullyAuthenticated) {
    return true;
  }
  if (session.hasPendingMfaStep) {
    return router.createUrlTree(['/admin/mfa']);
  }

  return session.restoreSession().pipe(
    map((authSession) => {
      if (!authSession) {
        return router.createUrlTree(['/admin/login']);
      }
      return session.hasPendingMfaStep ? router.createUrlTree(['/admin/mfa']) : true;
    }),
    catchError(() => of(router.createUrlTree(['/admin/login']))),
  );
}

function requireGuestAdmin(): Observable<boolean | UrlTree> | boolean | UrlTree {
  const session = inject(AdminSessionService);
  const router = inject(Router);

  if (session.isFullyAuthenticated) {
    return router.createUrlTree(['/admin']);
  }
  if (session.hasPendingMfaStep) {
    return router.createUrlTree(['/admin/mfa']);
  }

  return session.restoreSession().pipe(
    map((authSession) => {
      if (!authSession) {
        return true;
      }
      return session.hasPendingMfaStep ? router.createUrlTree(['/admin/mfa']) : router.createUrlTree(['/admin']);
    }),
    catchError(() => of(true)),
  );
}

function requirePendingAdminMfa(): Observable<boolean | UrlTree> | boolean | UrlTree {
  const session = inject(AdminSessionService);
  const router = inject(Router);

  if (session.hasPendingMfaStep) {
    return true;
  }
  if (session.isFullyAuthenticated) {
    return router.createUrlTree(['/admin']);
  }

  return session.restoreSession().pipe(
    map((authSession) => {
      if (!authSession) {
        return router.createUrlTree(['/admin/login']);
      }
      return session.hasPendingMfaStep ? true : router.createUrlTree(['/admin']);
    }),
    catchError(() => of(router.createUrlTree(['/admin/login']))),
  );
}

export const adminAuthGuard: CanActivateFn = () => requireAuthenticatedAdmin();
export const adminGuestGuard: CanActivateFn = () => requireGuestAdmin();
export const adminMfaGuard: CanActivateFn = () => requirePendingAdminMfa();
