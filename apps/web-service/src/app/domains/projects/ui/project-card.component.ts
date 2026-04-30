import { NgFor, NgIf } from '@angular/common';
import { Component, Input, inject } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';
import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { ProjectLink, ProjectSummary } from '@domains/projects/model/project-summary.model';

@Component({
  selector: 'app-project-card',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiCardComponent, UiChipComponent, HighlightChipComponent, UiLinkButtonComponent],
  templateUrl: './project-card.component.html'
})
export class ProjectCardComponent {
  private readonly i18n = inject(I18nService);

  @Input({ required: true }) project!: ProjectSummary;
  @Input() featured = false;

  protected activeGalleryIndex = 0;
  protected areTagsExpanded = false;

  private get tagPreviewLimit(): number {
    return this.featured ? 5 : 4;
  }

  protected get displayedTags(): string[] {
    return this.areTagsExpanded ? this.project.tags : this.project.tags.slice(0, this.tagPreviewLimit);
  }

  protected get hiddenTagCount(): number {
    return Math.max(this.project.tags.length - this.tagPreviewLimit, 0);
  }

  protected get shouldShowTagToggle(): boolean {
    return this.project.tags.length > this.tagPreviewLimit;
  }

  protected get tagToggleLabel(): string {
    if (this.areTagsExpanded) {
      return this.i18n.translate('common.actions.showLess');
    }

    return this.i18n.translate('common.actions.showMoreCount', { count: this.hiddenTagCount });
  }

  protected toggleTags(): void {
    this.areTagsExpanded = !this.areTagsExpanded;
  }

  protected get readMoreAction(): ProjectLink | null {
    const githubReadmeUrl = this.project.githubUrl?.trim();
    if (githubReadmeUrl) {
      return { label: this.i18n.translate('common.actions.readMore'), href: githubReadmeUrl };
    }

    return this.project.links.find((link) => !!link.href && /read|meer|github/i.test(link.label ?? '')) ?? null;
  }

  protected get mediaClickHref(): string | null {
    return this.readMoreAction?.href?.trim() || null;
  }

  protected get mediaClickAriaLabel(): string {
    return `${this.i18n.translate('common.actions.readMore')}: ${this.project.title}`;
  }

  protected get renderedTeaserHtml(): string {
    return renderMarkdownToHtml(this.project.teaser || this.project.shortDescription || '');
  }

  protected get renderedFeaturedSummaryHtml(): string {
    return renderMarkdownToHtml(this.project.summary || this.project.teaser || this.project.shortDescription || '');
  }

  protected get galleryImages(): ResolvedMedia[] {
    const images = [...(this.project.galleryImages ?? [])].filter((image) => !!image.url);

    if (!this.project.coverImageUrl) {
      return images;
    }

    const coverImage: ResolvedMedia = {
      id: this.project.coverImageFileId ?? this.project.id,
      url: this.project.coverImageUrl,
      alt: this.project.coverImageAlt || this.project.imageAlt || this.project.title,
    };

    const alreadyContainsCover = images.some((image) => {
      if (coverImage.id && image.id === coverImage.id) {
        return true;
      }
      return image.url === coverImage.url;
    });

    return alreadyContainsCover ? images : [coverImage, ...images];
  }

  protected get currentGalleryImage(): ResolvedMedia | null {
    const images = this.galleryImages;
    if (!images.length) {
      return null;
    }

    const safeIndex = this.activeGalleryIndex >= 0 && this.activeGalleryIndex < images.length ? this.activeGalleryIndex : 0;
    return images[safeIndex] ?? images[0] ?? null;
  }

  protected get galleryCounterLabel(): string {
    const count = this.galleryImages.length;
    if (count <= 1) {
      return '';
    }
    const safeIndex = this.activeGalleryIndex >= 0 && this.activeGalleryIndex < count ? this.activeGalleryIndex : 0;
    return `${safeIndex + 1} / ${count}`;
  }

  protected get hasMultipleGalleryImages(): boolean {
    return this.galleryImages.length > 1;
  }

  protected showPreviousGalleryImage(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.shiftGalleryImage(-1);
  }

  protected showNextGalleryImage(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.shiftGalleryImage(1);
  }

  protected get demoAction(): ProjectLink | null {
    const directDemoUrl = this.project.demoUrl?.trim();
    const linkedDemo = this.project.links.find((link) => this.isDemoLink(link));
    const externalProjectLink = this.project.links.find((link) => this.isNonRepositoryExternalLink(link));
    const href = directDemoUrl || linkedDemo?.href?.trim() || externalProjectLink?.href?.trim();

    if (!href) {
      return null;
    }

    return {
      label: this.i18n.translate('common.actions.liveDemo'),
      href,
    };
  }

  private shiftGalleryImage(direction: -1 | 1): void {
    const count = this.galleryImages.length;
    if (count <= 1) {
      this.activeGalleryIndex = 0;
      return;
    }
    this.activeGalleryIndex = (this.activeGalleryIndex + direction + count) % count;
  }

  private isDemoLink(link: ProjectLink): boolean {
    const href = link.href?.trim();
    if (!href) {
      return false;
    }

    const label = (link.label ?? '').toLowerCase();
    return label.includes('demo') || label.includes('live') || href === this.project.demoUrl;
  }

  private isNonRepositoryExternalLink(link: ProjectLink): boolean {
    const href = link.href?.trim();
    if (!href) {
      return false;
    }

    const label = (link.label ?? '').toLowerCase();
    return !label.includes('github') && href !== this.project.githubUrl;
  }

  protected get placeholderLabel(): string {
    return this.project.coverImageAlt || this.project.imageAlt || this.i18n.translate('pages.projects.card.placeholder');
  }
}
