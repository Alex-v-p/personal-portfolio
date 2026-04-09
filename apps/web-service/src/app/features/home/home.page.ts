import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { FEATURED_BLOG_POSTS } from '../../shared/mock-data/blog-posts.mock';
import { CONTACT_METHODS } from '../../shared/mock-data/contact-links.mock';
import { EXPERIENCES, PROFILE } from '../../shared/mock-data/profile.mock';
import { FEATURED_PROJECT } from '../../shared/mock-data/projects.mock';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [NgFor, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './home.page.html'
})
export class HomePageComponent {
  protected readonly profile = PROFILE;
  protected readonly experiences = EXPERIENCES;
  protected readonly featuredProject = FEATURED_PROJECT;
  protected readonly featuredBlogPost = FEATURED_BLOG_POSTS[0];
  protected readonly contactPreviewMethods = CONTACT_METHODS.slice(0, 4);
}
