import { DOCUMENT, isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Inject, Injectable, PLATFORM_ID, inject, signal } from '@angular/core';
import { toObservable } from '@angular/core/rxjs-interop';
import { firstValueFrom, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { AppLocale, DEFAULT_LOCALE, normalizeLocale } from './locales';

type TranslationNode = string | number | string[] | TranslationDictionary;
interface TranslationDictionary {
  [key: string]: TranslationNode;
}

@Injectable({ providedIn: 'root' })
export class I18nService {
  private readonly http = inject(HttpClient);

  private readonly currentLocaleSignal = signal<AppLocale>(DEFAULT_LOCALE);
  private readonly catalogs = new Map<AppLocale, TranslationDictionary>();
  private readonly storageKey = 'portfolio.locale';

  readonly locale = this.currentLocaleSignal.asReadonly();
  readonly localeChanges$ = toObservable(this.locale);

  constructor(
    @Inject(DOCUMENT) private readonly document: Document,
    @Inject(PLATFORM_ID) private readonly platformId: object
  ) {}

  async initialize(): Promise<void> {
    const locale = this.getLocaleFromUrl(this.document.location.pathname) ?? this.readStoredLocale() ?? DEFAULT_LOCALE;
    await this.loadLocale(locale);
  }

  currentLocale(): AppLocale {
    return this.currentLocaleSignal();
  }

  async setLocale(locale: AppLocale): Promise<void> {
    await this.loadLocale(locale);
  }

  async syncLocaleFromUrl(url: string): Promise<void> {
    const locale = this.getLocaleFromUrl(url) ?? DEFAULT_LOCALE;
    await this.loadLocale(locale);
  }

  translate(key: string, params?: Record<string, string | number | null | undefined>): string {
    const value = this.lookup(this.currentLocale(), key) ?? this.lookup(DEFAULT_LOCALE, key);

    if (typeof value !== 'string') {
      return key;
    }

    return this.interpolate(value, params);
  }

  translateList(key: string): string[] {
    const value = this.lookup(this.currentLocale(), key) ?? this.lookup(DEFAULT_LOCALE, key);
    return Array.isArray(value) ? value.filter((item): item is string => typeof item === 'string') : [];
  }

  getLocaleFromUrl(url: string): AppLocale | null {
    const pathname = this.extractPathname(url);
    const [firstSegment] = pathname.replace(/^\//, '').split('/');
    return normalizeLocale(firstSegment);
  }

  stripLocalePrefix(path: string): string {
    if (!path) {
      return '/';
    }

    const [pathname, suffix] = this.splitPath(path);
    const locale = this.getLocaleFromUrl(pathname);

    if (!locale) {
      return `${pathname || '/'}${suffix}`;
    }

    const strippedPath = pathname.replace(new RegExp(`^/${locale}(?=/|$)`), '') || '/';
    return `${strippedPath.startsWith('/') ? strippedPath : `/${strippedPath}`}${suffix}`;
  }

  prefixPath(path: string, locale = this.currentLocale()): string {
    if (!path) {
      return `/${locale}`;
    }

    if (this.isExternalPath(path) || path.startsWith('/admin')) {
      return path;
    }

    const stripped = this.stripLocalePrefix(path);
    const [pathname, suffix] = this.splitPath(stripped);

    if (pathname === '/' || pathname === '') {
      return `/${locale}${suffix}`;
    }

    return `/${locale}${pathname.startsWith('/') ? pathname : `/${pathname}`}${suffix}`;
  }

  localizeRouterCommands(commands: string | readonly string[] | null | undefined): string | readonly string[] | null {
    if (!commands) {
      return null;
    }

    if (typeof commands === 'string') {
      return this.prefixPath(commands);
    }

    const localizedCommands = [...commands];
    const [firstCommand] = localizedCommands;

    if (typeof firstCommand === 'string') {
      localizedCommands[0] = this.prefixPath(firstCommand);
    }

    return localizedCommands;
  }

  private async loadLocale(locale: AppLocale): Promise<void> {
    const targetLocale = normalizeLocale(locale) ?? DEFAULT_LOCALE;

    if (!this.catalogs.has(targetLocale)) {
      const catalog = await this.fetchCatalog(targetLocale);
      this.catalogs.set(targetLocale, catalog);
    }

    this.currentLocaleSignal.set(targetLocale);
    this.document.documentElement.lang = targetLocale;
    this.writeStoredLocale(targetLocale);
  }

  private async fetchCatalog(locale: AppLocale): Promise<TranslationDictionary> {
    const catalog = await firstValueFrom(
      this.http.get<TranslationDictionary>(`/i18n/${locale}.json`).pipe(catchError(() => of({})))
    );

    if (locale === DEFAULT_LOCALE) {
      return catalog;
    }

    if (!this.catalogs.has(DEFAULT_LOCALE)) {
      const defaultCatalog = await this.fetchCatalog(DEFAULT_LOCALE);
      this.catalogs.set(DEFAULT_LOCALE, defaultCatalog);
    }

    return catalog;
  }

  private lookup(locale: AppLocale, key: string): TranslationNode | null {
    const catalog = this.catalogs.get(locale);
    if (!catalog) {
      return null;
    }

    return key.split('.').reduce<TranslationNode | null>((current, segment) => {
      if (!current || typeof current === 'string' || typeof current === 'number' || Array.isArray(current)) {
        return null;
      }

      return current[segment] ?? null;
    }, catalog);
  }

  private interpolate(template: string, params?: Record<string, string | number | null | undefined>): string {
    if (!params) {
      return template;
    }

    return template.replace(/{{\s*(\w+)\s*}}/g, (_, key: string) => {
      const value = params[key];
      return value === null || value === undefined ? '' : String(value);
    });
  }

  private readStoredLocale(): AppLocale | null {
    if (!isPlatformBrowser(this.platformId)) {
      return null;
    }

    return normalizeLocale(window.localStorage.getItem(this.storageKey));
  }

  private writeStoredLocale(locale: AppLocale): void {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }

    window.localStorage.setItem(this.storageKey, locale);
  }

  private isExternalPath(path: string): boolean {
    return /^[a-z][a-z0-9+.-]*:/i.test(path) || path.startsWith('//') || path.startsWith('#');
  }

  private extractPathname(url: string): string {
    const [withoutHash] = url.split('#', 1);
    const [pathname] = withoutHash.split('?', 1);
    return pathname || '/';
  }

  private splitPath(path: string): [string, string] {
    const match = path.match(/^([^?#]*)(.*)$/);
    if (!match) {
      return [path, ''];
    }

    return [match[1] || '/', match[2] || ''];
  }
}
