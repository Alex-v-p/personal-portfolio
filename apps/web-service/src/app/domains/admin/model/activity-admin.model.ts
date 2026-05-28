import { AdminBlogTag, AdminSkillCategory, AdminSkillOption } from './taxonomy-admin.model';
import { AdminMediaFile } from './media-admin.model';

export interface AdminContactMessage {
  id: string;
  name: string;
  email: string;
  subject: string;
  message: string;
  sourcePage: string;
  isRead: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AdminSiteEvent {
  id: string;
  eventType: string;
  pagePath: string;
  visitorId: string;
  sessionId?: string | null;
  referrer?: string | null;
  userAgent?: string | null;
  ipAddress?: string | null;
  metadata?: Record<string, unknown> | null;
  createdAt: string;
  retentionEndsAt: string;
  secondsUntilRetentionEnd: number;
}

export interface AdminVisitSessionSummary {
  sessionId: string;
  visitorId: string;
  startedAt: string;
  lastActivityAt: string;
  totalEvents: number;
  pageViews: number;
  assistantMessages: number;
  contactSubmissions: number;
  entryPagePath?: string | null;
  lastPagePath?: string | null;
  ipAddress?: string | null;
  retentionEndsAt: string;
  secondsUntilRetentionEnd: number;
}

export interface AdminVisitorActivitySummary {
  visitorId: string;
  firstSeenAt: string;
  lastSeenAt: string;
  totalEvents: number;
  uniqueSessions: number;
  pageViews: number;
  assistantMessages: number;
  contactSubmissions: number;
  latestPagePath?: string | null;
  latestIpAddress?: string | null;
  retentionEndsAt: string;
  secondsUntilRetentionEnd: number;
}

export interface AdminAssistantConversationSummary {
  id: string;
  sessionId: string;
  visitorId?: string | null;
  siteSessionId?: string | null;
  pagePath?: string | null;
  startedAt: string;
  lastMessageAt: string;
  totalMessages: number;
  userMessageCount: number;
  assistantMessageCount: number;
  usedFallback?: boolean | null;
  firstUserMessage?: string | null;
  latestAssistantMessage?: string | null;
  retentionEndsAt: string;
  secondsUntilRetentionEnd: number;
}

export interface AdminSiteActivitySummary {
  totalEvents: number;
  uniqueVisitors: number;
  pageViews: number;
  assistantMessages: number;
  contactSubmissions: number;
  siteEventsRetentionDays: number;
  assistantActivityRetentionDays: number;
}

export interface AdminSiteActivity {
  summary: AdminSiteActivitySummary;
  visitors: AdminVisitorActivitySummary[];
  visits: AdminVisitSessionSummary[];
  events: AdminSiteEvent[];
  assistantConversations: AdminAssistantConversationSummary[];
}

export interface AdminReferenceData {
  skills: AdminSkillOption[];
  skillCategories: AdminSkillCategory[];
  mediaFiles: AdminMediaFile[];
  blogTags: AdminBlogTag[];
  projectStates: Array<'published' | 'archived' | 'completed' | 'paused'>;
  publicationStatuses: Array<'draft' | 'published' | 'archived'>;
}

export interface AdminCollectionResponse<T> {
  items: T[];
  total: number;
}
