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
    const documentUrl = this.cvDocumentUrl;
    return documentUrl ? this.withQueryParam(documentUrl, 'disposition', 'inline') : '';
  }

  protected get cvFileName(): string {
    const baseName = this.profile.name ? `${this.profile.name} CV` : 'CV';
    const extension = this.fileExtensionFromUrl(this.profile.resumeUrl || this.profile.resumePreviewUrl) || 'pdf';
    return `${this.sanitizeFileName(baseName)}.${extension}`;
  }

  private get cvDocumentUrl(): string {
    const sourceUrl = (this.profile.resumeUrl || this.profile.resumePreviewUrl || '').trim();
    if (!sourceUrl) {
      return '';
    }

    return this.withFileName(sourceUrl, this.cvFileName);
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
    return this.cvDocumentUrl;
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

  private withFileName(url: string, filename: string): string {
    if (!url.includes('/media-files/')) {
      return url;
    }

    const { path, query, fragment } = this.splitUrlParts(url);
    const lastSlashIndex = path.lastIndexOf('/');
    if (lastSlashIndex < 0) {
      return url;
    }

    const encodedFileName = encodeURIComponent(filename);
    return `${path.slice(0, lastSlashIndex + 1)}${encodedFileName}${query}${fragment}`;
  }

  private withQueryParam(url: string, key: string, value: string): string {
    const { path, query, fragment } = this.splitUrlParts(url);
    const params = new URLSearchParams(query.startsWith('?') ? query.slice(1) : query);
    params.set(key, value);
    const nextQuery = params.toString();

    return `${path}${nextQuery ? `?${nextQuery}` : ''}${fragment}`;
  }

  private splitUrlParts(url: string): { path: string; query: string; fragment: string } {
    const [withoutFragment, rawFragment = ''] = url.split('#', 2);
    const [path, rawQuery = ''] = withoutFragment.split('?', 2);

    return {
      path,
      query: rawQuery ? `?${rawQuery}` : '',
      fragment: rawFragment ? `#${rawFragment}` : '',
    };
  }

  private sanitizeFileName(value: string): string {
    const cleaned = value
      .trim()
      .replace(/[^a-z0-9._ -]+/gi, '-')
      .replace(/\s+/g, ' ')
      .replace(/-+/g, '-')
      .replace(/^[. -]+|[. -]+$/g, '');

    return cleaned || 'CV';
  }

  private fileExtensionFromUrl(value: string | null | undefined): string | null {
    const path = (value || '').split('#', 1)[0]?.split('?', 1)[0] ?? '';
    const fileName = decodeURIComponent(path.substring(path.lastIndexOf('/') + 1));
    const match = fileName.match(/\.([a-z0-9]{2,8})$/i);

    return match ? match[1].toLowerCase() : null;
  }
}
