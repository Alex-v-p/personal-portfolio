import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { API_BASE_URL } from '../../core/config/api.config';
import { adminAuthInterceptor } from './admin-auth.interceptor';

describe('adminAuthInterceptor', () => {
  let http: HttpClient;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: API_BASE_URL, useValue: '/api' },
        {
          provide: AdminSessionService,
          useValue: {
            csrfToken: 'csrf-token-1',
          },
        },
        provideHttpClient(withInterceptors([adminAuthInterceptor])),
        provideHttpClientTesting(),
      ],
    });

    http = TestBed.inject(HttpClient);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    TestBed.resetTestingModule();
  });

  it('adds credentials and csrf protection to mutating admin API requests', () => {
    http.post('/api/admin/projects', { title: 'Test' }).subscribe();

    const request = httpMock.expectOne('/api/admin/projects');
    expect(request.request.withCredentials).toBe(true);
    expect(request.request.headers.get('X-Portfolio-CSRF')).toBe('csrf-token-1');
    request.flush({ id: 'project-1' });
  });

  it('adds credentials but not csrf headers to read-only admin API requests', () => {
    http.get('/api/admin/projects').subscribe();

    const request = httpMock.expectOne('/api/admin/projects');
    expect(request.request.withCredentials).toBe(true);
    expect(request.request.headers.has('X-Portfolio-CSRF')).toBe(false);
    request.flush({ items: [], total: 0 });
  });

  it('does not modify public API requests', () => {
    http.get('/api/public/home').subscribe();

    const request = httpMock.expectOne('/api/public/home');
    expect(request.request.withCredentials).toBe(false);
    expect(request.request.headers.has('X-Portfolio-CSRF')).toBe(false);
    request.flush({ hero: {}, featuredProjects: [], featuredBlogPosts: [], expertiseGroups: [], experiencePreview: [], contactPreview: [] });
  });
});
