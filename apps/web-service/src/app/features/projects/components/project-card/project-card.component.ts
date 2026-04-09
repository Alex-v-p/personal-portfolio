import { NgFor, NgIf } from '@angular/common';
import { Component, Input } from '@angular/core';

import { UiCardComponent } from '../../../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../../../shared/components/chip/ui-chip.component';
import { UiLinkButtonComponent } from '../../../../shared/components/link-button/ui-link-button.component';
import { Project, ProjectLink } from '../../../../shared/models/project.model';

@Component({
  selector: 'app-project-card',
  standalone: true,
  imports: [NgFor, NgIf, UiCardComponent, UiChipComponent, UiLinkButtonComponent],
  templateUrl: './project-card.component.html'
})
export class ProjectCardComponent {
  @Input({ required: true }) project!: Project;
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

  protected get secondaryActions(): ProjectLink[] {
    return this.project.links.filter((link) => link !== this.primaryAction).slice(0, this.featured ? 2 : 1);
  }

  protected get placeholderLabel(): string {
    return this.project.coverImageAlt || this.project.imageAlt || 'Project cover placeholder';
  }
}
