import { Component } from '@angular/core';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '../../shared/components/section-title/ui-section-title.component';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [UiButtonComponent, UiCardComponent, UiChipComponent, UiLinkButtonComponent, UiSectionTitleComponent],
  template: `
    <div class="space-y-12 md:space-y-14">
      <section class="grid items-center gap-6 lg:grid-cols-[minmax(0,1.2fr)_minmax(18rem,0.9fr)]">
        <div class="space-y-4">
          <app-ui-section-title
            eyebrow="Home"
            title="A clean portfolio shell is ready to build on"
            description="Stage 1 gives the project a stable frame: shared navigation, reusable UI pieces, and all MVP routes wired up so future content drops into place cleanly."
          ></app-ui-section-title>

          <div class="flex flex-wrap gap-3" aria-label="Preview technology tags">
            <app-ui-chip tone="accent">Angular</app-ui-chip>
            <app-ui-chip>Nx workspace</app-ui-chip>
            <app-ui-chip>Standalone components</app-ui-chip>
          </div>

          <div class="flex flex-wrap gap-3">
            <app-ui-link-button routerLink="/projects" appearance="primary">View projects</app-ui-link-button>
            <app-ui-link-button routerLink="/contact">Contact me</app-ui-link-button>
            <app-ui-button appearance="ghost" [disabled]="true">CMS comes later</app-ui-button>
          </div>
        </div>

        <app-ui-card [featured]="true" padding="lg">
          <div class="grid min-h-80 place-items-center gap-6">
            <div class="aspect-[4/5] w-full max-w-72 rounded-[2rem] border border-stone-300 bg-gradient-to-b from-stone-500/15 to-stone-600/30 shadow-[1rem_1rem_0_rgba(112,103,92,0.22)]"></div>
            <div class="grid w-full max-w-80 gap-3">
              <div class="h-4 w-[90%] rounded-full bg-stone-500/20"></div>
              <div class="h-4 rounded-full bg-stone-500/20"></div>
              <div class="h-4 w-[55%] rounded-full bg-stone-500/20"></div>
              <div class="flex gap-3">
                <span class="inline-block h-8 w-18 rounded-full bg-stone-500/20"></span>
                <span class="inline-block h-8 w-18 rounded-full bg-stone-500/20"></span>
                <span class="inline-block h-8 w-18 rounded-full bg-stone-500/20"></span>
              </div>
            </div>
          </div>
        </app-ui-card>
      </section>

      <section class="grid gap-5 md:grid-cols-2">
        <app-ui-card>
          <p class="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">Shared sections</p>
          <h2 class="mb-3 text-[1.35rem] font-semibold tracking-tight text-stone-900">Global shell pieces</h2>
          <p class="m-0 text-base leading-7 text-stone-600">The navbar, footer, page container, and spacing system are now consistent across the whole portfolio.</p>
        </app-ui-card>

        <app-ui-card>
          <p class="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">Shared components</p>
          <h2 class="mb-3 text-[1.35rem] font-semibold tracking-tight text-stone-900">Reusable primitives</h2>
          <p class="m-0 text-base leading-7 text-stone-600">Buttons, section titles, chips, cards, link buttons, and empty states are available for later stages.</p>
        </app-ui-card>
      </section>
    </div>
  `
})
export class HomePageComponent {}
