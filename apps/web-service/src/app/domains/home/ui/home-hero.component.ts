import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { Profile } from '@domains/profile/model/profile.model';
import { SocialLink } from '@domains/profile/model/social-link.model';

@Component({
  selector: 'app-home-hero-section',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './home-hero.component.html'
})
export class HomeHeroSectionComponent {
  @Input({ required: true }) profile!: Profile;

  protected get avatarInitials(): string {
    const first = (this.profile.firstName || '').trim().charAt(0);
    const last = (this.profile.lastName || '').trim().charAt(0);
    return `${first}${last}`.toUpperCase() || 'AV';
  }

  protected get socialButtons(): Array<{ label: string; mark: string; href: string; openInNewTab: boolean }> {
    return (this.profile.socialLinks ?? [])
      .filter((link) => link.isVisible)
      .map((link) => ({
        label: link.label || this.formatPlatform(link.platform),
        mark: this.getSocialMark(link),
        href: this.getSocialHref(link),
        openInNewTab: !this.getSocialHref(link).startsWith('mailto:')
      }))
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

  private getSocialMark(link: SocialLink): string {
    const platform = (link.platform || '').trim().toLowerCase();

    if (platform === 'github') {
      return 'GH';
    }

    if (platform === 'linkedin') {
      return 'LI';
    }

    if (platform === 'email') {
      return 'EM';
    }

    if (platform === 'instagram') {
      return 'IG';
    }

    if (platform === 'x' || platform === 'twitter') {
      return 'X';
    }

    const source = (link.iconKey || link.label || link.platform || '').replace(/[^a-zA-Z0-9]/g, '');
    return source.slice(0, 2).toUpperCase() || 'LK';
  }

  private formatPlatform(platform: string): string {
    return platform ? platform.charAt(0).toUpperCase() + platform.slice(1) : 'Link';
  }

  private platformIsEmail(link: SocialLink): boolean {
    return (link.platform || '').trim().toLowerCase() === 'email';
  }
}
