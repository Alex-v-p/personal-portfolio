import { NgFor, NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, Input, inject } from '@angular/core';
import { Router } from '@angular/router';
import { take } from 'rxjs/operators';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { UiCardComponent } from '@shared/components/card/ui-card.component';
import { UiChipComponent } from '@shared/components/chip/ui-chip.component';
import { HighlightChipComponent } from '@shared/components/highlight-chip/highlight-chip.component';
import { UiLinkButtonComponent } from '@shared/components/link-button/ui-link-button.component';
import { UiIconComponent } from '@shared/icons/ui-icon.component';
import { renderMarkdownToHtml } from '@shared/utils/markdown.util';
import { localizeInternalAppLinkUrl } from '@shared/utils/internal-link.util';
import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { PublicProjectsApiService } from '@domains/projects/data/projects-api.service';
import { ProjectDetail } from '@domains/projects/model/project-detail.model';
import { ProjectLink, ProjectSummary } from '@domains/projects/model/project-summary.model';

import { ProjectDetailModalComponent } from './project-detail-modal.component';

@Component({
  selector: 'app-project-card',
  standalone: true,
  imports: [
    NgFor,
    NgIf,
    TranslatePipe,
    UiCardComponent,
    UiChipComponent,
    HighlightChipComponent,
    UiLinkButtonComponent,
    UiIconComponent,
    ProjectDetailModalComponent,
  ],
  templateUrl: './project-card.component.html'
})
export class ProjectCardComponent {
  private readonly i18n = inject(I18nService);
  private readonly projectsApi = inject(PublicProjectsApiService);
  private readonly router = inject(Router);
  private readonly changeDetector = inject(ChangeDetectorRef);

  @Input({ required: true }) project!: ProjectSummary;
  @Input() featured = false;

  protected activeGalleryIndex = 0;
  protected areTagsExpanded = false;
  protected detailModalProject: ProjectDetail | null = null;
  protected detailErrorMessage = '';
  protected isDetailLoading = false;
  protected isDetailModalOpen = false;

  private isDetailRequestInFlight = false;

  private get tagPreviewLimit(): number {
    return this.featured ? 5 : 4;
  }

  protected get displayedTags(): string[] {
    return this.areTagsExpanded ? this.project.tags : this.project.tags.slice(0, this.tagPreviewLimit);
  }

  protected get hiddenTagCount(): number {
    return Math.max(this.project.tags.length - this.tagPreviewLimit, 0);
  }

  protected get shouldShowTagToggle(): boolean {
    return this.project.tags.length > this.tagPreviewLimit;
  }

  protected get tagToggleLabel(): string {
    if (this.areTagsExpanded) {
      return this.i18n.translate('common.actions.showLess');
    }

    return this.i18n.translate('common.actions.showMoreCount', { count: this.hiddenTagCount });
  }

  protected toggleTags(): void {
    this.areTagsExpanded = !this.areTagsExpanded;
  }

  protected get readMoreAction(): ProjectLink | null {
    return this.buildReadMoreAction(this.project);
  }

  protected get githubAction(): ProjectLink | null {
    return this.buildGithubAction(this.project);
  }

  protected get demoAction(): ProjectLink | null {
    return this.buildDemoAction(this.project);
  }

  protected get modalReadMoreAction(): ProjectLink | null {
    return this.buildReadMoreAction(this.detailModalProject ?? this.project);
  }

  protected get modalGithubAction(): ProjectLink | null {
    return this.buildGithubAction(this.detailModalProject ?? this.project);
  }

  protected get modalDemoAction(): ProjectLink | null {
    return this.buildDemoAction(this.detailModalProject ?? this.project);
  }

  protected get primaryCardAction(): ProjectLink | null {
    return this.readMoreAction ?? this.demoAction;
  }

  protected get hasPopupCardAction(): boolean {
    return this.project.isCardPopupEnabled !== false && !!this.project.slug;
  }

  protected get hasCardClickAction(): boolean {
    return this.hasPopupCardAction || this.primaryCardAction !== null;
  }

  protected get cardRole(): 'button' | 'link' | null {
    if (this.hasPopupCardAction) {
      return 'button';
    }

    return this.primaryCardAction ? 'link' : null;
  }

