import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-chip',
  standalone: true,
  templateUrl: './ui-chip.component.html'
})
export class UiChipComponent {
  @Input() tone: 'default' | 'accent' | 'highlight' = 'default';

  protected get chipClasses(): string {
    const base = 'ui-chip';

    if (this.tone === 'accent') {
      return `${base} ui-chip-accent`;
    }

    if (this.tone === 'highlight') {
      return `${base} ui-chip-highlight`;
    }

    return base;
  }
}
