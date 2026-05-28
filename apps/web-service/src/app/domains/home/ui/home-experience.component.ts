import { NgFor, NgIf } from '@angular/common';
import { Component, Input, OnChanges, SimpleChanges, inject } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiSectionTitleComponent } from '@shared/components/section-title/ui-section-title.component';
import { Experience } from '@domains/experience/model/experience.model';
import { Profile } from '@domains/profile/model/profile.model';
import { I18nService } from '@core/i18n/i18n.service';
import { localizeInternalAppLinkUrl } from '@shared/utils/internal-link.util';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';

@Component({
  selector: 'app-home-experience-section',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiCardComponent, HighlightChipComponent, UiLinkButtonComponent, UiSectionTitleComponent],
  templateUrl: './home-experience.component.html',
  styleUrls: ['./home-experience.component.css']
})
export class HomeExperienceSectionComponent implements OnChanges {
  private readonly i18n = inject(I18nService);

  @Input({ required: true }) profile!: Profile;
  @Input() experiences: Experience[] = [];

  protected expandedExperienceId: string | null = null;


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
