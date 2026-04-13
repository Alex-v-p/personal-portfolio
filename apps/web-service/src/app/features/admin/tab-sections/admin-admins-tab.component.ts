import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminUser } from '../../../shared/models/admin.model';
import { AdminUserForm } from '../admin-page.forms';

@Component({
  selector: 'app-admin-admins-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-admins-tab.component.html'
})
export class AdminAdminsTabComponent {
  @Input({ required: true }) adminUsers: AdminUser[] = [];
  @Input() selectedAdminUserId: string | null = null;
  @Input() currentAdminId: string | null = null;
  @Input({ required: true }) adminUserForm!: AdminUserForm;

  @Output() readonly adminUserSelected = new EventEmitter<string>();
  @Output() readonly newAdminUserStarted = new EventEmitter<void>();
  @Output() readonly adminUserSaved = new EventEmitter<void>();
  @Output() readonly adminUserDeleted = new EventEmitter<void>();

  selectAdminUser(adminUserId: string): void {
    this.adminUserSelected.emit(adminUserId);
  }

  startNewAdminUser(): void {
    this.newAdminUserStarted.emit();
  }

  saveAdminUser(): void {
    this.adminUserSaved.emit();
  }

  deleteAdminUser(): void {
    this.adminUserDeleted.emit();
  }
}
