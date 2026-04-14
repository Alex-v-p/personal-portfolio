import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, ViewChild, inject } from '@angular/core';
import { forkJoin } from 'rxjs';
import { finalize, take } from 'rxjs/operators';

import { AdminContentApiService } from '@domains/admin/data/api/admin-content-api.service';
import { AdminMediaApiService } from '@domains/admin/data/api/admin-media-api.service';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminBlogPost, AdminMediaFile, AdminReferenceData } from '@domains/admin/model/admin.model';
import { AdminBlogPostForm, ScopedUploadForm, createEmptyBlogPostForm, createEmptyScopedUploadForm, toBlogPostForm } from '@domains/admin/model/forms/index';
import { AdminBlogTabComponent } from '@domains/admin/ui/tabs/admin-blog-tab.component';
import { buildBlogMediaFolder, resetScopedUploadForm } from '@domains/admin/media/state/admin-media.filters';
import { resolveSelection } from '@domains/admin/shell/state/admin-page.utils';

@Component({
  selector: 'app-admin-blog-page',
  standalone: true,
  imports: [CommonModule, AdminBlogTabComponent],
  templateUrl: './admin-blog.page.html',
})
export class AdminBlogPageComponent implements OnInit {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly contentApi = inject(AdminContentApiService);
  private readonly mediaApi = inject(AdminMediaApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  @ViewChild(AdminBlogTabComponent) private blogTabComponent?: AdminBlogTabComponent;

  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';

  protected blogPosts: AdminBlogPost[] = [];
  protected referenceData: AdminReferenceData = {
    skills: [],
    skillCategories: [],
    mediaFiles: [],
    blogTags: [],
    projectStates: ['published', 'archived', 'completed', 'paused'],
    publicationStatuses: ['draft', 'published', 'archived'],
  };

  protected selectedBlogPostId: string | null = null;
  protected blogPostForm: AdminBlogPostForm = createEmptyBlogPostForm();
  protected blogUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected blogInlineImageUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected uploadInProgressKey: string | null = null;

  ngOnInit(): void {
    this.loadBlogPage(false);
  }

  protected reload(): void {
    this.loadBlogPage(true);
  }

  protected selectBlogPost(postId: string): void {
    this.selectedBlogPostId = postId;
    const post = this.blogPosts.find((item) => item.id === postId);
    if (!post) {
      return;
    }

    this.blogPostForm = toBlogPostForm(post);
    this.blogUploadForm = createEmptyScopedUploadForm();
    this.blogInlineImageUploadForm = createEmptyScopedUploadForm();
    this.statusMessage = '';
  }

  protected startNewBlogPost(): void {
    this.selectedBlogPostId = null;
    this.blogPostForm = createEmptyBlogPostForm();
    this.blogUploadForm = createEmptyScopedUploadForm();
    this.blogInlineImageUploadForm = createEmptyScopedUploadForm();
    this.statusMessage = '';
  }

  protected saveBlogPost(): void {
    const payload = {
      slug: this.blogPostForm.slug || null,
      title: this.blogPostForm.title,
      excerpt: this.blogPostForm.excerpt,
      contentMarkdown: this.blogPostForm.contentMarkdown,
      coverImageFileId: this.blogPostForm.coverImageFileId || null,
      coverImageAlt: this.blogPostForm.coverImageAlt || null,
      readingTimeMinutes: this.blogPostForm.readingTimeMinutes,
      status: this.blogPostForm.status,
      isFeatured: this.blogPostForm.isFeatured,
      publishedAt: this.blogPostForm.publishedAt || null,
      seoTitle: this.blogPostForm.seoTitle || null,
      seoDescription: this.blogPostForm.seoDescription || null,
      tagIds: [...this.blogPostForm.tagIds],
    };

    const request$ = this.selectedBlogPostId
      ? this.contentApi.updateBlogPost(this.selectedBlogPostId, payload)
      : this.contentApi.createBlogPost(payload);

    request$.pipe(take(1)).subscribe({
      next: (savedPost) => {
        const wasEditing = Boolean(this.selectedBlogPostId);
        this.selectedBlogPostId = savedPost.id;
        this.statusMessage = wasEditing ? 'Blog post updated.' : 'Blog post created.';
        this.loadBlogPage(false);
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.statusMessage = error?.error?.detail || 'Saving the blog post failed.';
      },
    });
  }

  protected deleteBlogPost(): void {
    if (!this.selectedBlogPostId || !window.confirm('Delete this blog post?')) {
      return;
    }

    this.contentApi.deleteBlogPost(this.selectedBlogPostId).pipe(take(1)).subscribe({
      next: () => {
        this.selectedBlogPostId = null;
        this.startNewBlogPost();
        this.statusMessage = 'Blog post deleted.';
        this.loadBlogPage(false);
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.statusMessage = error?.error?.detail || 'Deleting the blog post failed.';
      },
    });
  }

  protected onScopedFileSelected(event: Event, form: ScopedUploadForm): void {
    const input = event.target as HTMLInputElement | null;
    form.file = input?.files?.[0] ?? null;
  }

  protected uploadBlogCover(): void {
    this.uploadScopedMedia('blog-cover', this.blogUploadForm, (media) => {
      this.blogPostForm.coverImageFileId = media.id;
      if (!this.blogPostForm.coverImageAlt) {
        this.blogPostForm.coverImageAlt = this.blogUploadForm.altText;
      }
    });
  }

  protected uploadBlogInlineImage(): void {
    this.uploadScopedMedia(
      'blog-inline-image',
      this.blogInlineImageUploadForm,
      (media) => this.blogTabComponent?.insertImageFromMedia(media),
      () => `Image uploaded to ${this.blogFolder} and inserted into the article.`,
    );
  }

  protected get blogFolder(): string {
    return buildBlogMediaFolder(this.blogPostForm.slug || this.blogPostForm.title);
  }

  private loadBlogPage(showReloadMessage: boolean): void {
    const currentSelection = this.selectedBlogPostId;
    this.isLoading = true;
    this.errorMessage = '';
    if (showReloadMessage) {
      this.statusMessage = 'Refreshing blog workspace…';
    }

    forkJoin({
      referenceData: this.overviewApi.getReferenceData(),
      blogPosts: this.contentApi.getBlogPosts(),
    }).pipe(
      take(1),
      finalize(() => {
        this.isLoading = false;
        this.changeDetectorRef.detectChanges();
      }),
    ).subscribe({
      next: ({ referenceData, blogPosts }) => {
        this.referenceData = referenceData;
        this.blogPosts = blogPosts.items;
        this.selectedBlogPostId = resolveSelection(currentSelection, this.blogPosts);
        this.blogPostForm = this.selectedBlogPostId
          ? toBlogPostForm(this.blogPosts.find((item) => item.id === this.selectedBlogPostId)!)
          : createEmptyBlogPostForm();
        this.blogUploadForm = createEmptyScopedUploadForm();
        this.blogInlineImageUploadForm = createEmptyScopedUploadForm();

        if (showReloadMessage) {
          this.statusMessage = 'Blog workspace refreshed.';
        }
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.errorMessage = error?.error?.detail || 'The blog admin workspace could not be loaded.';
      },
    });
  }

  private uploadScopedMedia(
    uploadKey: string,
    form: ScopedUploadForm,
    onSuccess: (media: AdminMediaFile) => void,
    successMessageBuilder?: (media: AdminMediaFile) => string,
  ): void {
    if (!form.file) {
      this.statusMessage = 'Choose a file before uploading.';
      return;
    }

    const formData = new FormData();
    formData.append('file', form.file);
    formData.append('folder', this.blogFolder);
    formData.append('visibility', form.visibility);
    if (form.title.trim()) {
      formData.append('title', form.title.trim());
    }
    if (form.altText.trim()) {
      formData.append('altText', form.altText.trim());
    }
    if (form.description.trim()) {
      formData.append('description', form.description.trim());
    }

    this.uploadInProgressKey = uploadKey;
    this.statusMessage = 'Uploading media…';
    this.mediaApi.uploadMedia(formData).pipe(
      take(1),
      finalize(() => {
        this.uploadInProgressKey = null;
        this.changeDetectorRef.detectChanges();
      }),
    ).subscribe({
      next: (media) => {
        this.referenceData = {
          ...this.referenceData,
          mediaFiles: [media, ...this.referenceData.mediaFiles.filter((item) => item.id !== media.id)],
        };
        onSuccess(media);
        resetScopedUploadForm(form);
        this.statusMessage = successMessageBuilder?.(media) ?? `Media uploaded to ${this.blogFolder} and selected automatically.`;
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.statusMessage = error?.error?.detail || 'Uploading media failed.';
      },
    });
  }
}
