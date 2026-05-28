import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-button',
  standalone: true,
  templateUrl: './ui-button.component.html'
})
export class UiButtonComponent {
  @Input() appearance: 'primary' | 'secondary' | 'ghost' = 'primary';
  @Input() type: 'button' | 'submit' | 'reset' = 'button';
  @Input() disabled = false;

  protected get buttonClasses(): string {
    const base = 'ui-btn';
    const variants = {
      primary: 'ui-btn-primary',
      secondary: 'ui-btn-secondary',
      ghost: 'ui-btn-ghost'
    } as const;

    return `${base} ${variants[this.appearance]}`;
  }
}
