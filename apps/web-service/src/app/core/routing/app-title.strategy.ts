import { Injectable, inject } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRouteSnapshot, RouterStateSnapshot, TitleStrategy } from '@angular/router';

import { I18nService } from '@core/i18n/i18n.service';

@Injectable()
export class AppTitleStrategy extends TitleStrategy {
  private readonly i18n = inject(I18nService);

  constructor(private readonly title: Title) {
    super();
  }

  override updateTitle(snapshot: RouterStateSnapshot): void {
    const routeTitle = this.resolveTitle(snapshot.root);
    const baseTitle = 'Portfolio';

    this.title.setTitle(routeTitle ? `${baseTitle} | ${routeTitle}` : baseTitle);
  }

  private resolveTitle(snapshot: ActivatedRouteSnapshot): string {
    const primaryChild = snapshot.children.find((child) => child.outlet === 'primary') ?? null;
    const childTitle = primaryChild ? this.resolveTitle(primaryChild) : '';

    if (childTitle) {
      return childTitle;
    }

    const titleKey = snapshot.data?.['titleKey'];
    if (typeof titleKey === 'string') {
      return this.i18n.translate(titleKey);
    }

    const staticTitle = snapshot.title;
    return typeof staticTitle === 'string' ? staticTitle : '';
  }
}
