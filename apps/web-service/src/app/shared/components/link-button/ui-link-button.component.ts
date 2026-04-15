import { NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-ui-link-button',
  standalone: true,
  imports: [NgIf, RouterLink],
  templateUrl: './ui-link-button.component.html'
})
export class UiLinkButtonComponent {
  @Input() routerLink: string | readonly string[] = '/';
  @Input() href: string | null = null;
  @Input() openInNewTab = false;
  @Input() appearance: 'primary' | 'secondary' | 'ghost' = 'secondary';

  protected get linkClasses(): string {
    const base = 'ui-btn';
    const variants = {
      primary: 'ui-btn-primary',
      secondary: 'ui-btn-secondary',
      ghost: 'ui-btn-ghost'
    } as const;

    return `${base} ${variants[this.appearance]}`;
  }
}
