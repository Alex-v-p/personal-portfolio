import { Component } from '@angular/core';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiEmptyStateComponent } from '../../shared/components/empty-state/ui-empty-state.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '../../shared/components/section-title/ui-section-title.component';

@Component({
  selector: 'app-contact-page',
  standalone: true,
  imports: [UiCardComponent, UiChipComponent, UiEmptyStateComponent, UiLinkButtonComponent, UiSectionTitleComponent],
  template: `
    <div class="space-y-12 md:space-y-14">
      <app-ui-section-title
        eyebrow="Contact"
        title="Contact route is ready for content"
        description="The low-fi structure now has a dedicated place for contact details, a form, and submission states without needing more layout work later."
      ></app-ui-section-title>

      <section class="grid gap-5 md:grid-cols-2">
        <app-ui-card [featured]="true">
          <div class="grid gap-4">
            <div class="flex flex-wrap gap-3">
              <app-ui-chip tone="accent">Email</app-ui-chip>
              <app-ui-chip>LinkedIn</app-ui-chip>
              <app-ui-chip>GitHub</app-ui-chip>
            </div>
            <p class="m-0 text-base leading-7 text-stone-600">This side can hold your direct contact details and social links in Stage 6.</p>
          </div>
        </app-ui-card>

        <app-ui-card>
          <app-ui-empty-state
            title="Form UI comes in Stage 6"
            description="This placeholder reserves the space for your name, email, and message fields while keeping the page route usable today."
            [hasActions]="true"
          >
            <div actions>
              <app-ui-link-button routerLink="/">Back home</app-ui-link-button>
            </div>
          </app-ui-empty-state>
        </app-ui-card>
      </section>
    </div>
  `
})
export class ContactPageComponent {}
