import { ChangeDetectorRef, Component, DestroyRef, OnInit, inject } from '@angular/core';
import { DOCUMENT, NgFor, NgIf } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { combineLatest } from 'rxjs';
import { finalize, map, switchMap } from 'rxjs/operators';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { UiIconComponent } from '@shared/icons';
import { BlogPostDetail } from '@domains/blog/model/blog-post-detail.model';
import { PublicBlogApiService } from '@domains/blog/data/blog-api.service';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';
import { SeoService } from '@shared/services/seo.service';

interface ShareAction {
  iconName: string;
  name: string;
  href: string;
}

@Component({
  selector: 'app-blog-post-page',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiButtonComponent, HighlightChipComponent, UiEmptyStateComponent, UiSkeletonComponent, UiIconComponent],
  templateUrl: './blog-post.page.html'
})
export class BlogPostPageComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly blogApi = inject(PublicBlogApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly seo = inject(SeoService);
  private readonly i18n = inject(I18nService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly document = inject(DOCUMENT);

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

  protected get blogListingHref(): string {
    return this.i18n.prefixPath('/blog');
  }

  protected get shareActions(): ShareAction[] {
    if (!this.post) {
      return [];
    }

    const pageUrl = this.currentShareUrl;
    const encodedUrl = encodeURIComponent(pageUrl);
    const encodedTitle = encodeURIComponent(this.post.title);

    return [
      {
        iconName: 'linkedin',
        name: 'LinkedIn',
        href: `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`,
      },
      {
        iconName: 'twitter',
        name: 'X',
        href: `https://x.com/intent/post?url=${encodedUrl}&text=${encodedTitle}`,
      },
    ];
  }

  private get currentShareUrl(): string {
    const origin = this.document.location?.origin ?? '';
    const localizedPath = this.i18n.prefixPath(`/blog/${this.post?.slug ?? this.currentSlug}`);
    return `${origin}${localizedPath}`;
  }
}
