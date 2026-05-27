import { NgIf } from '@angular/common';
import { Component, EventEmitter, HostListener, Input, OnChanges, Output, SimpleChanges } from '@angular/core';

import { UiImageLightboxImage } from './ui-image-lightbox.types';

@Component({
  selector: 'app-ui-image-lightbox',
  standalone: true,
  imports: [NgIf],
  templateUrl: './ui-image-lightbox.component.html'
})
export class UiImageLightboxComponent implements OnChanges {
  @Input() images: readonly UiImageLightboxImage[] = [];
  @Input() activeIndex = 0;
  @Input() title = 'Image';
  @Input() isOpen = false;
  @Output() readonly activeIndexChange = new EventEmitter<number>();
  @Output() readonly closed = new EventEmitter<void>();

  protected isZoomed = false;
  protected imageTransformOrigin = 'center center';

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isOpen'] && !this.isOpen) {
      this.resetZoom();
    }

    if (changes['activeIndex'] || changes['images']) {
      this.ensureSafeActiveIndex();
      this.resetZoom();
    }
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
    const imageUrl = this.selectedImage?.url?.trim();
    if (!imageUrl) {
      return 'none';
    }

    const escapedUrl = imageUrl.replace(/\"/g, '\\"');
    return `url("${escapedUrl}")`;
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
