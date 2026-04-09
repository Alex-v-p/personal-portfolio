import { NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-section-title',
  standalone: true,
  imports: [NgIf],
  templateUrl: './ui-section-title.component.html'
})
export class UiSectionTitleComponent {
  @Input() eyebrow = '';
  @Input() title = '';
  @Input() description = '';
  @Input() align: 'left' | 'center' = 'left';
  @Input() size: 'display' | 'section' = 'section';

  protected get headerClasses(): string {
    const base = 'grid gap-3';
    return this.align === 'center' ? `${base} mx-auto justify-items-center text-center` : base;
  }

  protected get titleClasses(): string {
    return this.size === 'display'
      ? 'm-0 max-w-[18ch] text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl lg:text-[3.4rem] lg:leading-[1.02]'
      : 'm-0 text-2xl font-semibold tracking-tight text-stone-950 sm:text-3xl';
  }
}
