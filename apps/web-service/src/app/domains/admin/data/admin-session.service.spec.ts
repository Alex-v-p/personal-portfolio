import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { AdminAuthApiService } from '@domains/admin/data/api/admin-auth-api.service';
import { AdminSessionService } from './admin-session.service';

const adminUserFixture = {
  id: 'admin-1',
  email: 'admin@example.com',
  displayName: 'Admin User',
  isActive: true,
  createdAt: '2026-04-13T10:00:00Z',
  mfaEnabled: true,
  mfaEnrolledAt: '2026-04-13T10:00:00Z',
  mfaRecoveryCodesRemaining: 8,
};

const fullSessionFixture = {
  csrfToken: 'csrf-token-1',
  expiresInSeconds: 3600,
  user: adminUserFixture,
  isMfaEnabled: true,
  isMfaVerified: true,
  mfaRequired: false,
  mfaSetupRequired: false,
};

describe('AdminSessionService', () => {
  beforeEach(() => {
    sessionStorage.clear();
    TestBed.resetTestingModule();
  });

  it('stores the current auth session after a successful login', () => {
    const navigate = vi.fn().mockResolvedValue(true);

    TestBed.configureTestingModule({
      providers: [
        AdminSessionService,
        {
          provide: Router,
          useValue: { navigate },
        },
        {
          provide: AdminAuthApiService,
          useValue: {
            login: () => of(fullSessionFixture),
            getCurrentAdmin: () => of(fullSessionFixture),
            beginMfaSetup: () => of(null),
            confirmMfaSetup: () => of(null),
            verifyMfa: () => of(fullSessionFixture),
            logout: () => of(void 0),
          },
        },
      ],
    });

    const service = TestBed.inject(AdminSessionService);
    let currentUser = null as typeof adminUserFixture | null;
    service.currentUser$.subscribe((user: typeof adminUserFixture | null) => {
      currentUser = user as typeof adminUserFixture | null;
    });

    service.login('admin@example.com', 'secret').subscribe();

    expect(service.csrfToken).toBe('csrf-token-1');
    expect(service.isAuthenticated).toBe(true);
    expect(service.isFullyAuthenticated).toBe(true);
    expect(currentUser?.email).toBe('admin@example.com');
    expect(JSON.parse(sessionStorage.getItem('portfolio.admin.auth-session') ?? '{}')).toMatchObject({
      user: { email: 'admin@example.com' },
      csrfToken: 'csrf-token-1',
    });
    expect(navigate).not.toHaveBeenCalled();
  });

  it('clears the stored session when restoreSession fails', () => {
    const navigate = vi.fn().mockResolvedValue(true);
    sessionStorage.setItem('portfolio.admin.auth-session', JSON.stringify(fullSessionFixture));

    TestBed.configureTestingModule({
      providers: [
        AdminSessionService,
        {
          provide: Router,
          useValue: { navigate },
        },
        {
          provide: AdminAuthApiService,
          useValue: {
            login: () => of(fullSessionFixture),
            getCurrentAdmin: () => throwError(() => new Error('Unauthorized')),
            beginMfaSetup: () => of(null),
            confirmMfaSetup: () => of(null),
            verifyMfa: () => of(fullSessionFixture),
            logout: () => of(void 0),
          },
        },
      ],
    });

    const service = TestBed.inject(AdminSessionService);
    let restoredSession = fullSessionFixture as typeof fullSessionFixture | null;
    service.restoreSession().subscribe((session) => {
      restoredSession = session as typeof fullSessionFixture;
    });

    expect(restoredSession).toBeNull();
    expect(service.csrfToken).toBeNull();
    expect(service.currentUser).toBeNull();
    expect(sessionStorage.getItem('portfolio.admin.auth-session')).toBeNull();
    expect(navigate).not.toHaveBeenCalled();
  });
});
