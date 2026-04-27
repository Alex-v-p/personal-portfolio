import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '@shared/components/section-title/ui-section-title.component';
import { UiIconComponent } from '@shared/icons';
import { ExpertiseGroup, ExpertiseSkill, Profile } from '@domains/profile/model/profile.model';

@Component({
  selector: 'app-home-expertise-section',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiCardComponent, HighlightChipComponent, UiLinkButtonComponent, UiSectionTitleComponent, UiIconComponent],
  templateUrl: './home-expertise.component.html'
})
export class HomeExpertiseSectionComponent {
  @Input({ required: true }) profile!: Profile;
  @Input() groups: ExpertiseGroup[] = [];

  protected skillItems(group: ExpertiseGroup): ExpertiseSkill[] {
    if (Array.isArray(group.skills) && group.skills.length) {
      return group.skills;
    }

    return (group.tags ?? []).map((tag) => ({ name: tag, yearsOfExperience: null, displayLabel: null, proficiencyLabel: null }));
  }

  protected formatSkillLabel(skill: ExpertiseSkill): string {
    if (skill.displayLabel) {
      return `${skill.name} - ${skill.displayLabel}`;
    }

    if (skill.proficiencyLabel) {
      return `${skill.name} - ${skill.proficiencyLabel}`;
    }

    return skill.yearsOfExperience && skill.yearsOfExperience > 0
      ? `${skill.name} - ${skill.yearsOfExperience}y`
      : skill.name;
  }
}
