import { ExpertiseGroupApi } from './common.contracts';
import { BlogPostSummaryApi } from './blog.contracts';
import { ExperienceApi } from './experience.contracts';
import { ContactMethodApi, ProfileApi } from './profile.contracts';
import { ProjectSummaryApi } from './projects.contracts';

export interface HomeApi {
  hero: ProfileApi;
  featuredProjects: ProjectSummaryApi[];
  featuredBlogPosts: BlogPostSummaryApi[];
  expertiseGroups: ExpertiseGroupApi[];
  experiencePreview: ExperienceApi[];
  contactPreview: ContactMethodApi[];
}
