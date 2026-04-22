import { DOCUMENT, isPlatformBrowser } from '@angular/common';
import { Inject, Injectable, PLATFORM_ID, inject } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';

import { I18nService } from '@core/i18n/i18n.service';
import { DEFAULT_LOCALE, SUPPORTED_LOCALES } from '@core/i18n/locales';

export interface PageSeoMetadata {
  title?: string;
  titleKey?: string;
  description?: string;
  descriptionKey?: string;
  keywords?: string[];
  keywordsKey?: string;
  image?: string;
  type?: 'website' | 'article' | 'profile';
  noIndex?: boolean;
  path?: string;
}

@Injectable({ providedIn: 'root' })
export class SeoService {
  private readonly i18n = inject(I18nService);

  constructor(
    private readonly title: Title,
    private readonly meta: Meta,
    @Inject(DOCUMENT) private readonly document: Document,
    @Inject(PLATFORM_ID) private readonly platformId: object
  ) {}

  updatePage(metadata: PageSeoMetadata): void {
    const siteName = this.i18n.translate('seo.defaults.siteName');
    const pageTitle = metadata.title?.trim() || (metadata.titleKey ? this.i18n.translate(metadata.titleKey) : '');
    const fullTitle = pageTitle ? `${pageTitle} • ${siteName}` : siteName;
    const description =
      metadata.description?.trim() ||
      (metadata.descriptionKey ? this.i18n.translate(metadata.descriptionKey) : '') ||
      this.i18n.translate('seo.defaults.description');
    const keywords = metadata.keywords?.length ? metadata.keywords : this.i18n.translateList(metadata.keywordsKey ?? 'seo.defaults.keywords');
    const type = metadata.type ?? 'website';
    const absoluteUrl = this.resolveUrl(metadata.path ?? this.document.location.pathname);
    const imageUrl = metadata.image ? this.resolveUrl(metadata.image) : undefined;
    const robots = metadata.noIndex ? 'noindex,nofollow' : 'index,follow';
    const currentLocale = this.i18n.currentLocale();

    this.document.documentElement.lang = currentLocale;

    this.title.setTitle(fullTitle);
    this.meta.updateTag({ name: 'description', content: description });
    this.meta.updateTag({ name: 'keywords', content: keywords.join(', ') });
    this.meta.updateTag({ name: 'robots', content: robots });

    this.meta.updateTag({ property: 'og:site_name', content: siteName });
    this.meta.updateTag({ property: 'og:title', content: fullTitle });
    this.meta.updateTag({ property: 'og:description', content: description });
    this.meta.updateTag({ property: 'og:type', content: type });
    this.meta.updateTag({ property: 'og:locale', content: currentLocale === 'nl' ? 'nl_BE' : 'en_GB' });
    this.updateOgLocaleAlternateTags(currentLocale);

    if (absoluteUrl) {
      this.meta.updateTag({ property: 'og:url', content: absoluteUrl });
      this.updateCanonicalLink(absoluteUrl);
      this.updateAlternateLinks(metadata.path ?? this.document.location.pathname);
    }

    this.meta.updateTag({ name: 'twitter:card', content: imageUrl ? 'summary_large_image' : 'summary' });
    this.meta.updateTag({ name: 'twitter:title', content: fullTitle });
    this.meta.updateTag({ name: 'twitter:description', content: description });

    if (imageUrl) {
      this.meta.updateTag({ property: 'og:image', content: imageUrl });
      this.meta.updateTag({ name: 'twitter:image', content: imageUrl });
    } else {
      this.meta.removeTag("property='og:image'");
      this.meta.removeTag("name='twitter:image'");
    }
  }

  private resolveUrl(path?: string): string | null {
    if (!path || !isPlatformBrowser(this.platformId)) {
      return null;
    }

    try {
      const localizedPath = this.shouldLocalizePath(path) ? this.i18n.prefixPath(path) : path;
      return new URL(localizedPath, this.document.baseURI).toString();
    } catch {
      return null;
    }
  }

  private shouldLocalizePath(path: string): boolean {
    return path.startsWith('/') && !path.startsWith('/admin');
  }

  private updateCanonicalLink(url: string): void {
    const head = this.document.head;
    let link = head.querySelector("link[rel='canonical']") as HTMLLinkElement | null;

    if (!link) {
      link = this.document.createElement('link');
      link.setAttribute('rel', 'canonical');
      head.appendChild(link);
    }

    link.setAttribute('href', url);
  }

  private updateAlternateLinks(path: string): void {
    if (!this.shouldLocalizePath(path)) {
      this.removeAlternateLinks();
      return;
    }

    const strippedPath = this.i18n.stripLocalePrefix(path);

    for (const locale of SUPPORTED_LOCALES) {
      const href = this.resolveUrl(this.i18n.prefixPath(strippedPath, locale));
      if (!href) {
        continue;
      }

      const selector = `link[rel='alternate'][hreflang='${locale}']`;
      let link = this.document.head.querySelector(selector) as HTMLLinkElement | null;

      if (!link) {
        link = this.document.createElement('link');
        link.setAttribute('rel', 'alternate');
        link.setAttribute('hreflang', locale);
        this.document.head.appendChild(link);
      }

      link.setAttribute('href', href);
    }

    const defaultHref = this.resolveUrl(this.i18n.prefixPath(strippedPath, DEFAULT_LOCALE));
    if (!defaultHref) {
      return;
    }

    let defaultLink = this.document.head.querySelector("link[rel='alternate'][hreflang='x-default']") as HTMLLinkElement | null;

    if (!defaultLink) {
      defaultLink = this.document.createElement('link');
      defaultLink.setAttribute('rel', 'alternate');
      defaultLink.setAttribute('hreflang', 'x-default');
      this.document.head.appendChild(defaultLink);
    }

    defaultLink.setAttribute('href', defaultHref);
  }

  private updateOgLocaleAlternateTags(currentLocale: 'en' | 'nl'): void {
    const alternateLocales = SUPPORTED_LOCALES
      .filter((locale) => locale !== currentLocale)
      .map((locale) => (locale === 'nl' ? 'nl_BE' : 'en_GB'));
    const existing = this.document.head.querySelectorAll("meta[property='og:locale:alternate']");
    existing.forEach((tag) => tag.remove());

    alternateLocales.forEach((localeValue) => {
      const tag = this.document.createElement('meta');
      tag.setAttribute('property', 'og:locale:alternate');
      tag.setAttribute('content', localeValue);
      this.document.head.appendChild(tag);
    });
  }

  private removeAlternateLinks(): void {
    const alternateLinks = this.document.head.querySelectorAll("link[rel='alternate']");
    alternateLinks.forEach((link) => link.remove());
  }
}
