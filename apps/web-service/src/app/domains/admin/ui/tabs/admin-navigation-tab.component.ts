import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminNavigationItem } from '@domains/admin/model/admin.model';
import { AdminNavigationItemForm } from '@domains/admin/model/forms/index';

type ContentLocale = 'en' | 'nl';

@Component({
  selector: 'app-admin-navigation-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-navigation-tab.component.html'
})
export class AdminNavigationTabComponent implements OnChanges {
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['selectedNavigationItemId']) {
      this.contentLocale = 'en';
    }
  }
  @Input({ required: true }) navigationItems: AdminNavigationItem[] = [];
  @Input() selectedNavigationItemId: string | null = null;
  @Input({ required: true }) navigationItemForm!: AdminNavigationItemForm;

  @Output() readonly navigationItemSelected = new EventEmitter<string>();
  @Output() readonly newNavigationItemStarted = new EventEmitter<void>();
  @Output() readonly navigationItemSaved = new EventEmitter<void>();
  @Output() readonly navigationItemDeleted = new EventEmitter<void>();

  protected contentLocale: ContentLocale = 'en';

  get visibleCount(): number {
    return this.navigationItems.filter((item) => item.isVisible).length;
  }

  get externalCount(): number {
    return this.navigationItems.filter((item) => item.isExternal).length;
  }

  get hiddenCount(): number {
    return this.navigationItems.filter((item) => !item.isVisible).length;
  }

  protected setContentLocale(locale: ContentLocale): void {
    this.contentLocale = locale;
  }

  selectNavigationItem(itemId: string): void {
    this.navigationItemSelected.emit(itemId);
  }

  startNewNavigationItem(): void {
    this.newNavigationItemStarted.emit();
  }

  saveNavigationItem(): void {
    this.navigationItemSaved.emit();
  }

  deleteNavigationItem(): void {
    this.navigationItemDeleted.emit();
  }
}
