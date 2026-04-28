import { NgFor, NgIf } from '@angular/common';
import { Component, Input, inject } from '@angular/core';

import { I18nService } from '@core/i18n/i18n.service';
import { TranslatePipe } from '@core/i18n/translate.pipe';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '@shared/components/section-title/ui-section-title.component';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { ProjectSummary } from '@domains/projects/model/project-summary.model';
import { ProjectCardComponent } from '@domains/projects/ui/project-card.component';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-home-featured-section',
  standalone: true,
  imports: [NgFor, NgIf, RouterLink, TranslatePipe, UiCardComponent, UiChipComponent, HighlightChipComponent, UiLinkButtonComponent, UiSectionTitleComponent, ProjectCardComponent],
  templateUrl: './home-featured.component.html'
})
export class HomeFeaturedSectionComponent {
  private readonly i18n = inject(I18nService);

  @Input({ required: true }) featuredBlogPost!: BlogPostSummary;
  @Input({ required: true }) primaryProject!: ProjectSummary;

  protected get hasFeaturedBlogPost(): boolean {
    return Boolean(this.featuredBlogPost?.title);
  }

  protected get hasPrimaryProject(): boolean {
    return Boolean(this.primaryProject?.title);
  }

  protected get featuredBlogArticleRouterLink(): string | readonly string[] {
    return this.i18n.localizeRouterCommands(['/blog', this.featuredBlogPost.slug]) ?? ['/blog', this.featuredBlogPost.slug];
  }

  protected get featuredBlogImageAriaLabel(): string {
    return `${this.i18n.translate('common.actions.readArticle')}: ${this.featuredBlogPost.title}`;
  }

}
