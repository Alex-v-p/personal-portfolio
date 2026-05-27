import { NgIf, NgTemplateOutlet } from '@angular/common';
import { Component, Input, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { I18nService } from '@core/i18n/i18n.service';
import { UiIconComponent } from '@shared/icons/ui-icon.component';

@Component({
  selector: 'app-ui-link-button',
  standalone: true,
  imports: [NgIf, NgTemplateOutlet, RouterLink, UiIconComponent],
  templateUrl: './ui-link-button.component.html'
})
export class UiLinkButtonComponent {
  @Input() routerLink: string | readonly string[] | null = '/';
  @Input() href: string | null = null;
  @Input() openInNewTab = false;
  @Input() appearance: 'primary' | 'secondary' | 'ghost' = 'secondary';

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


  protected get shouldShowExternalIcon(): boolean {
    return !!this.href && this.openInNewTab;
  }

  protected get opensInNewTabLabel(): string {
    return this.i18n.translate('common.actions.opensInNewTab');
  }

  protected get resolvedRouterLink(): string | readonly string[] | null {
    return this.href ? null : this.i18n.localizeRouterCommands(this.routerLink);
  }
}
