import { Component, Input } from '@angular/core';
import { NgIf } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-ui-link-button',
  standalone: true,
  imports: [NgIf, RouterLink],
  template: `
    <a
      *ngIf="href; else internalLink"
      [class]="linkClasses"
      [href]="href"
      [attr.target]="openInNewTab ? '_blank' : null"
      [attr.rel]="openInNewTab ? 'noreferrer noopener' : null"
    >
      <ng-content></ng-content>
    </a>

    <ng-template #internalLink>
      <a [class]="linkClasses" [routerLink]="routerLink">
        <ng-content></ng-content>
      </a>
    </ng-template>
  `
})
export class UiLinkButtonComponent {
  @Input() routerLink: string | readonly string[] = '/';
  @Input() href: string | null = null;
  @Input() openInNewTab = false;
  @Input() appearance: 'primary' | 'secondary' | 'ghost' = 'secondary';

  protected get linkClasses(): string {
    const base = 'inline-flex min-h-12 items-center justify-center gap-2 rounded-full border px-5 py-3 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400';
    const variants = {
      primary: 'border-stone-900 bg-stone-900 text-white hover:-translate-y-0.5 hover:bg-stone-800',
      secondary: 'border-stone-300 bg-white/85 text-stone-900 hover:-translate-y-0.5 hover:border-stone-400 hover:bg-white',
      ghost: 'border-transparent bg-transparent text-stone-500 hover:-translate-y-0.5 hover:border-stone-300 hover:bg-white/70 hover:text-stone-900'
    };

    return `${base} ${variants[this.appearance]}`;
  }
}
