export interface SiteEventCreatePayload {
  eventType: string;
  pagePath: string;
  visitorId?: string | null;
  sessionId?: string | null;
  referrer?: string | null;
  metadata?: Record<string, unknown> | null;
}
