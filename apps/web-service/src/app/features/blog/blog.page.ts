import { Component } from '@angular/core';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '../../shared/components/section-title/ui-section-title.component';

@Component({
  selector: 'app-blog-page',
  standalone: true,
  imports: [UiCardComponent, UiChipComponent, UiLinkButtonComponent, UiSectionTitleComponent],
  template: `
    <div class="space-y-12 md:space-y-14">
      <app-ui-section-title
        eyebrow="Blog"
        title="Blog overview route is in place"
        description="The overview page already matches the shared shell. Individual posts can now hang off the /blog/:slug route without changing the app frame."
      ></app-ui-section-title>

      <section class="grid gap-5 md:grid-cols-2">
        <app-ui-card>
          <div class="grid gap-4">
            <div class="flex flex-wrap gap-3">
              <app-ui-chip tone="accent">Featured</app-ui-chip>
              <app-ui-chip>5 min read</app-ui-chip>
            </div>
            <h2 class="m-0 text-[1.35rem] font-semibold tracking-tight text-stone-900">First placeholder post</h2>
            <p class="m-0 text-base leading-7 text-stone-600">A lightweight card placeholder proves the blog list layout and route transitions before real content arrives.</p>
            <app-ui-link-button routerLink="/blog/first-placeholder-post" appearance="ghost">Open post</app-ui-link-button>
          </div>
        </app-ui-card>

        <app-ui-card>
          <div class="grid gap-4">
            <div class="flex flex-wrap gap-3">
              <app-ui-chip>Draft layout</app-ui-chip>
              <app-ui-chip>Reusable card</app-ui-chip>
            </div>
            <h2 class="m-0 text-[1.35rem] font-semibold tracking-tight text-stone-900">Second placeholder post</h2>
            <p class="m-0 text-base leading-7 text-stone-600">The actual post feed, metadata, excerpts, and filters can be layered on during the dedicated blog stage.</p>
            <app-ui-link-button routerLink="/blog/second-placeholder-post" appearance="ghost">Open post</app-ui-link-button>
          </div>
        </app-ui-card>
      </section>
    </div>
  `
})
export class BlogPageComponent {}
