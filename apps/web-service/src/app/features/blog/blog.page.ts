import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';

@Component({
  selector: 'app-blog-page',
  standalone: true,
  imports: [NgFor, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './blog.page.html'
})
export class BlogPageComponent {
  protected readonly filters = ['DevOps', 'UI/UX', 'Career'];
  protected readonly pagerDots = [1, 2, 3];

  protected readonly posts = [
    {
      badge: 'Featured',
      date: 'July 29, 2025',
      readTime: '5 min read',
      title: 'Title of the Blog Post',
      excerpt: 'Excerpt: reflections on cost tracking, architecture, and shipping better digital experiences.',
      slug: '/blog/title-of-the-blog-post'
    },
    {
      badge: 'Featured',
      date: 'July 29, 2025',
      readTime: '5 min read',
      title: 'Title of the Blog Post',
      excerpt: 'Excerpt: reflections on cost tracking, architecture, and shipping better digital experiences.',
      slug: '/blog/title-of-the-blog-post'
    }
  ];
}
