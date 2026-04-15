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
import { PublicEventsApiService } from '@domains/site-activity/data/events-api.service';
import { SiteTrackingService } from '@domains/site-activity/data/site-tracking.service';

const PORTFOLIO_LIKED_STORAGE_KEY = 'portfolio.stats.liked';

@Component({
  selector: 'app-stats-page',
  standalone: true,
  imports: [NgFor, NgIf, UiButtonComponent, UiCardComponent, UiEmptyStateComponent, UiSkeletonComponent],
  templateUrl: './stats.page.html'
})
export class StatsPageComponent implements OnInit {
  private readonly statsApi = inject(PublicStatsApiService);
  private readonly eventsApi = inject(PublicEventsApiService);
  private readonly siteTracking = inject(SiteTrackingService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected contributionWeeks: number[][] = [];
  protected githubSummary: StatItem = this.createStatItem('github-summary', 'Public repos', '0');
  protected latestGithubSnapshot: GithubSnapshot = this.createEmptySnapshot();
  protected portfolioViewsCard: StatItem = this.createStatItem('highlight-total-views', 'Total views', '0');
  protected portfolioLikesCard: StatItem = this.createStatItem('highlight-portfolio-likes', 'Like counter', '0', 'Love this portfolio');
  protected portfolioStats: StatItem[] = [];
  protected monthLabels: string[] = [];
  protected weekdayLabels: string[] = [];
  protected contributionLegend = [0, 1, 2, 3, 4];
  protected isLoading = true;
  protected isSubmittingLike = false;
  protected hasLikedPortfolio = false;
  protected errorMessage = '';
  protected likeErrorMessage = '';

  ngOnInit(): void {
    this.hasLikedPortfolio = this.readLikeState();
    this.loadStats();
  }

  protected loadStats(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.likeErrorMessage = '';
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
          this.portfolioViewsCard = this.findStat(stats.portfolioHighlights, 'highlight-total-views', 'Total views');
          this.portfolioLikesCard = this.findStat(
            stats.portfolioHighlights,
            'highlight-portfolio-likes',
            'Like counter',
            'Love this portfolio'
          );
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

  protected submitPortfolioLike(): void {
    if (this.isSubmittingLike || this.hasLikedPortfolio || typeof window === 'undefined') {
      return;
    }

    this.isSubmittingLike = true;
    this.likeErrorMessage = '';

    this.eventsApi
      .createSiteEvent({
        eventType: 'portfolio_like',
        pagePath: window.location.pathname || '/stats',
        visitorId: this.siteTracking.visitorId,
        sessionId: this.siteTracking.sessionId,
        referrer: document.referrer || null,
        metadata: {
          route: window.location.pathname || '/stats',
          source: 'public-stats-like-button'
        }
      })
      .pipe(
        take(1),
        finalize(() => {
          this.isSubmittingLike = false;
          this.changeDetectorRef.detectChanges();
        })
      )
      .subscribe({
        next: () => {
          this.hasLikedPortfolio = true;
          this.writeLikeState(true);
          this.portfolioLikesCard = {
            ...this.portfolioLikesCard,
            value: String(this.portfolioLikesCount + 1)
          };
        },
        error: () => {
          this.likeErrorMessage = 'Your like could not be saved right now. Please try again in a moment.';
        }
      });
  }

  protected get hasStatsData(): boolean {
    return Boolean(
      this.contributionWeeks.length ||
      this.monthLabels.length ||
      this.latestGithubSnapshot.username ||
      this.latestGithubSnapshot.snapshotDate ||
      this.githubSummary.value !== '0' ||
      this.portfolioViewsCard.value !== '0' ||
      this.portfolioLikesCard.value !== '0'
    );
  }

  protected get contributionGridColumns(): string {
    return `repeat(${Math.max(this.contributionWeeks.length, 1)}, minmax(0, 1fr))`;
  }

  protected get portfolioLikesCount(): number {
    return Number(this.portfolioLikesCard.value) || 0;
  }

  protected get likesButtonLabel(): string {
    if (this.hasLikedPortfolio) {
      return 'Thanks for the love';
    }

    return this.isSubmittingLike ? 'Saving like…' : this.portfolioLikesCard.actionLabel || 'Love this portfolio';
  }

  protected getContributionCellClass(value: number): string {
    const base = 'aspect-square w-full rounded-[4px] border border-white/30';
    const tones = ['bg-stone-200', 'bg-lime-100', 'bg-lime-200', 'bg-lime-400', 'bg-lime-600'];

    return `${base} ${tones[value] ?? tones[0]}`;
  }

  protected getContributionLegendClass(value: number): string {
    const base = 'h-3.5 w-3.5 rounded-[4px] border border-white/30';
    const tones = ['bg-stone-200', 'bg-lime-100', 'bg-lime-200', 'bg-lime-400', 'bg-lime-600'];

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
    this.githubSummary = this.createStatItem('github-summary', 'Public repos', '0');
    this.latestGithubSnapshot = this.createEmptySnapshot();
    this.portfolioViewsCard = this.createStatItem('highlight-total-views', 'Total views', '0');
    this.portfolioLikesCard = this.createStatItem('highlight-portfolio-likes', 'Like counter', '0', 'Love this portfolio');
    this.portfolioStats = [];
    this.monthLabels = [];
    this.weekdayLabels = [];
  }

  private findStat(items: StatItem[] | undefined, id: string, fallbackLabel: string, actionLabel?: string): StatItem {
    const found = items?.find((item) => item.id === id);
    return found ?? this.createStatItem(id, fallbackLabel, '0', actionLabel);
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

  private createStatItem(id: string, label: string, value: string, actionLabel?: string): StatItem {
    return {
      id,
      label,
      value,
      description: '',
      actionLabel
    };
  }

  private readLikeState(): boolean {
    if (typeof window === 'undefined') {
      return false;
    }
    return window.localStorage.getItem(PORTFOLIO_LIKED_STORAGE_KEY) === 'true';
  }

  private writeLikeState(value: boolean): void {
    if (typeof window === 'undefined') {
      return;
    }
    window.localStorage.setItem(PORTFOLIO_LIKED_STORAGE_KEY, String(value));
  }
}
