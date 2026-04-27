import { AsyncPipe, NgClass, NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, DestroyRef, HostListener, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { NavigationCancel, NavigationEnd, NavigationError, NavigationStart, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter, take } from 'rxjs/operators';

import { AppLocale, SUPPORTED_LOCALES } from '@core/i18n/locales';
import { I18nService } from '@core/i18n/i18n.service';
import { TranslatePipe } from '@core/i18n/translate.pipe';
import { Profile } from '@domains/profile/model/profile.model';
import { SiteShellData } from '@domains/profile/model/site-shell.model';
import { PublicProfileApiService } from '@domains/profile/data/profile-api.service';
import { AssistantPanelComponent } from '@domains/assistant/ui/assistant-panel.component';
import { AssistantApiService } from '@domains/assistant/data/assistant-api.service';
import { SiteTrackingService } from '@domains/site-activity/data/site-tracking.service';
import { createEmptyProfile } from '@domains/profile/lib/profile-view.util';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { UiIconComponent } from '@shared/icons';
import { SeoService } from '@shared/services/seo.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [AsyncPipe, NgClass, NgFor, NgIf, RouterOutlet, RouterLink, RouterLinkActive, AssistantPanelComponent, UiSkeletonComponent, TranslatePipe, UiIconComponent],
  templateUrl: './app-shell.component.html'
})
export class AppShellComponent implements OnInit {
  private readonly profileApi = inject(PublicProfileApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly router = inject(Router);
  private readonly siteTracking = inject(SiteTrackingService);
  private readonly assistant = inject(AssistantApiService);
  private readonly destroyRef = inject(DestroyRef);
  private readonly seo = inject(SeoService);
  private readonly i18n = inject(I18nService);

  protected readonly locales = SUPPORTED_LOCALES;
  protected profile: Profile = createEmptyProfile();
  protected shellData: SiteShellData | null = null;
  protected isAdminRoute = false;
  protected quickLinks: Array<{ label: string; path: string; isExternal: boolean }> = [];
  protected footerLinks: Array<{ label: string; path: string; isExternal: boolean }> = [];
  protected isAssistantOpen = false;
  protected isRouteLoading = true;
  protected hasActiveRouteComponent = false;
  protected readonly assistantAvailability$ = this.assistant.availability$;

  protected readonly shellChrome = {
    headerVisible: true,
    assistantVisible: true,
    isStickyEnabled: true,
    hasScrolledPastThreshold: false,
    scrollDirection: 'up' as 'up' | 'down'
  };

  private lastScrollY = 0;

  ngOnInit(): void {
    this.isAdminRoute = this.router.url.startsWith('/admin');
    this.isRouteLoading = !this.isAdminRoute;
    if (!this.isAdminRoute) {
      this.siteTracking.trackPageView(this.router.url);
    }

    this.applyRouteSeo(this.router.url);

    this.router.events
      .pipe(
        filter(
          (event): event is NavigationStart | NavigationEnd | NavigationCancel | NavigationError =>
            event instanceof NavigationStart ||
            event instanceof NavigationEnd ||
            event instanceof NavigationCancel ||
            event instanceof NavigationError
        ),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe((event) => {
        if (event instanceof NavigationStart) {
          this.isRouteLoading = !event.url.startsWith('/admin');
          return;
        }

        if (event instanceof NavigationEnd) {
          this.isAdminRoute = event.urlAfterRedirects.startsWith('/admin');
          void this.i18n.syncLocaleFromUrl(event.urlAfterRedirects);
          this.rebuildNavigationLinks();
          this.applyRouteSeo(event.urlAfterRedirects);
          if (!this.isAdminRoute) {
            this.siteTracking.trackPageView(event.urlAfterRedirects);
          }
          this.changeDetectorRef.detectChanges();
          return;
        }

        this.isRouteLoading = false;
        this.changeDetectorRef.detectChanges();
      });

    this.profileApi.getSiteShell().pipe(take(1)).subscribe({
      next: (shell) => {
        this.shellData = shell;
        this.profile = shell.profile;
        this.rebuildNavigationLinks();
        this.changeDetectorRef.detectChanges();
      }
    });
  }

  protected get currentLocale(): AppLocale {
    return this.i18n.currentLocale();
  }

  protected get showRouteSkeleton(): boolean {
    return !this.isAdminRoute && this.isRouteLoading && !this.hasActiveRouteComponent;
  }

  protected onRouteActivate(): void {
    this.hasActiveRouteComponent = true;
    this.isRouteLoading = false;
    this.changeDetectorRef.detectChanges();
  }

  protected onRouteDeactivate(): void {
    this.hasActiveRouteComponent = false;
    this.isRouteLoading = !this.isAdminRoute;
    this.changeDetectorRef.detectChanges();
  }

  protected get mainContentContainerClasses(): string {
    return this.isAdminRoute
      ? 'mx-auto w-full max-w-[100rem] 2xl:max-w-[112rem]'
      : 'mx-auto w-full max-w-6xl';
  }

  protected get resources(): Array<{ label: string; href: string }> {
    const items: Array<{ label: string; href: string }> = [];

    if (this.profile.resumeUrl) {
      items.push({ label: this.i18n.translate('shell.resources.resume'), href: this.profile.resumeUrl });
    }

    for (const link of this.profile.socialLinks ?? []) {
      if (['github', 'linkedin'].includes(link.platform)) {
        items.push({ label: link.label, href: link.url });
      }
    }

    return items;
  }

  protected get socialLinks(): Array<{ label: string; href: string; iconName: string; openInNewTab: boolean }> {
    return (this.profile.socialLinks ?? [])
      .filter((link) => ['email', 'github', 'linkedin'].includes(link.platform))
      .map((link) => {
        const href = link.platform === 'email' ? `mailto:${this.profile.email}` : link.url;

        return {
          label: link.label,
          href,
          iconName: link.iconKey || link.platform,
          openInNewTab: !href.startsWith('mailto:')
        };
      });
  }

  protected get primaryEmail(): string {
    return this.profile.email;
  }

  protected get headerClasses(): string {
    const stickyState = this.shellChrome.isStickyEnabled ? 'sticky top-0' : 'relative';
    const visibleState = this.shellChrome.headerVisible ? 'translate-y-0 opacity-100' : '-translate-y-full opacity-0';

    return `${stickyState} z-30 px-4 pt-4 transition duration-300 sm:px-6 lg:px-8 ${visibleState}`;
  }

  protected toggleAssistant(): void {
    this.isAssistantOpen = !this.isAssistantOpen;
  }

  protected closeAssistant(): void {
    this.isAssistantOpen = false;
  }

  protected async switchLocale(locale: AppLocale): Promise<void> {
    if (locale === this.currentLocale || this.isAdminRoute) {
      return;
    }

    await this.i18n.setLocale(locale);
    const targetUrl = this.i18n.prefixPath(this.router.url, locale);
    await this.router.navigateByUrl(targetUrl);
  }

  protected localeToggleClasses(locale: AppLocale): string {
    const active = locale === this.currentLocale;

    return [
      'inline-flex h-9 w-9 items-center justify-center rounded-full transition-all duration-200',
      active
        ? 'bg-[var(--ui-accent)] text-white shadow-sm'
        : 'bg-transparent text-[var(--ui-text-muted)] hover:bg-white hover:text-[var(--ui-text)]'
    ].join(' ');
  }

  protected localeFlag(locale: AppLocale): string {
    return locale === 'en' ? '🇬🇧' : '🇧🇪';
  }

  protected localeAriaLabel(locale: AppLocale): string {
    return locale === 'en' ? 'Switch to English' : 'Schakel naar Nederlands';
  }

  protected get assistantButtonClasses(): string {
    const visibleState = this.shellChrome.assistantVisible ? 'translate-y-0 opacity-100' : 'pointer-events-none translate-y-4 opacity-0';
    const safePlacement = this.isContactRoute
      ? 'bottom-3 right-3 sm:bottom-4 sm:right-4 lg:right-6'
      : 'bottom-4 right-3 sm:bottom-6 sm:right-6 lg:bottom-8 lg:right-8';

    return `pointer-events-none fixed ${safePlacement} z-40 max-w-[calc(100vw-1rem)] transition duration-300 ${visibleState}`;
  }

  protected get assistantPanelClasses(): string {
    const openState = this.isAssistantOpen
      ? 'pointer-events-auto visible translate-y-0 scale-100 opacity-100'
      : 'invisible pointer-events-none translate-y-3 scale-95 opacity-0';

    return `mb-3 max-h-[min(42rem,calc(100vh-8rem))] w-[min(36rem,calc(100vw-1rem))] origin-bottom-right overflow-hidden transition-all duration-200 ease-out sm:mb-4 sm:w-[32rem] lg:w-[34rem] ${openState}`;
  }

  protected get assistantFabClasses(): string {
    const openState = this.isAssistantOpen
      ? 'scale-[0.985] shadow-[0_16px_36px_rgba(88,72,99,0.18)]'
      : 'hover:-translate-y-0.5 hover:shadow-[0_16px_32px_rgba(88,72,99,0.12)]';

    return `ui-fab pointer-events-auto inline-flex max-w-[calc(100vw-1rem)] items-center gap-3 rounded-[1.75rem] px-3 py-3 ui-btn-secondary transition-all duration-200 sm:px-4 ${openState}`;
  }

  private get isContactRoute(): boolean {
    return this.i18n.stripLocalePrefix(this.router.url).startsWith('/contact');
  }

  @HostListener('window:scroll')
  protected onWindowScroll(): void {
    if (typeof window === 'undefined') {
      return;
    }

    const currentScrollY = window.scrollY;
    this.shellChrome.hasScrolledPastThreshold = currentScrollY > 24;
    this.shellChrome.scrollDirection = currentScrollY > this.lastScrollY ? 'down' : 'up';
    this.shellChrome.headerVisible = true;
    this.shellChrome.assistantVisible = true;
    this.lastScrollY = Math.max(currentScrollY, 0);
  }

  private rebuildNavigationLinks(): void {
    const navigation = this.shellData?.navigation.filter((item) => item.isVisible) ?? [];

    this.quickLinks = navigation.map((item) => ({
      label: item.isExternal ? item.label : this.translateNavigationLabel(item.routePath, item.label),
      path: item.isExternal ? item.routePath : this.i18n.prefixPath(item.routePath),
      isExternal: item.isExternal,
    }));
    this.footerLinks = [...this.quickLinks];
  }

  private translateNavigationLabel(routePath: string, fallback: string): string {
    const lookup: Record<string, string> = {
      '/': 'navigation.home',
      '/projects': 'navigation.projects',
      '/blog': 'navigation.blog',
      '/contact': 'navigation.contact',
      '/stats': 'navigation.stats',
      '/assistant': 'navigation.assistant',
    };

    const translationKey = lookup[routePath];
    return translationKey ? this.i18n.translate(translationKey) : fallback;
  }

  private applyRouteSeo(url: string): void {
    const snapshot = this.router.routerState.snapshot.root;
    let current = snapshot;

    while (current.firstChild) {
      current = current.firstChild;
    }

    const seoData = current.data?.['seo'] as {
      title?: string;
      titleKey?: string;
      description?: string;
      descriptionKey?: string;
      keywords?: string[];
      keywordsKey?: string;
      type?: 'website' | 'article' | 'profile';
      noIndex?: boolean;
    } | undefined;

    if (!seoData) {
      return;
    }

    this.seo.updatePage({
      ...seoData,
      path: url,
    });
  }
}
