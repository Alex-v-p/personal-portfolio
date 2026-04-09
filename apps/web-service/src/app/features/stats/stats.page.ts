import { Component } from '@angular/core';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiSectionTitleComponent } from '../../shared/components/section-title/ui-section-title.component';

@Component({
  selector: 'app-stats-page',
  standalone: true,
  imports: [UiCardComponent, UiChipComponent, UiSectionTitleComponent],
  template: `
    <div class="space-y-12 md:space-y-14">
      <app-ui-section-title
        eyebrow="Stats"
        title="Stats route is wired and ready"
        description="This page matches the MVP route plan and can grow into metric cards or GitHub activity later without reshaping the app shell."
      ></app-ui-section-title>

      <section class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <app-ui-card [featured]="true">
          <div class="grid gap-4">
            <app-ui-chip tone="accent">Public repos</app-ui-chip>
            <strong class="text-5xl font-semibold leading-none tracking-tight text-stone-900">—</strong>
            <p class="m-0 text-base leading-7 text-stone-600">Placeholder metric</p>
          </div>
        </app-ui-card>

        <app-ui-card>
          <div class="grid gap-4">
            <app-ui-chip>Portfolio views</app-ui-chip>
            <strong class="text-5xl font-semibold leading-none tracking-tight text-stone-900">—</strong>
            <p class="m-0 text-base leading-7 text-stone-600">Placeholder metric</p>
          </div>
        </app-ui-card>

        <app-ui-card>
          <div class="grid gap-4">
            <app-ui-chip>Blog posts</app-ui-chip>
            <strong class="text-5xl font-semibold leading-none tracking-tight text-stone-900">—</strong>
            <p class="m-0 text-base leading-7 text-stone-600">Placeholder metric</p>
          </div>
        </app-ui-card>
      </section>
    </div>
  `
})
export class StatsPageComponent {}
