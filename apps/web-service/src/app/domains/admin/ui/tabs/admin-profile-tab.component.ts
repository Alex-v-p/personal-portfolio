import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminMediaFile } from '@domains/admin/model/admin.model';
import { AdminProfileForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { buildProfileMediaFolder } from '@domains/admin/media/state/admin-media.filters';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';

type ContentLocale = 'en' | 'nl';

@Component({
  selector: 'app-admin-profile-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-profile-tab.component.html'
})
export class AdminProfileTabComponent {
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

  protected contentLocale: ContentLocale = 'en';
  protected isGeneratingDutchDraft = false;
  protected translationMessage = '';

  protected setContentLocale(locale: ContentLocale): void {
    this.contentLocale = locale;
  }

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
    this.isGeneratingDutchDraft = true;
    this.translationMessage = '';
    this.contentLocale = 'en';
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'profile',
      context: 'Translate profile copy for a developer portfolio. Keep names, URLs, and platform names unchanged.',
      fields,
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.profileForm.headlineNl = response.translatedFields['headlineNl'] ?? this.profileForm.headlineNl;
        this.profileForm.shortIntroNl = response.translatedFields['shortIntroNl'] ?? this.profileForm.shortIntroNl;
        this.profileForm.longBioNl = response.translatedFields['longBioNl'] ?? this.profileForm.longBioNl;
        this.profileForm.ctaPrimaryLabelNl = response.translatedFields['ctaPrimaryLabelNl'] ?? this.profileForm.ctaPrimaryLabelNl;
        this.profileForm.ctaSecondaryLabelNl = response.translatedFields['ctaSecondaryLabelNl'] ?? this.profileForm.ctaSecondaryLabelNl;
        this.translationMessage = 'Dutch draft generated from the English copy.';
        this.isGeneratingDutchDraft = false;
      },
      error: (error) => {
        this.translationMessage = error?.error?.detail || 'Generating the Dutch draft failed.';
        this.isGeneratingDutchDraft = false;
      },
    });
  }
}
