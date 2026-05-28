import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { finalize, take } from 'rxjs/operators';

import { AdminMessagesApiService } from '@domains/admin/data/api/admin-messages-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminContactMessage } from '@domains/admin/model/admin.model';
import { AdminMessagesTabComponent } from '@domains/admin/ui/tabs/admin-messages-tab.component';
import { AdminMessageStatusFilter, buildMessageSourceOptions, countUnreadMessages, filterMessages } from '@domains/admin/messages/state/admin-messages.filters';

@Component({
  selector: 'app-admin-messages-page',
  standalone: true,
  imports: [CommonModule, AdminMessagesTabComponent],
  templateUrl: './admin-messages.page.html',
})
export class AdminMessagesPageComponent implements OnInit {
  private readonly messagesApi = inject(AdminMessagesApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';
  protected messages: AdminContactMessage[] = [];
  protected updatingMessageIds: string[] = [];

  protected messageSearchTerm = '';
  protected messageStatusFilter: AdminMessageStatusFilter = 'all';
  protected messageSourceFilter = 'all';

  ngOnInit(): void {
    this.loadMessages(false);
  }

  protected reload(): void {
    this.loadMessages(true);
  }

  protected get messageSourceOptions(): string[] {
    return buildMessageSourceOptions(this.messages);
  }

  protected get filteredMessages(): AdminContactMessage[] {
    return filterMessages(this.messages, {
      searchTerm: this.messageSearchTerm,
      status: this.messageStatusFilter,
      source: this.messageSourceFilter,
    });
  }

  protected get filteredMessageCount(): number {
    return this.filteredMessages.length;
  }

  protected get unreadFilteredMessageCount(): number {
    return countUnreadMessages(this.filteredMessages);
  }

  protected toggleMessageRead(message: AdminContactMessage): void {
    const nextIsRead = !message.isRead;
    const previousMessages = this.messages.map((item) => ({ ...item }));
    this.updatingMessageIds = [...this.updatingMessageIds, message.id];
    this.messages = this.messages.map((item) => item.id === message.id ? { ...item, isRead: nextIsRead } : item);
    this.statusMessage = nextIsRead ? 'Marking message as read…' : 'Marking message as unread…';
    this.changeDetectorRef.detectChanges();

    this.messagesApi.updateContactMessage(message.id, nextIsRead).pipe(take(1)).subscribe({
      next: (updatedMessage) => {
        this.messages = this.messages.map((item) => item.id === updatedMessage.id ? updatedMessage : item);
        this.statusMessage = updatedMessage.isRead ? 'Message marked as read.' : 'Message marked as unread.';
        this.updatingMessageIds = this.updatingMessageIds.filter((id) => id !== message.id);
        this.changeDetectorRef.detectChanges();
      },
      error: (error) => {
        if (error?.status === 401) {
          this.updatingMessageIds = this.updatingMessageIds.filter((id) => id !== message.id);
          this.adminSession.logout();
          return;
        }

        this.messages = previousMessages;
        this.statusMessage = error?.error?.detail || 'Updating message status failed.';
        this.updatingMessageIds = this.updatingMessageIds.filter((id) => id !== message.id);
        this.changeDetectorRef.detectChanges();
      },
    });
  }

  private loadMessages(showReloadMessage: boolean): void {
    this.isLoading = true;
    this.errorMessage = '';
    if (showReloadMessage) {
      this.statusMessage = 'Refreshing inbox…';
    }

    this.messagesApi.getContactMessages().pipe(
      take(1),
      finalize(() => {
        this.isLoading = false;
        this.changeDetectorRef.detectChanges();
      }),
    ).subscribe({
      next: (response) => {
        this.messages = response.items;
        if (this.messageSourceFilter !== 'all' && !this.messageSourceOptions.includes(this.messageSourceFilter)) {
          this.messageSourceFilter = 'all';
        }
        if (showReloadMessage) {
          this.statusMessage = 'Inbox refreshed.';
        }
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.errorMessage = error?.error?.detail || 'The contact inbox could not be loaded.';
      },
    });
  }
}
