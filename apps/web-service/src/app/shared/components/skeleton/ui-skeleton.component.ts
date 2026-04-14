import { NgClass } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-ui-skeleton',
  standalone: true,
  imports: [NgClass],
  templateUrl: './ui-skeleton.component.html'
})
export class UiSkeletonComponent {
  @Input() className = 'h-4 w-full rounded-2xl';
}
