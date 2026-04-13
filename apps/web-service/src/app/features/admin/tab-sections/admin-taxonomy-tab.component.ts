import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminReferenceData } from '../../../shared/models/admin.model';
import { AdminBlogTagForm, AdminSkillCategoryForm, AdminSkillForm } from '../admin-page.forms';
import { categoryName } from '../admin-page.display.utils';

@Component({
  selector: 'app-admin-taxonomy-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-taxonomy-tab.component.html'
})
export class AdminTaxonomyTabComponent {
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

  categoryName(categoryId: string): string {
    return categoryName(this.referenceData.skillCategories, categoryId);
  }

  selectSkillCategory(categoryId: string): void {
    this.skillCategorySelected.emit(categoryId);
  }

  startNewSkillCategory(): void {
    this.newSkillCategoryStarted.emit();
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
}
