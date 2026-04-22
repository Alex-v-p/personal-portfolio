import { NgFor, NgIf } from '@angular/common';
import { Component, Input, inject } from '@angular/core';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { ProjectLink, ProjectSummary } from '@domains/projects/model/project-summary.model';

@Component({
  selector: 'app-project-card',
  standalone: true,
  imports: [NgFor, NgIf, TranslatePipe, UiCardComponent, UiChipComponent, HighlightChipComponent, UiLinkButtonComponent],
  templateUrl: './project-card.component.html'
})
export class ProjectCardComponent {
  private readonly i18n = inject(I18nService);

  @Input({ required: true }) project!: ProjectSummary;
  @Input() featured = false;

  protected get displayedTags(): string[] {
    return this.project.tags.slice(0, this.featured ? 5 : 4);
  }

  protected get primaryAction(): ProjectLink | null {
    const externalDemo = this.project.links.find((link) => link.label.toLowerCase().includes('demo'));
    const externalGithub = this.project.links.find((link) => link.label.toLowerCase().includes('github'));
    const internalReadMore = this.project.links.find((link) => link.routerLink);

    return externalDemo ?? externalGithub ?? internalReadMore ?? this.project.links[0] ?? null;
  }

  protected get readMoreAction(): ProjectLink | null {
    return this.primaryAction;
  }

  protected get extraActions(): ProjectLink[] {
    return this.project.links
      .filter((link) => link !== this.readMoreAction)
      .filter((link) => (link.label ?? '').trim().length > 0)
      .slice(0, this.featured ? 1 : 0);
  }

  protected get secondaryActions(): ProjectLink[] {
    return this.project.links.filter((link) => link !== this.primaryAction).slice(0, this.featured ? 2 : 1);
  }

  protected get placeholderLabel(): string {
    return this.project.coverImageAlt || this.project.imageAlt || this.i18n.translate('pages.projects.card.placeholder');
  }
}
