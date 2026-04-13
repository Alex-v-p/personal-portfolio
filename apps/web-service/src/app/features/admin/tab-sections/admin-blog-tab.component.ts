import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, ElementRef, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminBlogPost, AdminMediaFile, AdminReferenceData } from '../../../shared/models/admin.model';
import { renderMarkdownToHtml } from '../../../shared/utils/markdown.util';
import {
  countMarkdownWords,
  insertCodeBlock,
  insertImageTemplate,
  insertSnippet,
  suggestReadingTimeMinutes,
  TextSelectionUpdate,
  toggleLinePrefix,
  wrapSelection,
} from '../admin-blog-editor.utils';
import { AdminBlogPostForm, ScopedUploadForm } from '../admin-page.forms';
import { formatTagSummary, isImageMedia } from '../admin-page.display.utils';
import { matchesSearch, slugify, toggleSelection } from '../admin-page.utils';

@Component({
  selector: 'app-admin-blog-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-blog-tab.component.html'
})
export class AdminBlogTabComponent implements OnChanges {
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

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

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedBlogPostId']) {
      this.blogMediaSearchTerm = '';
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
