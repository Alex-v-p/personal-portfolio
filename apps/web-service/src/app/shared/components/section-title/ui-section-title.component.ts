import { Component, Input } from '@angular/core';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-ui-section-title',
  standalone: true,
  imports: [NgIf],
  template: `
    <header [class]="headerClasses">
      <p *ngIf="eyebrow" class="m-0 text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">{{ eyebrow }}</p>
      <h1 class="m-0 max-w-[18ch] text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl lg:text-[3.4rem] lg:leading-[1.02]">{{ title }}</h1>
      <p *ngIf="description" class="m-0 max-w-[62ch] text-base leading-7 text-stone-600">{{ description }}</p>
      <ng-content></ng-content>
    </header>
  `
})
export class UiSectionTitleComponent {
  @Input() eyebrow = '';
  @Input() title = '';
  @Input() description = '';
  @Input() align: 'left' | 'center' = 'left';

  protected get headerClasses(): string {
    const base = 'grid gap-3';
    return this.align === 'center' ? `${base} mx-auto justify-items-center text-center` : base;
  }
}
