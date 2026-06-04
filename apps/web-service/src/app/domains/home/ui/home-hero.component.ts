import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiIconComponent } from '@shared/icons';
import { UiImageLightboxComponent } from '@shared/components/image-lightbox/ui-image-lightbox.component';
import { UiImageLightboxImage } from '@shared/components/image-lightbox/ui-image-lightbox.types';
import { HeroAction, Profile } from '@domains/profile/model/profile.model';
import { SocialLink } from '@domains/profile/model/social-link.model';

@Component({
  selector: 'app-home-hero-section',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiChipComponent, UiLinkButtonComponent, UiIconComponent, UiImageLightboxComponent],
  templateUrl: './home-hero.component.html'
})
export class HomeHeroSectionComponent {
  @Input({ required: true }) profile!: Profile;

  protected isHeroImageViewerOpen = false;
  protected isCvViewerOpen = false;

  protected get avatarInitials(): string {
    const first = (this.profile.firstName || '').trim().charAt(0);
    const last = (this.profile.lastName || '').trim().charAt(0);
    return `${first}${last}`.toUpperCase() || 'AV';
  }


  protected get heroLightboxImages(): UiImageLightboxImage[] {
    const imageUrl = (this.profile.heroImageUrl || this.profile.avatarUrl || '').trim();
    if (!imageUrl) {
      return [];
    }

    return [
      {
        id: this.profile.heroImageFileId || this.profile.avatarFileId || this.profile.id || 'home-hero',
        url: imageUrl,
        alt: this.profile.name || this.profile.heroTitle || 'Portfolio hero image',
      },
    ];
  }

  protected openHeroImage(event: Event): void {
    event.preventDefault();
    event.stopPropagation();

    if (!this.heroLightboxImages.length) {
      return;
    }

    this.isHeroImageViewerOpen = true;
  }

  protected closeHeroImageViewer(): void {
    this.isHeroImageViewerOpen = false;
  }


  protected get cvPreviewUrl(): string {
    return this.profile.resumePreviewUrl || this.profile.resumeUrl || '';
  }


  protected get cvLightboxDocuments(): UiImageLightboxImage[] {
    const documentUrl = this.cvPreviewUrl.trim();
    if (!documentUrl) {
      return [];
    }

    return [
      {
        id: this.profile.resumeFileId || `${this.profile.id || 'profile'}-cv`,
        url: documentUrl,
        alt: this.i18nCvTitle,
        type: 'document',
      },
    ];
  }

  protected get i18nCvTitle(): string {
    return this.profile.name ? `${this.profile.name} CV` : 'CV';
  }

  protected openCvPreview(event: Event): void {
    event.preventDefault();
    event.stopPropagation();

    if (!this.cvLightboxDocuments.length) {
      return;
    }

    this.isCvViewerOpen = true;
  }

  protected closeCvViewer(): void {
    this.isCvViewerOpen = false;
  }

  protected get cvDownloadUrl(): string {
    return this.profile.resumeUrl || this.profile.resumePreviewUrl || '';
  }

  protected isHeroCvAction(action: HeroAction): boolean {
    if (!this.cvDownloadUrl || action.appearance !== 'primary') {
      return false;
    }

    const href = (action.href ?? '').trim();
    const previewUrl = this.cvPreviewUrl.trim();
    const downloadUrl = this.cvDownloadUrl.trim();
    const normalizedLabel = action.label.trim().toLowerCase();

    return (
      (href.length > 0 && (href === previewUrl || href === downloadUrl)) ||
      normalizedLabel === 'cv' ||
      normalizedLabel.includes('cv') ||
      normalizedLabel.includes('resume')
    );
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
