import { NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { StatItem } from '@domains/stats/model/stat-item.model';

@Component({
  selector: 'app-stat-card',
  standalone: true,
  imports: [NgIf, UiButtonComponent, UiCardComponent],
  templateUrl: './stat-card.component.html'
})
export class StatCardComponent {
  @Input({ required: true }) item!: StatItem;
  @Input() tone: 'default' | 'muted' | 'highlight' = 'default';
  @Input() align: 'left' | 'center' = 'left';
  @Input() size: 'md' | 'lg' = 'md';

  protected get contentClasses(): string {
    const alignment = this.align === 'center' ? 'text-center items-center' : 'text-left items-start';
    const spacing = this.size === 'lg' ? 'gap-5 min-h-[16rem] justify-center' : 'gap-4 min-h-[11rem] justify-between';

    return `flex h-full flex-col ${alignment} ${spacing}`;
  }

  protected get valueClasses(): string {
    if (this.size === 'lg') {
      return 'text-5xl font-semibold leading-none tracking-tight ui-text-strong sm:text-6xl';
    }

    return 'text-4xl font-semibold leading-none tracking-tight ui-text-strong';
  }

  protected get wrapperClasses(): string {
    const tones = {
      default: '',
      muted: '[&_article]:border-transparent [&_article]:bg-[var(--ui-surface-muted)] [&_article]:shadow-none',
      highlight: '[&_article]:border-[color:var(--ui-border)] [&_article]:bg-[linear-gradient(135deg,var(--ui-surface-muted),var(--ui-surface-strong))] [&_article]:shadow-[var(--ui-shadow-panel)]'
    } as const;

    return tones[this.tone];
  }
}
