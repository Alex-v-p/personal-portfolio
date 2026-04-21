export const SUPPORTED_LOCALES = ['en', 'nl'] as const;

export type AppLocale = (typeof SUPPORTED_LOCALES)[number];

export const DEFAULT_LOCALE: AppLocale = 'en';

export function isSupportedLocale(value: string | null | undefined): value is AppLocale {
  return typeof value === 'string' && (SUPPORTED_LOCALES as readonly string[]).includes(value.toLowerCase());
}

export function normalizeLocale(value: string | null | undefined): AppLocale | null {
  if (!value) {
    return null;
  }

  const normalized = value.toLowerCase();
  return isSupportedLocale(normalized) ? normalized : null;
}
