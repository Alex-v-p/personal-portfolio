import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { ContactMethod } from '@domains/profile/model/contact-method.model';
import { Experience } from '@domains/experience/model/experience.model';
import { ExpertiseGroup, Profile } from '@domains/profile/model/profile.model';
import { ProjectSummary } from '@domains/projects/model/project-summary.model';

export interface HomePageData {
  hero: Profile;
  featuredProjects: ProjectSummary[];
  featuredBlogPosts: BlogPostSummary[];
  expertiseGroups: ExpertiseGroup[];
  experiencePreview: Experience[];
  contactPreview: ContactMethod[];
}
