import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import {
  CONTRIBUTION_WEEKS,
  GITHUB_SUMMARY,
  LATEST_GITHUB_SNAPSHOT,
  PORTFOLIO_HIGHLIGHTS,
  PORTFOLIO_STATS
} from '../../shared/mock-data/stats.mock';
import { StatItem } from '../../shared/models/stat-item.model';
import { StatCardComponent } from './components/stat-card/stat-card.component';

@Component({
  selector: 'app-stats-page',
  standalone: true,
  imports: [NgFor, UiCardComponent, StatCardComponent],
  templateUrl: './stats.page.html'
})
export class StatsPageComponent {
  protected readonly contributionWeeks = CONTRIBUTION_WEEKS;
  protected readonly githubSummary = GITHUB_SUMMARY;
  protected readonly latestGithubSnapshot = LATEST_GITHUB_SNAPSHOT;
  protected readonly portfolioHighlights = PORTFOLIO_HIGHLIGHTS;
  protected readonly portfolioStats = PORTFOLIO_STATS;
  protected readonly monthLabels = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'];
  protected readonly weekdayLabels = ['Mon', '', 'Wed', '', 'Fri', '', ''];

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
