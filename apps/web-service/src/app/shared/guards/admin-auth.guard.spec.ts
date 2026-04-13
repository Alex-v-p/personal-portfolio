import { TestBed } from '@angular/core/testing';
import { ActivatedRouteSnapshot, Router, RouterStateSnapshot, UrlTree, provideRouter } from '@angular/router';
import { beforeEach, describe, expect, it } from 'vitest';

import { adminAuthGuard, adminGuestGuard } from './admin-auth.guard';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';


const routeSnapshot = {} as ActivatedRouteSnapshot;
const stateSnapshot = { url: '/admin' } as RouterStateSnapshot;

function configureGuardTest(isAuthenticated: boolean): Router {
  TestBed.resetTestingModule();
  TestBed.configureTestingModule({
    providers: [
      provideRouter([]),
      {
        provide: AdminSessionService,
        useValue: {
          get isAuthenticated() {
            return isAuthenticated;
          },
        },
      },
    ],
  });

  return TestBed.inject(Router);
}

describe('adminAuthGuard', () => {
  beforeEach(() => {
    TestBed.resetTestingModule();
  });

  it('allows authenticated admins through', () => {
    configureGuardTest(true);

    const result = TestBed.runInInjectionContext(() => adminAuthGuard(routeSnapshot, stateSnapshot));

    expect(result).toBe(true);
  });

  it('redirects guests to the admin login page', () => {
    const router = configureGuardTest(false);

    const result = TestBed.runInInjectionContext(() => adminAuthGuard(routeSnapshot, stateSnapshot));

    expect(result instanceof UrlTree).toBe(true);
    expect(router.serializeUrl(result as UrlTree)).toBe('/admin/login');
  });
});

describe('adminGuestGuard', () => {
  it('allows guests to access the login page', () => {
    configureGuardTest(false);

    const result = TestBed.runInInjectionContext(() => adminGuestGuard(routeSnapshot, stateSnapshot));

    expect(result).toBe(true);
  });

  it('redirects authenticated admins away from the login page', () => {
    const router = configureGuardTest(true);

    const result = TestBed.runInInjectionContext(() => adminGuestGuard(routeSnapshot, stateSnapshot));

    expect(result instanceof UrlTree).toBe(true);
    expect(router.serializeUrl(result as UrlTree)).toBe('/admin');
  });
});
