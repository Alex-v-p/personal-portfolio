import { UrlMatchResult, UrlSegment } from '@angular/router';

import { isSupportedLocale } from '@core/i18n/locales';

export function localeMatcher(segments: UrlSegment[]): UrlMatchResult | null {
  const [firstSegment] = segments;

  if (!firstSegment || !isSupportedLocale(firstSegment.path)) {
    return null;
  }

  return {
    consumed: [firstSegment],
    posParams: {
      locale: firstSegment,
    },
  };
}
