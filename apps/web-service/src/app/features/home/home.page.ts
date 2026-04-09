import { Component } from '@angular/core';

import {
  HOME_CONTACT_PREVIEW_METHODS,
  HOME_EXPERIENCE_PREVIEW,
  HOME_EXPERTISE_GROUPS,
  HOME_FEATURED_BLOG_POST,
  HOME_HERO_PROFILE,
  HOME_PRIMARY_FEATURED_PROJECT
} from '../../shared/mock-data/home.mock';
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
export class HomePageComponent {
  protected readonly profile = HOME_HERO_PROFILE;
  protected readonly featuredBlogPost = HOME_FEATURED_BLOG_POST;
  protected readonly primaryProject = HOME_PRIMARY_FEATURED_PROJECT;
  protected readonly expertiseGroups = HOME_EXPERTISE_GROUPS;
  protected readonly experiencePreview = HOME_EXPERIENCE_PREVIEW;
  protected readonly contactPreviewMethods = HOME_CONTACT_PREVIEW_METHODS;
}
