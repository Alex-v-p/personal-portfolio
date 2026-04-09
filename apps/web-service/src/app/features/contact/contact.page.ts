import { Component } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { CONTACT_METHODS } from '../../shared/mock-data/contact-links.mock';
import { PROFILE } from '../../shared/mock-data/profile.mock';

@Component({
  selector: 'app-contact-page',
  standalone: true,
  imports: [NgFor, NgIf, UiButtonComponent, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './contact.page.html'
})
export class ContactPageComponent {
  protected readonly profile = PROFILE;
  protected readonly contactMethods = CONTACT_METHODS;
}
