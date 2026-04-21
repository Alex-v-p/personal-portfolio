import { NgIf } from '@angular/common';
import { ChangeDetectorRef, Component, DestroyRef, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { distinctUntilChanged } from 'rxjs/operators';
import { finalize, take } from 'rxjs/operators';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { I18nService } from '@core/i18n/i18n.service';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { ContactMethod } from '@domains/profile/model/contact-method.model';
import { Experience } from '@domains/experience/model/experience.model';
import { Profile, ExpertiseGroup } from '@domains/profile/model/profile.model';
import { ProjectSummary } from '@domains/projects/model/project-summary.model';
import { PublicProfileApiService } from '@domains/profile/data/profile-api.service';
import { createEmptyProfile } from '@domains/profile/lib/profile-view.util';
import { HomeContactPreviewSectionComponent } from '@domains/home/ui/home-contact-preview.component';
import { HomeExperienceSectionComponent } from '@domains/home/ui/home-experience.component';
import { HomeExpertiseSectionComponent } from '@domains/home/ui/home-expertise.component';
import { HomeFeaturedSectionComponent } from '@domains/home/ui/home-featured.component';
import { HomeHeroSectionComponent } from '@domains/home/ui/home-hero.component';
import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiEmptyStateComponent } from '@shared/components/empty-state/ui-empty-state.component';
import { UiSkeletonComponent } from '@shared/components/skeleton/ui-skeleton.component';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    NgIf,
    TranslatePipe,
    HomeHeroSectionComponent,
    HomeFeaturedSectionComponent,
    HomeExpertiseSectionComponent,
    HomeExperienceSectionComponent,
    HomeContactPreviewSectionComponent,
    UiButtonComponent,
    UiEmptyStateComponent,
    UiSkeletonComponent,
  ],
  templateUrl: './home.page.html'
})
export class HomePageComponent implements OnInit {
  private readonly profileApi = inject(PublicProfileApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly i18n = inject(I18nService);
  private readonly destroyRef = inject(DestroyRef);

  protected profile: Profile = createEmptyProfile();
  protected featuredBlogPost: BlogPostSummary = this.createEmptyBlogPost();
  protected primaryProject: ProjectSummary = this.createEmptyProject();
  protected contactPreviewMethods: ContactMethod[] = [];
  protected expertiseGroups: ExpertiseGroup[] = [];
  protected experiencePreview: Experience[] = [];
  protected isLoading = true;
  protected errorMessage = '';

  ngOnInit(): void {
    this.i18n.localeChanges$.pipe(distinctUntilChanged(), takeUntilDestroyed(this.destroyRef)).subscribe(() => {
      this.loadHome();
    });
  }

  protected loadHome(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.resetHomeData();

    this.profileApi
      .getHome()
      .pipe(
        take(1),
        finalize(() => {
          this.isLoading = false;
          this.changeDetectorRef.detectChanges();
        })
      )
      .subscribe({
        next: (home) => {
          this.profile = home.hero ?? createEmptyProfile();
          this.primaryProject = home.featuredProjects?.[0] ?? this.createEmptyProject();
          this.featuredBlogPost = home.featuredBlogPosts?.[0] ?? this.createEmptyBlogPost();
          this.contactPreviewMethods = Array.isArray(home.contactPreview) ? home.contactPreview : [];
          this.expertiseGroups = Array.isArray(home.expertiseGroups) ? home.expertiseGroups : [];
          this.experiencePreview = Array.isArray(home.experiencePreview) ? home.experiencePreview : [];
        },
        error: () => {
          this.resetHomeData();
          this.errorMessage = this.i18n.translate('pages.home.errors.load');
        }
      });
  }

  protected get hasHeroContent(): boolean {
    return Boolean(this.profile.heroTitle || this.profile.summary || this.profile.name || this.profile.skills.length || this.profile.heroActions.length);
  }

  protected get hasFeaturedContent(): boolean {
    return Boolean(this.primaryProject.title || this.featuredBlogPost.title);
  }

  protected get hasExpertiseContent(): boolean {
    return this.expertiseGroups.length > 0;
  }

  protected get hasExperienceContent(): boolean {
    return Boolean(this.profile.introParagraphs.length || this.experiencePreview.length);
  }

  protected get hasContactPreviewContent(): boolean {
    return this.contactPreviewMethods.length > 0;
  }

  protected get hasHomepageContent(): boolean {
    return this.hasHeroContent || this.hasFeaturedContent || this.hasExpertiseContent || this.hasExperienceContent || this.hasContactPreviewContent;
  }

  private resetHomeData(): void {
    this.profile = createEmptyProfile();
    this.featuredBlogPost = this.createEmptyBlogPost();
    this.primaryProject = this.createEmptyProject();
    this.contactPreviewMethods = [];
    this.expertiseGroups = [];
    this.experiencePreview = [];
  }

  private createEmptyBlogPost(): BlogPostSummary {
    return {
      id: '',
      slug: '',
      title: '',
      excerpt: '',
      publishedAt: '',
      readTime: '',
      readingTimeMinutes: 0,
      category: '',
      tags: [],
      featured: false,
      isFeatured: false,
      coverAlt: '',
      coverImageAlt: '',
      coverImageFileId: null,
      status: 'draft'
    };
  }

  private createEmptyProject(): ProjectSummary {
    return {
      id: '',
      slug: '',
      title: '',
      teaser: '',
      shortDescription: '',
      summary: '',
      organization: '',
      duration: '',
      durationLabel: '',
      status: '',
      state: 'published',
      category: '',
      tags: [],
      featured: false,
      isFeatured: false,
      imageAlt: '',
      coverImageAlt: '',
      coverImageFileId: null,
      highlight: '',
      sortOrder: 0,
      links: []
    };
  }
}
