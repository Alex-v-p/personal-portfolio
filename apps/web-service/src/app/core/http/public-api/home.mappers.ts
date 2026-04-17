import { HomePageData } from '@domains/home/model/home.model';

import { HomeApi } from './home.contracts';
import { normalizeBlogPostSummaries } from './blog.mappers';
import { normalizeExperienceList } from './experience.mappers';
import { normalizeContactMethods, normalizeExpertiseGroups, normalizeProfile } from './profile.mappers';
import { normalizeProjectSummaries } from './projects.mappers';

export function normalizeHome(home: HomeApi): HomePageData {
  return {
    hero: normalizeProfile(home.hero),
    featuredProjects: normalizeProjectSummaries(home.featuredProjects),
    featuredBlogPosts: normalizeBlogPostSummaries(home.featuredBlogPosts),
    expertiseGroups: normalizeExpertiseGroups(home.expertiseGroups),
    experiencePreview: normalizeExperienceList(home.experiencePreview),
    contactPreview: normalizeContactMethods(home.contactPreview),
  };
}
