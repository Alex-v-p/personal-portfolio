import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Subscription, timer } from 'rxjs';
import { switchMap, takeWhile } from 'rxjs/operators';

import {
  AssistantAvailabilityState,
  AssistantChatMessage,
  AssistantChatResponse,
  AssistantChatState,
  AssistantChatTaskAccepted,
  AssistantChatTaskStatus,
  AssistantHealthResponse,
} from '../model/assistant-chat.model';
import { SiteTrackingService } from '@domains/site-activity/data/site-tracking.service';

const ASSISTANT_STATE_STORAGE_KEY = 'portfolio.assistant.state';
const ASSISTANT_SESSION_STORAGE_KEY = 'portfolio.assistant.session-id';
const ASSISTANT_MAX_TASK_POLLS = 90;
const ASSISTANT_AVAILABILITY_POLL_MS = 30000;

const resolveAssistantApiBaseUrl = (): string => '/ai';

@Injectable({ providedIn: 'root' })
export class AssistantApiService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly assistantApiBaseUrl = resolveAssistantApiBaseUrl();
  private readonly siteTracking = inject(SiteTrackingService);
  private readonly stateSubject = new BehaviorSubject<AssistantChatState>(this.restoreState());
  private readonly availabilitySubject = new BehaviorSubject<AssistantAvailabilityState>({
    mode: 'checking',
    label: 'Checking status',
    detail: 'Checking whether the assistant model is reachable.',
    providerBackend: null,
    providerModel: null,
    checkedAt: null,
  });

  private chatTaskSubscription?: Subscription;

  readonly state$ = this.stateSubject.asObservable();
  readonly availability$ = this.availabilitySubject.asObservable();

  constructor() {
    this.refreshAvailability();
    timer(ASSISTANT_AVAILABILITY_POLL_MS, ASSISTANT_AVAILABILITY_POLL_MS)
      .pipe(switchMap(() => this.http.get<AssistantHealthResponse>(`${this.assistantApiBaseUrl}/health/status`)))
      .subscribe({
        next: (response) => this.availabilitySubject.next(this.toAvailabilityState(response)),
        error: () => this.markAvailabilityOffline(),
      });
  }

  get snapshot(): AssistantChatState {
    return this.stateSubject.value;
  }

  get availabilitySnapshot(): AssistantAvailabilityState {
    return this.availabilitySubject.value;
  }

  sendMessage(rawMessage: string, pagePath?: string): void {
    const message = rawMessage.trim();
    if (!message || this.snapshot.isLoading || this.availabilitySnapshot.mode === 'offline') {
      return;
    }

    const optimisticMessage: AssistantChatMessage = {
      role: 'user',
      text: message,
      createdAt: new Date().toISOString(),
      citations: [],
      tone: 'default',
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
        if ((error as HttpErrorResponse)?.status === 0) {
          this.markAvailabilityOffline();
        }
        this.applyFailureMessage(this.toFriendlyErrorMessage(error, 'send'));
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

  refreshAvailability(): void {
    this.http.get<AssistantHealthResponse>(`${this.assistantApiBaseUrl}/health/status`).subscribe({
      next: (response) => this.availabilitySubject.next(this.toAvailabilityState(response)),
      error: () => this.markAvailabilityOffline(),
    });
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
            this.applyFailureMessage(task.errorMessage || 'The assistant could not finish that reply. Please try again in a moment.');
            return;
          }
          if (pollCount >= ASSISTANT_MAX_TASK_POLLS) {
            this.applyFailureMessage('That reply is taking longer than expected. Please try again in a moment.');
          }
        },
        error: (error) => {
          if ((error as HttpErrorResponse)?.status === 0) {
            this.markAvailabilityOffline();
          }
          this.applyFailureMessage(this.toFriendlyErrorMessage(error, 'poll'));
        }
      });
  }

  private applyChatResponse(response: AssistantChatResponse): void {
    const assistantMessage: AssistantChatMessage = {
      role: 'assistant',
      text: response.message,
      createdAt: new Date().toISOString(),
      citations: response.citations ?? [],
      tone: 'default',
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
      tone: 'error',
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
        messages: Array.isArray(parsed.messages)
          ? parsed.messages.map((message) => ({
              ...message,
              tone: message.tone === 'error' ? 'error' : 'default',
            }))
          : [],
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

  private toAvailabilityState(response: AssistantHealthResponse): AssistantAvailabilityState {
    const labelMap: Record<AssistantHealthResponse['mode'], string> = {
      ready: 'Online',
      fallback: 'Fallback mode',
      preview: 'Preview mode',
    };

    return {
      mode: response.mode,
      label: labelMap[response.mode],
      detail: response.detail,
      providerBackend: response.providerBackend,
      providerModel: response.providerModel,
      checkedAt: response.checkedAt,
    };
  }

  private markAvailabilityOffline(): void {
    this.availabilitySubject.next({
      mode: 'offline',
      label: 'Offline',
      detail: 'The assistant service could not be reached. Try again when the app and Ollama services are back online.',
      providerBackend: null,
      providerModel: null,
      checkedAt: new Date().toISOString(),
    });
  }

  private toFriendlyErrorMessage(error: unknown, context: 'send' | 'poll'): string {
    const httpError = error as HttpErrorResponse | undefined;
    const detail = this.extractErrorDetail(httpError?.error);

    if (httpError?.status === 0) {
      return 'The assistant is offline right now. Please try again once the assistant service and local Ollama model are available.';
    }

    if (httpError?.status === 429) {
      return 'Too many assistant messages were sent in a short period. Please wait a moment before trying again.';
    }

    if ([502, 503, 504].includes(httpError?.status ?? 0)) {
      return 'The assistant is temporarily unavailable. The local model or assistant worker may still be starting up.';
    }

    if (httpError?.status === 404 && context === 'poll') {
      return 'The assistant lost track of that reply while it was processing. Please send your message again.';
    }

    if (detail) {
      return detail;
    }

    return context === 'poll'
      ? 'Checking the assistant reply failed. Please try again in a moment.'
      : 'The assistant could not answer that message right now. Please try again in a moment.';
  }

  private extractErrorDetail(value: unknown): string | null {
    if (typeof value === 'string' && value.trim()) {
      return value.trim();
    }
    if (value && typeof value === 'object' && 'detail' in value) {
      const detail = (value as { detail?: unknown }).detail;
      if (typeof detail === 'string' && detail.trim()) {
        return detail.trim();
      }
    }
    return null;
  }
}
