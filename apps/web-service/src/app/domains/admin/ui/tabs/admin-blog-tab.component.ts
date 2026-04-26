import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, ElementRef, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminBlogPost, AdminMediaFile, AdminReferenceData } from '@domains/admin/model/admin.model';
import { buildMarkdownDownloadLink, renderMarkdownToHtml } from '@shared/utils/markdown.util';
import {
  countMarkdownWords,
  insertCodeBlock,
  insertImageTemplate,
  insertSnippet,
  suggestReadingTimeMinutes,
  TextSelectionUpdate,
  toggleLinePrefix,
  wrapSelection,
} from '@domains/admin/blog/editor/admin-blog-editor.utils';
import { AdminBlogPostForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { formatTagSummary, isImageMedia } from '@domains/admin/shell/state/admin-page.display.utils';
import { matchesSearch, slugify, toggleSelection } from '@domains/admin/shell/state/admin-page.utils';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';

import { AdminLocalizedContentTabBase } from './admin-localized-content-tab.base';

@Component({
  selector: 'app-admin-blog-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-blog-tab.component.html'
})
export class AdminBlogTabComponent extends AdminLocalizedContentTabBase implements OnChanges {
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly overviewApi = inject(AdminOverviewApiService);

  @ViewChild('blogMarkdownEditor') private blogMarkdownEditor?: ElementRef<HTMLTextAreaElement>;

  @Input({ required: true }) blogPosts: AdminBlogPost[] = [];
  @Input() selectedBlogPostId: string | null = null;
  @Input({ required: true }) blogPostForm!: AdminBlogPostForm;
  @Input({ required: true }) blogUploadForm!: ScopedUploadForm;
  @Input({ required: true }) blogInlineImageUploadForm!: ScopedUploadForm;
  @Input({ required: true }) referenceData!: AdminReferenceData;
  @Input() uploadInProgressKey: string | null = null;

  @Output() readonly blogPostSelected = new EventEmitter<string>();
  @Output() readonly newBlogPostStarted = new EventEmitter<void>();
  @Output() readonly blogPostSaved = new EventEmitter<void>();
  @Output() readonly blogPostDeleted = new EventEmitter<void>();
  @Output() readonly scopedFileSelected = new EventEmitter<{ event: Event; form: ScopedUploadForm }>();
  @Output() readonly blogCoverUploadRequested = new EventEmitter<void>();
  @Output() readonly blogInlineImageUploadRequested = new EventEmitter<void>();
  @Output() readonly statusMessageSet = new EventEmitter<string>();

  protected blogMediaSearchTerm = '';
  protected blogDownloadMediaSearchTerm = '';

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedBlogPostId']) {
      this.blogMediaSearchTerm = '';
      this.blogDownloadMediaSearchTerm = '';
      this.resetLocalizedEditingState();
    }
  }

  protected get activeContentLocaleLabel(): string {
    return this.contentLocale === 'nl' ? 'Dutch' : 'English';
  }

  protected get activeBlogContentMarkdown(): string {
    return this.contentLocale === 'nl'
      ? (this.blogPostForm.contentMarkdownNl || '')
      : (this.blogPostForm.contentMarkdown || '');
  }

  protected set activeBlogContentMarkdown(value: string) {
    if (this.contentLocale === 'nl') {
      this.blogPostForm.contentMarkdownNl = value;
      return;
    }
    this.blogPostForm.contentMarkdown = value;
  }

  protected get renderedBlogContentPreview(): string {
    return renderMarkdownToHtml(this.activeBlogContentMarkdown);
  }

  protected get blogMarkdownWordCount(): number {
    return countMarkdownWords(this.activeBlogContentMarkdown);
  }

  protected get suggestedBlogReadingTimeMinutes(): number {
    return suggestReadingTimeMinutes(this.activeBlogContentMarkdown);
  }

  protected get filteredBlogImageMediaFiles(): AdminMediaFile[] {
    return [...this.referenceData.mediaFiles]
      .filter((media) => isImageMedia(media))
      .filter((media) => matchesSearch([media.title, media.altText, media.originalFilename, media.objectKey], this.blogMediaSearchTerm))
      .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
  }

  protected get filteredBlogDownloadMediaFiles(): AdminMediaFile[] {
    return [...this.referenceData.mediaFiles]
      .filter((media) => matchesSearch([media.title, media.altText, media.originalFilename, media.objectKey], this.blogDownloadMediaSearchTerm))
      .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
  }

  protected get blogFolder(): string {
    return `blog/${slugify(this.blogPostForm.slug || this.blogPostForm.title || 'untitled-post')}`;
  }

  protected formatTagSummary(post: AdminBlogPost): string {
    return formatTagSummary(post);
  }

  protected selectBlogPost(postId: string): void {
    this.blogPostSelected.emit(postId);
  }

  protected startNewBlogPost(): void {
    this.newBlogPostStarted.emit();
    this.resetLocalizedEditingState();
  }

  protected saveBlogPost(): void {
    this.blogPostSaved.emit();
  }

  protected deleteBlogPost(): void {
    this.blogPostDeleted.emit();
  }

  protected applySuggestedBlogReadingTime(): void {
    this.blogPostForm.readingTimeMinutes = this.suggestedBlogReadingTimeMinutes || null;
  }

  protected toggleBlogTag(tagId: string): void {
    this.blogPostForm.tagIds = toggleSelection(this.blogPostForm.tagIds, tagId);
  }

  protected onScopedFileSelected(event: Event, form: ScopedUploadForm): void {
    this.scopedFileSelected.emit({ event, form });
  }

  protected uploadBlogCover(): void {
    this.blogCoverUploadRequested.emit();
  }

  protected uploadBlogInlineImage(): void {
    this.blogInlineImageUploadRequested.emit();
  }

  protected wrapBlogSelection(prefix: string, suffix = '', placeholder = 'text'): void {
    this.updateBlogMarkdownSelection((content, selection) => wrapSelection(content, selection, prefix, suffix, placeholder));
  }

  protected toggleBlogLinePrefix(prefix: string): void {
    this.updateBlogMarkdownSelection((content, selection) => toggleLinePrefix(content, selection, prefix));
  }

  protected insertBlogMarkdownLink(): void {
    this.wrapBlogSelection('[', '](https://example.com)', 'Link text');
  }

  protected insertBlogMarkdownCodeBlock(): void {
    this.updateBlogMarkdownSelection((content, selection) => insertCodeBlock(content, selection));
  }

  protected insertBlogMarkdownDivider(): void {
    this.updateBlogMarkdownSelection((content, selection) => insertSnippet(content, selection, '\n---\n'));
  }

  protected insertBlogMarkdownImageTemplate(): void {
    this.updateBlogMarkdownSelection((content, selection) => insertImageTemplate(content, selection));
  }

  protected generateDutchDraft(): void {
    this.beginDutchDraftGeneration();
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'blog-post',
      context: 'Translate a technical portfolio blog post. Preserve markdown formatting, code blocks, links, alt text intent, and SEO tone.',
      fields: {
        titleNl: this.blogPostForm.title,
        excerptNl: this.blogPostForm.excerpt,
        contentMarkdownNl: this.blogPostForm.contentMarkdown,
        coverImageAltNl: this.blogPostForm.coverImageAlt,
        seoTitleNl: this.blogPostForm.seoTitle,
        seoDescriptionNl: this.blogPostForm.seoDescription,
      },
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.applyTranslatedFields(this.blogPostForm, response.translatedFields, {
          titleNl: 'titleNl',
          excerptNl: 'excerptNl',
          contentMarkdownNl: 'contentMarkdownNl',
          coverImageAltNl: 'coverImageAltNl',
          seoTitleNl: 'seoTitleNl',
          seoDescriptionNl: 'seoDescriptionNl',
        });
        this.finishDutchDraftGeneration(response, 'Dutch draft generated from the English blog post.');
      },
      error: (error) => {
        this.failDutchDraftGeneration(error, 'Generating the Dutch blog draft failed.');
      },
    });
  }

  public insertImageFromMedia(media: AdminMediaFile): void {
    const url = media.resolvedAsset?.url ?? media.publicUrl ?? null;
    if (!url) {
      this.statusMessageSet.emit('That media file does not have a usable URL yet.');
      return;
    }

    const markdown = this.buildBlogImageMarkdown(media, url);
    this.updateBlogMarkdownSelection((content, selection) => insertSnippet(content, selection, `\n${markdown}\n`));
    this.statusMessageSet.emit(`Image markdown inserted into the ${this.activeContentLocaleLabel.toLowerCase()} article body.`);
  }

  protected insertBlogImageFromMedia(media: AdminMediaFile): void {
    this.insertImageFromMedia(media);
  }

  protected isBlogDownloadImage(media: AdminMediaFile): boolean {
    return isImageMedia(media);
  }

  protected insertBlogDownloadFromMedia(media: AdminMediaFile): void {
    const url = media.resolvedAsset?.url ?? media.publicUrl ?? null;
    if (!url) {
      this.statusMessageSet.emit('That media file does not have a usable URL yet.');
      return;
    }

    const label = `Download ${media.title || media.originalFilename || 'file'}`;
    const markdown = buildMarkdownDownloadLink(label, url);
    this.updateBlogMarkdownSelection((content, selection) => insertSnippet(content, selection, `\n${markdown}\n`));
    this.statusMessageSet.emit(`Download markdown inserted into the ${this.activeContentLocaleLabel.toLowerCase()} article body.`);
  }

  private updateBlogMarkdownSelection(
    updater: (content: string, selection: { start: number; end: number }) => TextSelectionUpdate,
  ): void {
    const textarea = this.blogMarkdownEditor?.nativeElement;
    const content = this.activeBlogContentMarkdown;
    const selection = {
      start: textarea?.selectionStart ?? content.length,
      end: textarea?.selectionEnd ?? content.length,
    };
    const nextState = updater(content, selection);

    this.activeBlogContentMarkdown = nextState.value;
    this.changeDetectorRef.detectChanges();

    if (!textarea) {
      return;
    }

    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(nextState.selection.start, nextState.selection.end);
    });
  }

  private buildBlogImageMarkdown(media: AdminMediaFile, url: string): string {
    const altText = (media.altText || media.title || media.originalFilename || 'Blog image')
      .replace(/[\r\n]+/g, ' ')
      .replace(/\]/g, '\\]')
      .trim();
    return `![${altText}](${url})`;
  }
}
