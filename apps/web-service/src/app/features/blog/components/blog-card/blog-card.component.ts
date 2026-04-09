import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiCardComponent } from '../../../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../../../shared/components/link-button/ui-link-button.component';
import { BlogPost } from '../../../../shared/models/blog-post.model';

@Component({
  selector: 'app-blog-card',
  standalone: true,
  imports: [NgFor, NgIf, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './blog-card.component.html'
})
export class BlogCardComponent {
  @Input({ required: true }) post!: BlogPost;
  @Input() featured = false;

  protected get displayedTags(): string[] {
    return this.post.tags.slice(0, this.featured ? 4 : 3);
  }

  protected get placeholderLabel(): string {
    return this.post.coverImageAlt || this.post.coverAlt || 'Blog post cover placeholder';
  }
}
