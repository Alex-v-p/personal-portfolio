import { Component, OnInit, inject } from '@angular/core';
import { take } from 'rxjs/operators';

import { ContactMethod } from '../../shared/models/contact-method.model';
import { Experience } from '../../shared/models/experience.model';
import { BlogPost } from '../../shared/models/blog-post.model';
import { Profile, ExpertiseGroup } from '../../shared/models/profile.model';
import { Project } from '../../shared/models/project.model';
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

  protected profile: Profile = createEmptyProfile();
  protected featuredBlogPost: BlogPost = {
    id: '', slug: '', title: '', excerpt: '', publishedAt: '', readTime: '', readingTimeMinutes: 0, category: '', tags: [], featured: false, isFeatured: false, coverAlt: '', coverImageAlt: '', coverImageFileId: null, status: 'draft', contentMarkdown: ''
  };
  protected primaryProject: Project = {
    id: '', slug: '', title: '', teaser: '', shortDescription: '', summary: '', organization: '', duration: '', durationLabel: '', status: '', state: 'published', category: '', tags: [], featured: false, isFeatured: false, imageAlt: '', coverImageAlt: '', coverImageFileId: null, highlight: '', sortOrder: 0, links: []
  };
  protected contactPreviewMethods: ContactMethod[] = [];
  protected expertiseGroups: ExpertiseGroup[] = [];
  protected experiencePreview: Experience[] = [];

  ngOnInit(): void {
    this.portfolioApi.getHome().pipe(take(1)).subscribe({
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
