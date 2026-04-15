import { AsyncPipe, NgClass, NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, DestroyRef, HostListener, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { NavigationCancel, NavigationEnd, NavigationError, NavigationStart, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter, take } from 'rxjs/operators';

import { Profile } from '@domains/profile/model/profile.model';
import { SiteShellData } from '@domains/profile/model/site-shell.model';
import { PublicProfileApiService } from '@domains/profile/data/profile-api.service';
import { AssistantPanelComponent } from '@domains/assistant/ui/assistant-panel.component';
import { AssistantApiService } from '@domains/assistant/data/assistant-api.service';
import { SiteTrackingService } from '@domains/site-activity/data/site-tracking.service';
import { createEmptyProfile } from '@domains/profile/lib/profile-view.util';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [AsyncPipe, NgClass, NgFor, NgIf, RouterOutlet, RouterLink, RouterLinkActive, AssistantPanelComponent, UiSkeletonComponent],
  templateUrl: './app-shell.component.html'
})
export class AppShellComponent implements OnInit {
  private readonly profileApi = inject(PublicProfileApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly router = inject(Router);
  private readonly siteTracking = inject(SiteTrackingService);
  private readonly assistant = inject(AssistantApiService);
  private readonly destroyRef = inject(DestroyRef);

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
        this.quickLinks = shell.navigation.filter((item) => item.isVisible).map((item) => ({
          label: item.label,
          path: item.routePath,
          isExternal: item.isExternal,
        }));
        this.footerLinks = [...this.quickLinks];
        this.changeDetectorRef.detectChanges();
      }
    });
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
      items.push({ label: 'Resume', href: this.profile.resumeUrl });
    }

    for (const link of this.profile.socialLinks ?? []) {
      if (['github', 'linkedin'].includes(link.platform)) {
        items.push({ label: link.label, href: link.url });
      }
    }

    return items;
  }

  protected get socialLinks(): Array<{ label: string; href: string; mark: string }> {
    return (this.profile.socialLinks ?? [])
      .filter((link) => ['email', 'github', 'linkedin'].includes(link.platform))
      .map((link) => ({
        label: link.label,
        href: link.platform === 'email' ? `mailto:${this.profile.email}` : link.url,
        mark: link.platform === 'email' ? 'EM' : link.platform === 'github' ? 'GH' : 'LI'
      }));
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

  protected get assistantButtonClasses(): string {
    const visibleState = this.shellChrome.assistantVisible ? 'translate-y-0 opacity-100' : 'pointer-events-none translate-y-4 opacity-0';

    return `fixed bottom-6 right-4 z-40 transition duration-300 sm:bottom-8 sm:right-6 lg:right-8 ${visibleState}`;
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
}
