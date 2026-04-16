import { Component, Input } from '@angular/core';
import { NgClass } from '@angular/common';

@Component({
  selector: 'app-ui-card',
  standalone: true,
  imports: [NgClass],
  templateUrl: './ui-card.component.html'
})
export class UiCardComponent {
  @Input() padding: 'none' | 'sm' | 'md' | 'lg' = 'md';
  @Input() featured = false;

  protected get cardClasses(): string {
    const base = 'min-w-0 ui-card-surface';
    const padding = this.padding === 'lg' ? 'p-8' : 'p-6';
    const featured = this.featured ? 'ui-card-featured' : '';

    return `${base} ${padding} ${featured}`.trim();
  }
}
