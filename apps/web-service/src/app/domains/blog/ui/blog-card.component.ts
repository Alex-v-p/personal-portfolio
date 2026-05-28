import { NgFor, NgIf } from '@angular/common';
import { Component, Input, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

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
  imports: [NgFor, NgIf, RouterLink, TranslatePipe, UiCardComponent, UiChipComponent, HighlightChipComponent, UiLinkButtonComponent],
  templateUrl: './blog-card.component.html'
})
export class BlogCardComponent {
  private readonly i18n = inject(I18nService);
  private readonly router = inject(Router);

  @Input({ required: true }) post!: BlogPostSummary;
  @Input() featured = false;
  @Input() showSecondaryAction = true;

  protected areTagsExpanded = false;

  private get tagPreviewLimit(): number {
    return this.featured ? 4 : 3;
  }

  protected get articleRouterLink(): string | readonly string[] {
    return this.i18n.localizeRouterCommands(['/blog', this.post.slug]) ?? ['/blog', this.post.slug];
  }

  protected get articleAriaLabel(): string {
    return `${this.i18n.translate('common.actions.readArticle')}: ${this.post.title}`;
  }

  protected get displayedTags(): string[] {
    return this.areTagsExpanded ? this.post.tags : this.post.tags.slice(0, this.tagPreviewLimit);
  }

  protected get hiddenTagCount(): number {
    return Math.max(this.post.tags.length - this.tagPreviewLimit, 0);
  }

  protected get shouldShowTagToggle(): boolean {
    return this.post.tags.length > this.tagPreviewLimit;
  }

  protected get tagToggleLabel(): string {
    if (this.areTagsExpanded) {
      return this.i18n.translate('common.actions.showLess');
    }

    return this.i18n.translate('common.actions.showMoreCount', { count: this.hiddenTagCount });
  }

  protected toggleTags(event?: Event): void {
    event?.preventDefault();
    event?.stopPropagation();
    this.areTagsExpanded = !this.areTagsExpanded;
  }

  protected openArticleCard(event: Event): void {
    if (this.isNestedInteractiveTarget(event)) {
      return;
    }

    event.preventDefault();
    this.navigateToArticle();
  }

  protected navigateToArticle(): void {
    const routerLink = this.articleRouterLink;

    if (typeof routerLink === 'string') {
      this.router.navigateByUrl(routerLink);
      return;
    }

    this.router.navigate([...routerLink]);
  }

  private isNestedInteractiveTarget(event: Event): boolean {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return false;
    }

    const currentTarget = event.currentTarget instanceof HTMLElement ? event.currentTarget : null;
    const interactiveTarget = target.closest('a, button, input, label, select, textarea, [role="button"], [data-blog-card-interactive]');

    return !!interactiveTarget && interactiveTarget !== currentTarget;
  }

  protected get placeholderLabel(): string {
    return this.post.coverImageAlt || this.post.coverAlt || this.i18n.translate('pages.blog.card.placeholder');
  }
}
