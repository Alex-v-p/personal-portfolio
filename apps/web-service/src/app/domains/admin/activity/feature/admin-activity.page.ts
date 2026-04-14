import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnDestroy, OnInit, inject } from '@angular/core';
import { Subscription, timer } from 'rxjs';
import { finalize, take } from 'rxjs/operators';

import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminSiteActivity, AdminSiteEvent, AdminVisitSessionSummary, AdminVisitorActivitySummary } from '@domains/admin/model/admin.model';
import { AdminActivityTabComponent } from '@domains/admin/ui/tabs/admin-activity-tab.component';
import {
  ActivityTimelineEventFilter,
  ActivityVisitorFocus,
  ensureActivitySelections,
  filterActivityVisitors,
  filterSelectedActivityEvents,
  resolveSelectedActivityVisit,
  resolveSelectedActivityVisitor,
  selectedActivityConversations,
  visitsForVisitor,
} from '@domains/admin/activity/state/admin-activity.state';

@Component({
  selector: 'app-admin-activity-page',
  standalone: true,
  imports: [CommonModule, AdminActivityTabComponent],
  templateUrl: './admin-activity.page.html',
})
export class AdminActivityPageComponent implements OnInit, OnDestroy {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  private countdownSubscription?: Subscription;

  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';
  protected currentTimeMs = Date.now();

  protected siteActivity: AdminSiteActivity = {
    summary: {
      totalEvents: 0,
      uniqueVisitors: 0,
      pageViews: 0,
      assistantMessages: 0,
      contactSubmissions: 0,
      siteEventsRetentionDays: 0,
      assistantActivityRetentionDays: 0,
    },
    visitors: [],
    visits: [],
    events: [],
    assistantConversations: [],
  };
  protected selectedActivityVisitorId: string | null = null;
  protected selectedActivityVisitSessionId: string | null = null;
  protected activityVisitorSearchTerm = '';
  protected activityVisitorFocus: ActivityVisitorFocus = 'all';
  protected activityTimelineEventFilter: ActivityTimelineEventFilter = 'all';

  ngOnInit(): void {
    this.countdownSubscription = timer(0, 60_000).subscribe(() => {
      this.currentTimeMs = Date.now();
      this.changeDetectorRef.detectChanges();
    });
    this.loadActivityPage(false);
  }

  ngOnDestroy(): void {
    this.countdownSubscription?.unsubscribe();
  }

  protected reload(): void {
    this.loadActivityPage(true);
  }

  protected get filteredActivityVisitors(): AdminVisitorActivitySummary[] {
    return filterActivityVisitors(this.siteActivity, {
      visitorSearchTerm: this.activityVisitorSearchTerm,
      visitorFocus: this.activityVisitorFocus,
      timelineEventFilter: this.activityTimelineEventFilter,
    });
  }

  protected get selectedActivityVisitor(): AdminVisitorActivitySummary | null {
    return resolveSelectedActivityVisitor(this.filteredActivityVisitors, this.selectedActivityVisitorId);
  }

  protected get selectedActivityVisits(): AdminVisitSessionSummary[] {
    return visitsForVisitor(this.siteActivity, this.selectedActivityVisitorId);
  }

  protected get selectedActivityVisit(): AdminVisitSessionSummary | null {
    return resolveSelectedActivityVisit(this.selectedActivityVisits, this.selectedActivityVisitSessionId);
  }

  protected get selectedActivityEvents(): AdminSiteEvent[] {
    return filterSelectedActivityEvents(
      this.siteActivity,
      this.selectedActivityVisitorId,
      this.selectedActivityVisitSessionId,
      this.activityTimelineEventFilter,
    );
  }

  protected get selectedActivityConversations() {
    return selectedActivityConversations(this.siteActivity, this.selectedActivityVisitorId, this.selectedActivityVisitSessionId);
  }

  protected get selectedActivityEventCount(): number {
    return this.selectedActivityEvents.length;
  }

  protected selectActivityVisitor(visitorId: string): void {
    this.selectedActivityVisitorId = visitorId;
    this.selectedActivityVisitSessionId = visitsForVisitor(this.siteActivity, visitorId)[0]?.sessionId ?? null;
  }

  protected selectActivityVisit(sessionId: string | null): void {
    this.selectedActivityVisitSessionId = sessionId;
  }

  protected onActivityFiltersChanged(): void {
    const activitySelections = ensureActivitySelections(
      this.siteActivity,
      {
        visitorSearchTerm: this.activityVisitorSearchTerm,
        visitorFocus: this.activityVisitorFocus,
        timelineEventFilter: this.activityTimelineEventFilter,
      },
      this.selectedActivityVisitorId,
      this.selectedActivityVisitSessionId,
    );
    this.selectedActivityVisitorId = activitySelections.selectedVisitorId;
    this.selectedActivityVisitSessionId = activitySelections.selectedVisitSessionId;
  }

  private loadActivityPage(showReloadMessage: boolean): void {
    const currentSelections = {
      visitorId: this.selectedActivityVisitorId,
      visitSessionId: this.selectedActivityVisitSessionId,
    };

    this.isLoading = true;
    this.errorMessage = '';
    if (showReloadMessage) {
      this.statusMessage = 'Refreshing visitor activity…';
    }

    this.overviewApi.getSiteActivity().pipe(
      take(1),
      finalize(() => {
        this.isLoading = false;
        this.changeDetectorRef.detectChanges();
      }),
    ).subscribe({
      next: (siteActivity) => {
        this.siteActivity = siteActivity;
        const activitySelections = ensureActivitySelections(
          this.siteActivity,
          {
            visitorSearchTerm: this.activityVisitorSearchTerm,
            visitorFocus: this.activityVisitorFocus,
            timelineEventFilter: this.activityTimelineEventFilter,
          },
          currentSelections.visitorId,
          currentSelections.visitSessionId,
        );
        this.selectedActivityVisitorId = activitySelections.selectedVisitorId;
        this.selectedActivityVisitSessionId = activitySelections.selectedVisitSessionId;

        if (showReloadMessage) {
          this.statusMessage = 'Visitor activity refreshed.';
        }
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.errorMessage = error?.error?.detail || 'The activity explorer could not be loaded.';
      },
    });
  }
}
