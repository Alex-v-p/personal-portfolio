import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminNavigationItem } from '@domains/admin/model/admin.model';
import { AdminNavigationItemForm } from '@domains/admin/model/forms/index';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';

import { AdminLocalizedContentTabBase } from './admin-localized-content-tab.base';

@Component({
  selector: 'app-admin-navigation-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-navigation-tab.component.html'
})
export class AdminNavigationTabComponent extends AdminLocalizedContentTabBase {
  private readonly overviewApi = inject(AdminOverviewApiService);

  @Input({ required: true }) navigationItems: AdminNavigationItem[] = [];
  @Input() selectedNavigationItemId: string | null = null;
  @Input({ required: true }) navigationItemForm!: AdminNavigationItemForm;

  @Output() readonly navigationItemSelected = new EventEmitter<string>();
  @Output() readonly newNavigationItemStarted = new EventEmitter<void>();
  @Output() readonly navigationItemSaved = new EventEmitter<void>();
  @Output() readonly navigationItemDeleted = new EventEmitter<void>();


  get visibleCount(): number {
    return this.navigationItems.filter((item) => item.isVisible).length;
  }

  get externalCount(): number {
    return this.navigationItems.filter((item) => item.isExternal).length;
  }

  get hiddenCount(): number {
    return this.navigationItems.filter((item) => !item.isVisible).length;
  }

  selectNavigationItem(itemId: string): void {
    this.navigationItemSelected.emit(itemId);
  }

  startNewNavigationItem(): void {
    this.newNavigationItemStarted.emit();
    this.resetLocalizedEditingState();
  }

  saveNavigationItem(): void {
    this.navigationItemSaved.emit();
  }

  deleteNavigationItem(): void {
    this.navigationItemDeleted.emit();
  }

  generateDutchDraft(): void {
    this.beginDutchDraftGeneration();
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'navigation-item',
      context: 'Translate concise navigation labels for a developer portfolio. Keep route paths and proper names unchanged.',
      fields: { labelNl: this.navigationItemForm.label },
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.applyTranslatedFields(this.navigationItemForm, response.translatedFields, { labelNl: 'labelNl' });
        this.finishDutchDraftGeneration(response, 'Dutch draft generated from the English navigation label.');
      },
      error: (error) => {
        this.failDutchDraftGeneration(error, 'Generating the Dutch navigation draft failed.');
      },
    });
  }
}
