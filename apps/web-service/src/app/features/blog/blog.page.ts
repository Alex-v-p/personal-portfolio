import { NgFor, NgIf } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiEmptyStateComponent } from '../../shared/components/empty-state/ui-empty-state.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { BLOG_POSTS } from '../../shared/mock-data/blog-posts.mock';
import { BlogPost } from '../../shared/models/blog-post.model';

@Component({
  selector: 'app-blog-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, UiCardComponent, UiChipComponent, UiEmptyStateComponent, UiLinkButtonComponent],
  templateUrl: './blog.page.html'
})
export class BlogPageComponent {
  protected readonly totalPostCount = BLOG_POSTS.length;
  protected readonly pagerDots = [1, 2, 3];
  protected readonly filters = ['All', ...new Set(BLOG_POSTS.map((post) => post.category))];

  protected searchQuery = '';
  protected activeFilter = 'All';

  protected setFilter(filter: string): void {
    this.activeFilter = filter;
  }

  protected get filteredPosts(): BlogPost[] {
    return BLOG_POSTS
      .filter((post) => this.activeFilter === 'All' || post.category === this.activeFilter)
      .filter((post) => {
        const query = this.searchQuery.trim().toLowerCase();

        if (!query) {
          return true;
        }

        const haystack = [post.title, post.excerpt, post.category, ...post.tags].join(' ').toLowerCase();
        return haystack.includes(query);
      });
  }
}
