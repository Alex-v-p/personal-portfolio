import { Component, OnInit, inject } from '@angular/core';
import { take } from 'rxjs/operators';

import {
  HOME_CONTACT_PREVIEW_METHODS,
  HOME_EXPERIENCE_PREVIEW,
  HOME_EXPERTISE_GROUPS,
  HOME_FEATURED_BLOG_POST,
  HOME_HERO_PROFILE,
  HOME_PRIMARY_FEATURED_PROJECT
} from '../../shared/mock-data/home.mock';
import { ContactMethod } from '../../shared/models/contact-method.model';
import { BlogPost } from '../../shared/models/blog-post.model';
import { Profile } from '../../shared/models/profile.model';
import { Project } from '../../shared/models/project.model';
import { PublicPortfolioApiService } from '../../shared/services/public-portfolio-api.service';
import { buildContactMethodsFromProfile, mergeProfileWithFallback } from '../../shared/utils/profile-view.util';
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

  protected profile: Profile = HOME_HERO_PROFILE;
  protected featuredBlogPost: BlogPost = HOME_FEATURED_BLOG_POST;
  protected primaryProject: Project = HOME_PRIMARY_FEATURED_PROJECT;
  protected contactPreviewMethods: ContactMethod[] = HOME_CONTACT_PREVIEW_METHODS;
  protected readonly expertiseGroups = HOME_EXPERTISE_GROUPS;
  protected readonly experiencePreview = HOME_EXPERIENCE_PREVIEW;

  ngOnInit(): void {
    this.loadProfile();
    this.loadProjects();
    this.loadBlogPosts();
  }

  private loadProfile(): void {
    this.portfolioApi.getProfile().pipe(take(1)).subscribe({
      next: (profile) => {
        this.profile = mergeProfileWithFallback(profile, HOME_HERO_PROFILE);
        this.contactPreviewMethods = buildContactMethodsFromProfile(this.profile)
          .filter((method) => ['email', 'phone', 'github', 'linkedin'].includes(method.platform))
          .slice(0, 4);
      }
    });
  }

  private loadProjects(): void {
    this.portfolioApi.getProjects().pipe(take(1)).subscribe({
      next: (projects) => {
        if (!projects.length) {
          return;
        }

        this.primaryProject = projects.find((project) => project.isFeatured) ?? projects[0];
        if (!this.profile.skills.length) {
          this.profile = { ...this.profile, skills: this.primaryProject.tags.slice(0, 6) };
        }
      }
    });
  }

  private loadBlogPosts(): void {
    this.portfolioApi.getBlogPosts().pipe(take(1)).subscribe({
      next: (posts) => {
        if (!posts.length) {
          return;
        }

        this.featuredBlogPost = posts.find((post) => post.isFeatured) ?? posts[0];
      }
    });
  }
}
