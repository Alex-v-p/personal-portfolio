import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiCardComponent } from '../../shared/components/card/ui-card.component';

@Component({
  selector: 'app-stats-page',
  standalone: true,
  imports: [NgFor, UiButtonComponent, UiCardComponent],
  templateUrl: './stats.page.html'
})
export class StatsPageComponent {
  protected readonly contributionCells = [
    1,2,2,1,3,2,1, 2,3,2,1,1,2,3, 1,1,2,3,2,1,1, 2,2,3,1,4,2,1,
    1,2,1,2,3,1,2, 2,4,2,1,2,3,1, 1,2,3,2,1,2,3, 2,1,2,3,2,1,2,
    3,2,1,2,4,2,1, 1,2,3,1,2,2,3, 2,1,2,3,1,2,2, 1,2,3,2,1,2,3
  ];

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
