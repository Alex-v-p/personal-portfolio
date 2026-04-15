import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminGithubSnapshot, AdminGithubSnapshotsResponse } from '@domains/admin/model/admin.model';
import { AdminGithubSnapshotForm } from '@domains/admin/model/forms/index';
import { contributionPreview } from '@domains/admin/stats/state/admin-stats.state';
import { githubRefreshLabel, githubRefreshTone } from '@domains/admin/shared/state/admin-maintenance-display.utils';

@Component({
  selector: 'app-admin-stats-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-stats-tab.component.html'
})
export class AdminStatsTabComponent {
  @Input({ required: true }) githubSnapshots: AdminGithubSnapshot[] = [];
  @Input() githubAutoRefresh: AdminGithubSnapshotsResponse | null = null;
  @Input() selectedGithubSnapshotId: string | null = null;
  @Input({ required: true }) githubSnapshotForm!: AdminGithubSnapshotForm;
  @Input() isRefreshingGithub = false;
  @Input() currentTimeMs = Date.now();

  @Output() readonly githubSnapshotSelected = new EventEmitter<string>();
  @Output() readonly newGithubSnapshotStarted = new EventEmitter<void>();
  @Output() readonly githubRefreshRequested = new EventEmitter<void>();
  @Output() readonly githubSnapshotSaved = new EventEmitter<void>();
  @Output() readonly githubSnapshotDeleted = new EventEmitter<void>();

  get selectedSnapshot(): AdminGithubSnapshot | null {
    return this.githubSnapshots.find((item) => item.id === this.selectedGithubSnapshotId) ?? null;
  }

  get scheduledHours(): string {
    return (((this.githubAutoRefresh?.autoRefreshIntervalSeconds ?? 0) || 0) / 3600).toFixed(0);
  }

  get totalContributionDays(): number {
    return this.selectedSnapshot?.contributionDays.length ?? 0;
  }

  get statsKpis(): Array<{ label: string; value: string | number; hint: string }> {
    return [
      { label: 'Snapshots', value: this.githubSnapshots.length, hint: 'Saved GitHub records' },
      { label: 'Selected days', value: this.totalContributionDays, hint: 'Contribution cells in the selected snapshot' },
      { label: 'Refresh cadence', value: this.githubAutoRefresh?.autoRefreshIntervalSeconds ? `${this.scheduledHours}h` : 'Manual', hint: 'Automatic refresh schedule' },
      { label: 'Refresh status', value: this.githubRefreshLabel(this.selectedSnapshot), hint: this.githubAutoRefresh?.autoRefreshUsername || 'No auto-refresh username' },
    ];
  }

  selectGithubSnapshot(snapshotId: string): void {
    this.githubSnapshotSelected.emit(snapshotId);
  }

  startNewGithubSnapshot(): void {
    this.newGithubSnapshotStarted.emit();
  }

  refreshGithubSnapshot(): void {
    this.githubRefreshRequested.emit();
  }

  saveGithubSnapshot(): void {
    this.githubSnapshotSaved.emit();
  }

  deleteGithubSnapshot(): void {
    this.githubSnapshotDeleted.emit();
  }

  contributionPreview(snapshot: AdminGithubSnapshot): string {
    return contributionPreview(snapshot);
  }

  githubRefreshLabel(snapshot: AdminGithubSnapshot | null): string {
    if (snapshot) {
      return githubRefreshLabel(snapshot.autoRefreshStatus, snapshot.nextAutoRefreshAt, this.currentTimeMs);
    }

    return githubRefreshLabel(this.githubAutoRefresh?.autoRefreshStatus ?? 'disabled', this.githubAutoRefresh?.nextAutoRefreshAt, this.currentTimeMs);
  }

  githubRefreshTone(snapshot: AdminGithubSnapshot | null): string {
    if (snapshot) {
      return githubRefreshTone(snapshot.autoRefreshStatus, snapshot.nextAutoRefreshAt, this.currentTimeMs);
    }

    return githubRefreshTone(this.githubAutoRefresh?.autoRefreshStatus ?? 'disabled', this.githubAutoRefresh?.nextAutoRefreshAt, this.currentTimeMs);
  }
}
