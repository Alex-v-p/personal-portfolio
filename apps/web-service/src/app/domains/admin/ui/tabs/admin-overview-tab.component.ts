import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

import { AdminAssistantContextNote, AdminContactMessage, AdminDashboardSummary, AdminMediaFile } from '@domains/admin/model/admin.model';

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
  @Input() assistantContextNotes: AdminAssistantContextNote[] = [];

  @Output() readonly openTab = new EventEmitter<'media' | 'messages' | 'assistant'>();

  get primaryKpis(): Array<{ label: string; value: number; hint: string }> {
    return [
      { label: 'Projects', value: this.dashboard.projects, hint: 'Published and in-progress work' },
      { label: 'Blog posts', value: this.dashboard.blogPosts, hint: 'Entries currently in the CMS' },
      { label: 'Unread messages', value: this.dashboard.unreadMessages, hint: 'Inbox items waiting on review' },
      { label: 'Media files', value: this.dashboard.mediaFiles, hint: 'Assets ready for reuse' },
      { label: 'GitHub snapshots', value: this.dashboard.githubSnapshots, hint: 'Saved public stats snapshots' },
      { label: 'Assistant notes', value: this.assistantContextNotes.length, hint: 'Private RAG notes in the CMS' },
    ];
  }

  get secondaryKpis(): Array<{ label: string; value: number }> {
    return [
      { label: 'Skills', value: this.dashboard.skills },
      { label: 'Skill categories', value: this.dashboard.skillCategories },
      { label: 'Experience', value: this.dashboard.experiences },
      { label: 'Navigation items', value: this.dashboard.navigationItems },
      { label: 'Blog tags', value: this.dashboard.blogTags },
      { label: 'Admin users', value: this.dashboard.adminUsers },
    ];
  }

  get unreadPreviewCount(): number {
    return this.messages.filter((message) => !message.isRead).length;
  }

  setActiveTab(tabId: 'media' | 'messages' | 'assistant'): void {
    this.openTab.emit(tabId);
  }
}