  protected get mediaClickHref(): string | null {
    if (this.hasPopupCardAction) {
      return null;
    }

    return this.primaryCardAction?.href?.trim() || null;
  }

  protected get mediaClickAriaLabel(): string {
    return this.primaryCardAriaLabel ?? this.project.title;
  }

  protected get primaryCardAriaLabel(): string | null {
    if (this.hasPopupCardAction) {
      return `Open project details: ${this.project.title}`;
    }

    const action = this.primaryCardAction;
    if (!action) {
      return null;
    }

    return `${action.label}: ${this.project.title}`;
  }

  protected openCardAction(event: Event): void {
    if (!this.hasCardClickAction || this.isNestedInteractiveTarget(event)) {
      return;
    }

    event.preventDefault();

    if (this.hasPopupCardAction) {
      this.openProjectDetails();
      return;
    }

    this.openProjectLinkAction(this.primaryCardAction);
  }

  protected closeDetailModal(): void {
    this.isDetailModalOpen = false;
    this.isDetailLoading = false;
  }

  protected prefetchProjectDetails(): void {
    if (!this.hasPopupCardAction || this.detailModalProject || this.isDetailRequestInFlight) {
      return;
    }

    this.loadProjectDetails();
  }

  protected get renderedTeaserHtml(): string {
    return renderMarkdownToHtml(this.project.teaser || this.project.shortDescription || '', this.markdownRenderOptions);
  }

  protected get renderedFeaturedSummaryHtml(): string {
    return renderMarkdownToHtml(this.project.summary || this.project.teaser || this.project.shortDescription || '', this.markdownRenderOptions);
  }

  private get markdownRenderOptions(): { transformLinkUrl: (url: string) => string } {
    return { transformLinkUrl: (url) => localizeInternalAppLinkUrl(url, this.i18n) };
  }

  protected get galleryImages(): ResolvedMedia[] {
    const images = [...(this.project.galleryImages ?? [])].filter((image) => !!image.url);

    if (!this.project.coverImageUrl) {
      return images;
    }

    const coverImage: ResolvedMedia = {
      id: this.project.coverImageFileId ?? this.project.id,
      url: this.project.coverImageUrl,
      alt: this.project.coverImageAlt || this.project.imageAlt || this.project.title,
    };

    const alreadyContainsCover = images.some((image) => {
      if (coverImage.id && image.id === coverImage.id) {
        return true;
      }
      return image.url === coverImage.url;
    });

    return alreadyContainsCover ? images : [coverImage, ...images];
  }

  protected get currentGalleryImage(): ResolvedMedia | null {
    const images = this.galleryImages;
    if (!images.length) {
      return null;
    }

    const safeIndex = this.activeGalleryIndex >= 0 && this.activeGalleryIndex < images.length ? this.activeGalleryIndex : 0;
    return images[safeIndex] ?? images[0] ?? null;
  }

  protected get galleryCounterLabel(): string {
    const count = this.galleryImages.length;
    if (count <= 1) {
      return '';
    }
    const safeIndex = this.activeGalleryIndex >= 0 && this.activeGalleryIndex < count ? this.activeGalleryIndex : 0;
    return `${safeIndex + 1} / ${count}`;
  }

  protected get hasMultipleGalleryImages(): boolean {
    return this.galleryImages.length > 1;
  }

  protected showPreviousGalleryImage(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.shiftGalleryImage(-1);
  }

  protected showNextGalleryImage(event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.shiftGalleryImage(1);
  }

  private openProjectDetails(): void {
    this.detailErrorMessage = '';
    this.isDetailModalOpen = true;

    if (this.detailModalProject?.descriptionMarkdown?.trim()) {
      this.isDetailLoading = false;
      this.changeDetector.detectChanges();
      return;
    }

    this.isDetailLoading = true;
    this.changeDetector.detectChanges();
    this.loadProjectDetails();
  }

