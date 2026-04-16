import { NgFor, NgIf } from '@angular/common';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

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
  templateUrl: './home-experience.component.html',
  styleUrls: ['./home-experience.component.css']
})
export class HomeExperienceSectionComponent implements OnChanges {
  @Input({ required: true }) profile!: Profile;
  @Input() experiences: Experience[] = [];

  protected expandedExperienceId: string | null = null;

  ngOnChanges(changes: SimpleChanges): void {
    if (!changes['experiences']) {
      return;
    }

    const availableIds = new Set(this.experiences.map((item) => item.id));

    if (this.expandedExperienceId && !availableIds.has(this.expandedExperienceId)) {
      this.expandedExperienceId = this.experiences[0]?.id ?? null;
      return;
    }

    if (this.expandedExperienceId === null && this.experiences.length) {
      this.expandedExperienceId = this.experiences[0].id;
    }
  }

  protected isExpanded(experienceId: string): boolean {
    return this.expandedExperienceId === experienceId;
  }

  protected toggleExperience(experienceId: string): void {
    this.expandedExperienceId = this.expandedExperienceId === experienceId ? null : experienceId;
  }

  protected handleExperienceKeydown(event: KeyboardEvent, experienceId: string): void {
    if (event.key !== 'Enter' && event.key !== ' ') {
      return;
    }

    event.preventDefault();
    this.toggleExperience(experienceId);
  }
}
