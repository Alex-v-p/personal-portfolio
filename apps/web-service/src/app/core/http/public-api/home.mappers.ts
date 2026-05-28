import { AppLocale } from '@core/i18n/locales';
import { HomePageData } from '@domains/home/model/home.model';

import { HomeApi } from './home.contracts';
import { normalizeBlogPostSummaries } from './blog.mappers';
import { normalizeExperienceList } from './experience.mappers';
import { normalizeContactMethods, normalizeExpertiseGroups, normalizeProfile } from './profile.mappers';
import { normalizeProjectSummaries } from './projects.mappers';

export function normalizeHome(home: HomeApi, locale: AppLocale): HomePageData {
  return {
    hero: normalizeProfile(home.hero),
    featuredProjects: normalizeProjectSummaries(home.featuredProjects, locale),
    featuredBlogPosts: normalizeBlogPostSummaries(home.featuredBlogPosts, locale),
    expertiseGroups: normalizeExpertiseGroups(home.expertiseGroups),
    experiencePreview: normalizeExperienceList(home.experiencePreview, locale),
    contactPreview: normalizeContactMethods(home.contactPreview),
  };
}
