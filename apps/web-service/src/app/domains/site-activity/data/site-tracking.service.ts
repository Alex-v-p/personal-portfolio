import { Injectable, inject } from '@angular/core';

import { PublicEventsApiService } from '@domains/site-activity/data/events-api.service';

const VISITOR_STORAGE_KEY = 'portfolio.site.visitor-id';
const SESSION_STORAGE_KEY = 'portfolio.site.session-id';
@Injectable({ providedIn: 'root' })
export class SiteTrackingService {
  private readonly eventsApi = inject(PublicEventsApiService);
  private lastTrackedPagePath: string | null = null;

  get visitorId(): string {
    if (typeof window === 'undefined') {
      return 'server-visitor';
    }
    const existing = window.localStorage.getItem(VISITOR_STORAGE_KEY);
    if (existing) {
      return existing;
    }
    const created = this.generateId();
    window.localStorage.setItem(VISITOR_STORAGE_KEY, created);
    return created;
  }

  get sessionId(): string {
    if (typeof window === 'undefined') {
      return 'server-session';
    }
    const existing = window.sessionStorage.getItem(SESSION_STORAGE_KEY);
    if (existing) {
      return existing;
    }
    const created = this.generateId();
    window.sessionStorage.setItem(SESSION_STORAGE_KEY, created);
    return created;
  }

  trackPageView(pagePath: string): void {
    if (typeof window === 'undefined') {
      return;
    }
    const dedupeKey = `${pagePath}::${window.location.search}`;
    if (this.lastTrackedPagePath === dedupeKey) {
      return;
    }
    this.lastTrackedPagePath = dedupeKey;
    this.trackEvent('page_view', pagePath, { route: pagePath });
  }

  trackEvent(eventType: string, pagePath: string, metadata?: Record<string, unknown>): void {
    this.eventsApi.createSiteEvent({
      eventType,
      pagePath,
      visitorId: this.visitorId,
      sessionId: this.sessionId,
      referrer: typeof document !== 'undefined' ? document.referrer || null : null,
      metadata: metadata ?? null,
    }).subscribe({ error: () => undefined });
  }

  private generateId(): string {
    return globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
  }
}
