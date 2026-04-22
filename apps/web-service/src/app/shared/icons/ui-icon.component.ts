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
    if (typeof this.size === 'number' && Number.isFinite(this.size)) {
      return Math.max(12, this.size);
    }

    const lookup: Record<Exclude<IconSize, number>, number> = {
      xs: 14,
      sm: 16,
      md: 20,
      lg: 24,
      xl: 32,
    };

    return lookup[this.size];
  }

  protected get fallbackMark(): string {
    const source = (this.fallbackText ?? this.label ?? this.name ?? '').replace(/[^a-zA-Z0-9]/g, '');
    return source.slice(0, 2).toUpperCase() || '•';
  }

  protected get accessibleLabel(): string {
    return this.label?.trim() || getIconLabel(this.name) || this.fallbackMark;
  }
}
