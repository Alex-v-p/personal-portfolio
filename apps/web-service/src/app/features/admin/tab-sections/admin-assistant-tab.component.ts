import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

import { AdminAssistantKnowledgeStatus } from '../../../shared/models/admin.model';

@Component({
  selector: 'app-admin-assistant-tab',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-assistant-tab.component.html'
})
export class AdminAssistantTabComponent {
  @Input({ required: true }) assistantKnowledgeStatus!: AdminAssistantKnowledgeStatus;
  @Input() isRebuildingAssistantKnowledge = false;

  @Output() readonly rebuildRequested = new EventEmitter<void>();

  rebuildAssistantKnowledge(): void {
    this.rebuildRequested.emit();
  }
}
