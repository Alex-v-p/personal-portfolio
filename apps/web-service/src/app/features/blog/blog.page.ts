import { NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { finalize, take } from 'rxjs/operators';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiEmptyStateComponent } from '../../shared/components/empty-state/ui-empty-state.component';
import { PublicPortfolioApiService } from '../../shared/services/public-portfolio-api.service';
import { BlogPost } from '../../shared/models/blog-post.model';
import { BlogCardComponent } from './components/blog-card/blog-card.component';

@Component({
  selector: 'app-blog-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, UiButtonComponent, UiEmptyStateComponent, BlogCardComponent],
  templateUrl: './blog.page.html'
})
export class BlogPageComponent implements OnInit {
  private readonly portfolioApi = inject(PublicPortfolioApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected readonly pagerDots = [1, 2, 3];

  protected posts: BlogPost[] = [];
  protected searchQuery = '';
  protected selectedCategory = 'All topics';
  protected isLoading = true;
  protected errorMessage = '';

  ngOnInit(): void {
    this.loadPosts();
  }

  protected loadPosts(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.portfolioApi
      .getBlogPosts()
      .pipe(
        take(1),
        finalize(() => {
          this.isLoading = false;
          this.changeDetectorRef.detectChanges();
        })
      )
      .subscribe({
        next: (posts) => {
          this.posts = Array.isArray(posts) ? posts : [];
        },
        error: () => {
          this.posts = [];
          this.errorMessage = 'Blog posts could not be loaded from the portfolio API. Make sure the portfolio-api-service is running on port 8001.';
        }
      });
  }

  protected get totalPostCount(): number {
    return this.posts.length;
  }

  protected get categories(): string[] {
    return ['All topics', ...new Set(this.posts.map((post) => post.category))];
  }

  protected get filteredPosts(): BlogPost[] {
    const query = this.searchQuery.trim().toLowerCase();

    return this.posts.filter((post) => {
      const matchesCategory = this.selectedCategory === 'All topics' || post.category === this.selectedCategory;
      if (!matchesCategory) {
        return false;
      }

      if (!query) {
        return true;
      }

      const haystack = [post.title, post.excerpt, post.category, post.contentMarkdown, ...(post.tags ?? [])].join(' ').toLowerCase();
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
