import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Subscription, timer } from 'rxjs';
import { switchMap, takeWhile } from 'rxjs/operators';

import {
  AssistantChatMessage,
  AssistantChatResponse,
  AssistantChatState,
  AssistantChatTaskAccepted,
  AssistantChatTaskStatus,
} from '../model/assistant-chat.model';
import { SiteTrackingService } from '@domains/site-activity/data/site-tracking.service';

const ASSISTANT_STATE_STORAGE_KEY = 'portfolio.assistant.state';
const ASSISTANT_SESSION_STORAGE_KEY = 'portfolio.assistant.session-id';
const ASSISTANT_MAX_TASK_POLLS = 90;

const resolveAssistantApiBaseUrl = (): string => '/ai';

@Injectable({ providedIn: 'root' })
export class AssistantApiService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly assistantApiBaseUrl = resolveAssistantApiBaseUrl();
  private readonly siteTracking = inject(SiteTrackingService);
  private readonly stateSubject = new BehaviorSubject<AssistantChatState>(this.restoreState());

  private chatTaskSubscription?: Subscription;

  readonly state$ = this.stateSubject.asObservable();

  get snapshot(): AssistantChatState {
    return this.stateSubject.value;
  }

  sendMessage(rawMessage: string, pagePath?: string): void {
    const message = rawMessage.trim();
    if (!message || this.snapshot.isLoading) {
      return;
    }

    const optimisticMessage: AssistantChatMessage = {
      role: 'user',
      text: message,
      createdAt: new Date().toISOString(),
      citations: [],
    };

    this.patchState({
      isLoading: true,
      errorMessage: null,
      messages: [...this.snapshot.messages, optimisticMessage],
    });

    this.http.post<AssistantChatResponse | AssistantChatTaskAccepted>(`${this.assistantApiBaseUrl}/chat/respond`, {
      message,
      conversation_id: this.snapshot.conversationId,
      session_id: this.getOrCreateAssistantSessionId(),
      site_session_id: this.siteTracking.sessionId,
      visitor_id: this.siteTracking.visitorId,
      page_path: pagePath ?? this.router.url,
    }).subscribe({
      next: (response) => {
        if (this.isTaskAccepted(response)) {
          this.patchState({
            conversationId: response.conversationId ?? this.snapshot.conversationId,
            isLoading: true,
            errorMessage: null,
          });
          this.pollChatTask(response.taskId, response.pollAfterMs);
          return;
        }
        this.applyChatResponse(response);
      },
      error: (error) => {
        this.applyFailureMessage(error?.error?.detail || 'The assistant request failed. Check that the assistant service or reverse proxy is running and try again.');
      }
    });
  }

  resetConversation(): void {
    this.chatTaskSubscription?.unsubscribe();
    const emptyState: AssistantChatState = {
      conversationId: null,
      messages: [],
      isLoading: false,
      errorMessage: null,
    };
    if (typeof window !== 'undefined') {
      window.sessionStorage.removeItem(ASSISTANT_SESSION_STORAGE_KEY);
    }
    this.stateSubject.next(emptyState);
    this.persistState(emptyState);
  }

  private pollChatTask(taskId: string, pollAfterMs: number): void {
    this.chatTaskSubscription?.unsubscribe();
    let pollCount = 0;
    this.chatTaskSubscription = timer(pollAfterMs, pollAfterMs)
      .pipe(
        switchMap(() => this.http.get<AssistantChatTaskStatus>(`${this.assistantApiBaseUrl}/chat/tasks/${taskId}`)),
        takeWhile((task) => {
          pollCount += 1;
          const stillPending = task.status === 'queued' || task.status === 'running';
          return stillPending && pollCount < ASSISTANT_MAX_TASK_POLLS;
        }, true),
      )
      .subscribe({
        next: (task) => {
          if (task.status === 'succeeded' && task.message) {
            this.applyChatResponse({
              conversationId: task.conversationId,
              message: task.message,
              providerBackend: task.providerBackend ?? 'unknown',
              citations: task.citations ?? [],
            });
            return;
          }
          if (task.status === 'failed') {
            this.applyFailureMessage(task.errorMessage || 'The assistant worker failed to generate a response.');
            return;
          }
          if (pollCount >= ASSISTANT_MAX_TASK_POLLS) {
            this.applyFailureMessage('The assistant worker is still processing your message. Please try again in a moment.');
          }
        },
        error: (error) => {
          this.applyFailureMessage(error?.error?.detail || 'Checking assistant message progress failed.');
        }
      });
  }

  private applyChatResponse(response: AssistantChatResponse): void {
    const assistantMessage: AssistantChatMessage = {
      role: 'assistant',
      text: response.message,
      createdAt: new Date().toISOString(),
      citations: response.citations ?? [],
    };
    this.patchState({
      conversationId: response.conversationId ?? this.snapshot.conversationId,
      messages: [...this.snapshot.messages, assistantMessage],
      isLoading: false,
      errorMessage: null,
    });
  }

  private applyFailureMessage(text: string): void {
    const fallbackMessage: AssistantChatMessage = {
      role: 'assistant',
      text,
      createdAt: new Date().toISOString(),
      citations: [],
    };
    this.patchState({
      messages: [...this.snapshot.messages, fallbackMessage],
      isLoading: false,
      errorMessage: fallbackMessage.text,
    });
  }

  private patchState(partial: Partial<AssistantChatState>): void {
    const nextState: AssistantChatState = {
      ...this.snapshot,
      ...partial,
    };
    this.stateSubject.next(nextState);
    this.persistState(nextState);
  }

  private restoreState(): AssistantChatState {
    if (typeof window === 'undefined') {
      return { conversationId: null, messages: [], isLoading: false, errorMessage: null };
    }

    const rawState = window.sessionStorage.getItem(ASSISTANT_STATE_STORAGE_KEY);
    if (!rawState) {
      return { conversationId: null, messages: [], isLoading: false, errorMessage: null };
    }

    try {
      const parsed = JSON.parse(rawState) as AssistantChatState;
      return {
        conversationId: parsed.conversationId ?? null,
        messages: Array.isArray(parsed.messages) ? parsed.messages : [],
        isLoading: false,
        errorMessage: null,
      };
    } catch {
      return { conversationId: null, messages: [], isLoading: false, errorMessage: null };
    }
  }

  private persistState(state: AssistantChatState): void {
    if (typeof window === 'undefined') {
      return;
    }
    window.sessionStorage.setItem(ASSISTANT_STATE_STORAGE_KEY, JSON.stringify(state));
  }

  private getOrCreateAssistantSessionId(): string {
    if (typeof window === 'undefined') {
      return 'server-render';
    }
    const existing = window.sessionStorage.getItem(ASSISTANT_SESSION_STORAGE_KEY);
    if (existing) {
      return existing;
    }
    const sessionId = crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    window.sessionStorage.setItem(ASSISTANT_SESSION_STORAGE_KEY, sessionId);
    return sessionId;
  }

  private isTaskAccepted(value: AssistantChatResponse | AssistantChatTaskAccepted): value is AssistantChatTaskAccepted {
    return !!value && typeof value === 'object' && 'taskId' in value;
  }
}
