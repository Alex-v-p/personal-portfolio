import { Component, Input, inject } from '@angular/core';
import { Router } from '@angular/router';

import { I18nService } from '@core/i18n/i18n.service';

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
  private readonly i18n = inject(I18nService);

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

    const localizedRouterLink = this.localizedRouterLink;
    if (!localizedRouterLink) {
      return null;
    }

    const commands = Array.isArray(localizedRouterLink) ? localizedRouterLink : [localizedRouterLink];
    return this.router.serializeUrl(this.router.createUrlTree([...commands]));
  }

  protected handleClick(event: MouseEvent): void {
    if (this.href) {
      return;
    }

    const localizedRouterLink = this.localizedRouterLink;
    if (!localizedRouterLink) {
      return;
    }

    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }

    event.preventDefault();

    const commands = Array.isArray(localizedRouterLink) ? [...localizedRouterLink] : [localizedRouterLink];
    void this.router.navigate(commands);
  }

  private get localizedRouterLink(): string | readonly string[] | null {
    return this.i18n.localizeRouterCommands(this.routerLink);
  }
}
