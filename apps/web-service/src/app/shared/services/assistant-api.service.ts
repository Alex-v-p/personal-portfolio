import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';

import { AssistantChatMessage, AssistantChatResponse, AssistantChatState } from '../models/assistant-chat.model';

const ASSISTANT_STATE_STORAGE_KEY = 'portfolio.assistant.state';
const ASSISTANT_SESSION_STORAGE_KEY = 'portfolio.assistant.session-id';

const resolveAssistantApiBaseUrl = (): string => {
  if (typeof window === 'undefined') {
    return 'http://localhost:8012/api';
  }

  const { hostname, protocol } = window.location;
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return `${protocol}//${hostname}:8012/api`;
  }

  return '/ai';
};

@Injectable({ providedIn: 'root' })
export class AssistantApiService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly assistantApiBaseUrl = resolveAssistantApiBaseUrl();
  private readonly stateSubject = new BehaviorSubject<AssistantChatState>(this.restoreState());

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

    this.http.post<AssistantChatResponse>(`${this.assistantApiBaseUrl}/chat/respond`, {
      message,
      conversation_id: this.snapshot.conversationId,
      session_id: this.getOrCreateSessionId(),
      page_path: pagePath ?? this.router.url,
    }).subscribe({
      next: (response) => {
        const normalizedResponse = response as AssistantChatResponse & { conversation_id?: string; provider_backend?: string };
        const assistantMessage: AssistantChatMessage = {
          role: 'assistant',
          text: response.message,
          createdAt: new Date().toISOString(),
          citations: response.citations ?? [],
        };
        this.patchState({
          conversationId: normalizedResponse.conversationId ?? normalizedResponse.conversation_id ?? null,
          messages: [...this.snapshot.messages, assistantMessage],
          isLoading: false,
          errorMessage: null,
        });
      },
      error: (error) => {
        const fallbackMessage: AssistantChatMessage = {
          role: 'assistant',
          text: error?.error?.detail || 'The assistant request failed. Check that the assistant service is running and try again.',
          createdAt: new Date().toISOString(),
          citations: [],
        };
        this.patchState({
          messages: [...this.snapshot.messages, fallbackMessage],
          isLoading: false,
          errorMessage: fallbackMessage.text,
        });
      }
    });
  }

  resetConversation(): void {
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

  private getOrCreateSessionId(): string {
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
}
