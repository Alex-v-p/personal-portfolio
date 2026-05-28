import { Component, Input, inject } from '@angular/core';

import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { HighlightedSkillService } from '@shared/services/highlighted-skill.service';

@Component({
  selector: 'app-highlight-chip',
  standalone: true,
  imports: [UiChipComponent],
  templateUrl: './highlight-chip.component.html'
})
export class HighlightChipComponent {
  private readonly highlightedSkillService = inject(HighlightedSkillService);

  @Input({ required: true }) label = '';

  protected get tone(): 'default' | 'highlight' {
    return this.highlightedSkillService.isHighlighted(this.label) ? 'highlight' : 'default';
  }
}
