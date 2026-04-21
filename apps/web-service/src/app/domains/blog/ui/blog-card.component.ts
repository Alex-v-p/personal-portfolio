import { NgFor, NgIf } from '@angular/common';
import { Component, Input, inject } from '@angular/core';

import { I18nService } from '@core/i18n/i18n.service';
import { TranslatePipe } from '@core/i18n/translate.pipe';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';

@Component({
  selector: 'app-blog-card',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiCardComponent, UiChipComponent, HighlightChipComponent, UiLinkButtonComponent],
  templateUrl: './blog-card.component.html'
})
export class BlogCardComponent {
  private readonly i18n = inject(I18nService);

  @Input({ required: true }) post!: BlogPostSummary;
  @Input() featured = false;
  @Input() showSecondaryAction = true;

  protected get displayedTags(): string[] {
    return this.post.tags.slice(0, this.featured ? 4 : 3);
  }

  protected get placeholderLabel(): string {
    return this.post.coverImageAlt || this.post.coverAlt || this.i18n.translate('pages.blog.card.placeholder');
  }
}
