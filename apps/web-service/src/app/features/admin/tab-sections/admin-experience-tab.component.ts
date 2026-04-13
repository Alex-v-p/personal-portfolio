import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminExperience, AdminMediaFile, AdminSkillOption } from '../../../shared/models/admin.model';
import { AdminExperienceForm, ScopedUploadForm } from '../admin-page.forms';
import { slugify } from '../admin-page.utils';

@Component({
  selector: 'app-admin-experience-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-experience-tab.component.html'
})
export class AdminExperienceTabComponent {
  @Input({ required: true }) experiences: AdminExperience[] = [];
  @Input() selectedExperienceId: string | null = null;
  @Input({ required: true }) experienceForm!: AdminExperienceForm;
  @Input({ required: true }) skills: AdminSkillOption[] = [];
  @Input({ required: true }) mediaFiles: AdminMediaFile[] = [];
  @Input({ required: true }) experienceUploadForm!: ScopedUploadForm;
  @Input() uploadInProgressKey: string | null = null;

  @Output() readonly experienceSelected = new EventEmitter<string>();
  @Output() readonly newExperienceStarted = new EventEmitter<void>();
  @Output() readonly experienceSkillToggled = new EventEmitter<string>();
  @Output() readonly experienceSaved = new EventEmitter<void>();
  @Output() readonly experienceDeleted = new EventEmitter<void>();
  @Output() readonly scopedFileSelected = new EventEmitter<{ event: Event; form: ScopedUploadForm }>();
  @Output() readonly experienceLogoUploadRequested = new EventEmitter<void>();

  selectExperience(experienceId: string): void {
    this.experienceSelected.emit(experienceId);
  }

  startNewExperience(): void {
    this.newExperienceStarted.emit();
  }

  toggleExperienceSkill(skillId: string): void {
    this.experienceSkillToggled.emit(skillId);
  }

  saveExperience(): void {
    this.experienceSaved.emit();
  }

  deleteExperience(): void {
    this.experienceDeleted.emit();
  }

  onScopedFileSelected(event: Event, form: ScopedUploadForm): void {
    this.scopedFileSelected.emit({ event, form });
  }

  uploadExperienceLogo(): void {
    this.experienceLogoUploadRequested.emit();
  }

  mediaPreview(mediaId: string | null | undefined): AdminMediaFile | undefined {
    return this.mediaFiles.find((item) => item.id === mediaId);
  }

  buildExperienceFolder(): string {
    return `experience/${slugify(this.experienceForm.organizationName || this.experienceForm.roleTitle || 'experience')}`;
  }
}
