import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminNavigationItem } from '@domains/admin/model/admin.model';
import { AdminNavigationItemForm } from '@domains/admin/model/forms/index';

@Component({
  selector: 'app-admin-navigation-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-navigation-tab.component.html'
})
export class AdminNavigationTabComponent {
  @Input({ required: true }) navigationItems: AdminNavigationItem[] = [];
  @Input() selectedNavigationItemId: string | null = null;
  @Input({ required: true }) navigationItemForm!: AdminNavigationItemForm;

  @Output() readonly navigationItemSelected = new EventEmitter<string>();
  @Output() readonly newNavigationItemStarted = new EventEmitter<void>();
  @Output() readonly navigationItemSaved = new EventEmitter<void>();
  @Output() readonly navigationItemDeleted = new EventEmitter<void>();

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
