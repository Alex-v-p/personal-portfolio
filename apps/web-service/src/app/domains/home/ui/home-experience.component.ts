import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '@shared/components/section-title/ui-section-title.component';
import { Experience } from '@domains/experience/model/experience.model';
import { Profile } from '@domains/profile/model/profile.model';

@Component({
  selector: 'app-home-experience-section',
  standalone: true,
  imports: [NgFor, NgIf, UiCardComponent, UiChipComponent, UiLinkButtonComponent, UiSectionTitleComponent],
  templateUrl: './home-experience.component.html'
})
export class HomeExperienceSectionComponent {
  @Input({ required: true }) profile!: Profile;
  @Input() experiences: Experience[] = [];
}