  private loadProjectDetails(): void {
    if (this.isDetailRequestInFlight) {
      return;
    }

    this.isDetailRequestInFlight = true;

    this.projectsApi.getProjectBySlug(this.project.slug).pipe(take(1)).subscribe({
      next: (detail) => {
        this.isDetailRequestInFlight = false;
        this.isDetailLoading = false;

        if (!detail.descriptionMarkdown?.trim()) {
          this.detailModalProject = null;

          if (this.isDetailModalOpen) {
            this.isDetailModalOpen = false;
            this.changeDetector.detectChanges();
            this.openProjectLinkAction(this.primaryCardAction);
          }

          return;
        }

        this.detailErrorMessage = '';
        this.detailModalProject = detail;
        this.changeDetector.detectChanges();
      },
      error: () => {
        this.isDetailRequestInFlight = false;
        this.isDetailLoading = false;

        if (this.isDetailModalOpen) {
          this.detailErrorMessage = 'Project details could not be loaded right now.';
          this.changeDetector.detectChanges();
        }
      }
    });
  }

  private openProjectLinkAction(action: ProjectLink | null): void {
    if (!action) {
      return;
    }

    const href = action.href?.trim();
    if (href) {
      const openedWindow = window.open(href, '_blank', 'noopener,noreferrer');
      if (openedWindow) {
        openedWindow.opener = null;
      }
      return;
    }

    const routerLink = this.i18n.localizeRouterCommands(action.routerLink);
    if (!routerLink) {
      return;
    }

    if (typeof routerLink === 'string') {
      this.router.navigateByUrl(routerLink);
      return;
    }

    this.router.navigate([...routerLink]);
  }

  private buildReadMoreAction(project: ProjectSummary): ProjectLink | null {
    const readMoreUrl = project.readMoreUrl?.trim();
    if (readMoreUrl) {
      return { label: this.i18n.translate('common.actions.readMore'), href: readMoreUrl };
    }

    return project.links.find((link) => !!link.href && /read|meer/i.test(link.label ?? '')) ?? null;
  }

  private buildGithubAction(project: ProjectSummary): ProjectLink | null {
    const githubUrl = project.githubUrl?.trim();
    if (!githubUrl) {
      return null;
    }

    return { label: 'GitHub', href: githubUrl };
  }

  private buildDemoAction(project: ProjectSummary): ProjectLink | null {
    const directDemoUrl = project.demoUrl?.trim();
    const linkedDemo = project.links.find((link) => this.isDemoLink(project, link));
    const externalProjectLink = project.links.find((link) => this.isNonRepositoryExternalLink(project, link));
    const href = directDemoUrl || linkedDemo?.href?.trim() || externalProjectLink?.href?.trim();

    if (!href) {
      return null;
    }

    return {
      label: this.i18n.translate('common.actions.liveDemo'),
      href,
    };
  }

  private shiftGalleryImage(direction: -1 | 1): void {
    const count = this.galleryImages.length;
    if (count <= 1) {
      this.activeGalleryIndex = 0;
      return;
    }
    this.activeGalleryIndex = (this.activeGalleryIndex + direction + count) % count;
  }

  private isDemoLink(project: ProjectSummary, link: ProjectLink): boolean {
    const href = link.href?.trim();
    if (!href) {
      return false;
    }

    const label = (link.label ?? '').toLowerCase();
    return label.includes('demo') || label.includes('live') || href === project.demoUrl;
  }

  private isNonRepositoryExternalLink(project: ProjectSummary, link: ProjectLink): boolean {
    const href = link.href?.trim();
    if (!href) {
      return false;
    }

    const label = (link.label ?? '').toLowerCase();
    return !label.includes('github') && !label.includes('read') && !label.includes('meer') && href !== project.githubUrl && href !== project.readMoreUrl;
  }

  private isNestedInteractiveTarget(event: Event): boolean {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return false;
    }

    const currentTarget = event.currentTarget instanceof HTMLElement ? event.currentTarget : null;
    const interactiveTarget = target.closest('a, button, input, label, select, textarea, [role="button"], [data-project-card-interactive]');

    return !!interactiveTarget && interactiveTarget !== currentTarget;
  }

  protected get placeholderLabel(): string {
    return this.project.coverImageAlt || this.project.imageAlt || this.i18n.translate('pages.projects.card.placeholder');
  }
}
