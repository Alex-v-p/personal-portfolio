import { NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiButtonComponent } from '../../../../shared/components/button/ui-button.component';
import { UiCardComponent } from '../../../../shared/components/card/ui-card.component';
import { StatItem } from '../../../../shared/models/stat-item.model';

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
      return 'text-5xl font-semibold leading-none tracking-tight text-stone-950 sm:text-6xl';
    }

    return 'text-4xl font-semibold leading-none tracking-tight text-stone-950';
  }

  protected get wrapperClasses(): string {
    const tones = {
      default: '',
      muted: '[&_article]:border-stone-200 [&_article]:bg-stone-200/65 [&_article]:shadow-none',
      highlight: '[&_article]:border-stone-300 [&_article]:bg-gradient-to-br [&_article]:from-stone-100 [&_article]:to-white [&_article]:shadow-[0_20px_60px_rgba(40,31,20,0.08)]'
    } as const;

    return tones[this.tone];
  }
}
