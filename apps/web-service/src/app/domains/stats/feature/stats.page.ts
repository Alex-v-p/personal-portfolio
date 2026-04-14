import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { finalize, take } from 'rxjs/operators';

import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { GithubSnapshot } from '@domains/stats/model/github-snapshot.model';
import { StatItem } from '@domains/stats/model/stat-item.model';
import { PublicStatsApiService } from '@domains/stats/data/stats-api.service';
import { StatCardComponent } from '@domains/stats/ui/stat-card.component';

@Component({
  selector: 'app-stats-page',
  standalone: true,
  imports: [NgFor, NgIf, UiButtonComponent, UiCardComponent, UiEmptyStateComponent, UiSkeletonComponent, StatCardComponent],
  templateUrl: './stats.page.html'
})
export class StatsPageComponent implements OnInit {
  private readonly statsApi = inject(PublicStatsApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected contributionWeeks: number[][] = [];
  protected githubSummary: StatItem = { id: 'github-summary', label: 'GitHub activity', value: '0', description: '' };
  protected latestGithubSnapshot: GithubSnapshot = this.createEmptySnapshot();
  protected portfolioHighlights: StatItem[] = [];
  protected portfolioStats: StatItem[] = [];
  protected monthLabels: string[] = [];
  protected weekdayLabels: string[] = [];
  protected isLoading = true;
  protected errorMessage = '';

  ngOnInit(): void {
    this.loadStats();
  }

  protected loadStats(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.resetStats();

    this.statsApi
      .getStats()
      .pipe(
        take(1),
        finalize(() => {
          this.isLoading = false;
          this.changeDetectorRef.detectChanges();
        })
      )
      .subscribe({
        next: (stats) => {
          this.contributionWeeks = Array.isArray(stats.contributionWeeks) ? stats.contributionWeeks : [];
          this.githubSummary = stats.githubSummary ?? this.githubSummary;
          this.latestGithubSnapshot = stats.latestGithubSnapshot ?? this.createEmptySnapshot();
          this.portfolioHighlights = Array.isArray(stats.portfolioHighlights) ? stats.portfolioHighlights : [];
          this.portfolioStats = Array.isArray(stats.portfolioStats) ? stats.portfolioStats : [];
          this.monthLabels = Array.isArray(stats.monthLabels) ? stats.monthLabels : [];
          this.weekdayLabels = Array.isArray(stats.weekdayLabels) ? stats.weekdayLabels : [];
        },
        error: () => {
          this.resetStats();
          this.errorMessage = 'Stats could not be loaded from the portfolio API. Make sure the API or reverse proxy is running.';
        }
      });
  }

  protected get hasStatsData(): boolean {
    return Boolean(
      this.contributionWeeks.length ||
      this.portfolioHighlights.length ||
      this.portfolioStats.length ||
      this.latestGithubSnapshot.username ||
      this.latestGithubSnapshot.snapshotDate ||
      this.githubSummary.value !== '0'
    );
  }

  protected getContributionClass(value: number): string {
    const base = 'h-3.5 w-3.5 rounded-[4px] border border-white/30';
    const tones = [
      'bg-stone-200',
      'bg-lime-100',
      'bg-lime-200',
      'bg-lime-400',
      'bg-lime-600'
    ];

    return `${base} ${tones[value] ?? tones[0]}`;
  }

  protected trackByStatId(_: number, item: StatItem): string {
    return item.id;
  }

  protected trackByIndex(index: number): number {
    return index;
  }

  private resetStats(): void {
    this.contributionWeeks = [];
    this.githubSummary = { id: 'github-summary', label: 'GitHub activity', value: '0', description: '' };
    this.latestGithubSnapshot = this.createEmptySnapshot();
    this.portfolioHighlights = [];
    this.portfolioStats = [];
    this.monthLabels = [];
    this.weekdayLabels = [];
  }

  private createEmptySnapshot(): GithubSnapshot {
    return {
      id: '',
      snapshotDate: '',
      username: '',
      publicRepoCount: 0,
      followersCount: 0,
      followingCount: 0,
      totalStars: 0,
      totalCommits: 0,
      createdAt: '',
      contributionDays: []
    };
  }
}
