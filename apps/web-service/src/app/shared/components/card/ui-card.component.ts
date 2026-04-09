import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-card',
  standalone: true,
  template: `
    <article [class]="cardClasses">
      <ng-content></ng-content>
    </article>
  `
})
export class UiCardComponent {
  @Input() padding: 'md' | 'lg' = 'md';
  @Input() featured = false;

  protected get cardClasses(): string {
    const base = 'min-w-0 rounded-[1.75rem] border border-stone-200 bg-white/85 shadow-[0_18px_48px_rgba(40,31,20,0.06)]';
    const padding = this.padding === 'lg' ? 'p-8' : 'p-6';
    const featured = this.featured
      ? 'border-stone-300 bg-gradient-to-b from-white/95 to-stone-100/90'
      : '';

    return `${base} ${padding} ${featured}`.trim();
  }
}
