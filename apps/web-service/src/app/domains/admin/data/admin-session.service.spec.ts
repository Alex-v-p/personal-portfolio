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
};

describe('AdminSessionService', () => {
  beforeEach(() => {
    sessionStorage.clear();
    TestBed.resetTestingModule();
  });

  it('stores the csrf token and current user after a successful login', () => {
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
            login: () => of({
              csrfToken: 'csrf-token-1',
              expiresInSeconds: 3600,
              user: adminUserFixture,
            }),
            getCurrentAdmin: () => of({
              csrfToken: 'csrf-token-2',
              expiresInSeconds: 3600,
              user: adminUserFixture,
            }),
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

    service.login('admin@example.com', 'secret').subscribe((user: typeof adminUserFixture) => {
      currentUser = user;
    });

    expect(service.csrfToken).toBe('csrf-token-1');
    expect(service.isAuthenticated).toBe(true);
    expect(currentUser?.email).toBe('admin@example.com');
    expect(JSON.parse(sessionStorage.getItem('portfolio.admin.user') ?? '{}')).toMatchObject({ email: 'admin@example.com' });
    expect(sessionStorage.getItem('portfolio.admin.csrf-token')).toBe('csrf-token-1');
    expect(navigate).not.toHaveBeenCalled();
  });

  it('clears the stored session when restoreSession fails', () => {
    const navigate = vi.fn().mockResolvedValue(true);
    sessionStorage.setItem('portfolio.admin.csrf-token', 'stale-csrf');
    sessionStorage.setItem('portfolio.admin.user', JSON.stringify(adminUserFixture));

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
            login: () => of({ csrfToken: 'csrf-token-1', expiresInSeconds: 3600, user: adminUserFixture }),
            getCurrentAdmin: () => throwError(() => new Error('Unauthorized')),
            logout: () => of(void 0),
          },
        },
      ],
    });

    const service = TestBed.inject(AdminSessionService);
    let restoredUser: typeof adminUserFixture | null = adminUserFixture;
    service.restoreSession().subscribe((user: typeof adminUserFixture | null) => {
      restoredUser = user;
    });

    expect(restoredUser).toBeNull();
    expect(service.csrfToken).toBeNull();
    expect(service.currentUser).toBeNull();
    expect(sessionStorage.getItem('portfolio.admin.user')).toBeNull();
    expect(navigate).not.toHaveBeenCalled();
  });
});
