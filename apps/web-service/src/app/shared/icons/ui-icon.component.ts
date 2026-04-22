import { NgIf } from '@angular/common';
import { Component, Input, inject } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

import { getIconDefinition, getIconLabel } from './icon-registry';
import type { IconSize } from './icon.types';

@Component({
  selector: 'app-ui-icon',
  standalone: true,
  imports: [NgIf],
  templateUrl: './ui-icon.component.html',
  host: {
    class: 'inline-flex items-center justify-center align-middle leading-none select-none text-current',
    '[style.width.px]': 'pixelSize',
    '[style.height.px]': 'pixelSize',
    '[attr.aria-hidden]': 'decorative ? "true" : null',
    '[attr.role]': 'decorative ? null : "img"',
    '[attr.aria-label]': 'decorative ? null : accessibleLabel',
  },
})
export class UiIconComponent {
  private readonly sanitizer = inject(DomSanitizer);

  @Input() name: string | null | undefined;
  @Input() label?: string | null;
  @Input() fallbackText?: string | null;
  @Input() decorative = true;
  @Input() size: IconSize = 'md';

  protected get svgMarkup(): SafeHtml | null {
    const icon = getIconDefinition(this.name);
    return icon ? this.sanitizer.bypassSecurityTrustHtml(icon.svg) : null;
  }

  protected get pixelSize(): number {
    const size = this.size;

    if (typeof size === 'number' && Number.isFinite(size)) {
      return Math.max(14, size);
    }

    const lookup = {
      xs: 16,
      sm: 20,
      md: 24,
      lg: 28,
      xl: 36,
    } as const;

    switch (size) {
      case 'xs':
      case 'sm':
      case 'md':
      case 'lg':
      case 'xl':
        return lookup[size];
      default:
        return lookup.md;
    }
  }

  protected get fallbackMark(): string {
    const source = (this.fallbackText ?? this.label ?? this.name ?? '').replace(/[^a-zA-Z0-9]/g, '');
    return source.slice(0, 2).toUpperCase() || '•';
  }

  protected get accessibleLabel(): string {
    return this.label?.trim() || getIconLabel(this.name) || this.fallbackMark;
  }
}
