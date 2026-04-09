import { NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-empty-state',
  standalone: true,
  imports: [NgIf],
  templateUrl: './ui-empty-state.component.html'
})
export class UiEmptyStateComponent {
  @Input() title = '';
  @Input() description = '';
  @Input() hasActions = false;
}
