import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { finalize, take } from 'rxjs/operators';

import { AdminStatsApiService } from '@domains/admin/data/api/admin-stats-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminGithubContributionDay, AdminGithubSnapshot } from '@domains/admin/model/admin.model';
import { AdminGithubSnapshotForm, createEmptyGithubSnapshotForm, toGithubSnapshotForm } from '@domains/admin/model/forms/index';
import { AdminStatsTabComponent } from '@domains/admin/ui/tabs/admin-stats-tab.component';
import { parseContributionDays, parseGithubRawPayload } from '@domains/admin/stats/state/admin-stats.state';
import { resolveSelection } from '@domains/admin/shell/state/admin-page.utils';

@Component({
  selector: 'app-admin-stats-page',
  standalone: true,
  imports: [CommonModule, AdminStatsTabComponent],
  templateUrl: './admin-stats.page.html',
})
export class AdminStatsPageComponent implements OnInit {
  private readonly statsApi = inject(AdminStatsApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';
  protected githubSnapshots: AdminGithubSnapshot[] = [];
  protected selectedGithubSnapshotId: string | null = null;
  protected githubSnapshotForm: AdminGithubSnapshotForm = createEmptyGithubSnapshotForm();
  protected isRefreshingGithub = false;

  ngOnInit(): void {
    this.loadStatsPage(false);
  }

  protected reload(): void {
    this.loadStatsPage(true);
  }

  protected selectGithubSnapshot(snapshotId: string): void {
    this.selectedGithubSnapshotId = snapshotId;
    const snapshot = this.githubSnapshots.find((item) => item.id === snapshotId);
    if (!snapshot) {
      return;
    }

    this.githubSnapshotForm = toGithubSnapshotForm(snapshot);
    this.statusMessage = '';
  }

  protected startNewGithubSnapshot(): void {
    this.selectedGithubSnapshotId = null;
    this.githubSnapshotForm = createEmptyGithubSnapshotForm();
    this.statusMessage = '';
  }

  protected refreshGithubSnapshot(): void {
    this.isRefreshingGithub = true;
    this.statusMessage = '';

    this.statsApi.refreshGithubSnapshot({
      username: this.githubSnapshotForm.username.trim() || null,
      pruneHistory: true,
    }).pipe(take(1)).subscribe({
      next: (snapshot) => {
        this.isRefreshingGithub = false;
        this.selectedGithubSnapshotId = snapshot.id;
        this.githubSnapshotForm = toGithubSnapshotForm(snapshot);
        this.statusMessage = 'GitHub stats refreshed from the latest public profile data.';
        this.loadStatsPage(false);
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.isRefreshingGithub = false;
        this.statusMessage = error?.error?.detail || 'Refreshing GitHub stats failed.';
        this.changeDetectorRef.detectChanges();
      },
    });
  }

  protected saveGithubSnapshot(): void {
    let rawPayload: Record<string, unknown> | null = null;
    let contributionDays: AdminGithubContributionDay[] = [];

    try {
      rawPayload = parseGithubRawPayload(this.githubSnapshotForm.rawPayloadText);
      contributionDays = parseContributionDays(this.githubSnapshotForm.contributionDaysText);
    } catch (error) {
      this.statusMessage = error instanceof Error ? error.message : 'GitHub snapshot JSON could not be parsed.';
      return;
    }

    const payload = {
      snapshotDate: this.githubSnapshotForm.snapshotDate,
      username: this.githubSnapshotForm.username,
      publicRepoCount: this.githubSnapshotForm.publicRepoCount,
      followersCount: this.githubSnapshotForm.followersCount,
      followingCount: this.githubSnapshotForm.followingCount,
      totalStars: this.githubSnapshotForm.totalStars,
      totalCommits: this.githubSnapshotForm.totalCommits,
      rawPayload,
      contributionDays,
    };

    const request$ = this.selectedGithubSnapshotId
      ? this.statsApi.updateGithubSnapshot(this.selectedGithubSnapshotId, payload)
      : this.statsApi.createGithubSnapshot(payload);

    request$.pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = this.selectedGithubSnapshotId ? 'GitHub snapshot updated.' : 'GitHub snapshot created.';
        this.loadStatsPage(false);
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.statusMessage = error?.error?.detail || 'Saving the GitHub snapshot failed.';
      },
    });
  }

  protected deleteGithubSnapshot(): void {
    if (!this.selectedGithubSnapshotId || !window.confirm('Delete this GitHub snapshot?')) {
      return;
    }

    this.statsApi.deleteGithubSnapshot(this.selectedGithubSnapshotId).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'GitHub snapshot deleted.';
        this.startNewGithubSnapshot();
        this.loadStatsPage(false);
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.statusMessage = error?.error?.detail || 'Deleting the GitHub snapshot failed.';
      },
    });
  }

  private loadStatsPage(showReloadMessage: boolean): void {
    const currentSelection = this.selectedGithubSnapshotId;
    this.isLoading = true;
    this.errorMessage = '';
    if (showReloadMessage) {
      this.statusMessage = 'Refreshing GitHub stats workspace…';
    }

    this.statsApi.getGithubSnapshots().pipe(
      take(1),
      finalize(() => {
        this.isLoading = false;
        this.changeDetectorRef.detectChanges();
      }),
    ).subscribe({
      next: (response) => {
        this.githubSnapshots = response.items;
        this.selectedGithubSnapshotId = resolveSelection(currentSelection, this.githubSnapshots);
        this.githubSnapshotForm = this.selectedGithubSnapshotId
          ? toGithubSnapshotForm(this.githubSnapshots.find((item) => item.id === this.selectedGithubSnapshotId)!)
          : createEmptyGithubSnapshotForm();

        if (showReloadMessage) {
          this.statusMessage = 'GitHub stats workspace refreshed.';
        }
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.errorMessage = error?.error?.detail || 'The GitHub stats workspace could not be loaded.';
      },
    });
  }
}
