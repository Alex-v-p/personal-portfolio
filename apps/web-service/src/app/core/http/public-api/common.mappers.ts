import { ResolvedMedia } from '@domains/media/model/resolved-media.model';

import { MediaApi } from './common.contracts';

export function normalizeMedia(media: MediaApi | null | undefined): ResolvedMedia | null {
  if (!media?.url) {
    return null;
  }

  return {
    id: media.id,
    url: media.url,
    alt: media.alt ?? null,
    fileName: media.fileName ?? null,
    mimeType: media.mimeType ?? null,
    width: media.width ?? null,
    height: media.height ?? null,
  };
}

export function formatDate(value: string | null | undefined): string {
  if (!value) {
    return '';
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return parsed.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

export function formatPeriod(startDate: string, endDate?: string | null, isCurrent?: boolean): string {
  const start = formatMonthYear(startDate);
  const end = isCurrent ? 'Present' : endDate ? formatMonthYear(endDate) : 'Present';
  return `${start} - ${end}`;
}

export function formatMonthYear(value: string): string {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return parsed.toLocaleDateString('en-GB', {
    month: 'short',
    year: 'numeric',
  });
}
