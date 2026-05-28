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
      ? ['ui-alert', 'ui-alert-danger']
      : ['ui-card-soft'];
  }

  protected get iconClasses(): string[] {
    return [this.tone === 'error' ? 'ui-empty-icon-error' : 'ui-empty-icon'];
  }

  protected get titleClasses(): string[] {
    return ['ui-text-strong'];
  }

  protected get descriptionClasses(): string[] {
    return this.tone === 'error' ? ['ui-text-strong'] : ['ui-text-muted'];
  }

  protected get role(): 'alert' | 'status' {
    return this.tone === 'error' ? 'alert' : 'status';
  }
}
