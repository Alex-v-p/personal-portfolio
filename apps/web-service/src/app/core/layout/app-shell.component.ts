import { NgFor } from '@angular/common';
import { Component, HostListener } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { NAVIGATION_ITEMS } from '../../shared/mock-data/navigation-items.mock';
import { PROFILE } from '../../shared/mock-data/profile.mock';
import { SOCIAL_LINKS } from '../../shared/mock-data/social-links.mock';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [NgFor, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app-shell.component.html'
})
export class AppShellComponent {
  protected readonly profile = PROFILE;

  protected readonly quickLinks = NAVIGATION_ITEMS.filter((item) => item.isVisible).map((item) => ({
    label: item.label,
    path: item.routePath
  }));

  protected readonly footerLinks = [...this.quickLinks];

  protected readonly resources = [
    { label: 'Resume', href: PROFILE.resumeUrl ?? '/assets/mock-resume.pdf' },
    ...SOCIAL_LINKS.filter((link) => ['github', 'linkedin'].includes(link.platform)).map((link) => ({
      label: link.label,
      href: link.url
    }))
  ];

  protected readonly socialLinks = SOCIAL_LINKS
    .filter((link) => ['email', 'github', 'linkedin'].includes(link.platform))
    .map((link) => ({
      label: link.label,
      href: link.url,
      mark: link.platform === 'email' ? 'EM' : link.platform === 'github' ? 'GH' : 'LI'
    }));

  protected readonly primaryEmail = PROFILE.email;

  protected readonly shellChrome = {
    headerVisible: true,
    assistantVisible: true,
    isStickyEnabled: true,
    hasScrolledPastThreshold: false,
    scrollDirection: 'up' as 'up' | 'down'
  };

  private lastScrollY = 0;

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

    // The shell state is intentionally ready for a later sticky/hide-on-scroll pass.
    // For now, Stage 2 keeps the chrome visible while pages move to shared data.
    this.shellChrome.headerVisible = true;
    this.shellChrome.assistantVisible = true;

    this.lastScrollY = Math.max(currentScrollY, 0);
  }
}
