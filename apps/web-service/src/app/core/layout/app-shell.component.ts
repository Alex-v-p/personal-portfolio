import { NgFor } from '@angular/common';
import { Component, HostListener } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { CONTACT_METHODS } from '../../shared/mock-data/contact-links.mock';
import { PROFILE } from '../../shared/mock-data/profile.mock';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [NgFor, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app-shell.component.html'
})
export class AppShellComponent {
  protected readonly profile = PROFILE;

  protected readonly quickLinks = [
    { label: 'Home', path: '/' },
    { label: 'Projects', path: '/projects' },
    { label: 'Blog', path: '/blog' },
    { label: 'Contact', path: '/contact' },
    { label: 'Stats', path: '/stats' }
  ];

  protected readonly footerLinks = [...this.quickLinks];

  protected readonly resources = [
    { label: 'Resume', href: '/assets/mock-resume.pdf' },
    { label: 'GitHub', href: 'https://github.com/shuzu' },
    { label: 'LinkedIn', href: 'https://linkedin.com/in/alex-van-poppel' }
  ];

  protected readonly socialLinks = CONTACT_METHODS
    .filter((method) => ['email', 'github', 'linkedin'].includes(method.id))
    .map((method) => ({
      label: method.label,
      href: method.href,
      mark: method.id === 'email' ? 'EM' : method.id === 'github' ? 'GH' : 'LI'
    }));

  protected readonly primaryEmail = CONTACT_METHODS.find((method) => method.id === 'email')?.value ?? 'hello@shuzu.dev';

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
