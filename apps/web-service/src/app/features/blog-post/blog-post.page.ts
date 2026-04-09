import { Component, inject } from '@angular/core';
import { NgFor } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';

interface BlogPostViewModel {
  title: string;
  date: string;
  readTime: string;
  tags: string[];
  intro: string[];
  sections: Array<{ heading: string; paragraphs: string[] }>;
}

@Component({
  selector: 'app-blog-post-page',
  standalone: true,
  imports: [NgFor, RouterLink, UiChipComponent],
  templateUrl: './blog-post.page.html'
})
export class BlogPostPageComponent {
  private readonly route = inject(ActivatedRoute);

  private readonly posts: Record<string, BlogPostViewModel> = {
    'title-of-the-blog-post': {
      title: 'Title of blogPost',
      date: 'July 29, 2025',
      readTime: '5 min read',
      tags: ['Tag', 'Tag', 'Tag'],
      intro: [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ut efficitur risus. Proin malesuada urna id interdum consectetur. Integer convallis pharetra nisi, quis semper augue eleifend a.',
        'Praesent augue eros, porttitor non ligula sed, laoreet sagittis augue. Etiam eleifend a ligula eget ornare.'
      ],
      sections: [
        {
          heading: 'Header Text',
          paragraphs: [
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ut efficitur risus. Proin malesuada urna id interdum consectetur. Integer convallis pharetra nisi, quis semper augue eleifend a.',
            'Duis suscipit massa at imperdiet scelerisque. Donec non convallis mauris. Aenean interdum dui quis leo dapibus dictum.'
          ]
        },
        {
          heading: 'Another Section',
          paragraphs: [
            'Use this layout for long-form content later. The key point for now is that the page already has all the content regions from your wireframe: metadata, tags, share actions, image, and article body.'
          ]
        }
      ]
    }
  };

  protected get slug(): string {
    return this.route.snapshot.paramMap.get('slug') ?? 'title-of-the-blog-post';
  }

  protected get post(): BlogPostViewModel {
    return this.posts[this.slug] ?? {
      title: this.slug.replace(/-/g, ' ') || 'Blog Post',
      date: 'July 29, 2025',
      readTime: '5 min read',
      tags: ['Tag'],
      intro: ['This fallback article exists so any slug still renders inside the designed layout.'],
      sections: []
    };
  }

  protected readonly shareMarks = ['in', 'x'];
}
