import { NgFor, NgIf } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { UiCardComponent } from '../../shared/components/card/ui-card.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiEmptyStateComponent } from '../../shared/components/empty-state/ui-empty-state.component';
import { UiLinkButtonComponent } from '../../shared/components/link-button/ui-link-button.component';
import { FEATURED_PROJECT, PROJECTS } from '../../shared/mock-data/projects.mock';
import { Project } from '../../shared/models/project.model';

@Component({
  selector: 'app-projects-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, UiCardComponent, UiChipComponent, UiEmptyStateComponent, UiLinkButtonComponent],
  templateUrl: './projects.page.html'
})
export class ProjectsPageComponent {
  protected readonly featuredProject = FEATURED_PROJECT;
  protected readonly totalProjectCount = PROJECTS.length;
  protected readonly pagerDots = [1, 2, 3];
  protected readonly filters = ['All', ...new Set(PROJECTS.map((project) => project.category))];

  protected searchQuery = '';
  protected activeFilter = 'All';

  protected setFilter(filter: string): void {
    this.activeFilter = filter;
  }

  protected get filteredProjects(): Project[] {
    return PROJECTS
      .filter((project) => !project.featured)
      .filter((project) => this.activeFilter === 'All' || project.category === this.activeFilter)
      .filter((project) => {
        const query = this.searchQuery.trim().toLowerCase();

        if (!query) {
          return true;
        }

        const haystack = [project.title, project.shortDescription, project.summary, project.organization, ...project.tags]
          .join(' ')
          .toLowerCase();

        return haystack.includes(query);
      });
  }
}
