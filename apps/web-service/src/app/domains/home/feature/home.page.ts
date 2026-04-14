import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { NgIf } from '@angular/common';
import { finalize, take } from 'rxjs/operators';

import { ContactMethod } from '@domains/profile/model/contact-method.model';
import { Experience } from '@domains/experience/model/experience.model';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { Profile, ExpertiseGroup } from '@domains/profile/model/profile.model';
import { ProjectSummary } from '@domains/projects/model/project-summary.model';
import { PublicProfileApiService } from '@domains/profile/data/profile-api.service';
import { createEmptyProfile } from '@domains/profile/lib/profile-view.util';
import { HomeContactPreviewSectionComponent } from '@domains/home/ui/home-contact-preview.component';
import { HomeExperienceSectionComponent } from '@domains/home/ui/home-experience.component';
import { HomeExpertiseSectionComponent } from '@domains/home/ui/home-expertise.component';
import { HomeFeaturedSectionComponent } from '@domains/home/ui/home-featured.component';
import { HomeHeroSectionComponent } from '@domains/home/ui/home-hero.component';

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
  private readonly profileApi = inject(PublicProfileApiService);
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
    this.profileApi.getHome().pipe(take(1), finalize(() => { this.isLoading = false; this.changeDetectorRef.detectChanges(); })).subscribe({
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
