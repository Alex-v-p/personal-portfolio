import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminMediaFile } from '@domains/admin/model/admin.model';
import { AdminProfileForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { buildProfileMediaFolder } from '@domains/admin/media/state/admin-media.filters';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';

import { IconPickerComponent } from '@shared/icons';
import type { IconGroupKey } from '@shared/icons';

import { AdminLocalizedContentTabBase } from './admin-localized-content-tab.base';

@Component({
  selector: 'app-admin-profile-tab',
  standalone: true,
  imports: [CommonModule, FormsModule, IconPickerComponent],
  templateUrl: './admin-profile-tab.component.html'
})
export class AdminProfileTabComponent extends AdminLocalizedContentTabBase {
  private readonly overviewApi = inject(AdminOverviewApiService);

  @Input({ required: true }) profileForm!: AdminProfileForm;
  @Input({ required: true }) mediaFiles: AdminMediaFile[] = [];
  @Input({ required: true }) profileAvatarUploadForm!: ScopedUploadForm;
  @Input({ required: true }) profileHeroUploadForm!: ScopedUploadForm;
  @Input({ required: true }) profileResumeUploadForm!: ScopedUploadForm;
  @Input() uploadInProgressKey: string | null = null;

  @Output() readonly socialLinkAdded = new EventEmitter<void>();
  @Output() readonly socialLinkRemoved = new EventEmitter<number>();
  @Output() readonly profileSaved = new EventEmitter<void>();
  @Output() readonly scopedFileSelected = new EventEmitter<{ event: Event; form: ScopedUploadForm }>();
  @Output() readonly profileAvatarUploadRequested = new EventEmitter<void>();
  @Output() readonly profileHeroUploadRequested = new EventEmitter<void>();
  @Output() readonly profileResumeUploadRequested = new EventEmitter<void>();

  protected readonly socialIconGroups: readonly IconGroupKey[] = ['social', 'contact'];


  addSocialLink(): void {
    this.socialLinkAdded.emit();
  }

  removeSocialLink(index: number): void {
    this.socialLinkRemoved.emit(index);
  }

  saveProfile(): void {
    this.profileSaved.emit();
  }

  onScopedFileSelected(event: Event, form: ScopedUploadForm): void {
    this.scopedFileSelected.emit({ event, form });
  }

  uploadProfileAvatar(): void {
    this.profileAvatarUploadRequested.emit();
  }

  uploadProfileHero(): void {
    this.profileHeroUploadRequested.emit();
  }

  uploadProfileResume(): void {
    this.profileResumeUploadRequested.emit();
  }

  buildProfileFolder(): string {
    return buildProfileMediaFolder(this.profileForm.firstName, this.profileForm.lastName);
  }

  generateDutchDraft(): void {
    const fields = {
      headlineNl: this.profileForm.headline,
      shortIntroNl: this.profileForm.shortIntro,
      longBioNl: this.profileForm.longBio,
      ctaPrimaryLabelNl: this.profileForm.ctaPrimaryLabel,
      ctaSecondaryLabelNl: this.profileForm.ctaSecondaryLabel,
    };
    this.beginDutchDraftGeneration();
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'profile',
      context: 'Translate profile copy for a developer portfolio. Keep names, URLs, and platform names unchanged.',
      fields,
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.applyTranslatedFields(this.profileForm, response.translatedFields, {
          headlineNl: 'headlineNl',
          shortIntroNl: 'shortIntroNl',
          longBioNl: 'longBioNl',
          ctaPrimaryLabelNl: 'ctaPrimaryLabelNl',
          ctaSecondaryLabelNl: 'ctaSecondaryLabelNl',
        });
        this.finishDutchDraftGeneration(response, 'Dutch draft generated from the English copy.');
      },
      error: (error) => {
        this.failDutchDraftGeneration(error, 'Generating the Dutch draft failed.');
      },
    });
  }
}
