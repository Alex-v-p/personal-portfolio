import { AdminTranslationDraftResponse } from '@domains/admin/model/assistant-admin.model';

export type ContentLocale = 'en' | 'nl';

export abstract class AdminLocalizedContentTabBase {
  public contentLocale: ContentLocale = 'en';
  public isGeneratingDutchDraft = false;
  public translationMessage = '';

  public setContentLocale(locale: ContentLocale): void {
    this.contentLocale = locale;
  }

  protected resetLocalizedEditingState(): void {
    this.translationMessage = '';
    this.contentLocale = 'en';
    this.isGeneratingDutchDraft = false;
  }

  protected beginDutchDraftGeneration(): void {
    this.isGeneratingDutchDraft = true;
    this.translationMessage = '';
  }

  protected finishDutchDraftGeneration(
    response: AdminTranslationDraftResponse,
    successMessage: string,
    focusLocale: ContentLocale = 'nl',
  ): void {
    this.contentLocale = focusLocale;
    this.translationMessage = response.warnings.length > 0
      ? `${successMessage} Review ${response.warnings.length} field${response.warnings.length === 1 ? '' : 's'} for possible leftover English.`
      : successMessage;
    this.isGeneratingDutchDraft = false;
  }

  protected failDutchDraftGeneration(error: unknown, fallbackMessage: string): void {
    this.translationMessage = this.extractTranslationErrorMessage(error, fallbackMessage);
    this.isGeneratingDutchDraft = false;
  }

  protected applyTranslatedFields<T extends object>(
    form: T,
    translatedFields: Record<string, string>,
    keyMap: Partial<Record<keyof T, string>>,
  ): void {
    for (const [formKey, responseKey] of Object.entries(keyMap) as Array<[keyof T, string]>) {
      const translatedValue = translatedFields[responseKey];
      if (typeof translatedValue === 'string' && translatedValue.trim()) {
        form[formKey] = translatedValue as T[keyof T];
      }
    }
  }

  private extractTranslationErrorMessage(error: unknown, fallbackMessage: string): string {
    if (!error || typeof error !== 'object') {
      return fallbackMessage;
    }
    const errorRecord = error as { error?: { detail?: unknown }; message?: unknown };
    const detail = errorRecord.error?.detail;
    if (typeof detail === 'string' && detail.trim()) {
      return detail;
    }
    if (typeof errorRecord.message === 'string' && errorRecord.message.trim()) {
      return errorRecord.message;
    }
    return fallbackMessage;
  }
}
