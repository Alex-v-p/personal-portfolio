import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { forkJoin } from 'rxjs';
import { finalize, take } from 'rxjs/operators';

import { AdminMediaApiService } from '@domains/admin/data/api/admin-media-api.service';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminProfileApiService } from '@domains/admin/data/api/admin-profile-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminMediaFile } from '@domains/admin/model/admin.model';
import { AdminProfileForm, ScopedUploadForm, createEmptyProfileForm, createEmptyScopedUploadForm, toProfileForm } from '@domains/admin/model/forms/index';
import { buildProfileMediaFolder, resetScopedUploadForm } from '@domains/admin/media/state/admin-media.filters';
import { AdminProfileTabComponent } from '@domains/admin/ui/tabs/admin-profile-tab.component';

@Component({
  selector: 'app-admin-profile-page',
  standalone: true,
  imports: [CommonModule, AdminProfileTabComponent],
  templateUrl: './admin-profile.page.html',
})
export class AdminProfilePageComponent implements OnInit {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly profileApi = inject(AdminProfileApiService);
  private readonly mediaApi = inject(AdminMediaApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';
  protected profileForm: AdminProfileForm = createEmptyProfileForm();
  protected mediaFiles: AdminMediaFile[] = [];
  protected profileAvatarUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected profileHeroUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected profileResumeUploadForm: ScopedUploadForm = createEmptyScopedUploadForm();
  protected uploadInProgressKey: string | null = null;

  ngOnInit(): void {
    this.loadProfilePage(false);
  }

  protected reload(): void {
    this.loadProfilePage(true);
  }

  protected addSocialLink(): void {
    this.profileForm.socialLinks = [
      ...this.profileForm.socialLinks,
      { platform: '', label: '', url: '', iconKey: null, sortOrder: this.profileForm.socialLinks.length, isVisible: true },
    ];
  }

  protected removeSocialLink(index: number): void {
    this.profileForm.socialLinks = this.profileForm.socialLinks.filter((_, itemIndex) => itemIndex !== index);
  }

  protected saveProfile(): void {
    const payload = {
      firstName: this.profileForm.firstName,
      lastName: this.profileForm.lastName,
      headline: this.profileForm.headline,
      headlineNl: this.profileForm.headlineNl || null,
      shortIntro: this.profileForm.shortIntro,
      shortIntroNl: this.profileForm.shortIntroNl || null,
      longBio: this.profileForm.longBio || null,
      longBioNl: this.profileForm.longBioNl || null,
      location: this.profileForm.location || null,
      email: this.profileForm.email || null,
      phone: this.profileForm.phone || null,
      avatarFileId: this.profileForm.avatarFileId || null,
      heroImageFileId: this.profileForm.heroImageFileId || null,
      resumeFileId: this.profileForm.resumeFileId || null,
      ctaPrimaryLabel: this.profileForm.ctaPrimaryLabel || null,
      ctaPrimaryLabelNl: this.profileForm.ctaPrimaryLabelNl || null,
      ctaPrimaryUrl: this.profileForm.ctaPrimaryUrl || null,
      ctaSecondaryLabel: this.profileForm.ctaSecondaryLabel || null,
      ctaSecondaryLabelNl: this.profileForm.ctaSecondaryLabelNl || null,
      ctaSecondaryUrl: this.profileForm.ctaSecondaryUrl || null,
      isPublic: this.profileForm.isPublic,
      socialLinks: this.profileForm.socialLinks.map((link, index) => ({ ...link, sortOrder: index })),
    };

    this.profileApi.updateProfile(payload).pipe(take(1)).subscribe({
      next: () => {
        this.statusMessage = 'Profile updated.';
        this.loadProfilePage(false);
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.statusMessage = error?.error?.detail || 'Saving the profile failed.';
      },
    });
  }

  protected onScopedFileSelected(event: Event, form: ScopedUploadForm): void {
    const input = event.target as HTMLInputElement | null;
    form.file = input?.files?.[0] ?? null;
  }

  protected uploadProfileAvatar(): void {
    this.uploadScopedMedia('profile-avatar', this.profileAvatarUploadForm, (media) => {
      this.profileForm.avatarFileId = media.id;
    });
  }

  protected uploadProfileHero(): void {
    this.uploadScopedMedia('profile-hero', this.profileHeroUploadForm, (media) => {
      this.profileForm.heroImageFileId = media.id;
    });
  }

  protected uploadProfileResume(): void {
    this.uploadScopedMedia('profile-resume', this.profileResumeUploadForm, (media) => {
      this.profileForm.resumeFileId = media.id;
    });
  }

  private loadProfilePage(showReloadMessage: boolean): void {
    this.isLoading = true;
    this.errorMessage = '';
    if (showReloadMessage) {
      this.statusMessage = 'Refreshing profile workspace…';
    }

    forkJoin({
      profile: this.profileApi.getProfile(),
      referenceData: this.overviewApi.getReferenceData(),
    }).pipe(
      take(1),
      finalize(() => {
        this.isLoading = false;
        this.changeDetectorRef.detectChanges();
      }),
    ).subscribe({
      next: ({ profile, referenceData }) => {
        this.profileForm = toProfileForm(profile);
        this.mediaFiles = referenceData.mediaFiles;
        if (showReloadMessage) {
          this.statusMessage = 'Profile workspace refreshed.';
        }
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.errorMessage = error?.error?.detail || 'The profile workspace could not be loaded.';
      },
    });
  }

  private uploadScopedMedia(
    uploadKey: string,
    form: ScopedUploadForm,
    onSuccess: (media: AdminMediaFile) => void,
  ): void {
    if (!form.file) {
      this.statusMessage = 'Choose a file before uploading.';
      return;
    }

    const folder = buildProfileMediaFolder(this.profileForm.firstName, this.profileForm.lastName);
    const formData = new FormData();
    formData.append('file', form.file);
    formData.append('folder', folder);
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
        this.mediaFiles = [media, ...this.mediaFiles.filter((item) => item.id !== media.id)];
        onSuccess(media);
        resetScopedUploadForm(form);
        this.statusMessage = `Media uploaded to ${folder} and selected automatically.`;
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
