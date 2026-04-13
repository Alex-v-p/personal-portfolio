import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminContactMessage } from '../../../shared/models/admin.model';

@Component({
  selector: 'app-admin-messages-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-messages-tab.component.html'
})
export class AdminMessagesTabComponent {
  @Input() messageSearchTerm = '';
  @Input() messageStatusFilter: 'all' | 'unread' | 'read' = 'all';
  @Input() messageSourceFilter = 'all';
  @Input({ required: true }) messageSourceOptions: string[] = [];
  @Input({ required: true }) filteredMessages: AdminContactMessage[] = [];
  @Input() filteredMessageCount = 0;
  @Input() unreadFilteredMessageCount = 0;
  @Input() updatingMessageIds: string[] = [];

  @Output() readonly messageSearchTermChange = new EventEmitter<string>();
  @Output() readonly messageStatusFilterChange = new EventEmitter<'all' | 'unread' | 'read'>();
  @Output() readonly messageSourceFilterChange = new EventEmitter<string>();
  @Output() readonly messageReadToggleRequested = new EventEmitter<AdminContactMessage>();

  onMessageSearchTermChange(value: string): void {
    this.messageSearchTermChange.emit(value);
  }

  onMessageStatusFilterChange(value: 'all' | 'unread' | 'read'): void {
    this.messageStatusFilterChange.emit(value);
  }

  onMessageSourceFilterChange(value: string): void {
    this.messageSourceFilterChange.emit(value);
  }

  toggleMessageRead(message: AdminContactMessage): void {
    this.messageReadToggleRequested.emit(message);
  }

  isMessageUpdating(messageId: string): boolean {
    return this.updatingMessageIds.includes(messageId);
  }
}
