import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { NgIf } from '@angular/common';
import { finalize, take } from 'rxjs/operators';

import { ContactMethod } from '../../shared/models/contact-method.model';
import { Experience } from '../../shared/models/experience.model';
import { BlogPostSummary } from '../../shared/models/blog-post-summary.model';
import { Profile, ExpertiseGroup } from '../../shared/models/profile.model';
import { ProjectSummary } from '../../shared/models/project-summary.model';
import { PublicPortfolioApiService } from '../../shared/services/public-portfolio-api.service';
import { createEmptyProfile } from '../../shared/utils/profile-view.util';
import { HomeContactPreviewSectionComponent } from './components/home-contact-preview/home-contact-preview.component';
import { HomeExperienceSectionComponent } from './components/home-experience/home-experience.component';
import { HomeExpertiseSectionComponent } from './components/home-expertise/home-expertise.component';
import { HomeFeaturedSectionComponent } from './components/home-featured/home-featured.component';
import { HomeHeroSectionComponent } from './components/home-hero/home-hero.component';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    NgIf,
    HomeHeroSectionComponent,
    HomeFeaturedSectionComponent,
    HomeExpertiseSectionComponent,
    HomeExperienceSectionComponent,
    HomeContactPreviewSectionComponent
  ],
  templateUrl: './home.page.html'
})
export class HomePageComponent implements OnInit {
  private readonly portfolioApi = inject(PublicPortfolioApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected profile: Profile = createEmptyProfile();
  protected featuredBlogPost: BlogPostSummary = {
    id: '', slug: '', title: '', excerpt: '', publishedAt: '', readTime: '', readingTimeMinutes: 0, category: '', tags: [], featured: false, isFeatured: false, coverAlt: '', coverImageAlt: '', coverImageFileId: null, status: 'draft'
  };
  protected primaryProject: ProjectSummary = {
    id: '', slug: '', title: '', teaser: '', shortDescription: '', summary: '', organization: '', duration: '', durationLabel: '', status: '', state: 'published', category: '', tags: [], featured: false, isFeatured: false, imageAlt: '', coverImageAlt: '', coverImageFileId: null, highlight: '', sortOrder: 0, links: []
  };
  protected contactPreviewMethods: ContactMethod[] = [];
  protected expertiseGroups: ExpertiseGroup[] = [];
  protected experiencePreview: Experience[] = [];
  protected isLoading = true;

  ngOnInit(): void {
    this.portfolioApi.getHome().pipe(take(1), finalize(() => { this.isLoading = false; this.changeDetectorRef.detectChanges(); })).subscribe({
      next: (home) => {
        this.profile = home.hero;
        this.primaryProject = home.featuredProjects[0] ?? this.primaryProject;
        this.featuredBlogPost = home.featuredBlogPosts[0] ?? this.featuredBlogPost;
        this.contactPreviewMethods = home.contactPreview;
        this.expertiseGroups = home.expertiseGroups;
        this.experiencePreview = home.experiencePreview;
      }
    });
  }
}
