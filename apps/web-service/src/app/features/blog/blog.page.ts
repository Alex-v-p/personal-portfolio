import { NgFor, NgIf } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { UiEmptyStateComponent } from '../../shared/components/empty-state/ui-empty-state.component';
import { BLOG_POSTS } from '../../shared/mock-data/blog-posts.mock';
import { BlogPost } from '../../shared/models/blog-post.model';
import { BlogCardComponent } from './components/blog-card/blog-card.component';

@Component({
  selector: 'app-blog-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, UiEmptyStateComponent, BlogCardComponent],
  templateUrl: './blog.page.html'
})
export class BlogPageComponent {
  protected readonly totalPostCount = BLOG_POSTS.length;
  protected readonly pagerDots = [1, 2, 3];
  protected readonly categories = ['All topics', ...new Set(BLOG_POSTS.map((post) => post.category))];

  protected searchQuery = '';
  protected selectedCategory = 'All topics';

  protected get filteredPosts(): BlogPost[] {
    const query = this.searchQuery.trim().toLowerCase();

    return BLOG_POSTS.filter((post) => {
      const matchesCategory = this.selectedCategory === 'All topics' || post.category === this.selectedCategory;
      if (!matchesCategory) {
        return false;
      }

      if (!query) {
        return true;
      }

      const haystack = [post.title, post.excerpt, post.category, post.contentMarkdown, ...post.tags].join(' ').toLowerCase();
      return haystack.includes(query);
    });
  }

  protected get featuredPosts(): BlogPost[] {
    return this.filteredPosts.filter((post) => post.isFeatured).slice(0, 1);
  }

  protected get browseablePosts(): BlogPost[] {
    const featuredIds = new Set(this.featuredPosts.map((post) => post.id));
    return this.filteredPosts.filter((post) => !featuredIds.has(post.id));
  }

  protected get hasActiveFilters(): boolean {
    return !!this.searchQuery.trim() || this.selectedCategory !== 'All topics';
  }

  protected resetFilters(): void {
    this.searchQuery = '';
    this.selectedCategory = 'All topics';
  }
}
