import { NgFor } from '@angular/common';
import { Component, HostListener } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [NgFor, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './app-shell.component.html'
})
export class AppShellComponent {
  protected readonly quickLinks = [
    { label: 'Home', path: '/' },
    { label: 'Projects', path: '/projects' },
    { label: 'Blog', path: '/blog' },
    { label: 'Contact', path: '/contact' },
    { label: 'Stats', path: '/stats' }
  ];

  protected readonly footerLinks = [
    { label: 'Home', path: '/' },
    { label: 'Projects', path: '/projects' },
    { label: 'Blog', path: '/blog' },
    { label: 'Stats', path: '/stats' }
  ];

  protected readonly resources = ['Resume', 'GitHub', 'LinkedIn'];
  protected readonly socialMarks = ['GH', 'LI', 'EM'];

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
    const visibleState = this.shellChrome.assistantVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0 pointer-events-none';

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

    // Keep the chrome visible for now. This state exists so hide/show-on-scroll
    // behavior can be added later without restructuring the layout component.
    this.shellChrome.headerVisible = true;
    this.shellChrome.assistantVisible = true;

    this.lastScrollY = Math.max(currentScrollY, 0);
  }
}
