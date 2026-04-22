import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiIconComponent } from '@shared/icons';
import { Profile } from '@domains/profile/model/profile.model';
import { SocialLink } from '@domains/profile/model/social-link.model';

@Component({
  selector: 'app-home-hero-section',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiChipComponent, UiLinkButtonComponent, UiIconComponent],
  templateUrl: './home-hero.component.html'
})
export class HomeHeroSectionComponent {
  @Input({ required: true }) profile!: Profile;

  protected get avatarInitials(): string {
    const first = (this.profile.firstName || '').trim().charAt(0);
    const last = (this.profile.lastName || '').trim().charAt(0);
    return `${first}${last}`.toUpperCase() || 'AV';
  }

  protected get socialButtons(): Array<{
    label: string;
    iconName: string;
    fallbackText: string;
    href: string;
    openInNewTab: boolean;
  }> {
    return (this.profile.socialLinks ?? [])
      .filter((link) => link.isVisible)
      .map((link) => {
        const href = this.getSocialHref(link);
        const label = link.label || this.formatPlatform(link.platform);

        return {
          label,
          iconName: link.iconKey || link.platform,
          fallbackText: label,
          href,
          openInNewTab: !href.startsWith('mailto:')
        };
      })
      .filter((link) => Boolean(link.href));
  }

  private getSocialHref(link: SocialLink): string {
    if (link.url) {
      return link.url.startsWith('mailto:') || link.url.startsWith('http') ? link.url : this.platformIsEmail(link) ? `mailto:${link.url}` : link.url;
    }

    if (this.platformIsEmail(link) && this.profile.email) {
      return `mailto:${this.profile.email}`;
    }

    return '';
  }

  private formatPlatform(platform: string): string {
    return platform ? platform.charAt(0).toUpperCase() + platform.slice(1) : 'Link';
  }

  private platformIsEmail(link: SocialLink): boolean {
    return (link.platform || '').trim().toLowerCase() === 'email';
  }
}
