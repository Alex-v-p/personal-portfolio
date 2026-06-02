import { ChangeDetectorRef, Component, DestroyRef, OnInit, inject } from '@angular/core';
import { DOCUMENT, NgFor, NgIf } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { combineLatest, forkJoin, of } from 'rxjs';
import { catchError, finalize, map, switchMap } from 'rxjs/operators';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { UiIconComponent } from '@shared/icons';
import { BlogPostDetail } from '@domains/blog/model/blog-post-detail.model';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { PublicBlogApiService } from '@domains/blog/data/blog-api.service';
import { ProtectedDocumentsCardComponent } from '@domains/blog/ui/protected-documents-card.component';
import { extractMarkdownImages, renderMarkdownToHtml } from '@shared/utils/markdown.util';
import { localizeInternalAppLinkUrl } from '@shared/utils/internal-link.util';
import { SeoService } from '@shared/services/seo.service';
import { UiImageLightboxComponent } from '@shared/components/image-lightbox/ui-image-lightbox.component';
import { UiImageLightboxImage } from '@shared/components/image-lightbox/ui-image-lightbox.types';

interface ShareAction {
  iconName: string;
  name: string;
  href: string;
}

@Component({
  selector: 'app-blog-post-page',
  standalone: true,
  imports: [NgFor, NgIf, RouterLink, TranslatePipe, UiButtonComponent, UiLinkButtonComponent, HighlightChipComponent, UiEmptyStateComponent, UiSkeletonComponent, UiIconComponent, ProtectedDocumentsCardComponent, UiImageLightboxComponent],
  templateUrl: './blog-post.page.html',
  styleUrls: ['./blog-post.page.css']
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
  protected relatedPosts: BlogPostSummary[] = [];
  protected isLoading = true;
  protected errorMessage = '';
  protected currentSlug = '';
  protected isImageViewerOpen = false;
  protected activeImageIndex = 0;

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
          this.relatedPosts = [];
          this.closeImageViewer();
          return this.loadPostBundle(this.currentSlug).pipe(finalize(() => this.changeDetectorRef.detectChanges()));
        }),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: ({ post, posts }) => {
          this.post = post;
          this.relatedPosts = this.buildRelatedPosts(post, posts);
          this.isLoading = false;
          this.updateSeo(post);
        },
        error: () => {
          this.post = null;
          this.relatedPosts = [];
          this.closeImageViewer();
          this.isLoading = false;
          this.errorMessage = this.i18n.translate('pages.blogPost.errors.load');
        }
      });
  }


  private loadPostBundle(slug: string) {
    return forkJoin({
      post: this.blogApi.getBlogPostBySlug(slug),
      posts: this.blogApi.getBlogPosts().pipe(catchError(() => of([] as BlogPostSummary[]))),
    });
  }

  private buildRelatedPosts(currentPost: BlogPostDetail, posts: BlogPostSummary[]): BlogPostSummary[] {
    const currentTags = new Set(currentPost.tags.map((tag) => this.normalizeSuggestionToken(tag)));
    const currentCategory = this.normalizeSuggestionToken(currentPost.category);

    return posts
      .filter((post) => post.status === 'published' && post.id !== currentPost.id && post.slug !== currentPost.slug)
      .map((post, index) => ({
        post,
        index,
        score: this.calculateRelatedPostScore(post, currentTags, currentCategory),
      }))
      .sort((first, second) => second.score - first.score || first.index - second.index)
      .slice(0, 6)
      .map((suggestion) => suggestion.post);
  }

  private calculateRelatedPostScore(post: BlogPostSummary, currentTags: Set<string>, currentCategory: string): number {
    const sharedTagScore = post.tags.reduce((score, tag) => score + (currentTags.has(this.normalizeSuggestionToken(tag)) ? 2 : 0), 0);
    const categoryScore = currentCategory && this.normalizeSuggestionToken(post.category) === currentCategory ? 4 : 0;
    const featuredScore = post.isFeatured ? 1 : 0;

    return categoryScore + sharedTagScore + featuredScore;
  }

  private normalizeSuggestionToken(value: string): string {
    return value.trim().toLocaleLowerCase();
  }

  protected relatedArticleRouterLink(post: BlogPostSummary): string | readonly string[] {
    return this.i18n.localizeRouterCommands(['/blog', post.slug]) ?? ['/blog', post.slug];
  }

  protected relatedArticleAriaLabel(post: BlogPostSummary): string {
    return `${this.i18n.translate('common.actions.readArticle')}: ${post.title}`;
  }

  protected displayedRelatedTags(post: BlogPostSummary): string[] {
    return post.tags.slice(0, 2);
  }

  protected hiddenRelatedTagCount(post: BlogPostSummary): number {
    return Math.max(post.tags.length - 2, 0);
  }

  protected relatedArticlePlaceholderLabel(post: BlogPostSummary): string {
    return post.coverImageAlt || post.coverAlt || this.i18n.translate('pages.blog.card.placeholder');
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

    this.loadPostBundle(this.currentSlug).pipe(finalize(() => this.changeDetectorRef.detectChanges())).subscribe({
      next: ({ post, posts }) => {
        this.post = post;
        this.relatedPosts = this.buildRelatedPosts(post, posts);
        this.isLoading = false;
        this.updateSeo(post);
      },
      error: () => {
        this.post = null;
        this.relatedPosts = [];
        this.closeImageViewer();
        this.isLoading = false;
        this.errorMessage = this.i18n.translate('pages.blogPost.errors.load');
      }
    });
  }

  protected get renderedContent(): string {
    return this.post
      ? renderMarkdownToHtml(this.post.contentMarkdown, { transformLinkUrl: (url) => localizeInternalAppLinkUrl(url, this.i18n), enableImageLightbox: true })
      : '';
  }

  protected get blogListingRouterLink(): string | readonly string[] {
    return this.i18n.localizeRouterCommands('/blog') ?? '/blog';
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


  protected get blogLightboxImages(): UiImageLightboxImage[] {
    const post = this.post;
    if (!post) {
      return [];
    }

    const images: UiImageLightboxImage[] = [];
    const seenUrls = new Set<string>();

    const addImage = (image: UiImageLightboxImage): void => {
      const imageUrl = image.url.trim();
      if (!imageUrl || seenUrls.has(imageUrl)) {
        return;
      }

      images.push({ ...image, url: imageUrl });
      seenUrls.add(imageUrl);
    };

    if (post.coverImageUrl?.trim()) {
      addImage({
        id: 'cover',
        url: post.coverImageUrl,
        alt: post.coverImageAlt || post.title,
      });
    }

    extractMarkdownImages(post.contentMarkdown).forEach((image, index) => {
      addImage({
        id: `markdown-${index}`,
        url: image.url,
        alt: image.alt || image.title || post.title,
      });
    });

    return images;
  }

  protected openCoverImage(event: Event): void {
    event.preventDefault();
    this.openImageByUrl(this.post?.coverImageUrl ?? '');
  }

  protected openMarkdownImage(event: Event): void {
    const imageElement = this.findLightboxImageElement(event.target);
    if (!imageElement) {
      return;
    }

    event.preventDefault();
    this.openImageByUrl(imageElement.dataset['lightboxSrc'] ?? imageElement.getAttribute('src') ?? '');
  }

  protected openMarkdownImageFromKeyboard(event: KeyboardEvent): void {
    if (event.key !== 'Enter' && event.key !== ' ') {
      return;
    }

    this.openMarkdownImage(event);
  }

  protected updateActiveImageIndex(index: number): void {
    this.activeImageIndex = index;
  }

  protected closeImageViewer(): void {
    this.isImageViewerOpen = false;
  }

  private openImageByUrl(imageUrl: string): void {
    const normalizedUrl = imageUrl.trim();
    if (!normalizedUrl) {
      return;
    }

    const images = this.blogLightboxImages;
    const imageIndex = images.findIndex((image) => image.url === normalizedUrl);

    if (imageIndex < 0) {
      return;
    }

    this.activeImageIndex = imageIndex;
    this.isImageViewerOpen = true;
  }

  private findLightboxImageElement(target: EventTarget | null): HTMLImageElement | null {
    if (!(target instanceof Element)) {
      return null;
    }

    return target.closest<HTMLImageElement>('img.markdown-lightbox-image');
  }

  private get currentShareUrl(): string {
    const origin = this.document.location?.origin ?? '';
    const localizedPath = this.i18n.prefixPath(`/blog/${this.post?.slug ?? this.currentSlug}`);
    return `${origin}${localizedPath}`;
  }
}
