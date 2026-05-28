import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnDestroy, OnInit, inject } from '@angular/core';
import { Subscription, timer } from 'rxjs';
import { finalize, switchMap, take, takeWhile } from 'rxjs/operators';

import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminTasksApiService } from '@domains/admin/data/api/admin-tasks-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminAssistantKnowledgeStatus, AdminAsyncTaskAccepted } from '@domains/admin/model/admin.model';
import { AdminAssistantTabComponent } from '@domains/admin/ui/tabs/admin-assistant-tab.component';

@Component({
  selector: 'app-admin-assistant-page',
  standalone: true,
  imports: [CommonModule, AdminAssistantTabComponent],
  templateUrl: './admin-assistant.page.html',
})
export class AdminAssistantPageComponent implements OnInit, OnDestroy {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly tasksApi = inject(AdminTasksApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  private rebuildTaskSubscription?: Subscription;

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

  ngOnDestroy(): void {
    this.rebuildTaskSubscription?.unsubscribe();
  }

  protected reload(): void {
    this.loadAssistantStatus(true);
  }

  protected rebuildAssistantKnowledge(): void {
    this.isRebuildingAssistantKnowledge = true;
    this.statusMessage = '';

    this.overviewApi.rebuildAssistantKnowledge().pipe(take(1)).subscribe({
      next: (response) => {
        if (this.isAsyncTaskAccepted(response)) {
          this.statusMessage = 'Assistant knowledge rebuild queued. Waiting for the worker to finish indexing…';
          this.pollAssistantRebuildTask(response.taskId, response.pollAfterMs);
          return;
        }

        this.assistantKnowledgeStatus = response;
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


  private pollAssistantRebuildTask(taskId: string, pollAfterMs: number): void {
    this.rebuildTaskSubscription?.unsubscribe();
    this.rebuildTaskSubscription = timer(pollAfterMs, pollAfterMs)
      .pipe(
        switchMap(() => this.tasksApi.getTask(taskId)),
        takeWhile((task) => task.status === 'queued' || task.status === 'running', true),
      )
      .subscribe({
        next: (task) => {
          if (task.status === 'succeeded') {
            this.statusMessage = 'Assistant knowledge index rebuilt from the latest portfolio content.';
            this.refreshAssistantKnowledgeStatus();
            return;
          }

          if (task.status === 'failed') {
            this.isRebuildingAssistantKnowledge = false;
            this.statusMessage = task.errorMessage || 'Rebuilding the assistant knowledge index failed.';
            this.changeDetectorRef.detectChanges();
          }
        },
        error: (error) => {
          if (error?.status === 401) {
            this.adminSession.logout();
            return;
          }

          this.isRebuildingAssistantKnowledge = false;
          this.statusMessage = error?.error?.detail || 'Checking assistant rebuild progress failed.';
          this.changeDetectorRef.detectChanges();
        },
      });
  }

  private isAsyncTaskAccepted(value: AdminAssistantKnowledgeStatus | AdminAsyncTaskAccepted): value is AdminAsyncTaskAccepted {
    return !!value && typeof value === 'object' && 'taskId' in value;
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
