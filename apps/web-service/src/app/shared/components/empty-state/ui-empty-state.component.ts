import { Component, Input } from '@angular/core';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-ui-empty-state',
  standalone: true,
  imports: [NgIf],
  template: `
    <section class="grid justify-items-start gap-4 rounded-3xl border border-dashed border-stone-300 bg-stone-100/65 p-8">
      <div class="h-12 w-12 rounded-2xl border border-stone-300 bg-gradient-to-br from-stone-200 to-stone-300" aria-hidden="true"></div>
      <h2 class="m-0 text-xl font-semibold text-stone-900">{{ title }}</h2>
      <p class="m-0 max-w-[48ch] text-base leading-7 text-stone-600">{{ description }}</p>
      <div *ngIf="hasActions" class="flex flex-wrap gap-3">
        <ng-content select="[actions]"></ng-content>
      </div>
    </section>
  `
})
export class UiEmptyStateComponent {
  @Input() title = '';
  @Input() description = '';
  @Input() hasActions = false;
}
