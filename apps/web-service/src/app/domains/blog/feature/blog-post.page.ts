import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { finalize, switchMap } from 'rxjs/operators';

import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { BlogPostDetail } from '@domains/blog/model/blog-post-detail.model';
import { PublicBlogApiService } from '@domains/blog/data/blog-api.service';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';

@Component({
  selector: 'app-blog-post-page',
  standalone: true,
  imports: [NgFor, NgIf, RouterLink, UiButtonComponent, UiChipComponent, UiEmptyStateComponent],
  templateUrl: './blog-post.page.html'
})
export class BlogPostPageComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly blogApi = inject(PublicBlogApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

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
        },
        error: () => {
          this.post = null;
          this.isLoading = false;
          this.errorMessage = 'This blog post could not be loaded from the portfolio API.';
        }
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
