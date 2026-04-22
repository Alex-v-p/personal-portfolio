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
import { I18nService } from '@core/i18n/i18n.service';

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
  private readonly i18n = inject(I18nService);
  private readonly stateSubject = new BehaviorSubject<AssistantChatState>(this.restoreState());
  private readonly availabilitySubject = new BehaviorSubject<AssistantAvailabilityState>({
    mode: 'checking',
    label: this.translateOrFallback('assistantPopup.availability.checking.label', 'Checking availability'),
    detail: this.translateOrFallback('assistantPopup.availability.checking.detail', 'Looking up the assistant status and retrieving the latest portfolio context.'),
    providerBackend: null,
    providerModel: null,
    checkedAt: null,
  });

  private chatTaskSubscription?: Subscription;

  readonly state$ = this.stateSubject.asObservable();
  readonly availability$ = this.availabilitySubject.asObservable();

  constructor() {
    this.i18n.localeChanges$.subscribe(() => this.relocalizeAvailability());
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
      locale: this.i18n.currentLocale(),
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
            this.applyFailureMessage(task.errorMessage || this.translateOrFallback('assistantPopup.errors.finishFailed', 'The assistant reply ended unexpectedly.'));
            return;
          }
          if (pollCount >= ASSISTANT_MAX_TASK_POLLS) {
            this.applyFailureMessage(this.translateOrFallback('assistantPopup.errors.timeout', 'The assistant took too long to respond.'));
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
    return {
      mode: response.mode,
      label: this.localizedAvailabilityLabel(response.mode),
      detail: this.localizedAvailabilityDetail(response.mode),
      providerBackend: response.providerBackend,
      providerModel: response.providerModel,
      checkedAt: response.checkedAt,
    };
  }

  private relocalizeAvailability(): void {
    const current = this.availabilitySnapshot;
    this.availabilitySubject.next({
      ...current,
      label: this.localizedAvailabilityLabel(current.mode),
      detail: this.localizedAvailabilityDetail(current.mode),
    });
  }

  private localizedAvailabilityLabel(mode: AssistantAvailabilityState['mode']): string {
    switch (mode) {
      case 'checking':
        return this.translateOrFallback('assistantPopup.availability.checking.label', 'Checking availability');
      case 'ready':
        return this.translateOrFallback('assistantPopup.availability.ready.label', 'Ready');
      case 'fallback':
        return this.translateOrFallback('assistantPopup.availability.fallback.label', 'Fallback mode');
      case 'preview':
        return this.translateOrFallback('assistantPopup.availability.preview.label', 'Preview mode');
      default:
        return this.translateOrFallback('assistantPopup.availability.offline.label', 'Offline');
    }
  }

  private localizedAvailabilityDetail(mode: AssistantAvailabilityState['mode']): string {
    switch (mode) {
      case 'checking':
        return this.translateOrFallback('assistantPopup.availability.checking.detail', 'Looking up the assistant status and retrieving the latest portfolio context.');
      case 'ready':
        return this.translateOrFallback('assistantPopup.availability.ready.detail', 'The assistant can answer with live portfolio context.');
      case 'fallback':
        return this.translateOrFallback('assistantPopup.availability.fallback.detail', 'Live retrieval is limited right now, but the assistant can still answer from the available portfolio snapshot.');
      case 'preview':
        return this.translateOrFallback('assistantPopup.availability.preview.detail', 'The assistant is running in preview mode with limited retrieval coverage.');
      default:
        return this.translateOrFallback('assistantPopup.availability.offline.detail', 'The assistant service is unavailable right now.');
    }
  }

  private markAvailabilityOffline(): void {
    this.availabilitySubject.next({
      mode: 'offline',
      label: this.translateOrFallback('assistantPopup.availability.offline.label', 'Offline'),
      detail: this.translateOrFallback('assistantPopup.availability.offline.detail', 'The assistant service is unavailable right now.'),
      providerBackend: null,
      providerModel: null,
      checkedAt: new Date().toISOString(),
    });
  }

  private toFriendlyErrorMessage(error: unknown, context: 'send' | 'poll'): string {
    const httpError = error as HttpErrorResponse | undefined;
    const detail = this.extractErrorDetail(httpError?.error);

    if (httpError?.status === 0) {
      return this.translateOrFallback('assistantPopup.errors.offline', 'The assistant is currently offline.');
    }

    if (httpError?.status === 429) {
      return detail ?? this.translateOrFallback('assistantPopup.errors.rateLimited', 'Too many assistant messages were sent in a short period. Please wait a moment before trying again.');
    }

    if ([502, 503, 504].includes(httpError?.status ?? 0)) {
      return detail ?? this.translateOrFallback('assistantPopup.errors.temporarilyUnavailable', 'The assistant is temporarily unavailable.');
    }

    if (httpError?.status === 404 && context === 'poll') {
      return detail ?? this.translateOrFallback('assistantPopup.errors.lostReply', 'The reply could not be completed.');
    }

    if (detail) {
      return detail;
    }

    return context === 'poll'
      ? this.translateOrFallback('assistantPopup.errors.pollFailed', 'The assistant reply could not be refreshed.')
      : this.translateOrFallback('assistantPopup.errors.sendFailed', 'The message could not be sent.');
  }

  private translateOrFallback(key: string, fallback: string): string {
    const translated = this.i18n.translate(key);
    return translated === key ? fallback : translated;
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
