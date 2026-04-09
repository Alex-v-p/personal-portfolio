import { NgFor } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiCardComponent } from '../../../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../../../shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '../../../../shared/components/section-title/ui-section-title.component';
import { ProjectCardComponent } from '../../../projects/components/project-card/project-card.component';
import { BlogPost } from '../../../../shared/models/blog-post.model';
import { Project } from '../../../../shared/models/project.model';

@Component({
  selector: 'app-home-featured-section',
  standalone: true,
  imports: [NgFor, UiCardComponent, UiChipComponent, UiLinkButtonComponent, UiSectionTitleComponent, ProjectCardComponent],
  templateUrl: './home-featured.component.html'
})
export class HomeFeaturedSectionComponent {
  @Input({ required: true }) featuredBlogPost!: BlogPost;
  @Input({ required: true }) primaryProject!: Project;
}
