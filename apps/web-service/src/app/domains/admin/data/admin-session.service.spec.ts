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
    localStorage.clear();
    TestBed.resetTestingModule();
  });

  it('stores the token and current user after a successful login', () => {
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
              accessToken: 'admin-token',
              tokenType: 'bearer',
              expiresInSeconds: 3600,
              user: adminUserFixture,
            }),
            getCurrentAdmin: () => of(adminUserFixture),
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

    expect(service.token).toBe('admin-token');
    expect(service.isAuthenticated).toBe(true);
    expect(currentUser?.email).toBe('admin@example.com');
    expect(JSON.parse(localStorage.getItem('portfolio.admin.user') ?? '{}')).toMatchObject({ email: 'admin@example.com' });
    expect(navigate).not.toHaveBeenCalled();
  });

  it('clears the stored session when restoreSession fails', () => {
    const navigate = vi.fn().mockResolvedValue(true);
    localStorage.setItem('portfolio.admin.access-token', 'stale-token');
    localStorage.setItem('portfolio.admin.user', JSON.stringify(adminUserFixture));

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
            login: () => of({ accessToken: 'admin-token', tokenType: 'bearer', expiresInSeconds: 3600, user: adminUserFixture }),
            getCurrentAdmin: () => throwError(() => new Error('Unauthorized')),
          },
        },
      ],
    });

    const service = TestBed.inject(AdminSessionService);
    let receivedError: unknown;
    service.restoreSession().subscribe({
      error: (error: unknown) => {
        receivedError = error;
      },
    });

    expect(receivedError).toBeInstanceOf(Error);
    expect(service.token).toBeNull();
    expect(service.currentUser).toBeNull();
    expect(localStorage.getItem('portfolio.admin.user')).toBeNull();
    expect(navigate).not.toHaveBeenCalled();
  });
});
