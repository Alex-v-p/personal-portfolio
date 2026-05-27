import { NgFor, NgIf } from '@angular/common';
import { Component, EventEmitter, HostListener, Input, OnChanges, Output, SimpleChanges, inject } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiIconComponent } from '@shared/icons/ui-icon.component';
import { localizeInternalAppLinkUrl } from '@shared/utils/internal-link.util';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';
import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { ProjectDetail } from '@domains/projects/model/project-detail.model';
import { ProjectLink } from '@domains/projects/model/project-summary.model';

@Component({
  selector: 'app-project-detail-modal',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiChipComponent, UiIconComponent, UiLinkButtonComponent],
  templateUrl: './project-detail-modal.component.html'
})
export class ProjectDetailModalComponent implements OnChanges {
  private readonly i18n = inject(I18nService);

  @Input() project: ProjectDetail | null = null;
  @Input() isLoading = false;
  @Input() errorMessage = '';
  @Input() readMoreAction: ProjectLink | null = null;
  @Input() githubAction: ProjectLink | null = null;
  @Input() demoAction: ProjectLink | null = null;
  @Output() readonly closed = new EventEmitter<void>();

  protected activeImageIndex = 0;

  ngOnChanges(changes: SimpleChanges): void {
    const projectChange = changes['project'];
    if (!projectChange) {
      return;
    }

    const previousProject = projectChange.previousValue as ProjectDetail | null | undefined;
    const currentProject = projectChange.currentValue as ProjectDetail | null | undefined;

    if (previousProject?.id !== currentProject?.id) {
      this.activeImageIndex = 0;
    }
  }

  @HostListener('document:keydown.escape')
  onEscapeKey(): void {
    this.requestClose();
  }

  protected requestClose(): void {
    this.closed.emit();
  }

  protected stopPropagation(event: Event): void {
    event.stopPropagation();
  }

  protected get dialogTitleId(): string {
    return `project-detail-title-${this.project?.id ?? 'loading'}`;
  }

  protected get modalImages(): ResolvedMedia[] {
    const project = this.project;
    if (!project) {
      return [];
    }

    const images = [...(project.images?.length ? project.images : project.galleryImages ?? [])].filter((image) => !!image.url);

    if (!project.coverImageUrl) {
      return images;
    }

    const coverImage: ResolvedMedia = {
      id: project.coverImageFileId ?? project.id,
      url: project.coverImageUrl,
      alt: project.coverImageAlt || project.imageAlt || project.title,
    };

    const alreadyContainsCover = images.some((image) => {
      if (coverImage.id && image.id === coverImage.id) {
        return true;
      }
      return image.url === coverImage.url;
    });

    return alreadyContainsCover ? images : [coverImage, ...images];
  }

  protected get selectedImage(): ResolvedMedia | null {
    const images = this.modalImages;
    if (!images.length) {
      return null;
    }

    const safeIndex = this.activeImageIndex >= 0 && this.activeImageIndex < images.length ? this.activeImageIndex : 0;
    return images[safeIndex] ?? images[0] ?? null;
  }


  protected get selectedImageBackgroundImage(): string {
    const imageUrl = this.selectedImage?.url?.trim();
    if (!imageUrl) {
      return 'none';
    }

    const escapedUrl = imageUrl.replace(/\"/g, '\\"');
    return `url("${escapedUrl}")`;
  }

  protected get hasMultipleModalImages(): boolean {
    return this.modalImages.length > 1;
  }

  protected get modalGalleryCounterLabel(): string {
    const count = this.modalImages.length;
    if (count <= 1) {
      return '';
    }

    const safeIndex = this.activeImageIndex >= 0 && this.activeImageIndex < count ? this.activeImageIndex : 0;
    return `${safeIndex + 1} / ${count}`;
  }

  protected get renderedDescriptionHtml(): string {
    return renderMarkdownToHtml(this.project?.descriptionMarkdown ?? '', {
      transformLinkUrl: (url) => localizeInternalAppLinkUrl(url, this.i18n),
    });
  }

  protected showPreviousImage(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.shiftImage(-1);
  }

  protected showNextImage(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.shiftImage(1);
  }

  protected selectImage(index: number, event?: Event): void {
    event?.preventDefault();
    event?.stopPropagation();

    if (index < 0 || index >= this.modalImages.length) {
      return;
    }

    this.activeImageIndex = index;
  }

  protected trackImage(index: number, image: ResolvedMedia): string {
    return image.id ?? image.url ?? `${index}`;
  }

  private shiftImage(direction: -1 | 1): void {
    const count = this.modalImages.length;
    if (count <= 1) {
      this.activeImageIndex = 0;
      return;
    }

    this.activeImageIndex = (this.activeImageIndex + direction + count) % count;
  }
}
