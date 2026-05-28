import { AdminContactMessage } from '@domains/admin/model/admin.model';
import { matchesSearch } from '@domains/admin/shell/state/admin-page.utils';

export type AdminMessageStatusFilter = 'all' | 'unread' | 'read';

export interface AdminMessageFilterState {
  searchTerm: string;
  status: AdminMessageStatusFilter;
  source: string;
}

export function buildMessageSourceOptions(messages: AdminContactMessage[]): string[] {
  return Array.from(new Set(messages.map((message) => message.sourcePage).filter(Boolean))).sort((left, right) => left.localeCompare(right));
}

export function filterMessages(messages: AdminContactMessage[], filters: AdminMessageFilterState): AdminContactMessage[] {
  return [...messages]
    .filter((message) => filters.status === 'all' || (filters.status === 'unread' ? !message.isRead : message.isRead))
    .filter((message) => filters.source === 'all' || message.sourcePage === filters.source)
    .filter((message) => matchesSearch([message.name, message.email, message.subject, message.message, message.sourcePage], filters.searchTerm))
    .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
}

export function countUnreadMessages(messages: AdminContactMessage[]): number {
  return messages.filter((message) => !message.isRead).length;
}
