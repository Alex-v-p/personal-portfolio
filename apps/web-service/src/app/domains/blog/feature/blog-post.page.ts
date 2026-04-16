import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { finalize, switchMap } from 'rxjs/operators';

import { UiButtonComponent } from '@shared/components/button/ui-button.component';
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
  imports: [NgFor, NgIf, RouterLink, UiButtonComponent, HighlightChipComponent, UiEmptyStateComponent, UiSkeletonComponent],
  templateUrl: './blog-post.page.html'
})
export class BlogPostPageComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly blogApi = inject(PublicBlogApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly seo = inject(SeoService);

  protected readonly shareMarks = ['in', 'x'];

  protected post: BlogPostDetail | null = null;
  protected isLoading = true;
  protected errorMessage = '';
  protected currentSlug = '';

  ngOnInit(): void {
    this.route.paramMap
      .pipe(
        switchMap((params) => {
          this.currentSlug = params.get('slug') ?? '';
          this.isLoading = true;
          this.errorMessage = '';
          this.post = null;
          return this.blogApi.getBlogPostBySlug(this.currentSlug).pipe(
            finalize(() => this.changeDetectorRef.detectChanges())
          );
        })
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
          this.errorMessage = 'This blog post could not be loaded from the portfolio API.';
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
        this.errorMessage = 'This blog post could not be loaded from the portfolio API.';
      }
    });
  }

  protected get renderedContent(): string {
    return this.post ? renderMarkdownToHtml(this.post.contentMarkdown) : '';
  }
}
