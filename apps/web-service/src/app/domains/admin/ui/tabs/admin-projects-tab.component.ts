import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminProject, AdminReferenceData } from '@domains/admin/model/admin.model';
import { AdminProjectForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { slugify } from '@domains/admin/shell/state/admin-page.utils';

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
