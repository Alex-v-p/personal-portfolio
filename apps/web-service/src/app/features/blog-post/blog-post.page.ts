import { Component, inject } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';

@Component({
  selector: 'app-blog-post-page',
  standalone: true,
  imports: [TitleCasePipe, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  template: `
    <div class="max-w-4xl space-y-6">
      <app-ui-link-button routerLink="/blog" appearance="ghost">← Back to blog</app-ui-link-button>

      <app-ui-card padding="lg" [featured]="true">
        <div class="space-y-4">
          <div class="flex flex-wrap gap-3">
            <app-ui-chip tone="accent">Blog post route</app-ui-chip>
            <app-ui-chip>{{ slug | titlecase }}</app-ui-chip>
          </div>

          <div>
            <p class="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">Blog detail</p>
            <h1 class="m-0 text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl">{{ slug | titlecase }}</h1>
          </div>

          <div class="min-h-72 rounded-3xl border border-stone-200 bg-gradient-to-b from-stone-500/15 to-stone-600/30"></div>

          <p class="m-0 text-base leading-8 text-stone-600">
            This placeholder verifies that the single-post page exists and uses the same global shell as the rest of the portfolio.
            Real article content and content-format decisions can slot in during Stage 5.
          </p>
        </div>
      </app-ui-card>
    </div>
  `
})
export class BlogPostPageComponent {
  private readonly route = inject(ActivatedRoute);

  protected readonly slug = (this.route.snapshot.paramMap.get('slug') ?? 'blog-post').replace(/-/g, ' ');
}
