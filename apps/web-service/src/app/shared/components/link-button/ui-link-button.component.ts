import { Component, Input, inject } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-ui-link-button',
  standalone: true,
  templateUrl: './ui-link-button.component.html'
})
export class UiLinkButtonComponent {
  @Input() routerLink: string | readonly string[] | null = '/';
  @Input() href: string | null = null;
  @Input() openInNewTab = false;
  @Input() appearance: 'primary' | 'secondary' | 'ghost' = 'secondary';

  private readonly router = inject(Router);

  protected get linkClasses(): string {
    const base = 'ui-btn';
    const variants = {
      primary: 'ui-btn-primary',
      secondary: 'ui-btn-secondary',
      ghost: 'ui-btn-ghost'
    } as const;

    return `${base} ${variants[this.appearance]}`;
  }

  protected get resolvedHref(): string | null {
    if (this.href) {
      return this.href;
    }

    if (!this.routerLink) {
      return null;
    }

    const commands = Array.isArray(this.routerLink) ? this.routerLink : [this.routerLink];
    return this.router.serializeUrl(this.router.createUrlTree([...commands]));
  }

  protected handleClick(event: MouseEvent): void {
    if (this.href || !this.routerLink) {
      return;
    }

    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }

    event.preventDefault();

    const commands = Array.isArray(this.routerLink) ? [...this.routerLink] : [this.routerLink];
    void this.router.navigate(commands);
  }
}