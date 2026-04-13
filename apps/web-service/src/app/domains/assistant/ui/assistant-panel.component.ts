import { AsyncPipe, NgClass, NgFor, NgIf } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AssistantApiService } from '@domains/assistant/data/assistant-api.service';

@Component({
  selector: 'app-assistant-panel',
  standalone: true,
  imports: [NgIf, NgFor, NgClass, FormsModule, AsyncPipe],
  templateUrl: './assistant-panel.component.html'
})
export class AssistantPanelComponent {
  @Input() mode: 'widget' | 'page' = 'widget';
  @Output() close = new EventEmitter<void>();

  private readonly assistant = inject(AssistantApiService);

  protected readonly state$ = this.assistant.state$;
  protected draft = '';
  protected readonly starterPrompts = [
    'What projects are in this portfolio?',
    'Tell me about the CMS architecture.',
    'Which blog posts talk about AI or backend work?',
    'What technologies does this portfolio use?',
  ];

  protected sendMessage(): void {
    const message = this.draft.trim();
    if (!message) {
      return;
    }
    this.assistant.sendMessage(message);
    this.draft = '';
  }

  protected submitStarter(prompt: string): void {
    this.draft = prompt;
    this.sendMessage();
  }

  protected resetConversation(): void {
    this.assistant.resetConversation();
  }

  protected handleComposerKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }
}
