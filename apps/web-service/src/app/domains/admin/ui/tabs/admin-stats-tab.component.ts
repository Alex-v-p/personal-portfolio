import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminGithubSnapshot } from '@domains/admin/model/admin.model';
import { AdminGithubSnapshotForm } from '@domains/admin/model/forms/index';
import { contributionPreview } from '@domains/admin/shell/state/admin-page.display.utils';

@Component({
  selector: 'app-admin-stats-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-stats-tab.component.html'
})
export class AdminStatsTabComponent {
  @Input({ required: true }) githubSnapshots: AdminGithubSnapshot[] = [];
  @Input() selectedGithubSnapshotId: string | null = null;
  @Input({ required: true }) githubSnapshotForm!: AdminGithubSnapshotForm;
  @Input() isRefreshingGithub = false;

  @Output() readonly githubSnapshotSelected = new EventEmitter<string>();
  @Output() readonly newGithubSnapshotStarted = new EventEmitter<void>();
  @Output() readonly githubRefreshRequested = new EventEmitter<void>();
  @Output() readonly githubSnapshotSaved = new EventEmitter<void>();
  @Output() readonly githubSnapshotDeleted = new EventEmitter<void>();

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
}
