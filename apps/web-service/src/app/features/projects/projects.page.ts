import { NgFor, NgIf } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { UiButtonComponent } from '../../shared/components/button/ui-button.component';
import { UiChipComponent } from '../../shared/components/chip/ui-chip.component';
import { UiEmptyStateComponent } from '../../shared/components/empty-state/ui-empty-state.component';
import { UiSectionTitleComponent } from '../../shared/components/section-title/ui-section-title.component';
import { FEATURED_PROJECT, PROJECTS } from '../../shared/mock-data/projects.mock';
import { Project } from '../../shared/models/project.model';
import { ProjectCardComponent } from './components/project-card/project-card.component';

interface SkillFilterOption {
  name: string;
  projectCount: number;
}

@Component({
  selector: 'app-projects-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, UiButtonComponent, UiChipComponent, UiEmptyStateComponent, UiSectionTitleComponent, ProjectCardComponent],
  templateUrl: './projects.page.html'
})
export class ProjectsPageComponent {
  protected readonly featuredProject = FEATURED_PROJECT;
  protected readonly browsableProjects = PROJECTS.filter((project) => !project.isFeatured);
  protected readonly totalProjectCount = PROJECTS.length;
  protected readonly availableSkillFilters: SkillFilterOption[] = Array.from(
    new Set(this.browsableProjects.flatMap((project) => project.tags))
  )
    .sort((left, right) => left.localeCompare(right))
    .map((name) => ({
      name,
      projectCount: this.browsableProjects.filter((project) => project.tags.includes(name)).length
    }));

  protected searchQuery = '';
  protected selectedSkillFilters: string[] = [];
  protected isSkillMenuOpen = false;

  protected toggleSkillMenu(): void {
    this.isSkillMenuOpen = !this.isSkillMenuOpen;
  }

  protected closeSkillMenu(): void {
    this.isSkillMenuOpen = false;
  }

  protected toggleSkillFilter(filter: string): void {
    this.selectedSkillFilters = this.selectedSkillFilters.includes(filter)
      ? this.selectedSkillFilters.filter((item) => item !== filter)
      : [...this.selectedSkillFilters, filter];
  }

  protected clearSkillFilters(): void {
    this.selectedSkillFilters = [];
  }

  protected resetFilters(): void {
    this.searchQuery = '';
    this.selectedSkillFilters = [];
    this.isSkillMenuOpen = false;
  }

  protected isSkillSelected(filter: string): boolean {
    return this.selectedSkillFilters.includes(filter);
  }

  protected get hasActiveFilters(): boolean {
    return this.selectedSkillFilters.length > 0 || this.searchQuery.trim().length > 0;
  }

  protected get skillFilterLabel(): string {
    if (!this.selectedSkillFilters.length) {
      return 'All technologies';
    }

    if (this.selectedSkillFilters.length === 1) {
      return this.selectedSkillFilters[0];
    }

    if (this.selectedSkillFilters.length === 2) {
      return this.selectedSkillFilters.join(', ');
    }

    return `${this.selectedSkillFilters.length} technologies selected`;
  }

  protected clearSearch(): void {
    this.searchQuery = '';
  }

  protected get filteredProjects(): Project[] {
    const normalizedQuery = this.searchQuery.trim().toLowerCase();

    return this.browsableProjects.filter((project) => {
      const matchesSkill =
        this.selectedSkillFilters.length === 0 ||
        this.selectedSkillFilters.some((filter) => project.tags.includes(filter));
      const searchableContent = [project.title, project.shortDescription, project.summary, project.organization, ...project.tags]
        .join(' ')
        .toLowerCase();
      const matchesSearch = !normalizedQuery || searchableContent.includes(normalizedQuery);

      return matchesSkill && matchesSearch;
    });
  }
}
