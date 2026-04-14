import {
  AdminAssistantConversationSummary,
  AdminSiteActivity,
  AdminSiteEvent,
  AdminVisitSessionSummary,
  AdminVisitorActivitySummary,
} from '@domains/admin/model/admin.model';
import { matchesSearch } from '@domains/admin/shell/state/admin-page.utils';

export type ActivityVisitorFocus = 'all' | 'withAssistant' | 'withContacts' | 'withPageViews';
export type ActivityTimelineEventFilter = 'all' | 'page_view' | 'assistant_message' | 'contact_submit';

export interface AdminActivityFilterState {
  visitorSearchTerm: string;
  visitorFocus: ActivityVisitorFocus;
  timelineEventFilter: ActivityTimelineEventFilter;
}

export function filterActivityVisitors(siteActivity: AdminSiteActivity, filters: AdminActivityFilterState): AdminVisitorActivitySummary[] {
  return siteActivity.visitors
    .filter((visitor) => {
      if (filters.visitorFocus === 'withAssistant') {
        return visitor.assistantMessages > 0;
      }
      if (filters.visitorFocus === 'withContacts') {
        return visitor.contactSubmissions > 0;
      }
      if (filters.visitorFocus === 'withPageViews') {
        return visitor.pageViews > 0;
      }
      return true;
    })
    .filter((visitor) => matchesSearch([visitor.visitorId, visitor.latestPagePath, visitor.latestIpAddress], filters.visitorSearchTerm))
    .sort((left, right) => right.lastSeenAt.localeCompare(left.lastSeenAt));
}

export function visitsForVisitor(siteActivity: AdminSiteActivity, visitorId: string | null): AdminVisitSessionSummary[] {
  if (!visitorId) {
    return [];
  }

  return siteActivity.visits
    .filter((visit) => visit.visitorId === visitorId)
    .sort((left, right) => right.lastActivityAt.localeCompare(left.lastActivityAt));
}

export function resolveSelectedActivityVisitor(visitors: AdminVisitorActivitySummary[], selectedVisitorId: string | null): AdminVisitorActivitySummary | null {
  return visitors.find((visitor) => visitor.visitorId === selectedVisitorId) ?? null;
}

export function resolveSelectedActivityVisit(visits: AdminVisitSessionSummary[], selectedVisitSessionId: string | null): AdminVisitSessionSummary | null {
  return visits.find((visit) => visit.sessionId === selectedVisitSessionId) ?? null;
}

export function filterSelectedActivityEvents(
  siteActivity: AdminSiteActivity,
  selectedVisitorId: string | null,
  selectedVisitSessionId: string | null,
  timelineEventFilter: ActivityTimelineEventFilter,
): AdminSiteEvent[] {
  if (!selectedVisitorId) {
    return [];
  }

  return siteActivity.events
    .filter((event) => event.visitorId === selectedVisitorId)
    .filter((event) => !selectedVisitSessionId || event.sessionId === selectedVisitSessionId)
    .filter((event) => timelineEventFilter === 'all' || event.eventType === timelineEventFilter)
    .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
}

export function selectedActivityConversations(
  siteActivity: AdminSiteActivity,
  selectedVisitorId: string | null,
  selectedVisitSessionId: string | null,
): AdminAssistantConversationSummary[] {
  if (!selectedVisitorId) {
    return [];
  }

  return siteActivity.assistantConversations
    .filter((conversation) => conversation.visitorId === selectedVisitorId)
    .filter((conversation) => !selectedVisitSessionId || conversation.siteSessionId === selectedVisitSessionId)
    .sort((left, right) => right.lastMessageAt.localeCompare(left.lastMessageAt));
}

export function ensureActivitySelections(
  siteActivity: AdminSiteActivity,
  filters: AdminActivityFilterState,
  selectedVisitorId: string | null,
  selectedVisitSessionId: string | null,
): { selectedVisitorId: string | null; selectedVisitSessionId: string | null } {
  const visitors = filterActivityVisitors(siteActivity, filters);
  if (!visitors.length) {
    return { selectedVisitorId: null, selectedVisitSessionId: null };
  }

  const resolvedVisitorId = selectedVisitorId && visitors.some((visitor) => visitor.visitorId === selectedVisitorId)
    ? selectedVisitorId
    : visitors[0].visitorId;

  const visits = visitsForVisitor(siteActivity, resolvedVisitorId);
  if (!visits.length) {
    return { selectedVisitorId: resolvedVisitorId, selectedVisitSessionId: null };
  }

  if (selectedVisitSessionId === null) {
    return { selectedVisitorId: resolvedVisitorId, selectedVisitSessionId };
  }

  const resolvedVisitSessionId = visits.some((visit) => visit.sessionId === selectedVisitSessionId)
    ? selectedVisitSessionId
    : visits[0].sessionId;

  return { selectedVisitorId: resolvedVisitorId, selectedVisitSessionId: resolvedVisitSessionId };
}
