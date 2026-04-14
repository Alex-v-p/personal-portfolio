import { NgClass, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-empty-state',
  standalone: true,
  imports: [NgIf, NgClass],
  templateUrl: './ui-empty-state.component.html'
})
export class UiEmptyStateComponent {
  @Input() title = '';
  @Input() description = '';
  @Input() hasActions = false;
  @Input() tone: 'default' | 'error' = 'default';

  protected get containerClasses(): string[] {
    return this.tone === 'error'
      ? ['border-rose-200', 'bg-rose-50/90']
      : ['border-stone-300', 'bg-stone-100/65'];
  }

  protected get iconClasses(): string[] {
    return this.tone === 'error'
      ? ['border-rose-200', 'from-rose-100', 'to-rose-200']
      : ['border-stone-300', 'from-stone-200', 'to-stone-300'];
  }

  protected get titleClasses(): string[] {
    return this.tone === 'error' ? ['text-rose-950'] : ['text-stone-900'];
  }

  protected get descriptionClasses(): string[] {
    return this.tone === 'error' ? ['text-rose-900/80'] : ['text-stone-600'];
  }

  protected get role(): 'alert' | 'status' {
    return this.tone === 'error' ? 'alert' : 'status';
  }
}
