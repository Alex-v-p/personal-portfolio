import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, ElementRef, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminBlogPost, AdminMediaFile, AdminReferenceData } from '@domains/admin/model/admin.model';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';
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

type ContentLocale = 'en' | 'nl';

@Component({
  selector: 'app-admin-blog-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-blog-tab.component.html'
})
export class AdminBlogTabComponent implements OnChanges {
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
  protected isGeneratingDutchDraft = false;
  protected translationMessage = '';
  protected contentLocale: ContentLocale = 'en';

  protected setContentLocale(locale: ContentLocale): void {
    this.contentLocale = locale;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedBlogPostId']) {
      this.blogMediaSearchTerm = '';
      this.translationMessage = '';
    this.contentLocale = 'en';
    }
  }

  protected get renderedBlogContentPreview(): string {
    return renderMarkdownToHtml(this.blogPostForm.contentMarkdown || '');
  }

  protected get blogMarkdownWordCount(): number {
    return countMarkdownWords(this.blogPostForm.contentMarkdown);
  }

  protected get suggestedBlogReadingTimeMinutes(): number {
    return suggestReadingTimeMinutes(this.blogPostForm.contentMarkdown);
  }

  protected get filteredBlogImageMediaFiles(): AdminMediaFile[] {
    return [...this.referenceData.mediaFiles]
      .filter((media) => isImageMedia(media))
      .filter((media) => matchesSearch([media.title, media.altText, media.originalFilename, media.objectKey], this.blogMediaSearchTerm))
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
    this.isGeneratingDutchDraft = true;
    this.translationMessage = '';
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
        this.blogPostForm.titleNl = response.translatedFields['titleNl'] ?? this.blogPostForm.titleNl;
        this.blogPostForm.excerptNl = response.translatedFields['excerptNl'] ?? this.blogPostForm.excerptNl;
        this.blogPostForm.contentMarkdownNl = response.translatedFields['contentMarkdownNl'] ?? this.blogPostForm.contentMarkdownNl;
        this.blogPostForm.coverImageAltNl = response.translatedFields['coverImageAltNl'] ?? this.blogPostForm.coverImageAltNl;
        this.blogPostForm.seoTitleNl = response.translatedFields['seoTitleNl'] ?? this.blogPostForm.seoTitleNl;
        this.blogPostForm.seoDescriptionNl = response.translatedFields['seoDescriptionNl'] ?? this.blogPostForm.seoDescriptionNl;
        this.contentLocale = 'nl';
        this.translationMessage = 'Dutch draft generated from the English blog post.';
        this.isGeneratingDutchDraft = false;
      },
      error: (error) => {
        this.translationMessage = error?.error?.detail || 'Generating the Dutch blog draft failed.';
        this.isGeneratingDutchDraft = false;
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
    this.statusMessageSet.emit('Image markdown inserted into the blog post.');
  }

  protected insertBlogImageFromMedia(media: AdminMediaFile): void {
    this.insertImageFromMedia(media);
  }

  private updateBlogMarkdownSelection(
    updater: (content: string, selection: { start: number; end: number }) => TextSelectionUpdate,
  ): void {
    const textarea = this.blogMarkdownEditor?.nativeElement;
    const content = this.blogPostForm.contentMarkdown || '';
    const selection = {
      start: textarea?.selectionStart ?? content.length,
      end: textarea?.selectionEnd ?? content.length,
    };
    const nextState = updater(content, selection);

    this.blogPostForm.contentMarkdown = nextState.value;
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
