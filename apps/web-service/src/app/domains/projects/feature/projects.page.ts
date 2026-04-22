import { NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, DestroyRef, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { distinctUntilChanged } from 'rxjs/operators';
import { finalize, take } from 'rxjs/operators';

import { I18nService } from '@core/i18n/i18n.service';
import { TranslatePipe } from '@core/i18n/translate.pipe';
import { PublicProjectsApiService } from '@domains/projects/data/projects-api.service';
import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';
import { ProjectSummary } from '@domains/projects/model/project-summary.model';
import { ProjectCardComponent } from '@domains/projects/ui/project-card.component';

interface SkillFilterOption {
  name: string;
  projectCount: number;
}

@Component({
  selector: 'app-projects-page',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, TranslatePipe, UiButtonComponent, UiEmptyStateComponent, UiSkeletonComponent, ProjectCardComponent],
  templateUrl: './projects.page.html'
})
export class ProjectsPageComponent implements OnInit {
  private readonly projectsApi = inject(PublicProjectsApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly i18n = inject(I18nService);
  private readonly destroyRef = inject(DestroyRef);

  protected projects: ProjectSummary[] = [];
  protected searchQuery = '';
  protected selectedSkillFilters: string[] = [];
  protected isSkillMenuOpen = false;
  protected isLoading = true;
  protected errorMessage = '';

  ngOnInit(): void {
    this.i18n.localeChanges$.pipe(distinctUntilChanged(), takeUntilDestroyed(this.destroyRef)).subscribe(() => {
      this.loadProjects();
    });
  }

  protected loadProjects(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.projectsApi
      .getProjects()
      .pipe(
        take(1),
        finalize(() => {
          this.isLoading = false;
          this.changeDetectorRef.detectChanges();
        })
      )
      .subscribe({
        next: (projects) => {
          this.projects = Array.isArray(projects) ? projects : [];
        },
        error: () => {
          this.projects = [];
          this.errorMessage = this.i18n.translate('pages.projects.errors.load');
        }
      });
  }

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

  protected get featuredProject(): ProjectSummary | null {
    return this.projects.find((project) => project.isFeatured) ?? this.projects[0] ?? null;
  }

  protected get browsableProjects(): ProjectSummary[] {
    const featuredProjectId = this.featuredProject?.id;
    return this.projects.filter((project) => project.id !== featuredProjectId);
  }

  protected get totalProjectCount(): number {
    return this.projects.length;
  }

  protected get hasProjects(): boolean {
    return this.totalProjectCount > 0;
  }

  protected get availableSkillFilters(): SkillFilterOption[] {
    return Array.from(new Set(this.browsableProjects.flatMap((project) => project.tags ?? [])))
      .sort((left, right) => left.localeCompare(right))
      .map((name) => ({
        name,
        projectCount: this.browsableProjects.filter((project) => (project.tags ?? []).includes(name)).length
      }));
  }

  protected get skillFilterLabel(): string {
    if (!this.selectedSkillFilters.length) {
      return this.i18n.translate('pages.projects.filters.allTechnologies');
    }

    if (this.selectedSkillFilters.length === 1) {
      return this.selectedSkillFilters[0];
    }

    if (this.selectedSkillFilters.length === 2) {
      return this.selectedSkillFilters.join(', ');
    }

    return this.i18n.translate('pages.projects.filters.selectedCount', { count: this.selectedSkillFilters.length });
  }

  protected get filteredProjects(): ProjectSummary[] {
    const normalizedQuery = this.searchQuery.trim().toLowerCase();

    return this.browsableProjects.filter((project) => {
      const tags = project.tags ?? [];
      const matchesSkill = this.selectedSkillFilters.length === 0 || this.selectedSkillFilters.some((filter) => tags.includes(filter));
      const searchableContent = [project.title, project.shortDescription, project.summary, project.organization, ...tags].join(' ').toLowerCase();
      const matchesSearch = !normalizedQuery || searchableContent.includes(normalizedQuery);

      return matchesSkill && matchesSearch;
    });
  }
}
