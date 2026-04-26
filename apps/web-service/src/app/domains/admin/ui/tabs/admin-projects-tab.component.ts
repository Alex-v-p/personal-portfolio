import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminMediaFile, AdminProject, AdminReferenceData } from '@domains/admin/model/admin.model';
import { AdminProjectForm, AdminProjectGalleryImageForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { matchesSearch, slugify } from '@domains/admin/shell/state/admin-page.utils';
import { isImageMedia } from '@domains/admin/shell/state/admin-page.display.utils';

import { AdminLocalizedContentTabBase } from './admin-localized-content-tab.base';

@Component({
  selector: 'app-admin-projects-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-projects-tab.component.html'
})
export class AdminProjectsTabComponent extends AdminLocalizedContentTabBase {
  private readonly overviewApi = inject(AdminOverviewApiService);

  @Input({ required: true }) projects: AdminProject[] = [];
  @Input() selectedProjectId: string | null = null;
  @Input({ required: true }) projectForm!: AdminProjectForm;
  @Input({ required: true }) projectUploadForm!: ScopedUploadForm;
  @Input({ required: true }) referenceData!: AdminReferenceData;
  @Input() uploadInProgressKey: string | null = null;

  @Output() readonly projectSelected = new EventEmitter<string>();
  @Output() readonly newProjectStarted = new EventEmitter<void>();
  @Output() readonly projectSkillToggled = new EventEmitter<string>();
  @Output() readonly projectSaved = new EventEmitter<void>();
  @Output() readonly projectDeleted = new EventEmitter<void>();
  @Output() readonly scopedFileSelected = new EventEmitter<{ event: Event; form: ScopedUploadForm }>();
  @Output() readonly projectCoverUploadRequested = new EventEmitter<void>();

  protected selectedProjectGalleryMediaId: string | null = null;
  protected projectGallerySearchTerm = '';
  protected selectedProjectDownloadMediaId: string | null = null;

  selectProject(projectId: string): void {
    this.projectSelected.emit(projectId);
  }

  startNewProject(): void {
    this.newProjectStarted.emit();
    this.resetLocalizedEditingState();
  }

  toggleProjectSkill(skillId: string): void {
    this.projectSkillToggled.emit(skillId);
  }

  saveProject(): void {
    this.projectSaved.emit();
  }

  deleteProject(): void {
    this.projectDeleted.emit();
  }

  onScopedFileSelected(event: Event, form: ScopedUploadForm): void {
    this.scopedFileSelected.emit({ event, form });
  }

  uploadProjectCover(): void {
    this.projectCoverUploadRequested.emit();
  }

  protected get sortedGalleryImages(): AdminProjectGalleryImageForm[] {
    return [...(this.projectForm.images ?? [])].sort((left, right) => left.sortOrder - right.sortOrder);
  }

  protected get availableGalleryImageMediaFiles(): AdminMediaFile[] {
    const selected = new Set(this.projectForm.images.map((image) => image.imageFileId).filter(Boolean));
    return [...this.referenceData.mediaFiles]
      .filter((media) => isImageMedia(media))
      .filter((media) => !selected.has(media.id))
      .filter((media) => matchesSearch([media.title, media.altText, media.originalFilename, media.objectKey], this.projectGallerySearchTerm))
      .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
  }

  protected get selectedProjectDownloadMedia(): AdminMediaFile | null {
    return this.referenceData.mediaFiles.find((media) => media.id === this.selectedProjectDownloadMediaId) ?? null;
  }

  protected galleryMedia(image: AdminProjectGalleryImageForm): AdminMediaFile | null {
    return this.referenceData.mediaFiles.find((media) => media.id === image.imageFileId) ?? null;
  }

  protected addGalleryImageFromSelection(): void {
    const media = this.availableGalleryImageMediaFiles.find((item) => item.id === this.selectedProjectGalleryMediaId);
    if (!media) {
      return;
    }
    const isFirstImage = this.projectForm.images.length === 0;
    this.projectForm.images = [
      ...this.projectForm.images,
      {
        imageFileId: media.id,
        altText: media.altText || media.title || media.originalFilename || this.projectForm.title,
        altTextNl: '',
        sortOrder: this.projectForm.images.length,
        isCover: isFirstImage,
      },
    ];
    if (isFirstImage || !this.projectForm.coverImageFileId) {
      this.projectForm.coverImageFileId = media.id;
    }
    this.selectedProjectGalleryMediaId = null;
    this.normalizeGallerySortOrder();
  }

  protected removeGalleryImage(image: AdminProjectGalleryImageForm): void {
    this.projectForm.images = this.projectForm.images.filter((item) => item !== image);
    if (this.projectForm.coverImageFileId === image.imageFileId) {
      this.projectForm.coverImageFileId = this.projectForm.images[0]?.imageFileId ?? null;
    }
    this.normalizeGallerySortOrder();
  }

  protected moveGalleryImage(image: AdminProjectGalleryImageForm, direction: -1 | 1): void {
    const ordered = this.sortedGalleryImages;
    const currentIndex = ordered.indexOf(image);
    const nextIndex = currentIndex + direction;
    if (currentIndex < 0 || nextIndex < 0 || nextIndex >= ordered.length) {
      return;
    }
    [ordered[currentIndex], ordered[nextIndex]] = [ordered[nextIndex], ordered[currentIndex]];
    this.projectForm.images = ordered.map((item, index) => ({ ...item, sortOrder: index }));
  }

  protected setGalleryImageAsCover(image: AdminProjectGalleryImageForm): void {
    if (!image.imageFileId) {
      return;
    }
    this.projectForm.coverImageFileId = image.imageFileId;
    this.normalizeGallerySortOrder();
  }

  protected insertProjectDownloadFromMedia(): void {
    const media = this.selectedProjectDownloadMedia;
    const url = media?.resolvedAsset?.url ?? media?.publicUrl ?? null;
    if (!media || !url) {
      return;
    }
    const label = `Download ${media.title || media.originalFilename || 'file'}`.replace(/[\r\n]+/g, ' ').replace(/\]/g, '\\]').trim();
    const snippet = `\n[${label}](${url} \"download\")\n`;
    if (this.contentLocale === 'nl') {
      this.projectForm.teaserNl = `${this.projectForm.teaserNl || ''}${snippet}`.trimStart();
    } else {
      this.projectForm.teaser = `${this.projectForm.teaser || ''}${snippet}`.trimStart();
    }
  }

  private normalizeGallerySortOrder(): void {
    const coverImageFileId = this.projectForm.coverImageFileId;
    const ordered = this.sortedGalleryImages.map((image) => ({
      ...image,
      isCover: !!coverImageFileId && image.imageFileId === coverImageFileId,
    }));
    const cover = ordered.find((image) => image.isCover);
    const rest = ordered.filter((image) => image !== cover);
    this.projectForm.images = [...(cover ? [cover] : []), ...rest].map((image, index) => ({ ...image, sortOrder: index }));
  }

  buildProjectFolder(): string {
    return `projects/${slugify(this.projectForm.slug || this.projectForm.title || 'untitled-project')}`;
  }

  generateDutchDraft(): void {
    this.beginDutchDraftGeneration();
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'project',
      context: 'Translate project copy for a developer portfolio. Keep slugs, company names, technology names, repository names, and URLs unchanged unless they are ordinary prose.',
      fields: {
        titleNl: this.projectForm.title,
        teaserNl: this.projectForm.teaser,
        summaryNl: this.projectForm.summary,
        descriptionMarkdownNl: this.projectForm.descriptionMarkdown,
        durationLabelNl: this.projectForm.durationLabel,
        statusNl: this.projectForm.status,
      },
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.applyTranslatedFields(this.projectForm, response.translatedFields, {
          titleNl: 'titleNl',
          teaserNl: 'teaserNl',
          summaryNl: 'summaryNl',
          descriptionMarkdownNl: 'descriptionMarkdownNl',
          durationLabelNl: 'durationLabelNl',
          statusNl: 'statusNl',
        });
        this.finishDutchDraftGeneration(response, 'Dutch draft generated from the English project copy.');
      },
      error: (error) => {
        this.failDutchDraftGeneration(error, 'Generating the Dutch project draft failed.');
      },
    });
  }
}
