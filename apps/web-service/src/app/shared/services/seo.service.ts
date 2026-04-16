import { DOCUMENT, isPlatformBrowser } from '@angular/common';
import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';

export interface PageSeoMetadata {
  title?: string;
  description?: string;
  keywords?: string[];
  image?: string;
  type?: 'website' | 'article' | 'profile';
  noIndex?: boolean;
  path?: string;
}

@Injectable({ providedIn: 'root' })
export class SeoService {
  private readonly siteName = 'Alex van Poppel Portfolio';
  private readonly defaultDescription =
    'Applied Computer Science student and full-stack builder focused on practical web applications, software architecture, data projects, and self-hosting.';
  private readonly defaultKeywords = [
    'Alex van Poppel',
    'portfolio',
    'Applied Computer Science',
    'full-stack developer',
    'web development',
    'software architecture',
    'data projects',
    'self-hosting',
    'Belgium'
  ];

  constructor(
    private readonly title: Title,
    private readonly meta: Meta,
    @Inject(DOCUMENT) private readonly document: Document,
    @Inject(PLATFORM_ID) private readonly platformId: object
  ) {}

  updatePage(metadata: PageSeoMetadata): void {
    const pageTitle = metadata.title?.trim();
    const fullTitle = pageTitle ? `${pageTitle} • ${this.siteName}` : this.siteName;
    const description = metadata.description?.trim() || this.defaultDescription;
    const keywords = metadata.keywords?.length ? metadata.keywords.join(', ') : this.defaultKeywords.join(', ');
    const type = metadata.type ?? 'website';
    const absoluteUrl = this.resolveUrl(metadata.path);
    const imageUrl = metadata.image ? this.resolveUrl(metadata.image) : undefined;
    const robots = metadata.noIndex ? 'noindex,nofollow' : 'index,follow';

    this.title.setTitle(fullTitle);
    this.meta.updateTag({ name: 'description', content: description });
    this.meta.updateTag({ name: 'keywords', content: keywords });
    this.meta.updateTag({ name: 'robots', content: robots });

    this.meta.updateTag({ property: 'og:site_name', content: this.siteName });
    this.meta.updateTag({ property: 'og:title', content: fullTitle });
    this.meta.updateTag({ property: 'og:description', content: description });
    this.meta.updateTag({ property: 'og:type', content: type });

    if (absoluteUrl) {
      this.meta.updateTag({ property: 'og:url', content: absoluteUrl });
      this.updateCanonicalLink(absoluteUrl);
    }

    this.meta.updateTag({ name: 'twitter:card', content: imageUrl ? 'summary_large_image' : 'summary' });
    this.meta.updateTag({ name: 'twitter:title', content: fullTitle });
    this.meta.updateTag({ name: 'twitter:description', content: description });

    if (imageUrl) {
      this.meta.updateTag({ property: 'og:image', content: imageUrl });
      this.meta.updateTag({ name: 'twitter:image', content: imageUrl });
    } else {
      this.meta.removeTag("property='og:image'");
      this.meta.removeTag("name='twitter:image'");
    }
  }

  private resolveUrl(path?: string): string | null {
    if (!path || !isPlatformBrowser(this.platformId)) {
      return null;
    }

    try {
      return new URL(path, this.document.baseURI).toString();
    } catch {
      return null;
    }
  }

  private updateCanonicalLink(url: string): void {
    const head = this.document.head;
    let link = head.querySelector("link[rel='canonical']") as HTMLLinkElement | null;

    if (!link) {
      link = this.document.createElement('link');
      link.setAttribute('rel', 'canonical');
      head.appendChild(link);
    }

    link.setAttribute('href', url);
  }
}
