import { BlogPostSummary } from './blog-post-summary.model';
import { ContactMethod } from './contact-method.model';
import { Experience } from './experience.model';
import { ExpertiseGroup, Profile } from './profile.model';
import { ProjectSummary } from './project-summary.model';

export interface HomePageData {
  hero: Profile;
  featuredProjects: ProjectSummary[];
  featuredBlogPosts: BlogPostSummary[];
  expertiseGroups: ExpertiseGroup[];
  experiencePreview: Experience[];
  contactPreview: ContactMethod[];
}
