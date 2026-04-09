import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-button',
  standalone: true,
  template: `
    <button [attr.type]="type" [disabled]="disabled" [class]="buttonClasses">
      <ng-content></ng-content>
    </button>
  `
})
export class UiButtonComponent {
  @Input() appearance: 'primary' | 'secondary' | 'ghost' = 'primary';
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  @Input() disabled = false;

  protected get buttonClasses(): string {
    const base = 'inline-flex min-h-12 items-center justify-center gap-2 rounded-full border px-5 py-3 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400 disabled:cursor-not-allowed disabled:opacity-55';
    const variants = {
      primary: 'border-stone-900 bg-stone-900 text-white hover:-translate-y-0.5 hover:bg-stone-800',
      secondary: 'border-stone-300 bg-white/85 text-stone-900 hover:-translate-y-0.5 hover:border-stone-400 hover:bg-white',
      ghost: 'border-stone-200/0 bg-transparent text-stone-500 hover:-translate-y-0.5 hover:border-stone-300 hover:bg-white/70 hover:text-stone-900'
    };

    return `${base} ${variants[this.appearance]}`;
  }
}
