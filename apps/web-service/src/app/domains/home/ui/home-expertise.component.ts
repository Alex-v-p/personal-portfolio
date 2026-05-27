import { NgFor, NgIf } from '@angular/common';
import { Component, Input, inject } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '@shared/components/section-title/ui-section-title.component';
import { UiIconComponent } from '@shared/icons';
import { I18nService } from '@core/i18n/i18n.service';
import { localizeInternalAppLinkUrl } from '@shared/utils/internal-link.util';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';
import { ExpertiseGroup, ExpertiseSkill, Profile } from '@domains/profile/model/profile.model';

@Component({
  selector: 'app-home-expertise-section',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiCardComponent, HighlightChipComponent, UiLinkButtonComponent, UiSectionTitleComponent, UiIconComponent],
  templateUrl: './home-expertise.component.html'
})
export class HomeExpertiseSectionComponent {
  private readonly i18n = inject(I18nService);

  @Input({ required: true }) profile!: Profile;
  @Input() groups: ExpertiseGroup[] = [];


  protected get renderedLongBioHtml(): string {
    return this.renderLongBioMarkdown();
  }

  protected hasLongBio(): boolean {
    return Boolean(this.profile?.longBio?.trim() || this.profile?.introParagraphs?.length);
  }

  private renderLongBioMarkdown(): string {
    const markdown = this.profile?.longBio?.trim() || (this.profile?.introParagraphs ?? []).join('\n\n').trim();

    if (!markdown) {
      return '';
    }

    return renderMarkdownToHtml(markdown, {
      transformLinkUrl: (url) => localizeInternalAppLinkUrl(url, this.i18n),
    });
  }

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
