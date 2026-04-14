import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminProject, AdminReferenceData } from '@domains/admin/model/admin.model';
import { AdminProjectForm, ScopedUploadForm } from '@domains/admin/model/forms/index';
import { slugify } from '@domains/admin/shell/state/admin-page.utils';

@Component({
  selector: 'app-admin-projects-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-projects-tab.component.html'
})
export class AdminProjectsTabComponent {
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
}
