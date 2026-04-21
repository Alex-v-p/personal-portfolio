import { ChangeDetectorRef, Component, DestroyRef, OnInit, inject } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { combineLatest } from 'rxjs';
import { finalize, map, switchMap } from 'rxjs/operators';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { BlogPostDetail } from '@domains/blog/model/blog-post-detail.model';
import { PublicBlogApiService } from '@domains/blog/data/blog-api.service';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';
import { SeoService } from '@shared/services/seo.service';

@Component({
  selector: 'app-blog-post-page',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiLinkButtonComponent, UiButtonComponent, HighlightChipComponent, UiEmptyStateComponent, UiSkeletonComponent],
  templateUrl: './blog-post.page.html'
})
export class BlogPostPageComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly blogApi = inject(PublicBlogApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly seo = inject(SeoService);
  private readonly i18n = inject(I18nService);
  private readonly destroyRef = inject(DestroyRef);

  protected readonly shareMarks = ['in', 'x'];

  protected post: BlogPostDetail | null = null;
  protected isLoading = true;
  protected errorMessage = '';
  protected currentSlug = '';

  ngOnInit(): void {
    combineLatest([
      this.route.paramMap.pipe(map((params) => params.get('slug') ?? '')),
      this.i18n.localeChanges$
    ])
      .pipe(
        switchMap(([slug]) => {
          this.currentSlug = slug;
          this.isLoading = true;
          this.errorMessage = '';
          this.post = null;
          return this.blogApi.getBlogPostBySlug(this.currentSlug).pipe(finalize(() => this.changeDetectorRef.detectChanges()));
        }),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (post) => {
          this.post = post;
          this.isLoading = false;
          this.updateSeo(post);
        },
        error: () => {
          this.post = null;
          this.isLoading = false;
          this.errorMessage = this.i18n.translate('pages.blogPost.errors.load');
        }
      });
  }

  private updateSeo(post: BlogPostDetail): void {
    this.seo.updatePage({
      title: post.seoTitle?.trim() || post.title,
      description: post.seoDescription?.trim() || post.excerpt,
      keywords: [post.category, ...(post.tags ?? []), post.title],
      image: post.coverImageUrl,
      type: 'article',
      path: `/blog/${post.slug}`,
    });
  }

  protected retry(): void {
    if (!this.currentSlug) {
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.blogApi.getBlogPostBySlug(this.currentSlug).pipe(finalize(() => this.changeDetectorRef.detectChanges())).subscribe({
      next: (post) => {
        this.post = post;
        this.isLoading = false;
        this.updateSeo(post);
      },
      error: () => {
        this.post = null;
        this.isLoading = false;
        this.errorMessage = this.i18n.translate('pages.blogPost.errors.load');
      }
    });
  }

  protected get renderedContent(): string {
    return this.post ? renderMarkdownToHtml(this.post.contentMarkdown) : '';
  }
}
