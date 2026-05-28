import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-card',
  standalone: true,
  templateUrl: './ui-card.component.html'
})
export class UiCardComponent {
  @Input() padding: 'none' | 'sm' | 'md' | 'lg' = 'md';
  @Input() featured = false;

  protected get cardClasses(): string {
    const base = 'min-w-0 ui-card-surface';
    const padding =
      this.padding === 'none' ? 'p-0' :
      this.padding === 'sm' ? 'p-4' :
      this.padding === 'lg' ? 'p-8' :
      'p-6';

    const featured = this.featured ? ' ui-card-featured' : '';

    return `${base} ${padding}${featured}`;
  }
}