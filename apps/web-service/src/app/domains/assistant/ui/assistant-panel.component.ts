import { AsyncPipe, NgClass, NgFor, NgIf } from '@angular/common';
import { Component, EventEmitter, Input, Output, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AssistantApiService } from '@domains/assistant/data/assistant-api.service';
import { AssistantAvailabilityState, AssistantChatState } from '@domains/assistant/model/assistant-chat.model';
import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';

@Component({
  selector: 'app-assistant-panel',
  standalone: true,
  imports: [NgIf, NgFor, NgClass, FormsModule, AsyncPipe, TranslatePipe],
  templateUrl: './assistant-panel.component.html'
})
export class AssistantPanelComponent {
  @Input() mode: 'widget' | 'page' = 'widget';
  @Output() close = new EventEmitter<void>();

  private readonly assistant = inject(AssistantApiService);
  private readonly i18n = inject(I18nService);

  protected readonly state$ = this.assistant.state$;
  protected readonly availability$ = this.assistant.availability$;
  protected draft = '';

  protected get starterPrompts(): string[] {
    return [
      this.i18n.translate('assistantPopup.starterPrompts.projects'),
      this.i18n.translate('assistantPopup.starterPrompts.blog'),
      this.i18n.translate('assistantPopup.starterPrompts.specialities'),
    ];
  }

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
  protected isExternalCitationUrl(url: string | null | undefined): boolean {
    return !!url && /^https?:\/\//i.test(url);
  }

  protected getCitationTarget(url: string | null | undefined): string | null {
    if (!url) {
      return null;
    }
    return this.isExternalCitationUrl(url) ? '_blank' : '_self';
  }


  protected isComposerDisabled(state: AssistantChatState, availability: AssistantAvailabilityState): boolean {
    return state.isLoading || availability.mode === 'offline';
  }

  protected getAvailabilityDotClasses(mode: AssistantAvailabilityState['mode']): string {
    if (mode === 'ready') {
      return 'ui-status-dot-ready';
    }
    if (mode === 'fallback') {
      return 'ui-status-dot-fallback';
    }
    if (mode === 'preview') {
      return 'ui-status-dot-preview';
    }
    if (mode === 'offline') {
      return 'ui-status-dot-offline';
    }
    return 'ui-status-dot-default';
  }

  protected getStatusCardClasses(mode: AssistantAvailabilityState['mode']): string {
    if (mode === 'ready') {
      return 'ui-alert ui-alert-success';
    }
    if (mode === 'fallback') {
      return 'ui-alert ui-alert-warning';
    }
    if (mode === 'preview') {
      return 'ui-alert ui-alert-info';
    }
    if (mode === 'offline') {
      return 'ui-alert ui-alert-danger';
    }
    return 'ui-card-soft ui-text-muted';
  }

  protected getComposerRows(): number {
    return this.mode === 'page' ? 3 : 2;
  }

  protected getComposerHint(availability: AssistantAvailabilityState): string {
    if (availability.mode === 'fallback') {
      return this.i18n.translate('assistantPopup.composer.hints.fallback');
    }
    if (availability.mode === 'preview') {
      return this.i18n.translate('assistantPopup.composer.hints.preview');
    }
    if (availability.mode === 'offline') {
      return this.i18n.translate('assistantPopup.composer.hints.offline');
    }
    return this.i18n.translate('assistantPopup.composer.hints.ready');
  }
}
