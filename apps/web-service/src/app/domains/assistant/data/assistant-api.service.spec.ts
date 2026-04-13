import { HttpClient, provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { afterEach, beforeEach, describe, expect, it } from 'vitest';

import { AssistantApiService } from './assistant-api.service';
import { SiteTrackingService } from '@domains/site-activity/data/site-tracking.service';

describe('AssistantApiService', () => {
  let service: AssistantApiService;
  let httpMock: HttpTestingController;
  let router: Router;

  beforeEach(() => {
    sessionStorage.clear();

    TestBed.configureTestingModule({
      providers: [
        provideRouter([]),
        provideHttpClient(),
        provideHttpClientTesting(),
        {
          provide: SiteTrackingService,
          useValue: {
            visitorId: 'visitor-123',
            sessionId: 'site-session-123',
          },
        },
      ],
    });

    service = TestBed.inject(AssistantApiService);
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    Object.defineProperty(router, 'url', { configurable: true, get: () => '/projects' });
  });

  afterEach(() => {
    httpMock.verify();
    sessionStorage.clear();
    TestBed.resetTestingModule();
  });

  it('posts a normalized assistant request and stores the conversation state', () => {
    sessionStorage.setItem('portfolio.assistant.session-id', 'assistant-session-1');

    service.sendMessage('  Tell me about the backend.  ');

    expect(service.snapshot.isLoading).toBe(true);
    expect(service.snapshot.messages).toHaveLength(1);
    expect(service.snapshot.messages[0]).toMatchObject({ role: 'user', text: 'Tell me about the backend.' });

    const request = httpMock.expectOne('/ai/chat/respond');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toMatchObject({
      message: 'Tell me about the backend.',
      conversation_id: null,
      session_id: 'assistant-session-1',
      site_session_id: 'site-session-123',
      visitor_id: 'visitor-123',
      page_path: '/projects',
    });

    request.flush({
      conversationId: 'conversation-1',
      message: 'The backend uses FastAPI.',
      providerBackend: 'mock',
      citations: [
        {
          title: 'Portfolio CMS Project',
          sourceType: 'project',
          canonicalUrl: '/projects/personal-portfolio',
          excerpt: 'FastAPI powers the backend API.',
        },
      ],
    });

    expect(service.snapshot.isLoading).toBe(false);
    expect(service.snapshot.errorMessage).toBeNull();
    expect(service.snapshot.conversationId).toBe('conversation-1');
    expect(service.snapshot.messages).toHaveLength(2);
    expect(service.snapshot.messages[1]).toMatchObject({ role: 'assistant', text: 'The backend uses FastAPI.' });

    const persistedState = JSON.parse(sessionStorage.getItem('portfolio.assistant.state') ?? '{}') as { conversationId?: string };
    expect(persistedState.conversationId).toBe('conversation-1');
    expect(sessionStorage.getItem('portfolio.assistant.session-id')).toBe('assistant-session-1');
  });

  it('stores a readable fallback error when the assistant request fails', () => {
    service.sendMessage('Explain the CMS architecture.');

    const request = httpMock.expectOne('/ai/chat/respond');
    request.flush({ detail: 'Too many assistant messages were sent in a short period. Please wait a moment before trying again.' }, { status: 429, statusText: 'Too Many Requests' });

    expect(service.snapshot.isLoading).toBe(false);
    expect(service.snapshot.errorMessage).toContain('Too many assistant messages');
    const lastMessage = service.snapshot.messages[service.snapshot.messages.length - 1];
    expect(lastMessage).toMatchObject({
      role: 'assistant',
      text: 'Too many assistant messages were sent in a short period. Please wait a moment before trying again.',
    });
  });

  it('does not send an empty assistant message', () => {
    service.sendMessage('   ');

    httpMock.expectNone('/ai/chat/respond');
    expect(service.snapshot.messages).toEqual([]);
  });
});
