import { DOCUMENT, NgIf } from '@angular/common';
import { Component, EventEmitter, HostListener, Inject, Input, OnChanges, OnDestroy, Output, SimpleChanges } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import { TranslatePipe } from '@core/i18n/translate.pipe';

import { UiImageLightboxImage } from './ui-image-lightbox.types';

@Component({
  selector: 'app-ui-image-lightbox',
  standalone: true,
  imports: [NgIf, TranslatePipe],
  templateUrl: './ui-image-lightbox.component.html'
})
export class UiImageLightboxComponent implements OnChanges, OnDestroy {
  @Input() images: readonly UiImageLightboxImage[] = [];
  @Input() activeIndex = 0;
  @Input() title = 'Image';
  @Input() isOpen = false;
  @Output() readonly activeIndexChange = new EventEmitter<number>();
  @Output() readonly closed = new EventEmitter<void>();

  protected isZoomed = false;
  protected imageTransformOrigin = 'center center';

  private static openLightboxCount = 0;
  private static previousBodyOverflow: string | null = null;
  private static previousDocumentOverflow: string | null = null;

  private readonly trustedDocumentUrls = new Map<string, SafeResourceUrl>();
  private hasScrollLock = false;

  constructor(
    private readonly sanitizer: DomSanitizer,
    @Inject(DOCUMENT) private readonly documentRef: Document,
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isOpen']) {
      this.syncPageScrollLock();

      if (!this.isOpen) {
        this.resetZoom();
      }
    }

    if (changes['activeIndex'] || changes['images']) {
      this.ensureSafeActiveIndex();
      this.resetZoom();
    }
  }



  ngOnDestroy(): void {
    this.releasePageScrollLock();
  }

  @HostListener('document:keydown.escape')
  onEscapeKey(): void {
    if (this.isOpen) {
      this.close();
    }
  }

  @HostListener('document:keydown.arrowLeft', ['$event'])
  onArrowLeft(event: Event): void {
    if (!this.isOpen || !this.hasMultipleImages) {
      return;
    }

    event.preventDefault();
    this.showPrevious(event);
  }

  @HostListener('document:keydown.arrowRight', ['$event'])
  onArrowRight(event: Event): void {
    if (!this.isOpen || !this.hasMultipleImages) {
      return;
    }

    event.preventDefault();
    this.showNext(event);
  }

  protected get visibleImages(): readonly UiImageLightboxImage[] {
    return this.images.filter((image) => !!image.url?.trim());
  }

  protected get selectedImage(): UiImageLightboxImage | null {
    const images = this.visibleImages;
    if (!images.length) {
      return null;
    }

    return images[this.safeActiveIndex] ?? images[0] ?? null;
  }

  protected get safeActiveIndex(): number {
    const count = this.visibleImages.length;
    if (!count) {
      return 0;
    }

    return this.activeIndex >= 0 && this.activeIndex < count ? this.activeIndex : 0;
  }

  protected get backgroundImage(): string {
    if (this.selectedImage?.type === 'document') {
      return 'none';
    }

    const imageUrl = this.selectedImage?.url?.trim();
    if (!imageUrl) {
      return 'none';
    }

    const escapedUrl = imageUrl.replace(/\"/g, '\\"');
    return `url("${escapedUrl}")`;
  }

  protected get selectedDocumentUrl(): SafeResourceUrl | null {
    const selectedItem = this.selectedImage;
    const url = selectedItem?.url?.trim();
    if (selectedItem?.type !== 'document' || !url) {
      return null;
    }

    const cachedUrl = this.trustedDocumentUrls.get(url);
    if (cachedUrl) {
      return cachedUrl;
    }

    const trustedUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
    this.trustedDocumentUrls.set(url, trustedUrl);
    return trustedUrl;
  }

  protected get hasMultipleImages(): boolean {
    return this.visibleImages.length > 1;
  }

  protected get counterLabel(): string {
    const count = this.visibleImages.length;
    if (count <= 1) {
      return '';
    }

    return `${this.safeActiveIndex + 1} / ${count}`;
  }

  protected close(event?: Event): void {
    event?.preventDefault();
    event?.stopPropagation();
    this.resetZoom();
    this.closed.emit();
  }

  protected stopPropagation(event: Event): void {
    event.stopPropagation();
  }

  protected showPrevious(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.shiftImage(-1);
  }

  protected showNext(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.shiftImage(1);
  }

  protected updateZoomOrigin(event: PointerEvent): void {
    const target = event.currentTarget as HTMLElement | null;
    if (!target) {
      return;
    }

    const rect = target.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;
    this.imageTransformOrigin = `${Math.min(100, Math.max(0, x))}% ${Math.min(100, Math.max(0, y))}%`;
    this.isZoomed = true;
  }

  protected resetZoom(): void {
    this.isZoomed = false;
    this.imageTransformOrigin = 'center center';
  }


  private syncPageScrollLock(): void {
    if (this.isOpen) {
      this.applyPageScrollLock();
      return;
    }

    this.releasePageScrollLock();
  }

  private applyPageScrollLock(): void {
    if (this.hasScrollLock) {
      return;
    }

    const body = this.documentRef.body;
    const documentElement = this.documentRef.documentElement;
    if (!body || !documentElement) {
      return;
    }

    if (UiImageLightboxComponent.openLightboxCount === 0) {
      UiImageLightboxComponent.previousBodyOverflow = body.style.overflow;
      UiImageLightboxComponent.previousDocumentOverflow = documentElement.style.overflow;
      body.style.overflow = 'hidden';
      documentElement.style.overflow = 'hidden';
    }

    UiImageLightboxComponent.openLightboxCount += 1;
    this.hasScrollLock = true;
  }

  private releasePageScrollLock(): void {
    if (!this.hasScrollLock) {
      return;
    }

    UiImageLightboxComponent.openLightboxCount = Math.max(0, UiImageLightboxComponent.openLightboxCount - 1);
    this.hasScrollLock = false;

    if (UiImageLightboxComponent.openLightboxCount > 0) {
      return;
    }

    const body = this.documentRef.body;
    const documentElement = this.documentRef.documentElement;
    if (body) {
      body.style.overflow = UiImageLightboxComponent.previousBodyOverflow ?? '';
    }
    if (documentElement) {
      documentElement.style.overflow = UiImageLightboxComponent.previousDocumentOverflow ?? '';
    }

    UiImageLightboxComponent.previousBodyOverflow = null;
    UiImageLightboxComponent.previousDocumentOverflow = null;
  }

  private shiftImage(direction: -1 | 1): void {
    const count = this.visibleImages.length;
    if (count <= 1) {
      this.setActiveIndex(0);
      return;
    }

    this.setActiveIndex((this.safeActiveIndex + direction + count) % count);
    this.resetZoom();
  }

  private setActiveIndex(index: number): void {
    if (index === this.activeIndex) {
      return;
    }

    this.activeIndex = index;
    this.activeIndexChange.emit(index);
  }

  private ensureSafeActiveIndex(): void {
    const safeIndex = this.safeActiveIndex;
    if (safeIndex !== this.activeIndex) {
      this.setActiveIndex(safeIndex);
    }
  }
}
