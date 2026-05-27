import { NgFor, NgIf } from '@angular/common';
import { Component, EventEmitter, HostListener, Input, Output, inject } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { localizeInternalAppLinkUrl } from '@shared/utils/internal-link.util';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';
import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { ProjectDetail } from '@domains/projects/model/project-detail.model';
import { ProjectLink } from '@domains/projects/model/project-summary.model';

@Component({
  selector: 'app-project-detail-modal',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './project-detail-modal.component.html'
})
export class ProjectDetailModalComponent {
  private readonly i18n = inject(I18nService);

  @Input() project: ProjectDetail | null = null;
  @Input() isLoading = false;
  @Input() errorMessage = '';
  @Input() readMoreAction: ProjectLink | null = null;
  @Input() githubAction: ProjectLink | null = null;
  @Input() demoAction: ProjectLink | null = null;
  @Output() readonly closed = new EventEmitter<void>();

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

  protected get heroImage(): ResolvedMedia | null {
    return this.modalImages[0] ?? null;
  }

  protected get supportingImages(): ResolvedMedia[] {
    return this.modalImages.slice(1, 4);
  }

  protected get renderedDescriptionHtml(): string {
    return renderMarkdownToHtml(this.project?.descriptionMarkdown ?? '', {
      transformLinkUrl: (url) => localizeInternalAppLinkUrl(url, this.i18n),
    });
  }

  protected trackImage(index: number, image: ResolvedMedia): string {
    return image.id ?? image.url ?? `${index}`;
  }
}
