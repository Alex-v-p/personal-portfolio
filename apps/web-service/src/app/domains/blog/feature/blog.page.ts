import { NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { finalize, take } from 'rxjs/operators';

import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { PublicBlogApiService } from '@domains/blog/data/blog-api.service';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { BlogCardComponent } from '@domains/blog/ui/blog-card.component';

interface CategoryFilterOption {
  name: string;
  articleCount: number;
}

@Component({
  selector: 'app-blog-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, UiButtonComponent, UiChipComponent, UiEmptyStateComponent, UiSkeletonComponent, BlogCardComponent],
  templateUrl: './blog.page.html'
})
export class BlogPageComponent implements OnInit {
  private readonly blogApi = inject(PublicBlogApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected readonly pagerDots = [1, 2, 3];

  protected posts: BlogPostSummary[] = [];
  protected searchQuery = '';
  protected selectedCategories: string[] = [];
  protected isCategoryMenuOpen = false;
  protected isLoading = true;
  protected errorMessage = '';

  ngOnInit(): void {
    this.loadPosts();
  }

  protected loadPosts(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.blogApi
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
          this.errorMessage = 'Blog posts could not be loaded from the portfolio API. Make sure the API or reverse proxy is running.';
        }
      });
  }

  protected toggleCategoryMenu(): void {
    this.isCategoryMenuOpen = !this.isCategoryMenuOpen;
  }

  protected closeCategoryMenu(): void {
    this.isCategoryMenuOpen = false;
  }

  protected toggleCategoryFilter(category: string): void {
    this.selectedCategories = this.selectedCategories.includes(category)
      ? this.selectedCategories.filter((item) => item !== category)
      : [...this.selectedCategories, category];
  }

  protected clearCategoryFilters(): void {
    this.selectedCategories = [];
  }

  protected isCategorySelected(category: string): boolean {
    return this.selectedCategories.includes(category);
  }

  protected clearSearch(): void {
    this.searchQuery = '';
  }

  protected resetFilters(): void {
    this.searchQuery = '';
    this.selectedCategories = [];
    this.isCategoryMenuOpen = false;
  }

  protected get totalPostCount(): number {
    return this.posts.length;
  }

  protected get hasPosts(): boolean {
    return this.totalPostCount > 0;
  }

  protected get availableCategoryFilters(): CategoryFilterOption[] {
    return Array.from(new Set(this.posts.map((post) => post.category)))
      .sort((left, right) => left.localeCompare(right))
      .map((name) => ({
        name,
        articleCount: this.posts.filter((post) => post.category === name).length
      }));
  }

  protected get hasActiveFilters(): boolean {
    return !!this.searchQuery.trim() || this.selectedCategories.length > 0;
  }

  protected get categoryFilterLabel(): string {
    if (!this.selectedCategories.length) {
      return 'All topics';
    }

    if (this.selectedCategories.length === 1) {
      return this.selectedCategories[0];
    }

    if (this.selectedCategories.length === 2) {
      return this.selectedCategories.join(', ');
    }

    return `${this.selectedCategories.length} topics selected`;
  }

  protected get filteredPosts(): BlogPostSummary[] {
    const query = this.searchQuery.trim().toLowerCase();

    return this.posts.filter((post) => {
      const matchesCategory = this.selectedCategories.length === 0 || this.selectedCategories.includes(post.category);
      if (!matchesCategory) {
        return false;
      }

      if (!query) {
        return true;
      }

      const haystack = [post.title, post.excerpt, post.category, ...(post.tags ?? [])].join(' ').toLowerCase();
      return haystack.includes(query);
    });
  }

  protected get featuredPosts(): BlogPostSummary[] {
    return this.filteredPosts.filter((post) => post.isFeatured).slice(0, 1);
  }

  protected get browseablePosts(): BlogPostSummary[] {
    const featuredIds = new Set(this.featuredPosts.map((post) => post.id));
    return this.filteredPosts.filter((post) => !featuredIds.has(post.id));
  }
}
