import { BlogPost } from './blog-post.model';
import { ContactMethod } from './contact-method.model';
import { Experience } from './experience.model';
import { ExpertiseGroup, Profile } from './profile.model';
import { Project } from './project.model';

export interface HomePageData {
  hero: Profile;
  featuredProjects: Project[];
  featuredBlogPosts: BlogPost[];
  expertiseGroups: ExpertiseGroup[];
  experiencePreview: Experience[];
  contactPreview: ContactMethod[];
}
