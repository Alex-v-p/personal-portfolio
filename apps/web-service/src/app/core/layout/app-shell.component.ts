import { NgFor } from '@angular/common';
import { Component, HostListener, OnInit, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { take } from 'rxjs/operators';

import { NAVIGATION_ITEMS } from '../../shared/mock-data/navigation-items.mock';
import { PROFILE } from '../../shared/mock-data/profile.mock';
import { SOCIAL_LINKS } from '../../shared/mock-data/social-links.mock';
import { PublicPortfolioApiService } from '../../shared/services/public-portfolio-api.service';
import { mergeProfileWithFallback } from '../../shared/utils/profile-view.util';
import { Profile } from '../../shared/models/profile.model';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [NgFor, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app-shell.component.html'
})
export class AppShellComponent implements OnInit {
  private readonly portfolioApi = inject(PublicPortfolioApiService);

  protected profile: Profile = PROFILE;

  protected readonly quickLinks = NAVIGATION_ITEMS.filter((item) => item.isVisible).map((item) => ({
    label: item.label,
    path: item.routePath
  }));

  protected readonly footerLinks = [...this.quickLinks];

  protected readonly shellChrome = {
    headerVisible: true,
    assistantVisible: true,
    isStickyEnabled: true,
    hasScrolledPastThreshold: false,
    scrollDirection: 'up' as 'up' | 'down'
  };

  private lastScrollY = 0;

  ngOnInit(): void {
    this.portfolioApi.getProfile().pipe(take(1)).subscribe({
      next: (profile) => {
        this.profile = mergeProfileWithFallback(profile, PROFILE);
      }
    });
  }

  protected get resources(): Array<{ label: string; href: string }> {
    const items: Array<{ label: string; href: string }> = [];

    if (this.profile.resumeUrl) {
      items.push({ label: 'Resume', href: this.profile.resumeUrl });
    }

    for (const link of (this.profile.socialLinks ?? SOCIAL_LINKS)) {
      if (['github', 'linkedin'].includes(link.platform)) {
        items.push({ label: link.label, href: link.url });
      }
    }

    return items;
  }

  protected get socialLinks(): Array<{ label: string; href: string; mark: string }> {
    return (this.profile.socialLinks ?? SOCIAL_LINKS)
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
