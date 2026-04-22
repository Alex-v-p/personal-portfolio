import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { API_BASE_URL } from '@core/config/api.config';
import type { ProjectDetailApi, ProjectSummaryApi } from '@core/http/public-api/projects.contracts';
import { PublicProjectsApiService } from './projects-api.service';

const projectSummaryFixture: ProjectSummaryApi = {
  id: 'project-1',
  slug: 'portfolio',
  title: 'Portfolio',
  teaser: 'Personal portfolio teaser',
  summary: 'Personal portfolio summary',
  coverImageFileId: null,
  coverImage: null,
  githubUrl: null,
  githubRepoOwner: null,
  githubRepoName: null,
  demoUrl: null,
  companyName: null,
  startedOn: null,
  endedOn: null,
  durationLabel: 'Ongoing',
  status: 'Published',
  state: 'published',
  isFeatured: true,
  sortOrder: 1,
  publishedAt: '2026-04-15T10:00:00Z',
  createdAt: '2026-04-15T10:00:00Z',
  updatedAt: '2026-04-15T10:00:00Z',
  skills: [],
};

const projectDetailFixture: ProjectDetailApi = {
  ...projectSummaryFixture,
  descriptionMarkdown: 'Detailed case study',
  images: [],
};

describe('PublicProjectsApiService', () => {
  let service: PublicProjectsApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        PublicProjectsApiService,
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: API_BASE_URL, useValue: '/api' },
      ],
    });

    service = TestBed.inject(PublicProjectsApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    TestBed.resetTestingModule();
  });

  it('reuses the cached projects response across repeated calls', () => {
    let firstResultLength = 0;
    let secondResultLength = 0;

    service.getProjects().subscribe((projects) => {
      firstResultLength = projects.length;
    });
    service.getProjects().subscribe((projects) => {
      secondResultLength = projects.length;
    });

    const request = httpMock.expectOne((req) => req.url === '/api/public/projects' && req.params.get('locale') === 'en');
    expect(request.request.method).toBe('GET');
    request.flush({ items: [projectSummaryFixture] });

    expect(firstResultLength).toBe(1);
    expect(secondResultLength).toBe(1);
    httpMock.expectNone((req) => req.url === '/api/public/projects');
  });

  it('keeps detail responses cached per slug', () => {
    let firstProjectTitle = '';
    let secondProjectTitle = '';

    service.getProjectBySlug('portfolio').subscribe((project) => {
      firstProjectTitle = project.title;
    });
    service.getProjectBySlug('portfolio').subscribe((project) => {
      secondProjectTitle = project.title;
    });

    const firstRequest = httpMock.expectOne((req) => req.url === '/api/public/projects/portfolio' && req.params.get('locale') === 'en');
    firstRequest.flush(projectDetailFixture);

    expect(firstProjectTitle).toBe('Portfolio');
    expect(secondProjectTitle).toBe('Portfolio');
    httpMock.expectNone((req) => req.url === '/api/public/projects/portfolio');

    service.getProjectBySlug('another-project').subscribe();
    const secondRequest = httpMock.expectOne((req) => req.url === '/api/public/projects/another-project' && req.params.get('locale') === 'en');
    secondRequest.flush({ ...projectDetailFixture, id: 'project-2', slug: 'another-project', title: 'Another Project' });
  });

  it('clears a failed cached request so a later retry can refetch', () => {
    let capturedErrorMessage = '';

    service.getProjects().subscribe({
      error: (error) => {
        capturedErrorMessage = error.error?.detail ?? 'Unknown error';
      },
    });

    const failedRequest = httpMock.expectOne((req) => req.url === '/api/public/projects' && req.params.get('locale') === 'en');
    failedRequest.flush({ detail: 'Temporary outage' }, { status: 503, statusText: 'Service Unavailable' });

    expect(capturedErrorMessage).toBe('Temporary outage');

    service.getProjects().subscribe();
    const retryRequest = httpMock.expectOne((req) => req.url === '/api/public/projects' && req.params.get('locale') === 'en');
    retryRequest.flush({ items: [] });
  });
});
