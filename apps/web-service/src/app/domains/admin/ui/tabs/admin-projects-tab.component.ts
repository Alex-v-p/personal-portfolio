import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminProject, AdminReferenceData } from '@domains/admin/model/admin.model';
import { AdminProjectForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { slugify } from '@domains/admin/shell/state/admin-page.utils';

type ContentLocale = 'en' | 'nl';

@Component({
  selector: 'app-admin-projects-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-projects-tab.component.html'
})
export class AdminProjectsTabComponent {
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

  protected isGeneratingDutchDraft = false;
  protected translationMessage = '';
  protected contentLocale: ContentLocale = 'en';

  protected setContentLocale(locale: ContentLocale): void {
    this.contentLocale = locale;
  }

  selectProject(projectId: string): void {
    this.projectSelected.emit(projectId);
  }

  startNewProject(): void {
    this.newProjectStarted.emit();
    this.translationMessage = '';
    this.contentLocale = 'en';
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
    this.isGeneratingDutchDraft = true;
    this.translationMessage = '';
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
        this.projectForm.titleNl = response.translatedFields['titleNl'] ?? this.projectForm.titleNl;
        this.projectForm.teaserNl = response.translatedFields['teaserNl'] ?? this.projectForm.teaserNl;
        this.projectForm.summaryNl = response.translatedFields['summaryNl'] ?? this.projectForm.summaryNl;
        this.projectForm.descriptionMarkdownNl = response.translatedFields['descriptionMarkdownNl'] ?? this.projectForm.descriptionMarkdownNl;
        this.projectForm.durationLabelNl = response.translatedFields['durationLabelNl'] ?? this.projectForm.durationLabelNl;
        this.projectForm.statusNl = response.translatedFields['statusNl'] ?? this.projectForm.statusNl;
        this.contentLocale = 'nl';
        this.translationMessage = 'Dutch draft generated from the English project copy.';
        this.isGeneratingDutchDraft = false;
      },
      error: (error) => {
        this.translationMessage = error?.error?.detail || 'Generating the Dutch project draft failed.';
        this.isGeneratingDutchDraft = false;
      },
    });
  }
}
