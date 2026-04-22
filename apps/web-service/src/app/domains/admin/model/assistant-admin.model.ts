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
