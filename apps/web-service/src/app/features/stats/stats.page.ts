import { Component } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { CONTRIBUTION_CELLS, GITHUB_SUMMARY, LATEST_GITHUB_SNAPSHOT, PORTFOLIO_STATS } from '../../shared/mock-data/stats.mock';

@Component({
  selector: 'app-stats-page',
  standalone: true,
  imports: [NgFor, NgIf, UiButtonComponent, UiCardComponent],
  templateUrl: './stats.page.html'
})
export class StatsPageComponent {
  protected readonly contributionCells = CONTRIBUTION_CELLS;
  protected readonly githubSummary = GITHUB_SUMMARY;
  protected readonly latestGithubSnapshot = LATEST_GITHUB_SNAPSHOT;
  protected readonly portfolioStats = PORTFOLIO_STATS;

  protected getContributionClass(value: number): string {
    const base = 'h-4 w-4 rounded-[2px]';
    const tones = [
      'bg-stone-200',
      'bg-lime-100',
      'bg-lime-200',
      'bg-lime-400',
      'bg-lime-600'
    ];

    return `${base} ${tones[value] ?? tones[0]}`;
  }
}
