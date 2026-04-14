import { TestBed } from '@angular/core/testing';
import { ActivatedRouteSnapshot, Router, RouterStateSnapshot, UrlTree, provideRouter } from '@angular/router';
import { firstValueFrom, of } from 'rxjs';
import { beforeEach, describe, expect, it } from 'vitest';

import { adminAuthGuard, adminGuestGuard, adminMfaGuard } from './admin-auth.guard';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';

const routeSnapshot = {} as ActivatedRouteSnapshot;
const stateSnapshot = { url: '/admin' } as RouterStateSnapshot;

function configureGuardTest(options: { isFullyAuthenticated: boolean; hasPendingMfaStep?: boolean; restoreSession?: object | null }): Router {
  TestBed.resetTestingModule();
  TestBed.configureTestingModule({
    providers: [
      provideRouter([]),
      {
        provide: AdminSessionService,
        useValue: {
          get isFullyAuthenticated() {
            return options.isFullyAuthenticated;
          },
          get hasPendingMfaStep() {
            return options.hasPendingMfaStep ?? false;
          },
          restoreSession: () => of(options.restoreSession ?? null),
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

  it('allows fully authenticated admins through', () => {
    configureGuardTest({ isFullyAuthenticated: true });

    const result = TestBed.runInInjectionContext(() => adminAuthGuard(routeSnapshot, stateSnapshot));

    expect(result).toBe(true);
  });

  it('redirects partially authenticated admins to the MFA page', () => {
    const router = configureGuardTest({ isFullyAuthenticated: false, hasPendingMfaStep: true });

    const result = TestBed.runInInjectionContext(() => adminAuthGuard(routeSnapshot, stateSnapshot));

    expect(result instanceof UrlTree).toBe(true);
    expect(router.serializeUrl(result as UrlTree)).toBe('/admin/mfa');
  });

  it('restores the session for admins with a valid cookie-backed session', async () => {
    configureGuardTest({ isFullyAuthenticated: false, restoreSession: { user: { email: 'admin@example.com' } } });

    const result = TestBed.runInInjectionContext(() => adminAuthGuard(routeSnapshot, stateSnapshot));

    expect(await firstValueFrom(result as any)).toBe(true);
  });

  it('redirects guests to the admin login page', async () => {
    const router = configureGuardTest({ isFullyAuthenticated: false, restoreSession: null });

    const result = TestBed.runInInjectionContext(() => adminAuthGuard(routeSnapshot, stateSnapshot));
    const resolved = await firstValueFrom(result as any);

    expect(resolved instanceof UrlTree).toBe(true);
    expect(router.serializeUrl(resolved as UrlTree)).toBe('/admin/login');
  });
});

describe('adminGuestGuard', () => {
  it('allows guests to access the login page', async () => {
    configureGuardTest({ isFullyAuthenticated: false, restoreSession: null });

    const result = TestBed.runInInjectionContext(() => adminGuestGuard(routeSnapshot, stateSnapshot));

    expect(await firstValueFrom(result as any)).toBe(true);
  });

  it('redirects partially authenticated admins to the MFA page', () => {
    const router = configureGuardTest({ isFullyAuthenticated: false, hasPendingMfaStep: true });

    const result = TestBed.runInInjectionContext(() => adminGuestGuard(routeSnapshot, stateSnapshot));

    expect(result instanceof UrlTree).toBe(true);
    expect(router.serializeUrl(result as UrlTree)).toBe('/admin/mfa');
  });

  it('redirects authenticated admins away from the login page', () => {
    const router = configureGuardTest({ isFullyAuthenticated: true });

    const result = TestBed.runInInjectionContext(() => adminGuestGuard(routeSnapshot, stateSnapshot));

    expect(result instanceof UrlTree).toBe(true);
    expect(router.serializeUrl(result as UrlTree)).toBe('/admin');
  });
});

describe('adminMfaGuard', () => {
  it('allows partially authenticated admins to access the MFA page', () => {
    configureGuardTest({ isFullyAuthenticated: false, hasPendingMfaStep: true });

    const result = TestBed.runInInjectionContext(() => adminMfaGuard(routeSnapshot, stateSnapshot));

    expect(result).toBe(true);
  });
});
