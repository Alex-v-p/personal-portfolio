export interface AdminTranslationDraftRequest {
  sourceLocale: 'en' | 'nl';
  targetLocale: 'en' | 'nl';
  entityType: string;
  fields: Record<string, string>;
  context?: string | null;
}

export interface AdminTranslationDraftResponse {
  sourceLocale: 'en' | 'nl';
  targetLocale: 'en' | 'nl';
  entityType: string;
  translatedFields: Record<string, string>;
  providerBackend: string;
  providerModel?: string | null;
  warnings: string[];
}

export interface AdminAssistantContextNote {
  id: string;
  title: string;
  titleNl?: string | null;
  contentMarkdown: string;
  contentMarkdownNl?: string | null;
  category: string;
  isActive: boolean;
  sortOrder: number;
  createdAt: string;
  updatedAt: string;
}

export interface AdminAssistantContextNotesList {
  items: AdminAssistantContextNote[];
  total: number;
}

export interface AdminAssistantContextNotePayload {
  title: string;
  titleNl?: string | null;
  contentMarkdown: string;
  contentMarkdownNl?: string | null;
  category: string;
  isActive: boolean;
  sortOrder: number;
}
