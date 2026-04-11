import { Component, OnInit, inject } from '@angular/core';
import { NgFor } from '@angular/common';
import { take } from 'rxjs/operators';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { GithubSnapshot } from '../../shared/models/github-snapshot.model';
import { StatItem } from '../../shared/models/stat-item.model';
import { PublicPortfolioApiService } from '../../shared/services/public-portfolio-api.service';
import { StatCardComponent } from './components/stat-card/stat-card.component';

@Component({
  selector: 'app-stats-page',
  standalone: true,
  imports: [NgFor, UiCardComponent, StatCardComponent],
  templateUrl: './stats.page.html'
})
export class StatsPageComponent implements OnInit {
  private readonly portfolioApi = inject(PublicPortfolioApiService);

  protected contributionWeeks: number[][] = [];
  protected githubSummary: StatItem = { id: 'github-summary', label: 'GitHub activity', value: '0', description: '' };
  protected latestGithubSnapshot: GithubSnapshot = {
    id: '', snapshotDate: '', username: '', publicRepoCount: 0, followersCount: 0, followingCount: 0, totalStars: 0, totalCommits: 0, createdAt: '', contributionDays: []
  };
  protected portfolioHighlights: StatItem[] = [];
  protected portfolioStats: StatItem[] = [];
  protected monthLabels: string[] = [];
  protected weekdayLabels: string[] = [];

  ngOnInit(): void {
    this.portfolioApi.getStats().pipe(take(1)).subscribe({
      next: (stats) => {
        this.contributionWeeks = stats.contributionWeeks;
        this.githubSummary = stats.githubSummary;
        this.latestGithubSnapshot = stats.latestGithubSnapshot;
        this.portfolioHighlights = stats.portfolioHighlights;
        this.portfolioStats = stats.portfolioStats;
        this.monthLabels = stats.monthLabels;
        this.weekdayLabels = stats.weekdayLabels;
      }
    });
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
}
