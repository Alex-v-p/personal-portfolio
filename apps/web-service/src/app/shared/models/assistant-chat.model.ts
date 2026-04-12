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
  conversationId: string;
  message: string;
  providerBackend: string;
  citations: AssistantCitation[];
}

export interface AssistantChatState {
  conversationId: string | null;
  messages: AssistantChatMessage[];
  isLoading: boolean;
  errorMessage: string | null;
}
