import { NgFor } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiCardComponent } from '../../../../shared/components/card/ui-card.component';
import { UiLinkButtonComponent } from '../../../../shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '../../../../shared/components/section-title/ui-section-title.component';
import { ContactMethod } from '../../../../shared/models/contact-method.model';

@Component({
  selector: 'app-home-contact-preview-section',
  standalone: true,
  imports: [NgFor, UiCardComponent, UiLinkButtonComponent, UiSectionTitleComponent],
  templateUrl: './home-contact-preview.component.html'
})
export class HomeContactPreviewSectionComponent {
  @Input() methods: ContactMethod[] = [];

  protected getMethodMark(platform: string): string {
    const marks: Record<string, string> = {
      email: 'EM',
      phone: 'PH',
      github: 'GH',
      linkedin: 'LI',
      location: 'LO'
    };

    return marks[platform] ?? platform.slice(0, 2).toUpperCase();
  }
}
