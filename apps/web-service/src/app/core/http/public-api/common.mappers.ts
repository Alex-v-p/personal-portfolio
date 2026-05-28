import { AppLocale } from '@core/i18n/locales';
import { ResolvedMedia } from '@domains/media/model/resolved-media.model';

import { MediaApi } from './common.contracts';

export function normalizeMedia(media: MediaApi | null | undefined): ResolvedMedia | null {
  if (!media?.url) {
    return null;
  }

  return {
    id: media.id,
    url: media.url,
    downloadUrl: media.downloadUrl ?? null,
    alt: media.alt ?? null,
    fileName: media.fileName ?? null,
    mimeType: media.mimeType ?? null,
    width: media.width ?? null,
    height: media.height ?? null,
  };
}

export function formatDate(value: string | null | undefined, locale: AppLocale = 'en'): string {
  if (!value) {
    return '';
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return parsed.toLocaleDateString(resolveDateLocale(locale), {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

export function formatPeriod(startDate: string, endDate: string | null | undefined, locale: AppLocale, isCurrent?: boolean): string {
  const start = formatMonthYear(startDate, locale);
  const end = isCurrent ? presentLabel(locale) : endDate ? formatMonthYear(endDate, locale) : presentLabel(locale);
  return `${start} - ${end}`;
}

export function formatMonthYear(value: string, locale: AppLocale = 'en'): string {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return parsed.toLocaleDateString(resolveDateLocale(locale), {
    month: 'short',
    year: 'numeric',
  });
}

export function readingTimeLabel(readingTimeMinutes: number, locale: AppLocale): string {
  if (readingTimeMinutes <= 0) {
    return locale === 'nl' ? 'Concept' : 'Draft';
  }

  return locale === 'nl' ? `${readingTimeMinutes} min leestijd` : `${readingTimeMinutes} min read`;
}

export function presentLabel(locale: AppLocale): string {
  return locale === 'nl' ? 'Nu' : 'Present';
}

function resolveDateLocale(locale: AppLocale): string {
  return locale === 'nl' ? 'nl-BE' : 'en-GB';
}
