import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-chip',
  standalone: true,
  templateUrl: './ui-chip.component.html'
})
export class UiChipComponent {
  @Input() tone: 'default' | 'accent' = 'default';

  protected get chipClasses(): string {
    const base = 'inline-flex min-h-8 items-center gap-1.5 rounded-full border px-3 py-1 text-[0.82rem] font-semibold whitespace-nowrap';
    const variant = this.tone === 'accent'
      ? 'border-stone-300 bg-stone-200/75 text-stone-900'
      : 'border-stone-200 bg-white/75 text-stone-600';

    return `${base} ${variant}`;
  }
}
