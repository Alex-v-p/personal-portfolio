import { I18nService } from '@core/i18n/i18n.service';

const NON_ROUTE_PREFIX_PATTERN = /^\/(api|assets|media|uploads|files|icons|i18n)\b/i;
const LOCALE_PREFIX_PATTERN = /^\/(en|nl)(?=\/|$)/i;

export const isInternalPublicRouteUrl = (url: string): boolean => {
  const trimmedUrl = url.trim();

  if (!trimmedUrl.startsWith('/') || trimmedUrl.startsWith('//')) {
    return false;
  }

  const [pathname] = trimmedUrl.split(/[?#]/, 1);
  const normalizedPathname = pathname || '/';

  if (NON_ROUTE_PREFIX_PATTERN.test(normalizedPathname) || normalizedPathname.startsWith('/admin')) {
    return false;
  }

  const pathWithoutLocale = normalizedPathname.replace(LOCALE_PREFIX_PATTERN, '') || '/';

  return (
    pathWithoutLocale === '/' ||
    pathWithoutLocale === '/projects' ||
    pathWithoutLocale.startsWith('/projects/') ||
    pathWithoutLocale === '/blog' ||
    pathWithoutLocale.startsWith('/blog/') ||
    pathWithoutLocale === '/contact' ||
    pathWithoutLocale === '/stats' ||
    pathWithoutLocale === '/assistant' ||
    pathWithoutLocale === '/experience'
  );
};

export const localizeInternalAppLinkUrl = (url: string, i18n: I18nService): string => {
  const trimmedUrl = url.trim();

  if (!isInternalPublicRouteUrl(trimmedUrl)) {
    return trimmedUrl;
  }

  const [pathname, suffix = ''] = trimmedUrl.match(/^([^?#]*)(.*)$/)?.slice(1) ?? [trimmedUrl, ''];
  const pathWithoutLocale = (pathname || '/').replace(LOCALE_PREFIX_PATTERN, '') || '/';

  if (pathWithoutLocale === '/experience') {
    return i18n.prefixPath(`/${suffix || '#experience'}`);
  }

  return i18n.prefixPath(trimmedUrl);
};
