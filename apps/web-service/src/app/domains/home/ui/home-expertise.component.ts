import { NgFor } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiSectionTitleComponent } from '@shared/components/section-title/ui-section-title.component';
import { ExpertiseGroup } from '@domains/profile/model/profile.model';

@Component({
  selector: 'app-home-expertise-section',
  standalone: true,
  imports: [NgFor, UiCardComponent, HighlightChipComponent, UiSectionTitleComponent],
  templateUrl: './home-expertise.component.html'
})
export class HomeExpertiseSectionComponent {
  @Input() groups: ExpertiseGroup[] = [];
}
