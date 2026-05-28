import { NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, DestroyRef, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { distinctUntilChanged } from 'rxjs/operators';
import { finalize, take } from 'rxjs/operators';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { PublicBlogApiService } from '@domains/blog/data/blog-api.service';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { BlogCardComponent } from '@domains/blog/ui/blog-card.component';
import { UiBreadcrumbsComponent } from '@shared/components/breadcrumbs/ui-breadcrumbs.component';

interface CategoryFilterOption {
  name: string;
  articleCount: number;
}

@Component({
  selector: 'app-blog-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, TranslatePipe, UiButtonComponent, UiEmptyStateComponent, UiSkeletonComponent, BlogCardComponent, UiBreadcrumbsComponent],
  templateUrl: './blog.page.html'
})
export class BlogPageComponent implements OnInit {
  private readonly blogApi = inject(PublicBlogApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly i18n = inject(I18nService);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly browsePageSize = 4;

  protected posts: BlogPostSummary[] = [];
  protected searchQuery = '';
  protected selectedCategories: string[] = [];
  protected isCategoryMenuOpen = false;
  protected isLoading = true;
  protected errorMessage = '';
  protected currentBrowsePage = 1;

  ngOnInit(): void {
    this.i18n.localeChanges$.pipe(distinctUntilChanged(), takeUntilDestroyed(this.destroyRef)).subscribe(() => {
      this.loadPosts();
    });
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
          this.currentBrowsePage = 1;
        },
        error: () => {
          this.posts = [];
          this.errorMessage = this.i18n.translate('pages.blog.errors.load');
        }
      });
  }

  protected toggleCategoryMenu(): void {
    this.isCategoryMenuOpen = !this.isCategoryMenuOpen;
  }

  protected closeCategoryMenu(): void {
    this.isCategoryMenuOpen = false;
  }

  protected updateSearchQuery(value: string): void {
    this.searchQuery = value;
    this.currentBrowsePage = 1;
  }

  protected toggleCategoryFilter(category: string): void {
    this.selectedCategories = this.selectedCategories.includes(category)
      ? this.selectedCategories.filter((item) => item !== category)
      : [...this.selectedCategories, category];
    this.currentBrowsePage = 1;
  }

  protected clearCategoryFilters(): void {
    this.selectedCategories = [];
    this.currentBrowsePage = 1;
  }

  protected isCategorySelected(category: string): boolean {
    return this.selectedCategories.includes(category);
  }

  protected resetFilters(): void {
    this.searchQuery = '';
    this.selectedCategories = [];
    this.isCategoryMenuOpen = false;
    this.currentBrowsePage = 1;
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

  protected get categoryFilterLabel(): string {
    if (!this.selectedCategories.length) {
      return this.i18n.translate('pages.blog.filters.allTopics');
    }

    if (this.selectedCategories.length === 1) {
      return this.selectedCategories[0];
    }

    if (this.selectedCategories.length === 2) {
      return this.selectedCategories.join(', ');
    }

    return this.i18n.translate('pages.blog.filters.selectedCount', { count: this.selectedCategories.length });
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

  protected get totalBrowsePages(): number {
    return Math.max(1, Math.ceil(this.browseablePosts.length / this.browsePageSize));
  }

  protected get browsePageNumbers(): number[] {
    return Array.from({ length: this.totalBrowsePages }, (_, index) => index + 1);
  }

  protected get paginatedBrowseablePosts(): BlogPostSummary[] {
    const safePage = Math.min(Math.max(this.currentBrowsePage, 1), this.totalBrowsePages);
    if (safePage !== this.currentBrowsePage) {
      this.currentBrowsePage = safePage;
    }

    const startIndex = (safePage - 1) * this.browsePageSize;
    return this.browseablePosts.slice(startIndex, startIndex + this.browsePageSize);
  }

  protected get visiblePostCount(): number {
    return this.featuredPosts.length + this.paginatedBrowseablePosts.length;
  }

  protected get hasPostPagination(): boolean {
    return this.browseablePosts.length > 0;
  }

  protected goToBrowsePage(page: number): void {
    this.currentBrowsePage = Math.min(Math.max(page, 1), this.totalBrowsePages);
    this.scrollToPageTop();
  }

  protected goToPreviousBrowsePage(): void {
    this.goToBrowsePage(this.currentBrowsePage - 1);
  }

  protected goToNextBrowsePage(): void {
    this.goToBrowsePage(this.currentBrowsePage + 1);
  }

  private scrollToPageTop(): void {
    if (typeof window === 'undefined') {
      return;
    }

    window.requestAnimationFrame(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}
