import { Component } from '@angular/core';
import { NgFor } from '@angular/common';
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
}
