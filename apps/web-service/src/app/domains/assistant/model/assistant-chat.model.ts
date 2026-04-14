export interface AssistantCitation {
  title: string;
  sourceType: string;
  canonicalUrl?: string | null;
  excerpt: string;
}

export interface AssistantChatMessage {
  role: 'user' | 'assistant';
  text: string;
  createdAt?: string | null;
  citations: AssistantCitation[];
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
