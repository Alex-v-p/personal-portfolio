import { NgFor } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiChipComponent } from '../../../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../../../shared/components/link-button/ui-link-button.component';
import { Profile } from '../../../../shared/models/profile.model';

@Component({
  selector: 'app-home-hero-section',
  standalone: true,
  imports: [NgFor, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './home-hero.component.html'
})
export class HomeHeroSectionComponent {
  @Input({ required: true }) profile!: Profile;
}
