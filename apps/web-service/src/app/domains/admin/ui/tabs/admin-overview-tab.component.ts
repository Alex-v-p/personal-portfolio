import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

import { AdminContactMessage, AdminDashboardSummary, AdminMediaFile } from '@domains/admin/model/admin.model';

@Component({
  selector: 'app-admin-overview-tab',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-overview-tab.component.html'
})
export class AdminOverviewTabComponent {
  @Input({ required: true }) dashboard!: AdminDashboardSummary;
  @Input({ required: true }) messages: AdminContactMessage[] = [];
  @Input({ required: true }) mediaFiles: AdminMediaFile[] = [];

  @Output() readonly openTab = new EventEmitter<'media' | 'messages'>();

  setActiveTab(tabId: 'media' | 'messages'): void {
    this.openTab.emit(tabId);
  }
}
