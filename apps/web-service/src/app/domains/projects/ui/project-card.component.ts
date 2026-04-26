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

  protected get readMoreAction(): ProjectLink | null {
    return this.project.links.find((link) => link.routerLink) ?? {
      label: this.i18n.translate('common.actions.readMore'),
      routerLink: ['/projects', this.project.slug],
    };
  }

  protected get demoAction(): ProjectLink | null {
    const directDemoUrl = this.project.demoUrl?.trim();
    const linkedDemo = this.project.links.find((link) => this.isDemoLink(link));
    const externalProjectLink = this.project.links.find((link) => this.isNonRepositoryExternalLink(link));
    const href = directDemoUrl || linkedDemo?.href?.trim() || externalProjectLink?.href?.trim();

    if (!href) {
      return null;
    }

    return {
      label: this.i18n.translate('common.actions.liveDemo'),
      href,
    };
  }

  private isDemoLink(link: ProjectLink): boolean {
    const href = link.href?.trim();
    if (!href) {
      return false;
    }

    const label = (link.label ?? '').toLowerCase();
    return label.includes('demo') || label.includes('live') || href === this.project.demoUrl;
  }

  private isNonRepositoryExternalLink(link: ProjectLink): boolean {
    const href = link.href?.trim();
    if (!href) {
      return false;
    }

    const label = (link.label ?? '').toLowerCase();
    return !label.includes('github') && href !== this.project.githubUrl;
  }

  protected get placeholderLabel(): string {
    return this.project.coverImageAlt || this.project.imageAlt || this.i18n.translate('pages.projects.card.placeholder');
  }
}
