import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminMediaFile } from '@domains/admin/model/admin.model';
import { AdminProfileForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { buildProfileMediaFolder } from '@domains/admin/media/state/admin-media.filters';

@Component({
  selector: 'app-admin-profile-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-profile-tab.component.html'
})
export class AdminProfileTabComponent {
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
}
