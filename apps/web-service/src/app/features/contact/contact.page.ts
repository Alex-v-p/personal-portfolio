import { Component } from '@angular/core';
import { NgFor } from '@angular/common';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';

@Component({
  selector: 'app-contact-page',
  standalone: true,
  imports: [NgFor, UiButtonComponent, UiCardComponent, UiChipComponent],
  templateUrl: './contact.page.html'
})
export class ContactPageComponent {
  protected readonly contactMethods = [
    { label: 'Email', value: 'your.email@example.com' },
    { label: 'GitHub', value: 'github.com/shuzu' },
    { label: 'LinkedIn', value: 'linkedin.com/in/your-name' },
    { label: 'Location', value: 'Belgium' }
  ];

  protected readonly availability = ['Open to internships', 'Open to freelance', 'Based in Belgium'];
}
