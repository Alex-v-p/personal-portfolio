import { inject, Injectable } from '@angular/core';

import { BlogPostDetail } from '../models/blog-post-detail.model';
import { BlogPostSummary } from '../models/blog-post-summary.model';
import { ContactMessageCreatedResponse, ContactMessageDraft } from '../models/contact-message.model';
import { Experience } from '../models/experience.model';
import { GithubSnapshot } from '../models/github-snapshot.model';
import { HomePageData } from '../models/home.model';
import { Profile } from '../models/profile.model';
import { ProjectDetail } from '../models/project-detail.model';
import { ProjectSummary } from '../models/project-summary.model';
import { SiteEventCreatePayload } from '../models/site-event.model';
import { NavigationItem, SiteShellData } from '../models/site-shell.model';
import { PublicBlogApiService } from './public-api/public-blog-api.service';
import { PublicContactApiService } from './public-api/public-contact-api.service';
import { PublicEventsApiService } from './public-api/public-events-api.service';
import { PublicExperienceApiService } from './public-api/public-experience-api.service';
import { PublicProfileApiService } from './public-api/public-profile-api.service';
import { PublicProjectsApiService } from './public-api/public-projects-api.service';
import { PublicStatsApiService } from './public-api/public-stats-api.service';
import { Observable } from 'rxjs';
import { StatsPageData } from '../models/stats-page.model';

@Injectable({ providedIn: 'root' })
export class PublicPortfolioApiService {
  private readonly profileApi = inject(PublicProfileApiService);
  private readonly projectsApi = inject(PublicProjectsApiService);
  private readonly blogApi = inject(PublicBlogApiService);
  private readonly experienceApi = inject(PublicExperienceApiService);
  private readonly statsApi = inject(PublicStatsApiService);
  private readonly contactApi = inject(PublicContactApiService);
  private readonly eventsApi = inject(PublicEventsApiService);

  getProfile(): Observable<Profile> {
    return this.profileApi.getProfile();
  }

  getNavigation(): Observable<NavigationItem[]> {
    return this.profileApi.getNavigation();
  }

  getSiteShell(): Observable<SiteShellData> {
    return this.profileApi.getSiteShell();
  }

  getHome(): Observable<HomePageData> {
    return this.profileApi.getHome();
  }

  getProjects(): Observable<ProjectSummary[]> {
    return this.projectsApi.getProjects();
  }

  getProjectBySlug(slug: string): Observable<ProjectDetail> {
    return this.projectsApi.getProjectBySlug(slug);
  }

  getBlogPosts(): Observable<BlogPostSummary[]> {
    return this.blogApi.getBlogPosts();
  }

  getBlogPostBySlug(slug: string): Observable<BlogPostDetail> {
    return this.blogApi.getBlogPostBySlug(slug);
  }

  getExperience(): Observable<Experience[]> {
    return this.experienceApi.getExperience();
  }

  getGithubSnapshot(): Observable<GithubSnapshot> {
    return this.statsApi.getGithubSnapshot();
  }

  getStats(): Observable<StatsPageData> {
    return this.statsApi.getStats();
  }

  submitContactMessage(payload: ContactMessageDraft): Observable<ContactMessageCreatedResponse> {
    return this.contactApi.submitContactMessage(payload);
  }

  createSiteEvent(payload: SiteEventCreatePayload): Observable<{ message: string; eventId: string }> {
    return this.eventsApi.createSiteEvent(payload);
  }
}
