import { NgFor, NgIf } from '@angular/common';
import { Component, Input, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { I18nService } from '@core/i18n/i18n.service';

export interface UiBreadcrumbItem {
  label: string;
  path?: string | null;
}

@Component({
  selector: 'app-ui-breadcrumbs',
  standalone: true,
  imports: [NgFor, NgIf, RouterLink],
  templateUrl: './ui-breadcrumbs.component.html',
})
export class UiBreadcrumbsComponent {
  private readonly i18n = inject(I18nService);

  @Input() items: UiBreadcrumbItem[] = [];

  protected routerLinkFor(item: UiBreadcrumbItem): string | readonly string[] | null {
    return this.i18n.localizeRouterCommands(item.path);
  }
}
