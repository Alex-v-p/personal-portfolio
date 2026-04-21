import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminNavigationItem } from '@domains/admin/model/admin.model';
import { AdminNavigationItemForm } from '@domains/admin/model/forms/index';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';

type ContentLocale = 'en' | 'nl';

@Component({
  selector: 'app-admin-navigation-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-navigation-tab.component.html'
})
export class AdminNavigationTabComponent {
  private readonly overviewApi = inject(AdminOverviewApiService);

  @Input({ required: true }) navigationItems: AdminNavigationItem[] = [];
  @Input() selectedNavigationItemId: string | null = null;
  @Input({ required: true }) navigationItemForm!: AdminNavigationItemForm;

  @Output() readonly navigationItemSelected = new EventEmitter<string>();
  @Output() readonly newNavigationItemStarted = new EventEmitter<void>();
  @Output() readonly navigationItemSaved = new EventEmitter<void>();
  @Output() readonly navigationItemDeleted = new EventEmitter<void>();

  protected isGeneratingDutchDraft = false;
  protected translationMessage = '';
  protected contentLocale: ContentLocale = 'en';

  protected setContentLocale(locale: ContentLocale): void {
    this.contentLocale = locale;
  }

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
    this.translationMessage = '';
    this.contentLocale = 'en';
  }

  saveNavigationItem(): void {
    this.navigationItemSaved.emit();
  }

  deleteNavigationItem(): void {
    this.navigationItemDeleted.emit();
  }

  generateDutchDraft(): void {
    this.isGeneratingDutchDraft = true;
    this.translationMessage = '';
    this.overviewApi.generateTranslationDraft({
      sourceLocale: 'en',
      targetLocale: 'nl',
      entityType: 'navigation-item',
      context: 'Translate concise navigation labels for a developer portfolio. Keep route paths and proper names unchanged.',
      fields: { labelNl: this.navigationItemForm.label },
    }).pipe(take(1)).subscribe({
      next: (response) => {
        this.navigationItemForm.labelNl = response.translatedFields['labelNl'] ?? this.navigationItemForm.labelNl;
        this.contentLocale = 'nl';
        this.translationMessage = 'Dutch draft generated from the English navigation label.';
        this.isGeneratingDutchDraft = false;
      },
      error: (error) => {
        this.translationMessage = error?.error?.detail || 'Generating the Dutch navigation draft failed.';
        this.isGeneratingDutchDraft = false;
      },
    });
  }
}
