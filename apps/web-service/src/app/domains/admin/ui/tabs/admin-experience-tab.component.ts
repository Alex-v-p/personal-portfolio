import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminExperience, AdminMediaFile, AdminSkillOption } from '@domains/admin/model/admin.model';
import { AdminExperienceForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { slugify } from '@domains/admin/shell/state/admin-page.utils';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';

type ContentLocale = 'en' | 'nl';

@Component({
  selector: 'app-admin-experience-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-experience-tab.component.html'
})
export class AdminExperienceTabComponent {
  private readonly overviewApi = inject(AdminOverviewApiService);

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

  protected isGeneratingDutchDraft = false;
  protected translationMessage = '';
  protected contentLocale: ContentLocale = 'en';

  protected setContentLocale(locale: ContentLocale): void {
    this.contentLocale = locale;
  }

  selectExperience(experienceId: string): void {
    this.experienceSelected.emit(experienceId);
  }

  startNewExperience(): void {
    this.newExperienceStarted.emit();
    this.translationMessage = '';
    this.contentLocale = 'en';
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

  generateDutchDraft(): void {
    this.isGeneratingDutchDraft = true;
    this.translationMessage = '';
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'experience',
      context: 'Translate an experience entry for a developer portfolio. Keep organization names and technology names unchanged where appropriate.',
      fields: {
        roleTitleNl: this.experienceForm.roleTitle,
        summaryNl: this.experienceForm.summary,
        descriptionMarkdownNl: this.experienceForm.descriptionMarkdown,
      },
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.experienceForm.roleTitleNl = response.translatedFields['roleTitleNl'] ?? this.experienceForm.roleTitleNl;
        this.experienceForm.summaryNl = response.translatedFields['summaryNl'] ?? this.experienceForm.summaryNl;
        this.experienceForm.descriptionMarkdownNl = response.translatedFields['descriptionMarkdownNl'] ?? this.experienceForm.descriptionMarkdownNl;
        this.contentLocale = 'nl';
        this.translationMessage = 'Dutch draft generated from the English experience copy.';
        this.isGeneratingDutchDraft = false;
      },
      error: (error) => {
        this.translationMessage = error?.error?.detail || 'Generating the Dutch experience draft failed.';
        this.isGeneratingDutchDraft = false;
      },
    });
  }
}
