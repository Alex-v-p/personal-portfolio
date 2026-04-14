import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '@shared/components/section-title/ui-section-title.component';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { ProjectSummary } from '@domains/projects/model/project-summary.model';
import { ProjectCardComponent } from '@domains/projects/ui/project-card.component';

@Component({
  selector: 'app-home-featured-section',
  standalone: true,
  imports: [NgFor, NgIf, UiCardComponent, UiChipComponent, UiLinkButtonComponent, UiSectionTitleComponent, ProjectCardComponent],
  templateUrl: './home-featured.component.html'
})
export class HomeFeaturedSectionComponent {
  @Input({ required: true }) featuredBlogPost!: BlogPostSummary;
  @Input({ required: true }) primaryProject!: ProjectSummary;

  protected get hasFeaturedBlogPost(): boolean {
    return Boolean(this.featuredBlogPost?.title);
  }

  protected get hasPrimaryProject(): boolean {
    return Boolean(this.primaryProject?.title);
  }
}
