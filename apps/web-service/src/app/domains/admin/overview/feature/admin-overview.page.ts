import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { Router } from '@angular/router';
import { forkJoin } from 'rxjs';
import { finalize, take } from 'rxjs/operators';

import { AdminMessagesApiService } from '@domains/admin/data/api/admin-messages-api.service';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminContactMessage, AdminDashboardSummary, AdminMediaFile } from '@domains/admin/model/admin.model';
import { AdminOverviewTabComponent } from '@domains/admin/ui/tabs/admin-overview-tab.component';

@Component({
  selector: 'app-admin-overview-page',
  standalone: true,
  imports: [CommonModule, AdminOverviewTabComponent],
  templateUrl: './admin-overview.page.html',
})
export class AdminOverviewPageComponent implements OnInit {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly messagesApi = inject(AdminMessagesApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly router = inject(Router);

  protected isLoading = true;
  protected errorMessage = '';
  protected dashboard: AdminDashboardSummary = {
    projects: 0,
    blogPosts: 0,
    unreadMessages: 0,
    skills: 0,
    skillCategories: 0,
    mediaFiles: 0,
    experiences: 0,
    navigationItems: 0,
    blogTags: 0,
    adminUsers: 0,
    githubSnapshots: 0,
  };
  protected messages: AdminContactMessage[] = [];
  protected mediaFiles: AdminMediaFile[] = [];

  ngOnInit(): void {
    this.loadOverview();
  }

  protected openTab(tabId: 'media' | 'messages'): void {
    void this.router.navigate(['/admin', tabId]);
  }

  private loadOverview(): void {
    this.isLoading = true;
    this.errorMessage = '';

    forkJoin({
      dashboard: this.overviewApi.getDashboardSummary(),
      referenceData: this.overviewApi.getReferenceData(),
      messages: this.messagesApi.getContactMessages(),
    })
      .pipe(
        take(1),
        finalize(() => {
          this.isLoading = false;
          this.changeDetectorRef.detectChanges();
        }),
      )
      .subscribe({
        next: ({ dashboard, referenceData, messages }) => {
          this.dashboard = dashboard;
          this.mediaFiles = referenceData.mediaFiles;
          this.messages = messages.items;
        },
        error: (error) => {
          if (error?.status === 401) {
            this.adminSession.logout();
            return;
          }

          this.errorMessage = 'The admin overview could not be loaded. Check that the API is running and that your admin token is still valid.';
        },
      });
  }
}
