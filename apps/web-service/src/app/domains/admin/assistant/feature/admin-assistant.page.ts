import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { finalize, take } from 'rxjs/operators';

import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminAssistantKnowledgeStatus } from '@domains/admin/model/admin.model';
import { AdminAssistantTabComponent } from '@domains/admin/ui/tabs/admin-assistant-tab.component';

@Component({
  selector: 'app-admin-assistant-page',
  standalone: true,
  imports: [CommonModule, AdminAssistantTabComponent],
  templateUrl: './admin-assistant.page.html',
})
export class AdminAssistantPageComponent implements OnInit {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';
  protected isRebuildingAssistantKnowledge = false;
  protected assistantKnowledgeStatus: AdminAssistantKnowledgeStatus = {
    totalDocuments: 0,
    totalChunks: 0,
    documentsBySourceType: {},
    latestUpdatedAt: null,
  };

  ngOnInit(): void {
    this.loadAssistantStatus(false);
  }

  protected reload(): void {
    this.loadAssistantStatus(true);
  }

  protected rebuildAssistantKnowledge(): void {
    this.isRebuildingAssistantKnowledge = true;
    this.statusMessage = '';

    this.overviewApi.rebuildAssistantKnowledge().pipe(take(1)).subscribe({
      next: (status) => {
        this.assistantKnowledgeStatus = status;
        this.statusMessage = 'Assistant knowledge index rebuilt from the latest portfolio content.';
        this.refreshAssistantKnowledgeStatus();
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.isRebuildingAssistantKnowledge = false;
        this.statusMessage = error?.error?.detail || 'Rebuilding the assistant knowledge index failed.';
        this.changeDetectorRef.detectChanges();
      },
    });
  }

  private refreshAssistantKnowledgeStatus(): void {
    this.overviewApi.getAssistantKnowledgeStatus().pipe(take(1)).subscribe({
      next: (status) => {
        this.assistantKnowledgeStatus = status;
        this.isRebuildingAssistantKnowledge = false;
        this.changeDetectorRef.detectChanges();
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.isRebuildingAssistantKnowledge = false;
        this.changeDetectorRef.detectChanges();
      },
    });
  }

  private loadAssistantStatus(showReloadMessage: boolean): void {
    this.isLoading = true;
    this.errorMessage = '';
    if (showReloadMessage) {
      this.statusMessage = 'Refreshing assistant knowledge status…';
    }

    this.overviewApi.getAssistantKnowledgeStatus().pipe(
      take(1),
      finalize(() => {
        this.isLoading = false;
        this.changeDetectorRef.detectChanges();
      }),
    ).subscribe({
      next: (status) => {
        this.assistantKnowledgeStatus = status;
        if (showReloadMessage) {
          this.statusMessage = 'Assistant knowledge status refreshed.';
        }
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.errorMessage = error?.error?.detail || 'The assistant knowledge workspace could not be loaded.';
      },
    });
  }
}
