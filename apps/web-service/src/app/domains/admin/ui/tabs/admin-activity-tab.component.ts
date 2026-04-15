import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import {
  AdminAssistantConversationSummary,
  AdminSiteActivity,
  AdminSiteEvent,
  AdminVisitSessionSummary,
  AdminVisitorActivitySummary,
} from '@domains/admin/model/admin.model';
import { retentionCountdownLabel, retentionCountdownTone } from '@domains/admin/shared/state/admin-maintenance-display.utils';

@Component({
  selector: 'app-admin-activity-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-activity-tab.component.html'
})
export class AdminActivityTabComponent {
  @Input({ required: true }) siteActivity!: AdminSiteActivity;
  @Input() activityVisitorSearchTerm = '';
  @Input() activityVisitorFocus: 'all' | 'withAssistant' | 'withContacts' | 'withPageViews' = 'all';
  @Input() activityTimelineEventFilter: 'all' | 'page_view' | 'assistant_message' | 'contact_submit' = 'all';
  @Input({ required: true }) filteredActivityVisitors: AdminVisitorActivitySummary[] = [];
  @Input() selectedActivityVisitorId: string | null = null;
  @Input() selectedActivityVisitor: AdminVisitorActivitySummary | null = null;
  @Input({ required: true }) selectedActivityVisits: AdminVisitSessionSummary[] = [];
  @Input() selectedActivityVisitSessionId: string | null = null;
  @Input() selectedActivityVisit: AdminVisitSessionSummary | null = null;
  @Input({ required: true }) selectedActivityEvents: AdminSiteEvent[] = [];
  @Input({ required: true }) selectedActivityConversations: AdminAssistantConversationSummary[] = [];
  @Input() selectedActivityEventCount = 0;
  @Input() currentTimeMs = Date.now();

  @Output() readonly refreshRequested = new EventEmitter<void>();
  @Output() readonly activityVisitorSearchTermChange = new EventEmitter<string>();
  @Output() readonly activityVisitorFocusChange = new EventEmitter<'all' | 'withAssistant' | 'withContacts' | 'withPageViews'>();
  @Output() readonly activityTimelineEventFilterChange = new EventEmitter<'all' | 'page_view' | 'assistant_message' | 'contact_submit'>();
  @Output() readonly filtersChanged = new EventEmitter<void>();
  @Output() readonly activityVisitorSelected = new EventEmitter<string>();
  @Output() readonly activityVisitSelected = new EventEmitter<string | null>();

  get averageEventsPerVisitor(): string {
    const uniqueVisitors = this.siteActivity.summary.uniqueVisitors || 1;
    return (this.siteActivity.summary.totalEvents / uniqueVisitors).toFixed(1);
  }

  get averageVisitsPerVisitor(): string {
    const uniqueVisitors = this.siteActivity.summary.uniqueVisitors || 1;
    return (this.siteActivity.visits.length / uniqueVisitors).toFixed(1);
  }

  get activityKpis(): Array<{ label: string; value: number | string; hint: string }> {
    return [
      { label: 'Total events', value: this.siteActivity.summary.totalEvents, hint: `${this.siteActivity.summary.siteEventsRetentionDays} day retention` },
      { label: 'Unique visitors', value: this.siteActivity.summary.uniqueVisitors, hint: `${this.filteredActivityVisitors.length} in current results` },
      { label: 'Tracked visits', value: this.siteActivity.visits.length, hint: `${this.averageVisitsPerVisitor} visits / visitor` },
      { label: 'Page views', value: this.siteActivity.summary.pageViews, hint: `${this.averageEventsPerVisitor} events / visitor` },
      { label: 'Assistant messages', value: this.siteActivity.summary.assistantMessages, hint: `${this.siteActivity.summary.assistantActivityRetentionDays} day chat retention` },
      { label: 'Contact submits', value: this.siteActivity.summary.contactSubmissions, hint: 'Recorded from contact forms' },
    ];
  }

  loadCms(): void {
    this.refreshRequested.emit();
  }

  onActivityVisitorSearchTermChange(value: string): void {
    this.activityVisitorSearchTermChange.emit(value);
    this.filtersChanged.emit();
  }

  onActivityVisitorFocusChange(value: 'all' | 'withAssistant' | 'withContacts' | 'withPageViews'): void {
    this.activityVisitorFocusChange.emit(value);
    this.filtersChanged.emit();
  }

  onActivityTimelineEventFilterChange(value: 'all' | 'page_view' | 'assistant_message' | 'contact_submit'): void {
    this.activityTimelineEventFilterChange.emit(value);
    this.filtersChanged.emit();
  }

  onActivityFiltersChanged(): void {
    this.filtersChanged.emit();
  }

  selectActivityVisitor(visitorId: string): void {
    this.activityVisitorSelected.emit(visitorId);
  }

  selectActivityVisit(sessionId: string | null): void {
    this.activityVisitSelected.emit(sessionId);
  }

  retentionLabel(targetIso: string): string {
    return retentionCountdownLabel(targetIso, this.currentTimeMs);
  }

  retentionTone(targetIso: string): string {
    return retentionCountdownTone(targetIso, this.currentTimeMs);
  }
}
