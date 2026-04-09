import { NgFor, NgIf } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiEmptyStateComponent } from '../../shared/components/empty-state/ui-empty-state.component';
import { UiSectionTitleComponent } from '../../shared/components/section-title/ui-section-title.component';
import { FEATURED_PROJECT, PROJECTS } from '../../shared/mock-data/projects.mock';
import { Project } from '../../shared/models/project.model';
import { ProjectCardComponent } from './components/project-card/project-card.component';

@Component({
  selector: 'app-projects-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, UiButtonComponent, UiEmptyStateComponent, UiSectionTitleComponent, ProjectCardComponent],
  templateUrl: './projects.page.html'
})
export class ProjectsPageComponent {
  protected readonly featuredProject = FEATURED_PROJECT;
  protected readonly browsableProjects = PROJECTS.filter((project) => !project.isFeatured);
  protected readonly totalProjectCount = PROJECTS.length;
  protected readonly availableSkillFilters = [
    'All',
    ...new Set(
      PROJECTS
        .flatMap((project) => project.tags)
        .sort((left, right) => left.localeCompare(right))
    )
  ];

  protected searchQuery = '';
  protected activeSkillFilter = 'All';

  protected setSkillFilter(filter: string): void {
    this.activeSkillFilter = filter;
  }

  protected resetFilters(): void {
    this.searchQuery = '';
    this.activeSkillFilter = 'All';
  }

  protected get hasActiveFilters(): boolean {
    return this.activeSkillFilter !== 'All' || this.searchQuery.trim().length > 0;
  }

  protected get filteredProjects(): Project[] {
    const normalizedQuery = this.searchQuery.trim().toLowerCase();

    return this.browsableProjects.filter((project) => {
      const matchesSkill = this.activeSkillFilter === 'All' || project.tags.includes(this.activeSkillFilter);
      const searchableContent = [project.title, project.shortDescription, project.summary, project.organization, ...project.tags]
        .join(' ')
        .toLowerCase();
      const matchesSearch = !normalizedQuery || searchableContent.includes(normalizedQuery);

      return matchesSkill && matchesSearch;
    });
  }
}
