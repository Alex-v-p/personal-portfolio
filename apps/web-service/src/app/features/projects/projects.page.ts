import { Component } from '@angular/core';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiEmptyStateComponent } from '../../shared/components/empty-state/ui-empty-state.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '../../shared/components/section-title/ui-section-title.component';

@Component({
  selector: 'app-projects-page',
  standalone: true,
  imports: [UiCardComponent, UiChipComponent, UiEmptyStateComponent, UiLinkButtonComponent, UiSectionTitleComponent],
  template: `
    <div class="space-y-12 md:space-y-14">
      <app-ui-section-title
        eyebrow="Projects"
        title="Projects route is ready"
        description="The listing route now exists inside the shared shell. Search, filtering, cards, and real content can plug in here during Stage 4."
      ></app-ui-section-title>

      <app-ui-card [featured]="true" padding="lg">
        <div class="space-y-4">
          <div class="flex flex-wrap gap-3">
            <app-ui-chip tone="accent">Featured layout</app-ui-chip>
            <app-ui-chip>Search comes in Stage 4</app-ui-chip>
            <app-ui-chip>Filters come in Stage 4</app-ui-chip>
          </div>

          <app-ui-empty-state
            title="No project data is wired in yet"
            description="This page now has a permanent route, a stable container, and reusable components. The real project cards will be added once mock data is introduced."
            [hasActions]="true"
          >
            <div actions>
              <app-ui-link-button routerLink="/blog">See the blog route</app-ui-link-button>
            </div>
          </app-ui-empty-state>
        </div>
      </app-ui-card>
    </div>
  `
})
export class ProjectsPageComponent {}
