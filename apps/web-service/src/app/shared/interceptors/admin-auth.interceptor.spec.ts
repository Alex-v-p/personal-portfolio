import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { API_BASE_URL } from '../../core/config/api.config';
import { adminAuthInterceptor } from './admin-auth.interceptor';

describe('adminAuthInterceptor', () => {
  let http: HttpClient;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [
        { provide: API_BASE_URL, useValue: '/api' },
        provideHttpClient(withInterceptors([adminAuthInterceptor])),
        provideHttpClientTesting(),
      ],
    });

    http = TestBed.inject(HttpClient);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
    TestBed.resetTestingModule();
  });

  it('adds the bearer token to admin API requests', () => {
    localStorage.setItem('portfolio.admin.access-token', 'test-token');

    http.get('/api/admin/projects').subscribe();

    const request = httpMock.expectOne('/api/admin/projects');
    expect(request.request.headers.get('Authorization')).toBe('Bearer test-token');
    request.flush({ items: [], total: 0 });
  });

  it('does not add the bearer token to public API requests', () => {
    localStorage.setItem('portfolio.admin.access-token', 'test-token');

    http.get('/api/public/home').subscribe();

    const request = httpMock.expectOne('/api/public/home');
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush({ hero: {}, featuredProjects: [], featuredBlogPosts: [], expertiseGroups: [], experiencePreview: [], contactPreview: [] });
  });

  it('does not add the bearer token when no admin session exists', () => {
    http.get('/api/admin/dashboard').subscribe();

    const request = httpMock.expectOne('/api/admin/dashboard');
    expect(request.request.headers.has('Authorization')).toBe(false);
    request.flush({});
  });
});
