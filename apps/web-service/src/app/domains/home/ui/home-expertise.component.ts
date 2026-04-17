import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '@shared/components/section-title/ui-section-title.component';
import { ExpertiseGroup, ExpertiseSkill, Profile } from '@domains/profile/model/profile.model';

@Component({
  selector: 'app-home-expertise-section',
  standalone: true,
  imports: [NgFor, NgIf, UiCardComponent, HighlightChipComponent, UiLinkButtonComponent, UiSectionTitleComponent],
  templateUrl: './home-expertise.component.html'
})
export class HomeExpertiseSectionComponent {
  @Input({ required: true }) profile!: Profile;
  @Input() groups: ExpertiseGroup[] = [];

  protected skillItems(group: ExpertiseGroup): ExpertiseSkill[] {
    if (Array.isArray(group.skills) && group.skills.length) {
      return group.skills;
    }

    return (group.tags ?? []).map((tag) => ({ name: tag, yearsOfExperience: null }));
  }

  protected formatSkillLabel(skill: ExpertiseSkill): string {
    return skill.yearsOfExperience && skill.yearsOfExperience > 0
      ? `${skill.name} - ${skill.yearsOfExperience}y`
      : skill.name;
  }
}
