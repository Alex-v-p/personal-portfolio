import { HttpClient, provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { API_BASE_URL } from '../../core/config/api.config';
import { PublicPortfolioApiService } from './public-portfolio-api.service';

describe('PublicPortfolioApiService', () => {
  let service: PublicPortfolioApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: API_BASE_URL, useValue: '/api' },
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(PublicPortfolioApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
    TestBed.resetTestingModule();
  });

  it('normalizes the home payload into frontend-facing view models', () => {
    let received: unknown;

    service.getHome().subscribe((value: unknown) => {
      received = value;
    });

    const request = httpMock.expectOne('/api/public/home');
    expect(request.request.method).toBe('GET');
    request.flush({
      hero: {
        id: 'profile-1',
        firstName: 'Alex',
        lastName: 'van Poppel',
        headline: 'Software Engineer',
        shortIntro: 'Builder of web apps.',
        longBio: 'Longer bio.',
        location: 'Belgium',
        email: 'hello@example.com',
        phone: '+32 000 000',
        avatarFileId: 'avatar-1',
        heroImageFileId: 'hero-1',
        resumeFileId: 'resume-1',
        avatar: { id: 'avatar-1', url: 'http://media.example/avatar.png', alt: 'Avatar', fileName: 'avatar.png', mimeType: 'image/png', width: 200, height: 200 },
        heroImage: { id: 'hero-1', url: 'http://media.example/hero.png', alt: 'Hero', fileName: 'hero.png', mimeType: 'image/png', width: 1200, height: 630 },
        resume: { id: 'resume-1', url: 'http://media.example/resume.pdf', alt: 'Resume', fileName: 'resume.pdf', mimeType: 'application/pdf', width: null, height: null },
        ctaPrimaryLabel: 'View project',
        ctaPrimaryUrl: '/projects/personal-portfolio',
        ctaSecondaryLabel: 'GitHub',
        ctaSecondaryUrl: 'https://github.com/shuzu',
        isPublic: true,
        socialLinks: [{ id: 'social-1', profileId: 'profile-1', platform: 'github', label: 'GitHub', url: 'https://github.com/shuzu', iconKey: 'github', sortOrder: 1, isVisible: true }],
        footerDescription: 'Footer text',
        introParagraphs: ['Paragraph one'],
        availability: ['Open to internships'],
        skills: ['Angular', 'FastAPI'],
        expertiseGroups: [{ title: 'Core stack', tags: ['Angular', 'FastAPI'] }],
        createdAt: '2026-04-13T10:00:00Z',
        updatedAt: '2026-04-13T10:00:00Z',
      },
      featuredProjects: [
        {
          id: 'project-1',
          slug: 'personal-portfolio',
          title: 'Personal Portfolio',
          teaser: 'Portfolio teaser',
          summary: 'Portfolio summary',
          descriptionMarkdown: '## Project body',
          coverImageFileId: 'cover-1',
          coverImage: { id: 'cover-1', url: 'http://media.example/cover.png', alt: 'Cover', fileName: 'cover.png', mimeType: 'image/png', width: 1200, height: 630 },
          githubUrl: 'https://github.com/shuzu/personal-portfolio',
          githubRepoOwner: 'shuzu',
          githubRepoName: 'personal-portfolio',
          demoUrl: 'https://portfolio.example',
          companyName: 'Independent',
          startedOn: '2026-01-01',
          endedOn: null,
          durationLabel: '3 months',
          status: 'Live',
          state: 'published',
          isFeatured: true,
          sortOrder: 1,
          publishedAt: '2026-01-01T10:00:00Z',
          createdAt: '2026-01-01T10:00:00Z',
          updatedAt: '2026-01-01T10:00:00Z',
          skills: [{ id: 'skill-1', categoryId: 'cat-1', name: 'Angular', yearsOfExperience: 2, iconKey: 'angular', sortOrder: 1, isHighlighted: true }],
          images: [],
        },
      ],
      featuredBlogPosts: [
        {
          id: 'post-1',
          slug: 'portfolio-shell',
          title: 'Building a portfolio shell',
          excerpt: 'How the shell was built.',
          contentMarkdown: '# Body',
          coverImageFileId: 'blog-cover-1',
          coverImageAlt: 'Blog cover',
          coverImage: { id: 'blog-cover-1', url: 'http://media.example/blog-cover.png', alt: 'Blog cover', fileName: 'blog-cover.png', mimeType: 'image/png', width: 1200, height: 630 },
          readingTimeMinutes: 6,
          status: 'published',
          isFeatured: true,
          publishedAt: '2026-02-01T10:00:00Z',
          seoTitle: 'SEO title',
          seoDescription: 'SEO description',
          createdAt: '2026-02-01T10:00:00Z',
          updatedAt: '2026-02-01T10:00:00Z',
          tags: [{ id: 'tag-1', name: 'Architecture', slug: 'architecture' }],
        },
      ],
      expertiseGroups: [{ title: 'Core stack', tags: ['Angular', 'FastAPI'] }],
      experiencePreview: [],
      contactPreview: [{ id: 'contact-1', platform: 'email', label: 'Email', value: 'hello@example.com', href: 'mailto:hello@example.com', actionLabel: 'Send email', iconKey: 'mail', description: 'Get in touch', sortOrder: 1, isVisible: true }],
    });

    expect(received).toMatchObject({
      hero: {
        name: 'Alex van Poppel',
        greeting: "Hi, I'm Alex",
        heroActions: [
          { label: 'View project', routerLink: '/projects/personal-portfolio', openInNewTab: false },
          { label: 'GitHub', href: 'https://github.com/shuzu', openInNewTab: true },
        ],
      },
      featuredProjects: [
        {
          slug: 'personal-portfolio',
          coverImageUrl: 'http://media.example/cover.png',
          links: [
            { label: 'Live Demo', href: 'https://portfolio.example' },
            { label: 'GitHub', href: 'https://github.com/shuzu/personal-portfolio' },
            { label: 'Read more', routerLink: ['/projects', 'personal-portfolio'] },
          ],
        },
      ],
      featuredBlogPosts: [{ slug: 'portfolio-shell', readTime: '6 min read', category: 'Architecture' }],
      contactPreview: [{ platform: 'email', href: 'mailto:hello@example.com' }],
    });
  });

  it('preserves the public contact API contract when submitting messages', () => {
    let received: unknown;

    service.submitContactMessage({
      name: 'Alex',
      email: 'alex@example.com',
      subject: 'Internship',
      message: 'I would like to discuss an internship opportunity.',
      sourcePage: '/contact',
      visitorId: 'visitor-1',
      sessionId: 'session-1',
      website: '',
    }).subscribe((value: unknown) => {
      received = value;
    });

    const request = httpMock.expectOne('/api/contact/messages');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toMatchObject({
      name: 'Alex',
      email: 'alex@example.com',
      subject: 'Internship',
      visitorId: 'visitor-1',
      sessionId: 'session-1',
      website: '',
    });

    request.flush({
      message: 'Contact message created.',
      item: {
        id: 'message-1',
        name: 'Alex',
        email: 'alex@example.com',
        subject: 'Internship',
        message: 'I would like to discuss an internship opportunity.',
        sourcePage: '/contact',
        visitorId: 'visitor-1',
        sessionId: 'session-1',
        website: '',
        isRead: false,
        createdAt: '2026-04-13T10:00:00Z',
        updatedAt: '2026-04-13T10:00:00Z',
      },
    });

    expect(received).toMatchObject({
      message: 'Contact message created.',
      item: {
        id: 'message-1',
        sourcePage: '/contact',
        isRead: false,
      },
    });
  });
});
