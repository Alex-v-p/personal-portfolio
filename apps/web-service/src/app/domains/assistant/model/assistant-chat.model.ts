export interface AssistantCitation {
  title: string;
  sourceType: string;
  canonicalUrl?: string | null;
  excerpt: string;
}

export type AssistantMessageTone = 'default' | 'error';

export interface AssistantChatMessage {
  role: 'user' | 'assistant';
  text: string;
  createdAt?: string | null;
  citations: AssistantCitation[];
  tone?: AssistantMessageTone;
}

export interface AssistantChatResponse {
  conversationId: string | null;
  message: string;
  providerBackend: string;
  citations: AssistantCitation[];
}

export type AssistantChatTaskState = 'queued' | 'running' | 'succeeded' | 'failed';

export interface AssistantChatTaskAccepted {
  taskId: string;
  conversationId: string | null;
  status: AssistantChatTaskState;
  pollAfterMs: number;
}

export interface AssistantChatTaskStatus {
  taskId: string;
  conversationId: string | null;
  status: AssistantChatTaskState;
  submittedAt: string;
  startedAt?: string | null;
  completedAt?: string | null;
  errorMessage?: string | null;
  message?: string | null;
  providerBackend?: string | null;
  citations: AssistantCitation[];
}

export interface AssistantChatState {
  conversationId: string | null;
  messages: AssistantChatMessage[];
  isLoading: boolean;
  errorMessage: string | null;
}

export type AssistantAvailabilityMode = 'checking' | 'ready' | 'fallback' | 'preview' | 'offline';

export interface AssistantHealthResponse {
  status: string;
  mode: Exclude<AssistantAvailabilityMode, 'checking' | 'offline'>;
  providerBackend: string;
  providerModel: string;
  providerAvailable: boolean;
  configured: boolean;
  detail: string;
  checkedAt: string;
}

export interface AssistantAvailabilityState {
  mode: AssistantAvailabilityMode;
  label: string;
  detail: string;
  providerBackend: string | null;
  providerModel: string | null;
  checkedAt: string | null;
}
