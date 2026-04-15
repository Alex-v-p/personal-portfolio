import { AsyncPipe, NgClass, NgFor, NgIf } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AssistantApiService } from '@domains/assistant/data/assistant-api.service';
import { AssistantAvailabilityState, AssistantChatState } from '@domains/assistant/model/assistant-chat.model';

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
  protected readonly availability$ = this.assistant.availability$;
  protected draft = '';
  protected readonly starterPrompts = [
    'What projects are in this portfolio?',
    'Tell me about the CMS architecture.',
    'Which blog posts talk about AI or backend work?',
    'What technologies does this portfolio use?',
  ];

  protected sendMessage(): void {
    const message = this.draft.trim();
    if (!message || this.assistant.availabilitySnapshot.mode === 'offline') {
      return;
    }
    this.assistant.sendMessage(message);
    this.draft = '';
  }

  protected submitStarter(prompt: string): void {
    if (this.assistant.availabilitySnapshot.mode === 'offline') {
      return;
    }
    this.draft = prompt;
    this.sendMessage();
  }

  protected resetConversation(): void {
    this.assistant.resetConversation();
  }

  protected refreshAvailability(): void {
    this.assistant.refreshAvailability();
  }

  protected handleComposerKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  protected isComposerDisabled(state: AssistantChatState, availability: AssistantAvailabilityState): boolean {
    return state.isLoading || availability.mode === 'offline';
  }

  protected getAvailabilityDotClasses(mode: AssistantAvailabilityState['mode']): string {
    if (mode === 'ready') {
      return 'bg-emerald-500';
    }
    if (mode === 'fallback') {
      return 'bg-amber-500';
    }
    if (mode === 'preview') {
      return 'bg-sky-500';
    }
    if (mode === 'offline') {
      return 'bg-rose-500';
    }
    return 'bg-stone-400';
  }

  protected getStatusCardClasses(mode: AssistantAvailabilityState['mode']): string {
    if (mode === 'ready') {
      return 'border-emerald-200 bg-emerald-50/80 text-emerald-900';
    }
    if (mode === 'fallback') {
      return 'border-amber-200 bg-amber-50/80 text-amber-950';
    }
    if (mode === 'preview') {
      return 'border-sky-200 bg-sky-50/80 text-sky-950';
    }
    if (mode === 'offline') {
      return 'border-rose-200 bg-rose-50/80 text-rose-950';
    }
    return 'border-stone-200 bg-stone-50 text-stone-700';
  }

  protected getComposerHint(availability: AssistantAvailabilityState): string {
    if (availability.mode === 'fallback') {
      return 'Model offline · replies will use indexed portfolio content only';
    }
    if (availability.mode === 'preview') {
      return 'Preview mode · responses are coming from the local fallback formatter';
    }
    if (availability.mode === 'offline') {
      return 'Assistant unavailable · check the assistant service and local model';
    }
    return 'Enter sends · Shift+Enter adds a line';
  }
}
