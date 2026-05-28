import { ChangeDetectorRef, Component, DestroyRef, OnInit, inject } from '@angular/core';
import { DOCUMENT, NgFor, NgIf } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
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
  imports: [NgFor, NgIf, RouterLink, TranslatePipe, UiButtonComponent, HighlightChipComponent, UiEmptyStateComponent, UiSkeletonComponent, UiIconComponent, ProtectedDocumentsCardComponent, UiImageLightboxComponent],
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
          this.closeImageViewer();
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
          this.closeImageViewer();
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
