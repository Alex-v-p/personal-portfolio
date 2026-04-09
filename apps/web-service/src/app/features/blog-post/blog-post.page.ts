import { Component, inject } from '@angular/core';
import { NgFor } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { BLOG_POSTS } from '../../shared/mock-data/blog-posts.mock';
import { BlogPost } from '../../shared/models/blog-post.model';

@Component({
  selector: 'app-blog-post-page',
  standalone: true,
  imports: [NgFor, RouterLink, UiChipComponent],
  templateUrl: './blog-post.page.html'
})
export class BlogPostPageComponent {
  private readonly route = inject(ActivatedRoute);

  protected readonly shareMarks = ['in', 'x'];

  protected get slug(): string {
    return this.route.snapshot.paramMap.get('slug') ?? BLOG_POSTS[0].slug;
  }

  protected get post(): BlogPost {
    return BLOG_POSTS.find((post) => post.slug === this.slug) ?? {
      id: 'fallback-post',
      slug: this.slug,
      title: this.slug.replace(/-/g, ' ') || 'Blog Post',
      excerpt: 'Fallback mock blog post content.',
      publishedAt: 'July 29, 2025',
      readTime: '5 min read',
      readingTimeMinutes: 5,
      category: 'General',
      tags: ['Fallback'],
      featured: false,
      isFeatured: false,
      coverAlt: 'Fallback blog cover',
      coverImageAlt: 'Fallback blog cover',
      status: 'published',
      intro: ['This fallback article exists so any mock slug still renders inside the designed layout.'],
      sections: []
    };
  }
}
