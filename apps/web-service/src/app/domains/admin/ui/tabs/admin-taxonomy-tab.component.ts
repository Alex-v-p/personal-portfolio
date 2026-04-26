import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminReferenceData } from '@domains/admin/model/admin.model';
import { AdminBlogTagForm, AdminSkillCategoryForm, AdminSkillForm } from '@domains/admin/model/forms/index';
import { categoryName } from '@domains/admin/shell/state/admin-page.display.utils';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';

import { IconPickerComponent, UiIconComponent } from '@shared/icons';
import type { IconGroupKey } from '@shared/icons';

import { AdminLocalizedContentTabBase } from './admin-localized-content-tab.base';

@Component({
  selector: 'app-admin-taxonomy-tab',
  standalone: true,
  imports: [CommonModule, FormsModule, IconPickerComponent, UiIconComponent],
  templateUrl: './admin-taxonomy-tab.component.html'
})
export class AdminTaxonomyTabComponent extends AdminLocalizedContentTabBase {
  private readonly overviewApi = inject(AdminOverviewApiService);

  @Input({ required: true }) referenceData!: AdminReferenceData;
  @Input() selectedSkillCategoryId: string | null = null;
  @Input() selectedSkillId: string | null = null;
  @Input() selectedBlogTagId: string | null = null;
  @Input({ required: true }) skillCategoryForm!: AdminSkillCategoryForm;
  @Input({ required: true }) skillForm!: AdminSkillForm;
  @Input({ required: true }) blogTagForm!: AdminBlogTagForm;

  @Output() readonly skillCategorySelected = new EventEmitter<string>();
  @Output() readonly newSkillCategoryStarted = new EventEmitter<void>();
  @Output() readonly skillCategorySaved = new EventEmitter<void>();
  @Output() readonly skillCategoryDeleted = new EventEmitter<void>();
  @Output() readonly skillSelected = new EventEmitter<string>();
  @Output() readonly newSkillStarted = new EventEmitter<void>();
  @Output() readonly skillSaved = new EventEmitter<void>();
  @Output() readonly skillDeleted = new EventEmitter<void>();
  @Output() readonly blogTagSelected = new EventEmitter<string>();
  @Output() readonly newBlogTagStarted = new EventEmitter<void>();
  @Output() readonly blogTagSaved = new EventEmitter<void>();
  @Output() readonly blogTagDeleted = new EventEmitter<void>();


  protected readonly skillCategoryIconGroups: readonly IconGroupKey[] = ['expertise', 'tech', 'contact', 'social'];
  protected readonly skillIconGroups: readonly IconGroupKey[] = ['tech', 'expertise', 'contact', 'social'];


  get highlightedSkillCount(): number {
    return this.referenceData.skills.filter((skill) => skill.isHighlighted).length;
  }

  categoryName(categoryId: string): string {
    return categoryName(this.referenceData.skillCategories, categoryId);
  }

  skillMetricLabel(skill: { yearsOfExperience?: number | null; proficiencyLabel?: string | null; proficiencyLabelNl?: string | null }): string {
    const explicitLabel = skill.proficiencyLabel || skill.proficiencyLabelNl;

    if (explicitLabel) {
      return explicitLabel;
    }

    if (skill.yearsOfExperience !== null && skill.yearsOfExperience !== undefined) {
      return `${skill.yearsOfExperience} year${skill.yearsOfExperience === 1 ? '' : 's'}`;
    }

    return 'No metric';
  }

  selectSkillCategory(categoryId: string): void {
    this.skillCategorySelected.emit(categoryId);
  }

  startNewSkillCategory(): void {
    this.newSkillCategoryStarted.emit();
    this.resetLocalizedEditingState();
  }

  saveSkillCategory(): void {
    this.skillCategorySaved.emit();
  }

  deleteSkillCategory(): void {
    this.skillCategoryDeleted.emit();
  }

  selectSkill(skillId: string): void {
    this.skillSelected.emit(skillId);
  }

  startNewSkill(): void {
    this.newSkillStarted.emit();
  }

  saveSkill(): void {
    this.skillSaved.emit();
  }

  deleteSkill(): void {
    this.skillDeleted.emit();
  }

  selectBlogTag(tagId: string): void {
    this.blogTagSelected.emit(tagId);
  }

  startNewBlogTag(): void {
    this.newBlogTagStarted.emit();
  }

  saveBlogTag(): void {
    this.blogTagSaved.emit();
  }

  deleteBlogTag(): void {
    this.blogTagDeleted.emit();
  }

  generateDutchDraft(): void {
    this.beginDutchDraftGeneration();
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'skill-category',
      context: 'Translate concise skill-category labels and descriptions for a developer portfolio. Keep technology names unchanged when appropriate.',
      fields: {
        nameNl: this.skillCategoryForm.name,
        descriptionNl: this.skillCategoryForm.description,
      },
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.applyTranslatedFields(this.skillCategoryForm, response.translatedFields, {
          nameNl: 'nameNl',
          descriptionNl: 'descriptionNl',
        });
        this.finishDutchDraftGeneration(response, 'Dutch draft generated from the English skill category.');
      },
      error: (error) => {
        this.failDutchDraftGeneration(error, 'Generating the Dutch skill-category draft failed.');
      },
    });
  }
}
