import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-chip',
  standalone: true,
  templateUrl: './ui-chip.component.html'
})
export class UiChipComponent {
  @Input() tone: 'default' | 'accent' = 'default';

  protected get chipClasses(): string {
    const base = 'ui-chip';
    return this.tone === 'accent' ? `${base} ui-chip-accent` : base;
  }
}
