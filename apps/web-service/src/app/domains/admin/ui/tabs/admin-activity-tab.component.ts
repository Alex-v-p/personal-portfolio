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
